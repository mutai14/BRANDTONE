"""
Formatting rules enforcement for BrandTone.
"""

import re
from typing import Dict, List, Tuple, Any


class FormattingRules:
    """Enforces formatting rules on marketing text."""
    
    def __init__(self):
        """Initialize formatting rules."""
        # Default formatting rules
        self.rules = {
            "all_caps": {
                "pattern": r'\b[A-Z]{3,}\b',
                "description": "Avoid using ALL CAPS words",
                "fix": self._fix_all_caps
            },
            "multiple_exclamations": {
                "pattern": r'!{2,}',
                "description": "Avoid using multiple exclamation points",
                "fix": self._fix_multiple_exclamations
            },
            "inconsistent_bullets": {
                "pattern": r'(?:(?<=\n)|^)\s*[-*•+]\s',
                "description": "Maintain consistent bullet formatting",
                "fix": self._fix_inconsistent_bullets
            },
            "long_sentences": {
                "pattern": r'[^.!?]+[.!?]',
                "description": "Avoid overly long sentences (>30 words)",
                "fix": self._fix_long_sentences
            },
            "excessive_emdashes": {
                "pattern": r'—',
                "description": "Limit use of em-dashes to avoid AI-generated patterns",
                "fix": self._fix_excessive_emdashes
            }
        }
    
    def _fix_all_caps(self, text: str, match: re.Match) -> str:
        """Fix ALL CAPS by converting to title case."""
        return match.group(0).title()
    
    def _fix_multiple_exclamations(self, text: str, match: re.Match) -> str:
        """Fix multiple exclamation points by replacing with a single one."""
        return "!"
    
    def _fix_inconsistent_bullets(self, text: str, match: re.Match) -> str:
        """Standardize bullet points to use '• '."""
        return "• "
    
    def _fix_excessive_emdashes(self, text: str, match: re.Match) -> str:
        """
        Replace some em-dashes with other punctuation to avoid overuse.
        
        Args:
            text: The full text being processed
            match: The regex match object for the em-dash
            
        Returns:
            A replacement string (either keeps the em-dash or replaces it)
        """
        # Count total em-dashes in the text
        total_emdashes = text.count('—')
        
        # If there are more than 2 em-dashes, replace some with other punctuation
        if total_emdashes > 2:
            # Keep first em-dash, replace others with commas or periods
            first_dash_pos = text.find('—')
            current_pos = match.start()
            
            if current_pos == first_dash_pos:
                return '—'  # Keep the first em-dash
            else:
                # Randomly choose between comma, period, or keeping the em-dash
                # This creates natural variation
                import random
                replacements = [',', '.', '—', '—']  # 50% chance of keeping
                return random.choice(replacements)
        
        return '—'  # Keep the em-dash if there aren't too many
        
    def _fix_long_sentences(self, text: str, match: re.Match) -> str:
        """Check if sentence is too long and mark it for review."""
        sentence = match.group(0)
        word_count = len(sentence.split())
        if word_count > 30:
            # Just return the original; we'll flag it in the violations report
            pass
        return sentence
    
    def add_custom_rule(self, name: str, pattern: str, description: str, fix_function: callable) -> None:
        """
        Add a custom formatting rule.
        
        Args:
            name: Name of the rule.
            pattern: Regex pattern to match.
            description: Description of the rule.
            fix_function: Function to fix violations.
        """
        self.rules[name] = {
            "pattern": pattern,
            "description": description,
            "fix": fix_function
        }
    
    def remove_rule(self, rule_name: str) -> bool:
        """
        Remove a formatting rule.
        
        Args:
            rule_name: Name of the rule to remove.
            
        Returns:
            True if rule was removed, False if it didn't exist.
        """
        if rule_name in self.rules:
            del self.rules[rule_name]
            return True
        return False
    
    def check_violations(self, text: str) -> Dict[str, List[str]]:
        """
        Check for formatting violations.
        
        Args:
            text: Text to check.
            
        Returns:
            Dictionary of rule names and their violations.
        """
        violations = {}
        
        for rule_name, rule in self.rules.items():
            matches = list(re.finditer(rule["pattern"], text))
            if matches:
                violations[rule_name] = [
                    {
                        "text": match.group(0),
                        "start": match.start(),
                        "end": match.end()
                    }
                    for match in matches
                ]
                
                # Special case for long sentences
                if rule_name == "long_sentences":
                    violations[rule_name] = [
                        v for v in violations[rule_name] 
                        if len(v["text"].split()) > 30
                    ]
                    if not violations[rule_name]:
                        del violations[rule_name]
        
        return violations
    
    def fix_violations(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Fix formatting violations.
        
        Args:
            text: Text to fix.
            
        Returns:
            Tuple of (fixed_text, report).
        """
        original_text = text
        violations = self.check_violations(text)
        fixes_applied = {}
        
        # Apply fixes in reverse order of appearance to avoid offset issues
        all_matches = []
        for rule_name, rule_violations in violations.items():
            for violation in rule_violations:
                all_matches.append((
                    rule_name,
                    violation["start"],
                    violation["end"],
                    violation["text"]
                ))
        
        # Sort by start position in descending order
        all_matches.sort(key=lambda x: x[1], reverse=True)
        
        # Apply fixes
        for rule_name, start, end, original in all_matches:
            rule = self.rules[rule_name]
            # Create a match object (this is a bit hacky but works for our purpose)
            match = re.match(rule["pattern"], original)
            if not match:
                # If we can't recreate the match object, use the original text
                match = type('obj', (object,), {'group': lambda self, *args: original})()
            
            # Apply the fix
            fixed_text = rule["fix"](text, match)
            
            # Replace the text
            text = text[:start] + fixed_text + text[end:]
            
            # Record the fix
            if rule_name not in fixes_applied:
                fixes_applied[rule_name] = []
            fixes_applied[rule_name].append({
                "original": original,
                "fixed": fixed_text
            })
        
        # Prepare the report
        report = {
            "violations_found": len(all_matches),
            "fixes_applied": fixes_applied,
            "rules_triggered": list(violations.keys())
        }
        
        return text, report
