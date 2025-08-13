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

class AdvancedTextSimplifier:
    def __init__(self):
        # Comprehensive word replacement dictionary
        self.complex_words = {
            # Technical terms
            'diagnosis': 'problem finding', 'fix path': 'solution', 'code snippet': 'small code example',
            'API call': 'program request', 'web builder': 'website maker', 'plug in': 'add',
            'almost impossible': 'very hard', 'fail': 'not work', 'working': 'good',
            
            # Common complex words
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
        
        # Phrase replacements for better simplification
        self.phrase_replacements = {
            'in one go': 'all at once',
            'instead of': 'rather than',
            'If you want': 'If you like',
            'That would make it': 'This will make it',
            'almost impossible': 'very hard',
            'for it to fail again': 'to not work again',
            'it will have both': 'it will get both',
            'can just plug it in': 'can easily add it',
            'working code snippet': 'good code example',
            'API call + prompt': 'program request and instructions',
            'web builder': 'website maker',
            'builder AI': 'helper program'
        }
        
    async def simplify(self, text: str, target_level: str, preserve_meaning: bool) -> str:
        await asyncio.sleep(0.5)  # Simulate API call delay
        
        original_text = text
        simplified_text = text
        
        # Step 1: Replace complex phrases first
        for complex_phrase, simple_phrase in self.phrase_replacements.items():
            simplified_text = re.sub(r'\b' + re.escape(complex_phrase) + r'\b', simple_phrase, simplified_text, flags=re.IGNORECASE)
        
        # Step 2: Replace complex words based on target level
        if target_level == "elementary":
            simplified_text = self._elementary_simplification(simplified_text)
        elif target_level == "middle_school":
            simplified_text = self._middle_school_simplification(simplified_text)
        elif target_level == "high_school":
            simplified_text = self._high_school_simplification(simplified_text)
        elif target_level == "college":
            simplified_text = self._college_simplification(simplified_text)
        
        # Step 3: Break down complex sentences
        simplified_text = self._break_complex_sentences(simplified_text, target_level)
        
        # Step 4: Add explanations for technical terms
        if target_level in ["elementary", "middle_school"]:
            simplified_text = self._add_explanations(simplified_text)
        
        return simplified_text
    
    def _elementary_simplification(self, text: str) -> str:
        # Replace most complex words with simple alternatives
        for complex_word, simple_word in self.complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text, flags=re.IGNORECASE)
        
        # Additional elementary-level simplifications
        elementary_replacements = {
            'complicated': 'hard',
            'difficult': 'hard',
            'challenging': 'hard',
            'sophisticated': 'smart',
            'advanced': 'hard',
            'complex': 'hard',
            'elaborate': 'detailed',
            'comprehensive': 'complete',
            'thorough': 'complete',
            'extensive': 'big',
            'substantial': 'big',
            'significant': 'important',
            'crucial': 'important',
            'essential': 'needed',
            'fundamental': 'basic',
            'elementary': 'basic',
            'rudimentary': 'basic',
            'preliminary': 'first',
            'initial': 'first',
            'primary': 'main',
            'principal': 'main',
            'dominant': 'main',
            'prevalent': 'common',
            'widespread': 'common',
            'ubiquitous': 'everywhere',
            'omnipresent': 'everywhere',
            'pervasive': 'everywhere'
        }
        
        for complex_word, simple_word in elementary_replacements.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text, flags=re.IGNORECASE)
        
        return text
    
    def _middle_school_simplification(self, text: str) -> str:
        # Replace moderately complex words
        medium_complex_words = {k: v for k, v in self.complex_words.items() 
                              if len(k) > 8 or k in ['utilize', 'facilitate', 'implement', 'methodology']}
        
        for complex_word, simple_word in medium_complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text, flags=re.IGNORECASE)
        
        return text
    
    def _high_school_simplification(self, text: str) -> str:
        # Replace only very complex words
        advanced_complex_words = {k: v for k, v in self.complex_words.items() 
                                if len(k) > 10}
        
        for complex_word, simple_word in advanced_complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text, flags=re.IGNORECASE)
        
        return text
    
    def _college_simplification(self, text: str) -> str:
        # Replace only the most complex words, keep academic tone
        college_complex_words = {k: v for k, v in self.complex_words.items() 
                               if len(k) > 12}
        
        for complex_word, simple_word in college_complex_words.items():
            text = re.sub(r'\b' + complex_word + r'\b', simple_word, text, flags=re.IGNORECASE)
        
        return text
    
    def _break_complex_sentences(self, text: str, target_level: str) -> str:
        # Break down very long sentences
        sentences = text.split('. ')
        simplified_sentences = []
        
        for sentence in sentences:
            if len(sentence) > 80:  # Very long sentence
                simplified_sentences.extend(self._split_long_sentence(sentence))
            elif len(sentence) > 50:  # Long sentence
                if target_level in ["elementary", "middle_school"]:
                    simplified_sentences.extend(self._split_long_sentence(sentence))
                else:
                    simplified_sentences.append(sentence)
            else:
                simplified_sentences.append(sentence)
        
        return '. '.join(simplified_sentences)
    
    def _split_long_sentence(self, sentence: str) -> list:
        # Split by common conjunctions
        conjunctions = [' and ', ' or ', ' but ', ' so ', ' because ', ' however ', ' therefore ', ' moreover ', ' furthermore ']
        
        for conj in conjunctions:
            if conj in sentence:
                parts = sentence.split(conj)
                if len(parts) > 1:
                    return [part.strip() for part in parts if part.strip()]
        
        # Split by commas if no conjunctions
        comma_parts = sentence.split(', ')
        if len(comma_parts) > 1 and len(comma_parts[0]) > 25:
            return [part.strip() for part in comma_parts if part.strip()]
        
        # If still too long, split by "that" or "which"
        if ' that ' in sentence:
            parts = sentence.split(' that ')
            if len(parts) > 1:
                return [part.strip() for part in parts if part.strip()]
        
        return [sentence]
    
    def _add_explanations(self, text: str) -> str:
        # Add simple explanations for technical terms
        explanations = {
            'AI': 'artificial intelligence (computer helper)',
            'API': 'application programming interface (way programs talk to each other)',
            'code snippet': 'small piece of computer code',
            'web builder': 'website creation tool',
            'diagnosis': 'problem finding',
            'fix path': 'solution steps'
        }
        
        for term, explanation in explanations.items():
            # Only add explanation if term appears and explanation isn't already there
            if term in text and explanation not in text:
                text = re.sub(r'\b' + term + r'\b', f"{term} ({explanation})", text, flags=re.IGNORECASE)
        
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
    title="AI-Based Accessibility Enhancer (Advanced Mode)", 
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
text_simplifier = AdvancedTextSimplifier()
print("🚀 Advanced text simplifier initialized successfully")

@app.get("/")
async def root():
    return {
        "message": "AI-Based Accessibility Enhancer API (Advanced Mode)",
        "status": "running",
        "text_simplifier": "available",
        "note": "This version has comprehensive text simplification with phrase replacement and sentence breaking"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": ["text_simplifier"],
        "mode": "advanced_comprehensive",
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
    print("🚀 Starting AI-Based Accessibility Enhancer (Advanced Mode)")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("🔧 This version has COMPREHENSIVE text simplification")
    print("💡 Features: phrase replacement, sentence breaking, technical explanations")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
