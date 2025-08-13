#!/usr/bin/env python3
"""
Test script for the improved TextSimplifier
"""

import asyncio
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.text_simplifier import TextSimplifier

async def test_simplifier():
    """Test the text simplifier with the example text"""
    
    # Example text from user
    example_text = """Artificial intelligence is a branch of computer science that focuses on creating machines capable of performing tasks that normally require human intelligence. These tasks include understanding language, recognizing patterns, solving problems, and making decisions. In recent years, advances in AI have led to breakthroughs in healthcare, education, transportation, and many other fields, making it a powerful tool for shaping the future."""
    
    simplifier = TextSimplifier()
    
    print("Testing Text Simplifier with different reading levels...")
    print("=" * 80)
    print(f"Original text:\n{example_text}\n")
    
    # Test different reading levels
    levels = ["elementary", "middle_school", "high_school", "college"]
    
    for level in levels:
        print(f"\n--- {level.upper()} LEVEL ---")
        try:
            simplified = await simplifier.simplify(example_text, target_level=level)
            print(f"Simplified text:\n{simplified}")
            
            # Calculate readability scores
            original_score = simplifier.calculate_readability(example_text)
            simplified_score = simplifier.calculate_readability(simplified)
            
            print(f"\nReadability scores:")
            print(f"  Original: {original_score:.1f}")
            print(f"  Simplified: {simplified_score:.1f}")
            print(f"  Improvement: {simplified_score - original_score:.1f}")
            
        except Exception as e:
            print(f"Error testing {level} level: {e}")
        
        print("-" * 40)

if __name__ == "__main__":
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key before running this test")
        sys.exit(1)
    
    print("Starting Text Simplifier test...")
    asyncio.run(test_simplifier()) 