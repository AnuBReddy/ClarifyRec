from .nlp import extract_preferences
from .preference import PreferenceProfile
from .recommender import recommend

class ImmediateUpdater:
    name = "Immediate update baseline"
    def __init__(self): self.profile = PreferenceProfile()
    def process(self, text):
        parsed = extract_preferences(text); self.profile.apply(parsed, "immediate")
        return {"status":"updated", "message":"I updated your profile using the explicit preferences I recognised.", "parsed":parsed, "recommendations":recommend(self.profile), "profile":self.profile.to_dict()}

class WeightedUpdater:
    name = "Weighted update baseline"
    def __init__(self): self.profile = PreferenceProfile()
    def process(self, text):
        parsed = extract_preferences(text)
        weight = min(1.25, 0.75 + 0.1 * (len(self.profile.history) + 1))
        self.profile.apply(parsed, "weighted", weight)
        return {"status":"updated", "message":f"I updated recognised preferences (feedback weight {weight:.2f}).", "parsed":parsed, "recommendations":recommend(self.profile), "profile":self.profile.to_dict()}

class ClarifyRec:
    name = "ClarifyRec (uncertainty-aware)"
    def __init__(self):
        self.profile = PreferenceProfile(); self.pending = None
    def process(self, text):
        if self.pending:
            options = self.pending["options"]
            low = text.lower()
            chosen = next((o for o in options if any(w in low for w in o.split() if len(w)>3)), None)
            if chosen is None and any(x in low for x in ["first", "1"]): chosen = options[0]
            if chosen is None and any(x in low for x in ["second", "2"]): chosen = options[1]
            if chosen is None and any(x in low for x in ["third", "3"]): chosen = options[2]
            if chosen is None:
                return {"status":"clarification_pending", "message":"Please choose one interpretation: " + "; ".join(f"{i+1}. {o}" for i,o in enumerate(options)), "parsed":{}, "recommendations":[], "profile":self.profile.to_dict()}
            if "humorous" in chosen: self.profile.likes["comedy"] = self.profile.likes.get("comedy",0)+1
            elif "serious" in chosen or "emotionally intense" in chosen: self.profile.dislikes["serious"] = self.profile.dislikes.get("serious",0)+1
            elif "sad" in chosen: self.profile.constraints["ending"] = "not tragic"
            elif "lighter tone" in chosen: self.profile.likes["lighthearted"] = self.profile.likes.get("lighthearted",0)+1
            self.profile.history.append(text); self.pending = None
            return {"status":"resolved", "message":f"Thanks — I interpreted that as: {chosen}. I have updated your profile.", "parsed":{"clarification":chosen}, "recommendations":recommend(self.profile), "profile":self.profile.to_dict()}
        parsed = extract_preferences(text)
        if parsed["ambiguous"]:
            ambiguity = parsed["ambiguous"][0]
            safe = dict(parsed)
            safe["dislikes"] = [x for x in parsed["dislikes"] if x != "serious"]
            safe["likes"] = [x for x in parsed["likes"] if x != "serious"]
            safe["constraints"] = []
            self.profile.apply(safe, "immediate")
            self.pending = {"phrase":ambiguity["phrase"], "options":ambiguity["interpretations"]}
            return {"status":"clarification_pending", "message":f"When you say '{ambiguity['phrase']}', which meaning is closest? " + " / ".join(f"{i+1}. {o}" for i,o in enumerate(ambiguity["interpretations"])), "parsed":parsed, "recommendations":[], "profile":self.profile.to_dict()}
        self.profile.apply(parsed, "immediate")
        return {"status":"updated", "message":"That correction is specific enough, so I updated your preferences without an extra question.", "parsed":parsed, "recommendations":recommend(self.profile), "profile":self.profile.to_dict()}

STRATEGIES = {"Immediate update":ImmediateUpdater, "Weighted update":WeightedUpdater, "ClarifyRec":ClarifyRec}
