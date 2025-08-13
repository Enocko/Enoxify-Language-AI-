from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import os
from dotenv import load_dotenv
import asyncio
import time
import re

class RealTextSimplifier:
    def __init__(self):
        self.complex_words = {
            'utilize': 'use', 'facilitate': 'help', 'implement': 'do', 'methodology': 'method',
            'subsequently': 'then', 'consequently': 'so', 'nevertheless': 'but', 'furthermore': 'also',
            'moreover': 'also', 'additionally': 'also', 'previously': 'before', 'approximately': 'about',
            'demonstrate': 'show', 'indicate': 'show', 'illustrate': 'show', 'establish': 'make',
            'maintain': 'keep', 'obtain': 'get', 'acquire': 'get', 'comprehend': 'understand',
            'perceive': 'see', 'observe': 'see', 'examine': 'look at', 'investigate': 'look into',
            'analyze': 'study', 'evaluate': 'check', 'assess': 'check', 'determine': 'find out',
            'identify': 'find', 'recognize': 'know', 'acknowledge': 'know', 'appreciate': 'like',
            'conceptualize': 'think', 'contemplate': 'think about', 'deliberate': 'think about',
            'formulate': 'make', 'generate': 'make', 'initiate': 'start', 'originate': 'start',
            'proceed': 'go on', 'terminate': 'end', 'conclude': 'end', 'finalize': 'finish',
            'accomplish': 'do', 'achieve': 'do', 'attain': 'get to', 'secure': 'get',
            'procure': 'get', 'retrieve': 'get back', 'accumulate': 'gather', 'assemble': 'put together',
            'compile': 'put together', 'consolidate': 'put together', 'integrate': 'put together',
            'synthesize': 'put together', 'coordinate': 'organize', 'orchestrate': 'organize',
            'administer': 'manage', 'supervise': 'watch over', 'monitor': 'watch', 'regulate': 'control',
            'moderate': 'control', 'optimize': 'make better', 'enhance': 'make better', 'improve': 'make better',
            'augment': 'add to', 'supplement': 'add to', 'complement': 'go with', 'correspond': 'match',
            'coincide': 'match', 'correlate': 'go together', 'interrelate': 'go together',
            'interconnect': 'connect', 'synchronize': 'time together', 'harmonize': 'go together',
            'reconcile': 'make agree', 'mediate': 'help agree', 'negotiate': 'talk about',
            'collaborate': 'work together', 'cooperate': 'work together', 'participate': 'take part',
            'contribute': 'help', 'enable': 'let', 'empower': 'let', 'authorize': 'let',
            'sanction': 'allow', 'endorse': 'support', 'advocate': 'support', 'promote': 'support',
            'encourage': 'support', 'motivate': 'push', 'inspire': 'push', 'stimulate': 'push',
            'provoke': 'cause', 'elicit': 'get', 'extract': 'get', 'derive': 'get',
            'deduce': 'figure out', 'infer': 'figure out', 'postulate': 'guess', 'hypothesize': 'guess',
            'speculate': 'guess', 'anticipate': 'expect', 'foresee': 'see coming', 'predict': 'guess',
            'project': 'guess', 'estimate': 'guess', 'calculate': 'figure out', 'compute': 'figure out',
            'ascertain': 'find out', 'verify': 'check', 'validate': 'check', 'confirm': 'check',
            'substantiate': 'prove', 'corroborate': 'prove', 'authenticate': 'prove real',
            'certify': 'prove', 'legitimize': 'make legal', 'institutionalize': 'make official',
            'standardize': 'make the same', 'normalize': 'make normal', 'stabilize': 'make steady',
            'streamline': 'make smooth', 'simplify': 'make simple', 'clarify': 'make clear',
            'elucidate': 'make clear', 'illuminate': 'make clear', 'elaborate': 'explain more',
            'expound': 'explain more', 'articulate': 'say clearly', 'verbalize': 'say',
            'communicate': 'tell', 'convey': 'tell', 'transmit': 'send', 'disseminate': 'spread',
            'propagate': 'spread', 'circulate': 'spread', 'distribute': 'give out', 'allocate': 'give',
            'assign': 'give', 'designate': 'pick', 'nominate': 'pick', 'appoint': 'pick',
            'label': 'name', 'categorize': 'sort', 'classify': 'sort', 'organize': 'sort',
            'arrange': 'put in order', 'sequence': 'put in order', 'prioritize': 'put first',
            'rank': 'put in order', 'evaluate': 'judge', 'assess': 'judge', 'appraise': 'judge',
            'review': 'look at', 'scrutinize': 'look closely', 'explore': 'look into',
            'research': 'look into', 'study': 'learn about', 'inspect': 'look at',
            'track': 'follow', 'trace': 'follow', 'pursue': 'go after', 'seek': 'look for',
            'search': 'look for', 'discover': 'find', 'uncover': 'find', 'reveal': 'show',
            'expose': 'show', 'disclose': 'tell', 'divulge': 'tell', 'confess': 'tell',
            'admit': 'tell', 'realize': 'know', 'grasp': 'get', 'enjoy': 'like', 'value': 'like',
            'cherish': 'love', 'treasure': 'love', 'adore': 'love', 'admire': 'like',
            'respect': 'like', 'esteem': 'like', 'honor': 'respect', 'revere': 'respect',
            'worship': 'love', 'idolize': 'love', 'glorify': 'praise', 'praise': 'say good things',
            'compliment': 'say good things', 'flatter': 'say good things', 'encourage': 'cheer up',
            'assist': 'help', 'aid': 'help', 'serve': 'help', 'benefit': 'help', 'profit': 'help',
            'gain': 'get', 'earn': 'get', 'win': 'get', 'complete': 'finish', 'cease': 'stop',
            'halt': 'stop', 'pause': 'stop', 'suspend': 'stop', 'interrupt': 'stop',
            'discontinue': 'stop', 'abandon': 'give up', 'desert': 'leave', 'forsake': 'leave',
            'relinquish': 'give up', 'surrender': 'give up', 'yield': 'give up', 'submit': 'give up',
            'concede': 'give up'
        }
        
    async def simplify(self, text: str, target_level: str, preserve_meaning: bool) -> str:
        await asyncio.sleep(0.5)
        
        original_text = text
        text = text.lower()
        
        if target_level == "basic":
            simplified = self._basic_simplification(text)
        elif target_level == "medium":
            simplified = self._medium_simplification(text)
        else:
            simplified = self._advanced_simplification(text)
        
        if simplified and simplified[0].isalpha():
            simplified = simplified[0].upper() + simplified[1:]
        
        simplified = self._restore_capitalization(original_text, simplified)
        return simplified
    
    def _basic_simplification(self, text: str) -> str:
        for complex_word, simple_word in self.complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        sentences = text.split('. ')
        simplified_sentences = []
        for sentence in sentences:
            if len(sentence) > 50:
                parts = re.split(r'\s+(and|or|but|so|because|however|therefore)\s+', sentence)
                if len(parts) > 1:
                    simplified_sentences.extend([p.strip() for p in parts if p.strip()])
                else:
                    simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        return '. '.join(simplified_sentences)
    
    def _medium_simplification(self, text: str) -> str:
        medium_complex_words = {k: v for k, v in self.complex_words.items() 
                              if len(k) > 8 or k in ['utilize', 'facilitate', 'implement', 'methodology']}
        
        for complex_word, simple_word in medium_complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        return text
    
    def _advanced_simplification(self, text: str) -> str:
        advanced_complex_words = {k: v for k, v in self.complex_words.items() 
                                if len(k) > 10}
        
        for complex_word, simple_word in advanced_complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        return text
    
    def _restore_capitalization(self, original: str, simplified: str) -> str:
        words = simplified.split()
        original_words = original.split()
        
        for i, word in enumerate(words):
            if i < len(original_words):
                if original_words[i][0].isupper() and len(original_words[i]) > 1:
                    words[i] = word.capitalize()
        
        return ' '.join(words)
    
    def calculate_readability(self, text: str) -> float:
        words = text.split()
        sentences = text.split('.')
        syllables = self._count_syllables(text)
        
        if len(words) == 0 or len(sentences) == 0:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        return max(0.0, min(100.0, score))
    
    def _count_syllables(self, text: str) -> int:
        text = text.lower()
        count = 0
        vowels = 'aeiouy'
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        return max(1, count)

