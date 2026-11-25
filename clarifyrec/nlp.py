"""Local, rule-based preference extraction. No network calls or external model required."""
import re

ALIASES = {
 "romance": ["romance", "romantic", "love story"],
 "comedy": ["comedy", "comedy", "funny", "humorous"],
 "drama": ["drama", "dramatic"], "mystery": ["mystery", "detective"],
 "adventure": ["adventure", "adventurous"], "science fiction": ["sci-fi", "science fiction"],
 "lighthearted": ["lighthearted", "light-hearted", "feel-good", "feel good"],
 "serious": ["serious", "heavy", "dark"], "fast": ["fast-paced", "fast paced", "quick-moving"],
 "slow": ["slow-paced", "slow paced", "slow"],
 "happy": ["happy ending", "positive ending", "uplifting ending"],
 "tragic": ["tragic ending", "sad ending", "unhappy ending"],
}
AMBIGUOUS = {
 "lighter": ["less emotionally intense", "more humorous", "less serious"],
 "light": ["less emotionally intense", "more humorous", "less serious"],
 "not too heavy": ["avoid serious themes", "avoid sad or tragic endings", "prefer a lighter tone"],
 "nothing too heavy": ["avoid serious themes", "avoid sad or tragic endings", "prefer a lighter tone"],
 "dark": ["dark humour", "dark themes", "low-light visual style"],
}

def _contains(text, phrase):
    return re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text) is not None

def extract_preferences(message):
    """Return explicit likes/dislikes, ambiguity and contradiction cues."""
    text = message.lower().strip()
    result = {"likes": [], "dislikes": [], "constraints": [], "ambiguous": [], "revision": False, "raw": message}
    for term, variants in ALIASES.items():
        for phrase in variants:
            if _contains(text, phrase):
                start = text.find(phrase)
                prefix = text[max(0, start - 45):start]
                neg = bool(re.search(r"(?:don't(?: want| like)?|do not(?: want| like)?|dislike|avoid|no|not|without|hate|rather than|instead of|nothing too)(?:\s+\w+){0,3}\s*$", prefix))
                target = result["dislikes"] if neg else result["likes"]
                if term not in target:
                    target.append(term)
                break
    for phrase, interpretations in AMBIGUOUS.items():
        if _contains(text, phrase):
            result["ambiguous"].append({"phrase": phrase, "interpretations": interpretations})
    result["revision"] = any(x in text for x in ["actually", "change my mind", "instead", "now i want", "rather than", "forget that"])
    if any(x in text for x in ["no tragic", "avoid tragic", "don't want a tragic", "do not want a tragic", "no sad ending"]):
        result["constraints"].append({"attribute": "ending", "value": "not tragic"})
    if "happy ending" in text:
        result["constraints"].append({"attribute": "ending", "value": "happy"})
    return result
