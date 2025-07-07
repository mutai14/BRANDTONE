"""
Core tone conversion functionality for BrandTone.
"""

from typing import Dict, Any, List, Tuple
from utils import call_openai

class ToneConverter:
    """
    Converts text to match specified brand tones.
    """
    
    def __init__(self):
        """Initialize the tone converter with predefined tone profiles."""
        # Define tone profiles with characteristics and examples
        self.tone_profiles = {
            "casual": {
                "description": "Friendly, conversational, and approachable. Uses contractions, simpler vocabulary, and a personal tone.",
                "characteristics": [
                    "Uses contractions (don't, we're, it's)",
                    "Employs first and second person (we, you)",
                    "Incorporates colloquial expressions",
                    "Uses shorter sentences and paragraphs",
                    "Asks rhetorical questions occasionally"
                ],
                "example": "Hey there! We're excited to show you our new product. It's designed with you in mind, and we think you'll love how easy it is to use."
            },
            "formal": {
                "description": "Professional, authoritative, and precise. Avoids contractions, uses complex vocabulary, and maintains emotional distance.",
                "characteristics": [
                    "Avoids contractions",
                    "Uses third person perspective predominantly",
                    "Employs precise vocabulary and technical terms when appropriate",
                    "Maintains longer, more complex sentence structures",
                    "Avoids colloquialisms and slang"
                ],
                "example": "Company XYZ is pleased to announce the launch of its latest innovation. The product has been meticulously engineered to deliver optimal performance and efficiency for all users."
            },
            "playful": {
                "description": "Energetic, humorous, and engaging. Uses wordplay, creative language, and conveys excitement.",
                "characteristics": [
                    "Incorporates wordplay and puns",
                    "Uses more exclamatory statements (limited to one ! per sentence)",
                    "Employs creative metaphors and analogies",
                    "Keeps sentences varied but generally shorter",
                    "Occasionally breaks conventional grammar rules for effect"
                ],
                "example": "Ready for a wild ride? Our new gadget isn't just a tool—it's your new sidekick! Think of it as the Swiss Army knife of software, but way more fun."
            },
            "technical": {
                "description": "Precise, detailed, and data-driven. Focuses on specifications, functionality, and technical benefits.",
                "characteristics": [
                    "Uses industry-specific terminology accurately",
                    "Emphasizes specifications and technical features",
                    "Maintains logical flow with clear transitions",
                    "Incorporates data points and measurable benefits",
                    "Minimizes emotional language in favor of factual statements"
                ],
                "example": "The XJ-5000 features a 2.4GHz quad-core processor with 16GB RAM, enabling 40% faster rendering compared to previous models. Its proprietary cooling system maintains optimal operating temperature under high-load conditions."
            },
            "genz": {
                "description": "Ultra-casual, internet-savvy, and relatable. Uses Gen-Z slang, abbreviations, and a very conversational tone while keeping it PG-13.",
                "characteristics": [
                    "Uses modern internet slang and abbreviations (e.g., 'fr' for for real, 'lowkey', 'highkey')",
                    "Employs emojis and casual punctuation (!!, !!, !?, ??)",
                    "Uses first and second person liberally",
                    "Short, punchy sentences with occasional sentence fragments",
                    "References internet culture and memes when appropriate",
                    "Keeps language casual but professional enough for most brands",
                    "Uses abbreviations like 'tbh', 'ngl', 'imo' naturally"
                ],
                "example": "okay so this new drop is actually fire 🔥 ngl we went all out on this one. it's giving major main character energy fr. tap in before it's gone!!"
            }
        }
    
    def get_available_tones(self) -> List[str]:
        """
        Get the list of available tone profiles.
        
        Returns:
            List of available tone names.
        """
        return list(self.tone_profiles.keys())
    
    def get_tone_details(self, tone_name: str) -> Dict[str, Any]:
        """
        Get details about a specific tone profile.
        
        Args:
            tone_name: Name of the tone profile.
            
        Returns:
            Dictionary with tone details or empty dict if not found.
        """
        return self.tone_profiles.get(tone_name, {})
    
    def convert_text(self, text: str, target_tone: str) -> Tuple[str, Dict[str, Any]]:
        """
        Convert text to match a target tone.
        
        Args:
            text: The text to convert.
            target_tone: The target tone profile name.
            
        Returns:
            Tuple of (converted_text, metadata).
        """
        if target_tone not in self.tone_profiles:
            return text, {"error": f"Tone profile '{target_tone}' not found"}
        
        # Get the tone profile
        tone_profile = self.tone_profiles[target_tone]
        
        # Create the prompt for OpenAI
        prompt = self._create_tone_conversion_prompt(text, target_tone, tone_profile)
        
        # Call OpenAI API
        converted_text = call_openai(prompt)
        
        # Create metadata
        metadata = {
            "original_text": text,
            "target_tone": target_tone,
            "tone_description": tone_profile["description"],
            "characteristics_applied": tone_profile["characteristics"]
        }
        
        # Optionally run a QA check
        qa_result = self._run_qa_check(converted_text, target_tone, tone_profile)
        metadata["qa_check"] = qa_result
        
        return converted_text, metadata
    
    def _create_tone_conversion_prompt(self, text: str, tone_name: str, tone_profile: Dict[str, Any]) -> str:
        """
        Create a prompt for the OpenAI API to convert text to a target tone.
        
        Args:
            text: The text to convert.
            tone_name: The name of the target tone.
            tone_profile: The tone profile details.
            
        Returns:
            Prompt for the OpenAI API.
        """
        prompt = f"""
        Rewrite the following marketing text to match a {tone_name} tone. 

        Tone characteristics:
        {tone_profile['description']}
        
        Specific style elements to incorporate:
        {chr(10).join('- ' + char for char in tone_profile['characteristics'])}
        
        Example of the target tone:
        "{tone_profile['example']}"
        
        Follow these additional formatting rules:
        1. Do not use ALL CAPS for emphasis
        2. Use at most one exclamation point per paragraph (except for genz tone)
        3. Keep bullet points consistent using the • symbol
        4. Aim for sentences with 20 words or fewer (can be more flexible with genz tone)
        
        Original text:
        "{text}"
        
        Rewritten text in {tone_name} tone:
        """
        return prompt
    
    def _run_qa_check(self, text: str, tone_name: str, tone_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run a QA check on the converted text.
        
        Args:
            text: The converted text.
            tone_name: The name of the target tone.
            tone_profile: The tone profile details.
            
        Returns:
            QA check results.
        """
        prompt = f"""
        Analyze the following text that was rewritten to match a {tone_name} tone.
        
        Tone characteristics:
        {tone_profile['description']}
        
        Expected style elements:
        {chr(10).join('- ' + char for char in tone_profile['characteristics'])}
        
        Text to analyze:
        "{text}"
        
        Please provide an analysis in JSON format with the following structure:
        {{
            "tone_accuracy": "Score from 1-10",
            "grammar_correctness": "Score from 1-10",
            "strengths": ["List of what works well"],
            "improvement_areas": ["List of suggestions for improvement"],
            "forbidden_elements_found": ["List any ALL CAPS, multiple exclamation points, or inconsistent formatting found"]
        }}
        
        Return ONLY the JSON object, nothing else.
        """
        
        # Call OpenAI API
        qa_response = call_openai(prompt)
        
        # Try to parse the JSON response
        try:
            import json
            qa_result = json.loads(qa_response)
        except:
            # If JSON parsing fails, return the raw response
            qa_result = {"raw_response": qa_response}
        
        return qa_result
    
    def add_custom_tone(self, name: str, description: str, characteristics: List[str], example: str) -> bool:
        """
        Add a custom tone profile.
        
        Args:
            name: Name of the tone.
            description: Description of the tone.
            characteristics: List of tone characteristics.
            example: Example text in this tone.
            
        Returns:
            True if tone was added, False if it already existed.
        """
        if name in self.tone_profiles:
            return False
            
        self.tone_profiles[name] = {
            "description": description,
            "characteristics": characteristics,
            "example": example
        }
        return True
