import openai
import re
import os
from typing import Dict, List, Optional

class TextSimplifier:
    """Advanced text simplifier using OpenAI GPT-4 for ChatGPT-level quality"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.readability_levels = {
            "elementary": {
                "description": "Very simple vocabulary, short sentences (5-8 words), basic explanations",
                "max_sentence_length": 8,
                "complexity": "minimal"
            },
            "middle_school": {
                "description": "Simple vocabulary, medium sentences (8-12 words), clear explanations",
                "max_sentence_length": 12,
                "complexity": "simple"
            },
            "high_school": {
                "description": "Moderate vocabulary, varied sentences (10-15 words), some explanations",
                "max_sentence_length": 15,
                "complexity": "moderate"
            },
            "college": {
                "description": "Advanced vocabulary, complex sentences, academic tone, no explanations needed",
                "max_sentence_length": 25,
                "complexity": "advanced"
            }
        }
    
    async def simplify(self, text: str, target_level: str, preserve_meaning: bool = True) -> Dict[str, any]:
        """Simplify text using OpenAI GPT-4 for professional quality"""
        try:
            if target_level not in self.readability_levels:
                raise ValueError(f"Invalid reading level: {target_level}")
            
            level_config = self.readability_levels[target_level]
            
            # Create detailed system prompt for OpenAI
            system_prompt = self._create_system_prompt(target_level, level_config)
            
            # User prompt with the text to simplify
            user_prompt = f"Please simplify the following text according to the specified reading level:\n\n{text}"
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            simplified_text = response.choices[0].message.content.strip()
            
            # Post-process for consistency
            simplified_text = self._post_process_text(simplified_text, target_level)
            
            # Calculate readability score
            readability_score = self._calculate_readability(simplified_text)
            
            return {
                "original_text": text,
                "simplified_text": simplified_text,
                "target_level": target_level,
                "readability_score": readability_score,
                "level_config": level_config
            }
            
        except Exception as e:
            raise Exception(f"Text simplification failed: {str(e)}")
    
    def _create_system_prompt(self, target_level: str, level_config: Dict) -> str:
        """Create detailed system prompt for OpenAI based on reading level"""
        
        prompts = {
            "elementary": """You are an expert educator specializing in simplifying complex text for elementary school students (ages 6-10).

CRITICAL REQUIREMENTS:
1. Use ONLY simple, everyday words that a 6-10 year old would know
2. Keep sentences VERY SHORT (5-8 words maximum)
3. Break complex ideas into simple, clear statements
4. Add brief explanations for any technical terms in parentheses
5. Use active voice and simple present tense
6. Avoid complex punctuation (no semicolons, colons, or dashes)
7. Make the text engaging and easy to understand
8. Ensure perfect grammar and natural flow

EXAMPLE TRANSFORMATION:
Original: "The quantum mechanical properties of subatomic particles exhibit wave-particle duality."
Simplified: "Tiny particles act in strange ways. They can be like waves. They can also be like particles. This is called wave-particle duality. (Wave-particle duality means particles can act like both waves and particles.)"

OUTPUT: Provide ONLY the simplified text, no explanations or meta-commentary.""",

            "middle_school": """You are an expert educator specializing in simplifying complex text for middle school students (ages 11-14).

CRITICAL REQUIREMENTS:
1. Use simple, clear vocabulary suitable for 11-14 year olds
2. Keep sentences moderately short (8-12 words maximum)
3. Explain complex concepts in straightforward terms
4. Add brief explanations for technical terms when needed
5. Use clear, logical sentence structure
6. Maintain the original meaning while making it accessible
7. Use active voice and clear transitions
8. Ensure perfect grammar and natural flow

EXAMPLE TRANSFORMATION:
Original: "The quantum mechanical properties of subatomic particles exhibit wave-particle duality."
Simplified: "Subatomic particles have special properties called quantum mechanical properties. These particles show wave-particle duality, which means they can behave like both waves and particles at the same time."

OUTPUT: Provide ONLY the simplified text, no explanations or meta-commentary.""",

            "high_school": """You are an expert educator specializing in adapting complex text for high school students (ages 15-18).

CRITICAL REQUIREMENTS:
1. Use vocabulary appropriate for high school level
2. Allow varied sentence lengths (10-15 words average)
3. Maintain some complexity while ensuring clarity
4. Provide brief explanations for very technical terms only
5. Use sophisticated but accessible language
6. Keep the academic tone while improving readability
7. Ensure logical flow and coherence
8. Ensure perfect grammar and natural flow

EXAMPLE TRANSFORMATION:
Original: "The quantum mechanical properties of subatomic particles exhibit wave-particle duality."
Simplified: "Subatomic particles display quantum mechanical properties, including wave-particle duality. This fundamental principle demonstrates that particles can exhibit both wave-like and particle-like characteristics simultaneously."

OUTPUT: Provide ONLY the simplified text, no explanations or meta-commentary.""",

            "college": """You are an expert academic writer specializing in enhancing complex text for college-level readers.

CRITICAL REQUIREMENTS:
1. Maintain or enhance sophisticated vocabulary
2. Allow complex sentence structures (up to 25 words)
3. Preserve academic rigor and precision
4. No need for explanations - assume college-level knowledge
5. Enhance clarity and flow while maintaining complexity
6. Use precise, scholarly language
7. Ensure logical coherence and academic standards
8. Ensure perfect grammar and natural flow

EXAMPLE TRANSFORMATION:
Original: "The quantum mechanical properties of subatomic particles exhibit wave-particle duality."
Enhanced: "The quantum mechanical properties of subatomic particles manifest wave-particle duality, a fundamental principle that challenges classical physics paradigms and demonstrates the inherent complexity of quantum systems."

OUTPUT: Provide ONLY the enhanced text, no explanations or meta-commentary."""
        }
        
        return prompts.get(target_level, prompts["high_school"])
    
    def _post_process_text(self, text: str, target_level: str) -> str:
        """Post-process text for consistency and quality"""
        
        # Basic cleanup
        text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
        text = text.strip()
        
        # Ensure proper sentence endings
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        # Fix common issues
        text = re.sub(r'\.{2,}', '.', text)  # Fix multiple periods
        text = re.sub(r'!{2,}', '!', text)   # Fix multiple exclamation marks
        text = re.sub(r'\?{2,}', '?', text)  # Fix multiple question marks
        
        # Ensure proper spacing after punctuation
        text = re.sub(r'([.!?])([A-Za-z])', r'\1 \2', text)
        
        # Fix spacing around parentheses
        text = re.sub(r'\(\s+', '(', text)
        text = re.sub(r'\s+\)', ')', text)
        
        return text
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate Flesch Reading Ease score"""
        try:
            sentences = len(re.split(r'[.!?]+', text))
            words = len(text.split())
            syllables = self._count_syllables(text)
            
            if sentences == 0 or words == 0:
                return 0.0
            
            # Flesch Reading Ease formula
            score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
            return max(0.0, min(100.0, score))
        except:
            return 50.0  # Default score if calculation fails
    
    def _count_syllables(self, text: str) -> int:
        """Simple syllable counting"""
        text = text.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        return max(1, count)
