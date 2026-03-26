import openai
import re
import os
from typing import Dict, List, Optional

class TextSimplifier:
    """Advanced text simplifier using OpenAI GPT-4 for ChatGPT-level quality"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        # Fallback simplifier exists only to keep the UI usable during development.
        # For best results (ChatGPT-like quality), set OPENAI_API_KEY to a valid key.
        self.allow_fallback = str(os.getenv("ALLOW_FALLBACK_SIMPLIFIER", "false")).strip().lower() in (
            "1",
            "true",
            "yes",
            "y",
        )
        # If OPENAI_API_KEY is missing/invalid, we still want the app to work,
        # so we fall back to a local rule-based simplifier.
        self.client = openai.OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
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
    
        # Rule-based fallback substitutions (used when OpenAI isn't available).
        # Kept intentionally small/targeted to reduce unintended changes.
        self.complex_words = {
            "utilize": "use",
            "facilitate": "help",
            "implement": "do",
            "methodology": "method",
            "subsequently": "then",
            "consequently": "so",
            "nevertheless": "but",
            "furthermore": "also",
            "moreover": "also",
            "additionally": "also",
            "approximately": "about",
            "demonstrate": "show",
            "indicate": "show",
            "illustrate": "show",
            "establish": "make",
            "maintain": "keep",
            "obtain": "get",
            "acquire": "get",
            "comprehend": "understand",
            "analyze": "study",
            "evaluate": "check",
            "assess": "check",
            "determine": "find out",
            "identify": "find",
            "recognize": "know",
            "acknowledge": "know",
            "appreciate": "like",
            "conceptualize": "think",
            "deliberate": "think about",
            "generate": "make",
            "initiate": "start",
            "originate": "start",
            "proceed": "go on",
            "terminate": "end",
            "conclude": "end",
            "finalize": "finish",
            "accomplish": "do",
            "achieve": "do",
            "attain": "get",
            "secure": "get",
            "procure": "get",
            "retrieve": "get back",
            "accumulate": "gather",
            "integrate": "put together",
            "synthesize": "put together",
            "coordinate": "organize",
            "orchestrate": "organize",
            "administer": "manage",
            "supervise": "watch over",
            "monitor": "watch",
            "regulate": "control",
            "optimize": "make better",
            "enhance": "make better",
            "improve": "make better",
            "augment": "add to",
            "supplement": "add to",
            "complement": "go with",
            "negotiate": "talk about",
            "collaborate": "work together",
            "cooperate": "work together",
            "participate": "take part",
            "contribute": "help",
            "enable": "let",
            "authorize": "let",
            "endorse": "support",
            "promote": "support",
            "encourage": "support",
            "motivate": "push",
            "inspire": "push",
            "stimulate": "push",
            "provoke": "cause",
            "extract": "get",
            "derive": "get",
            "verify": "check",
            "confirm": "check",
            "substantiate": "prove",
            "corroborate": "prove",
            "authenticate": "prove real",
            "certify": "prove",
            "standardize": "make the same",
            "normalize": "make normal",
            "streamline": "make smooth",
            "simplify": "make simple",
            "clarify": "make clear",
            "elucidate": "make clear",
            "elaborate": "explain more",
            "articulate": "say clearly",
            "communicate": "tell",
            "convey": "tell",
            "transmit": "send",
            "disseminate": "spread",
            "distribute": "give out",
            "allocate": "give",
            "assign": "give",
            "organize": "sort",
            "arrange": "put in order",
            "sequence": "put in order",
            "prioritize": "put first",
            "evaluate": "judge",
        }

    def _normalize_for_rules(self, text: str) -> str:
        # Keep punctuation; we only lowercase for matching/substitution.
        return text.lower()

    def _restore_capitalization(self, original: str, simplified: str) -> str:
        # Best-effort: keep the first character of words capitalized if the
        # corresponding original word started with a capital letter.
        words = simplified.split()
        original_words = original.split()
        for i, word in enumerate(words):
            if i < len(original_words) and original_words[i] and original_words[i][0].isupper() and len(original_words[i]) > 1:
                words[i] = word.capitalize()
        return " ".join(words)

    def _apply_word_replacements(self, text: str, word_map: Dict[str, str]) -> str:
        # Apply whole-word substitutions (case-insensitive).
        for complex_word, simple_word in word_map.items():
            pattern = r"\b" + re.escape(complex_word) + r"\b"
            text = re.sub(pattern, simple_word, text, flags=re.IGNORECASE)
        return text

    def _split_long_sentence(self, sentence: str) -> List[str]:
        # Split at conjunctions to shorten sentences for younger readers.
        # Use a non-capturing group so the conjunction tokens are not included in the output.
        # Note: we intentionally do NOT split on "and" because it often appears inside
        # phrases like "both X and Y" and splitting it produces grammatical fragments.
        parts = re.split(r"\s+(?:or|but|so|because|however|therefore)\s+", sentence, flags=re.IGNORECASE)
        cleaned = [p.strip() for p in parts if p and p.strip()]
        if len(cleaned) > 1:
            return cleaned

        # If no conjunction split, fall back to comma split.
        comma_parts = [p.strip() for p in sentence.split(",") if p.strip()]
        return comma_parts if len(comma_parts) > 1 else [sentence.strip()]

    def _chunk_sentence_words(self, sentence: str, max_words: int) -> List[str]:
        tokens = sentence.split()
        if max_words <= 0:
            return [sentence]
        if len(tokens) <= max_words:
            return [sentence]
        chunks = [" ".join(tokens[i:i + max_words]) for i in range(0, len(tokens), max_words)]

        # Smooth awkward breaks like "... of both. waves ..."
        # by merging chunks when the boundary would be ungrammatical.
        boundary_bad_end = {"both", "of", "to", "in", "on", "with", "at", "by", "from", "for", "the", "a", "an"}
        boundary_bad_start = {"and", "or", "but", "so"}
        smoothed: List[str] = []
        i = 0
        while i < len(chunks):
            cur = chunks[i].strip()
            nxt = chunks[i + 1].strip() if i + 1 < len(chunks) else ""
            cur_last = cur.split()[-1].lower() if cur else ""
            nxt_first = nxt.split()[0].lower() if nxt else ""

            if nxt and (cur_last in boundary_bad_end or nxt_first in boundary_bad_start):
                merged = (cur + " " + nxt).strip()
                smoothed.append(merged)
                i += 2
                continue

            smoothed.append(cur)
            i += 1

        chunks = [c for c in smoothed if c]
        # Avoid tiny trailing chunks that create choppy/incorrect punctuation.
        if len(chunks) >= 2 and len(chunks[-1].split()) <= 3:
            chunks[-2] = (chunks[-2] + " " + chunks[-1]).strip()
            chunks.pop()
        return chunks

    def _cleanup_punctuation(self, text: str) -> str:
        # Normalize whitespace + common punctuation artifacts for readability.
        text = re.sub(r"\s+", " ", (text or "").strip())
        # Remove spaces before punctuation.
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)
        # Avoid duplicated punctuation like ".." or "!!".
        text = re.sub(r"([.!?])\1+", r"\1", text)
        # Avoid comma directly before a period.
        text = re.sub(r",\.", ".", text)
        # Ensure there is exactly one space after sentence-ending punctuation.
        text = re.sub(r"([.!?])(\w)", r"\1 \2", text)
        return text.strip()

    def _split_into_segments(self, text: str) -> List[str]:
        # Convert semicolons/colons/dashes to periods so we don't retain odd punctuation placement.
        normalized = text
        normalized = normalized.replace("\n", " ")
        normalized = re.sub(r"[;:]+", ".", normalized)
        normalized = re.sub(r"[—–\-]{1,2}", " ", normalized)
        normalized = self._cleanup_punctuation(normalized)

        # Split into sentence-like segments.
        parts = re.split(r"(?<=[.!?])\s+", normalized)
        return [p.strip() for p in parts if p and p.strip()]

    def _fallback_simplify(self, text: str, target_level: str, preserve_meaning: bool = True) -> Dict[str, any]:
        original_text = text
        # Keep original for capitalization heuristics; rules operate on a lowercase copy.
        working_original = (text or "").strip()
        working = self._normalize_for_rules(working_original)

        # Pick which substitutions to apply based on level.
        if target_level == "elementary":
            level_words = self.complex_words
        elif target_level in ["middle_school", "middle-school", "medium"]:
            level_words = {k: v for k, v in self.complex_words.items() if len(k) > 8 or k in ["utilize", "facilitate", "implement", "methodology"]}
        elif target_level == "high_school":
            level_words = {k: v for k, v in self.complex_words.items() if len(k) > 10}
        elif target_level == "college":
            level_words = {k: v for k, v in self.complex_words.items() if len(k) > 12}
        else:
            level_words = self.complex_words

        working = self._apply_word_replacements(working, level_words)

        # Lightweight phrase rewrites to improve grammar in fallback mode.
        # (These are intentionally small and safe-ish; they only trigger on common markers.)
        working = re.sub(r"\bwhereby\b", "this means", working)
        working = re.sub(r"\bdepending on\b", "this depends on", working)
        # Handle combined phrase first so we don't create leftover "employed".
        working = re.sub(r"\bmethod of observation employed\b", "how we observe things", working)
        working = re.sub(r"\bmethod of observation\b", "how we observe things", working)
        working = re.sub(r"\bobservation employed\b", "observation", working)
        working = re.sub(r"\bthis depends on the how\b", "this depends on how", working)

        # Simplification by word budget per sentence/segment.
        level_config = self.readability_levels.get(target_level, self.readability_levels["high_school"])
        max_words = int(level_config.get("max_sentence_length", 12))

        simplified_segments: List[str] = []
        for seg in self._split_into_segments(working):
            seg = seg.strip()
            if not seg:
                continue

            # If the segment is long, try splitting it into smaller clause-ish parts.
            candidates: List[str] = [seg]
            seg_lower = seg.lower()
            if any(tok in seg_lower for tok in [" or ", " but ", " so ", " because ", " however ", " therefore "]) and len(seg.split()) > max_words:
                candidates = self._split_long_sentence(seg)
            elif "," in seg and len(seg.split()) > max_words:
                # Split comma lists into smaller parts.
                candidates = [c.strip() for c in seg.split(",") if c.strip()]

            # Chunk by words if still too long.
            for cand in candidates:
                cand = cand.strip()
                if not cand:
                    continue
                # Prefer not to chunk aggressively; it tends to create fragments.
                # Only chunk as a last resort when we still have very long segments.
                if len(cand.split()) > max_words * 2:
                    simplified_segments.extend(self._chunk_sentence_words(cand, max_words))
                else:
                    simplified_segments.append(cand)

        # Join segments into clean sentences.
        cleaned_segments = []
        for s in simplified_segments:
            # Remove trailing punctuation so joining doesn't create "random" punctuation.
            s2 = re.sub(r"[.!?;:,]+$", "", s).strip()
            if s2:
                # Avoid chunks that start with leading conjunctions.
                s2 = re.sub(r"^(and|but|so)\s+", "", s2).strip()
                cleaned_segments.append(s2)

        working = ". ".join(cleaned_segments)
        working = self._cleanup_punctuation(working)

        if target_level == "elementary":
            # Add a couple of extra plain-word swaps.
            improvements = {
                "data": "information",
                "analysis": "study",
                "research": "study",
                "experiment": "test",
                "hypothesis": "guess",
                "concept": "idea",
                "strategy": "plan",
                "framework": "plan",
                "procedure": "way",
            }
            working = self._apply_word_replacements(working, improvements)

        # Restore some capitalization: capitalize each sentence's first letter.
        working = working.strip()
        if working:
            segments = re.split(r"(?<=[.!?])\s+", working)
            segments = [seg[:1].upper() + seg[1:] if seg else seg for seg in segments]
            working = " ".join(segments)

        simplified_text = working

        # Ensure sentence end punctuation.
        if simplified_text and simplified_text[-1] not in [".", "!", "?"]:
            simplified_text += "."

        readability_score = self._calculate_readability(simplified_text)
        level_config = self.readability_levels.get(target_level, self.readability_levels["high_school"])

        return {
            "original_text": original_text,
            "simplified_text": simplified_text,
            "target_level": target_level,
            "readability_score": readability_score,
            "level_config": level_config,
        }

    async def simplify(self, text: str, target_level: str, preserve_meaning: bool = True) -> Dict[str, any]:
        """Simplify text using OpenAI GPT-4 for professional quality"""
        try:
            if target_level not in self.readability_levels:
                raise ValueError(f"Invalid reading level: {target_level}")
            
            level_config = self.readability_levels[target_level]
            
            if self.client is None:
                if self.allow_fallback:
                    return self._fallback_simplify(text=text, target_level=target_level, preserve_meaning=preserve_meaning)
                raise Exception(
                    "OPENAI_API_KEY is not configured. Set a valid OPENAI_API_KEY in backend/.env and restart the backend."
                )

            # Create detailed system prompt for OpenAI
            system_prompt = self._create_system_prompt(target_level, level_config)
            
            # User prompt with the text to simplify
            user_prompt = f"Please simplify the following text according to the specified reading level:\n\n{text}"
            
            # Call OpenAI API
            openai_model = os.getenv("OPENAI_SIMPLIFY_MODEL", "gpt-4o-mini")
            response = self.client.chat.completions.create(
                model=openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
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
            # If OpenAI errors out (invalid/missing key, rate limits, etc),
            # either fall back (dev mode) or fail loudly so you don't get low-quality output.
            if self.allow_fallback:
                return self._fallback_simplify(text=text, target_level=target_level, preserve_meaning=preserve_meaning)

            openai_error_text = str(e).lower()
            if any(
                token in openai_error_text
                for token in ["invalid api key", "incorrect api key", "authentication", "401", "unauthorized", "not authorized"]
            ):
                raise Exception(
                    "OpenAI authentication failed for text simplification. Your OPENAI_API_KEY is invalid/unauthorized."
                )

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