from pydantic import BaseModel

class TextSimplificationRequest(BaseModel):
    text: str
    target_level: str = "medium"
    preserve_meaning: bool = True

class TextSimplificationResponse(BaseModel):
    simplified_text: str
    readability_score: float

load_dotenv()
app = FastAPI(title="AI-Based Accessibility Enhancer (Real Mode)", 
              description="Convert educational content into accessible formats with real text simplification", 
              version="1.0.0")

app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://localhost:3000", "http://localhost:8000"], 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"])

text_simplifier = RealTextSimplifier()

@app.get("/")
async def root():
    return {"message": "AI-Based Accessibility Enhancer API (Real Mode)"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "services": ["text_simplifier"], "mode": "real"}

@app.post("/simplify-text", response_model=TextSimplificationResponse)
async def simplify_text(request: TextSimplificationRequest):
    simplified_text = await text_simplifier.simplify(
        request.text, 
        request.target_level, 
        request.preserve_meaning
    )
    readability_score = text_simplifier.calculate_readability(simplified_text)
    
    return TextSimplificationResponse(
        simplified_text=simplified_text,
        readability_score=readability_score
    )

if __name__ == "__main__":
    print("🚀 Starting AI-Based Accessibility Enhancer (Real Mode)")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("🔧 This version has REAL text simplification logic")
    uvicorn.run(app, host="0.0.0.0", port=8000)
