#!/usr/bin/env python3
"""
Intelligent Text Simplifier with proper grammar and meaningful simplification
"""

import time
import re
from typing import Dict, Any

class MockTextSimplifier:
    def __init__(self):
        self.readability_levels = {
            "elementary": "Use very simple words and short sentences suitable for 8-10 year olds. Replace complex vocabulary with basic synonyms.",
            "middle_school": "Use clear, simple language suitable for 11-14 year olds. Break down complex ideas into understandable parts.",
            "high_school": "Use accessible language suitable for 15-18 year olds. Simplify technical terms but maintain academic tone.",
            "college": "Use clear academic language suitable for college students. Simplify complex concepts while preserving depth."
        }
    
    async def simplify(self, text: str, target_level: str = "middle_school", preserve_meaning: bool = True) -> str:
        """
        Intelligent simplification that provides meaningful differences for each level
        """
        # Simulate processing time
        time.sleep(0.5)
        
        # Apply different simplification strategies based on level
        if target_level == "elementary":
            simplified = self._simplify_elementary(text)
        elif target_level == "middle_school":
            simplified = self._simplify_middle_school(text)
        elif target_level == "high_school":
            simplified = self._simplify_high_school(text)
        else:  # college
            simplified = self._simplify_college(text)
        
        # Post-process the text for grammar and formatting
        simplified = self._post_process_text(simplified)
        
        return simplified
    
    def _simplify_elementary(self, text: str) -> str:
        """Elementary level: Very simple vocabulary, clear explanations, natural sentence breaks"""
        
        # Comprehensive vocabulary simplification with proper replacements
        replacements = {
            "quantum mechanical": "quantum",
            "subatomic particles": "tiny particles",
            "exhibit": "show",
            "wave-particle duality": "wave and particle behavior",
            "fundamental principle": "basic rule",
            "challenges": "goes against",
            "classical physics": "old physics",
            "paradigms": "ways of thinking",
            "artificial intelligence": "smart computer programs",
            "computer science": "computer learning",
            "branch": "part",
            "focuses on": "works on",
            "creating": "making",
            "machines": "computers",
            "capable of": "able to",
            "performing tasks": "doing jobs",
            "normally": "usually",
            "require": "need",
            "human intelligence": "human thinking",
            "understanding": "knowing",
            "language": "words",
            "recognizing": "finding",
            "patterns": "similar things",
            "solving": "fixing",
            "problems": "things that need fixing",
            "making decisions": "choosing what to do",
            "recent years": "lately",
            "advances": "improvements",
            "led to": "caused",
            "breakthroughs": "big discoveries",
            "healthcare": "health help",
            "education": "learning",
            "transportation": "moving people",
            "fields": "areas",
            "powerful": "strong",
            "tool": "helper",
            "shaping": "changing",
            "future": "what comes next"
        }
        
        # Apply replacements intelligently
        simplified = text
        for complex, simple in replacements.items():
            pattern = re.compile(re.escape(complex), re.IGNORECASE)
            simplified = pattern.sub(simple, simplified)
        
        # Break into natural, simple sentences (not arbitrary breaks!)
        sentences = simplified.split('. ')
        simple_sentences = []
        
        for sentence in sentences:
            if sentence.strip():
                # Only break very long sentences at natural points
                if len(sentence.split()) > 15:
                    # Look for natural break points: conjunctions, prepositions, etc.
                    natural_breaks = re.findall(r'\b(and|but|or|so|because|however|that|which|when|where)\b', sentence, re.IGNORECASE)
                    
                    if natural_breaks:
                        # Break at the first natural conjunction
                        for break_word in natural_breaks:
                            if break_word.lower() in sentence.lower():
                                parts = sentence.split(f' {break_word} ', 1)
                                if len(parts) == 2:
                                    # Add the conjunction back to the second part
                                    parts[1] = f"{break_word} {parts[1]}"
                                    simple_sentences.extend(parts)
                                    break
                                else:
                                    simple_sentences.append(sentence)
                            else:
                                simple_sentences.append(sentence)
                    else:
                        # If no natural breaks, keep the sentence but add explanation
                        simple_sentences.append(sentence)
                else:
                    simple_sentences.append(sentence)
        
        # Add simple explanations for complex concepts
        result = '. '.join(simple_sentences)
        
        # Add explanations for key terms (only where it makes sense)
        explanations = {
            "quantum": "Quantum means very small and strange.",
            "tiny particles": "Tiny particles are the smallest parts of everything.",
            "wave and particle behavior": "Wave and particle behavior means things can act like both waves and particles."
        }
        
        for term, explanation in explanations.items():
            if term.lower() in result.lower():
                # Only add explanation if it's not already there
                if f"({explanation})" not in result:
                    result = result.replace(term, f"{term} ({explanation})", 1)
        
        return result
    
    def _simplify_middle_school(self, text: str) -> str:
        """Middle school level: Clear language with moderate complexity"""
        
        # Moderate vocabulary simplification
        replacements = {
            "quantum mechanical": "quantum",
            "subatomic particles": "subatomic particles",
            "exhibit": "show",
            "wave-particle duality": "wave-particle duality (both wave and particle behavior)",
            "fundamental principle": "basic principle",
            "challenges": "questions",
            "classical physics": "traditional physics",
            "paradigms": "ways of thinking",
            "artificial intelligence": "AI (smart computer programs)",
            "computer science": "computer science",
            "branch": "area",
            "focuses on": "concentrates on",
            "creating": "building",
            "machines": "computers and robots",
            "capable of": "able to",
            "performing tasks": "completing tasks",
            "normally": "typically",
            "require": "need",
            "human intelligence": "human thinking",
            "understanding": "comprehending",
            "language": "speech and writing",
            "recognizing": "identifying",
            "patterns": "repeating structures",
            "solving": "resolving",
            "problems": "challenges",
            "making decisions": "choosing options",
            "recent years": "in recent times",
            "advances": "progress",
            "led to": "resulted in",
            "breakthroughs": "important discoveries",
            "healthcare": "medical care",
            "education": "learning and teaching",
            "transportation": "ways to move people",
            "fields": "areas of study",
            "powerful": "effective",
            "tool": "instrument",
            "shaping": "influencing",
            "future": "what lies ahead"
        }
        
        # Apply replacements
        simplified = text
        for complex, simple in replacements.items():
            pattern = re.compile(re.escape(complex), re.IGNORECASE)
            simplified = pattern.sub(simple, simplified)
        
        # Only break extremely long sentences at logical points
        sentences = simplified.split('. ')
        moderate_sentences = []
        
        for sentence in sentences:
            if sentence.strip():
                # Only break sentences longer than 25 words
                if len(sentence.split()) > 25:
                    # Look for logical break points
                    logical_breaks = re.findall(r'\b(and|but|or|so|because|however|therefore|that|which)\b', sentence, re.IGNORECASE)
                    
                    if logical_breaks:
                        # Break at the first logical conjunction
                        for break_word in logical_breaks:
                            if break_word.lower() in sentence.lower():
                                parts = sentence.split(f' {break_word} ', 1)
                                if len(parts) == 2:
                                    parts[1] = f"{break_word} {parts[1]}"
                                    moderate_sentences.extend(parts)
                                    break
                                else:
                                    moderate_sentences.append(sentence)
                            else:
                                moderate_sentences.append(sentence)
                    else:
                        moderate_sentences.append(sentence)
                else:
                    moderate_sentences.append(sentence)
        
        return '. '.join(moderate_sentences) + '.'
    
    def _simplify_high_school(self, text: str) -> str:
        """High school level: Accessible academic language"""
        
        # Minimal vocabulary changes
        replacements = {
            "quantum mechanical": "quantum",
            "subatomic particles": "subatomic particles",
            "exhibit": "demonstrate",
            "wave-particle duality": "wave-particle duality",
            "fundamental principle": "fundamental principle",
            "challenges": "questions",
            "classical physics": "classical physics",
            "paradigms": "paradigms",
            "artificial intelligence": "AI",
            "computer science": "computer science",
            "branch": "field",
            "focuses on": "specializes in",
            "creating": "developing",
            "machines": "computing systems",
            "capable of": "able to",
            "performing tasks": "executing tasks",
            "normally": "typically",
            "require": "necessitate",
            "human intelligence": "human cognitive abilities",
            "understanding": "comprehending",
            "language": "linguistic communication",
            "recognizing": "identifying",
            "patterns": "systematic structures",
            "solving": "resolving",
            "problems": "complex challenges",
            "making decisions": "decision-making",
            "recent years": "recently",
            "advances": "technological progress",
            "led to": "resulted in",
            "breakthroughs": "significant discoveries",
            "healthcare": "medical services",
            "education": "academic instruction",
            "transportation": "mobility systems",
            "fields": "disciplines",
            "powerful": "influential",
            "tool": "methodology",
            "shaping": "influencing",
            "future": "future developments"
        }
        
        # Apply replacements
        simplified = text
        for complex, simple in replacements.items():
            pattern = re.compile(re.escape(complex), re.IGNORECASE)
            simplified = pattern.sub(simple, simplified)
        
        # Keep sentence structure, minimal changes
        return simplified
    
    def _simplify_college(self, text: str) -> str:
        """College level: Enhanced academic language with minimal changes"""
        
        # Enhance academic language and add depth
        enhancements = {
            "quantum mechanical": "quantum mechanical",
            "subatomic particles": "subatomic particles",
            "exhibit": "demonstrate",
            "wave-particle duality": "wave-particle duality",
            "fundamental principle": "fundamental principle",
            "challenges": "challenges",
            "classical physics": "classical physics",
            "paradigms": "paradigms",
            "AI": "artificial intelligence (AI)",
            "computer science": "computer science",
            "branch": "subdiscipline",
            "focuses on": "concentrates on",
            "creating": "developing",
            "machines": "computational systems and intelligent machines",
            "tasks": "complex computational tasks",
            "human intelligence": "human cognitive capabilities and reasoning",
            "understanding": "comprehending and analyzing",
            "language": "linguistic systems and natural language",
            "patterns": "systematic patterns and regularities",
            "solving": "systematically resolving and analyzing",
            "problems": "complex problems and challenges",
            "making decisions": "decision-making processes and strategic thinking",
            "advances": "technological advances and innovations",
            "breakthroughs": "scientific breakthroughs and discoveries",
            "healthcare": "healthcare systems and medical technologies",
            "education": "educational systems and learning methodologies",
            "transportation": "transportation systems and mobility solutions",
            "fields": "academic disciplines and research areas",
            "powerful tool": "influential methodological tool and framework",
            "shaping": "influencing and transforming",
            "future": "future developments and technological evolution"
        }
        
        # Apply enhancements
        simplified = text
        for simple, enhanced in enhancements.items():
            pattern = re.compile(re.escape(simple), re.IGNORECASE)
            simplified = pattern.sub(enhanced, simplified)
        
        # Maintain complex sentence structures but ensure clarity
        sentences = simplified.split('. ')
        enhanced_sentences = []
        
        for sentence in sentences:
            if sentence.strip():
                # Add academic connectors for flow (only where appropriate)
                if not sentence.startswith(('Furthermore', 'Moreover', 'Additionally', 'In addition', 'However')):
                    # Add variety to sentence starters
                    starters = ['Furthermore, ', 'Moreover, ', 'Additionally, ', 'In addition, ']
                    if len(enhanced_sentences) > 0:
                        sentence = starters[len(enhanced_sentences) % len(starters)] + sentence
                
                enhanced_sentences.append(sentence.strip())
        
        return '. '.join(enhanced_sentences) + '.'
    
    def _post_process_text(self, text: str) -> str:
        """Post-process simplified text for better grammar and formatting"""
        
        # Fix common grammar issues
        text = re.sub(r'\b(are|is|was|were)\s+(a|an)\s+', r'\1 ', text)  # Remove unnecessary articles
        text = re.sub(r'\b(have|has|had)\s+(a|an)\s+', r'\1 ', text)  # Fix have/has articles
        
        # Fix sentence structure
        text = re.sub(r'([.!?])\s*([a-z])', lambda m: m.group(1) + ' ' + m.group(2).upper(), text)
        text = re.sub(r'^\s*([a-z])', lambda m: m.group(1).upper(), text)  # Capitalize first letter
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Ensure proper sentence spacing
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        # Clean up excessive punctuation
        text = re.sub(r'\.{3,}', '...', text)
        text = re.sub(r'!{2,}', '!', text)
        text = re.sub(r'\?{2,}', '?', text)
        
        # Clean up spacing around punctuation
        text = re.sub(r'\s+([,.!?])', r'\1', text)
        
        # Ensure text ends with proper punctuation
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        # Fix double spaces
        text = re.sub(r'\s{2,}', ' ', text)
        
        return text.strip()
    
    def calculate_readability(self, text: str) -> float:
        """Calculate readability score"""
        try:
            sentences = len(re.split(r'[.!?]+', text))
            words = len(text.split())
            syllables = self._count_syllables(text)
            
            if sentences == 0 or words == 0:
                return 0.0
            
            # Flesch Reading Ease formula
            score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
            
            # Clamp score between 0 and 100
            return max(0.0, min(100.0, score))
            
        except Exception:
            return 50.0
    
    def _count_syllables(self, text: str) -> int:
        """Simple syllable counting algorithm"""
        text = text.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        # Adjust for common patterns
        if text.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
            
        return count

# Test the improved mock simplifier
if __name__ == "__main__":
    import asyncio
    
    async def test_mock():
        simplifier = MockTextSimplifier()
        
        example_text = """The quantum mechanical properties of subatomic particles exhibit wave-particle duality, a fundamental principle that challenges classical physics paradigms."""
        
        print("Testing Improved Mock Text Simplifier...")
        print("=" * 60)
        print(f"Original text:\n{example_text}\n")
        
        levels = ["elementary", "middle_school", "high_school", "college"]
        
        for level in levels:
            print(f"\n--- {level.upper()} LEVEL ---")
            simplified = await simplifier.simplify(example_text, target_level=level)
            print(f"Simplified text:\n{simplified}")
            
            original_score = simplifier.calculate_readability(example_text)
            simplified_score = simplifier.calculate_readability(simplified)
            
            print(f"\nReadability scores:")
            print(f"  Original: {original_score:.1f}")
            print(f"  Simplified: {simplified_score:.1f}")
            print(f"  Improvement: {simplified_score - original_score:.1f}")
            print("-" * 40)
    
    asyncio.run(test_mock()) 