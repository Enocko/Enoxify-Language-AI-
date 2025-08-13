from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv
import asyncio
import re
from pydantic import BaseModel

class TextSimplificationRequest(BaseModel):
    text: str
    target_level: str = "medium"
    preserve_meaning: bool = True

class TextSimplificationResponse(BaseModel):
    original_text: str
    simplified_text: str
    readability_score: float
    success: bool
    error_message: str = None

class DemoTextSimplifier:
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
            'research': 'study', 'study': 'learn about', 'inspect': 'look at',
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
        await asyncio.sleep(0.5)  # Simulate API call delay
        
        original_text = text
        text = text.lower()
        
        # Map frontend levels to backend levels
        if target_level == "elementary":
            simplified = self._basic_simplification(text)
        elif target_level == "middle_school":
            simplified = self._medium_simplification(text)
        elif target_level == "high_school":
            simplified = self._advanced_simplification(text)
        elif target_level == "college":
            simplified = self._college_simplification(text)
        else:
            # Default to medium if unknown
            simplified = self._medium_simplification(text)
        
        # Restore capitalization and formatting
        simplified = self._restore_capitalization(original_text, simplified)
        
        # Add level-specific improvements
        if target_level == "elementary":
            simplified = self._add_basic_improvements(simplified)
        elif target_level == "middle_school":
            simplified = self._add_medium_improvements(simplified)
        
        return simplified
    
    def _basic_simplification(self, text: str) -> str:
        # Replace complex words
        for complex_word, simple_word in self.complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        # Break long sentences
        sentences = text.split('. ')
        simplified_sentences = []
        for sentence in sentences:
            if len(sentence) > 30:
                parts = re.split(r'\s+(and|or|but|so|because|however|therefore)\s+', sentence)
                if len(parts) > 1:
                    simplified_sentences.extend([p.strip() for p in parts if p.strip()])
                else:
                    # Split by commas if no conjunctions
                    comma_parts = sentence.split(', ')
                    if len(comma_parts) > 1 and len(comma_parts[0]) > 15:
                        simplified_sentences.extend([p.strip() for p in comma_parts if p.strip()])
                    else:
                        simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        return '. '.join(simplified_sentences)
    
    def _medium_simplification(self, text: str) -> str:
        # Replace only the most complex words
        medium_complex_words = {k: v for k, v in self.complex_words.items() 
                              if len(k) > 8 or k in ['utilize', 'facilitate', 'implement', 'methodology']}
        
        for complex_word, simple_word in medium_complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        return text
    
    def _advanced_simplification(self, text: str) -> str:
        # Replace only very complex words
        advanced_complex_words = {k: v for k, v in self.complex_words.items() 
                                if len(k) > 10}
        
        for complex_word, simple_word in advanced_complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        return text
    
    def _college_simplification(self, text: str) -> str:
        # Replace only the most complex words, keep academic tone
        college_complex_words = {k: v for k, v in self.complex_words.items() 
                               if len(k) > 12}
        
        for complex_word, simple_word in college_complex_words.items():
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
    
    def _add_basic_improvements(self, text: str) -> str:
        # Add simple explanations for complex concepts
        improvements = {
            'data': 'information',
            'analysis': 'study',
            'research': 'study',
            'experiment': 'test',
            'hypothesis': 'guess',
            'theory': 'idea',
            'concept': 'idea',
            'principle': 'rule',
            'method': 'way',
            'technique': 'way',
            'strategy': 'plan',
            'approach': 'way',
            'framework': 'plan',
            'structure': 'plan',
            'system': 'plan',
            'process': 'way',
            'procedure': 'way',
            'protocol': 'rule',
            'guideline': 'rule',
            'standard': 'rule'
        }
        
        for complex_word, simple_word in improvements.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        return text
    
    def _add_medium_improvements(self, text: str) -> str:
        # Add some explanations but keep academic tone
        improvements = {
            'utilize': 'use',
            'facilitate': 'help',
            'implement': 'do',
            'demonstrate': 'show',
            'indicate': 'show',
            'establish': 'make',
            'maintain': 'keep',
            'obtain': 'get',
            'acquire': 'get'
        }
        
        for complex_word, simple_word in improvements.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text)
        
        return text
    
    def calculate_readability(self, text: str) -> float:
        try:
            words = text.split()
            sentences = [s for s in text.split('.') if s.strip()]
            syllables = self._count_syllables(text)
            
            if len(words) == 0 or len(sentences) == 0:
                return 0.0
            
            avg_sentence_length = len(words) / len(sentences)
            avg_syllables_per_word = syllables / len(words)
            
            score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            return max(0.0, min(100.0, score))
        except:
            return 0.0
    
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

# Initialize FastAPI app
load_dotenv()
app = FastAPI(
    title="AI-Based Accessibility Enhancer (Demo Mode)", 
    description="Convert educational content into accessible formats using advanced text simplification algorithms", 
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000", "http://localhost:8000"], 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Initialize the text simplifier
text_simplifier = DemoTextSimplifier()
print("🚀 Demo text simplifier initialized successfully")

@app.get("/")
async def root():
    return {
        "message": "AI-Based Accessibility Enhancer API (Demo Mode)",
        "status": "running",
        "text_simplifier": "available",
        "note": "This is a demo version with advanced text simplification. For OpenAI integration, set OPENAI_API_KEY in .env"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": ["text_simplifier"],
        "mode": "demo_advanced",
        "openai_configured": False
    }

@app.post("/simplify-text", response_model=TextSimplificationResponse)
async def simplify_text(request: TextSimplificationRequest):
    try:
        print(f"📥 Received simplification request for {request.target_level} level")
        print(f"📝 Text: {request.text[:100]}{'...' if len(request.text) > 100 else ''}")
        
        simplified_text = await text_simplifier.simplify(
            request.text, 
            request.target_level, 
            request.preserve_meaning
        )
        
        readability_score = text_simplifier.calculate_readability(simplified_text)
        
        print(f"✅ Simplification successful. Readability score: {readability_score:.1f}")
        print(f"📝 Original: {request.text[:50]}...")
        print(f"📝 Simplified: {simplified_text[:50]}...")
        
        return TextSimplificationResponse(
            original_text=request.text,
            simplified_text=simplified_text,
            readability_score=readability_score,
            success=True
        )
        
    except Exception as e:
        error_msg = f"Text simplification failed: {str(e)}"
        print(f"❌ {error_msg}")
        
        return TextSimplificationResponse(
            original_text=request.text,
            simplified_text="",
            readability_score=0.0,
            success=False,
            error_message=error_msg
        )

if __name__ == "__main__":
    print("🚀 Starting AI-Based Accessibility Enhancer (Demo Mode)")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("🔧 This version has ADVANCED text simplification algorithms")
    print("💡 To use OpenAI: set OPENAI_API_KEY in .env file")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
