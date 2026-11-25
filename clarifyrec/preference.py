from dataclasses import dataclass, field

@dataclass
class PreferenceProfile:
    likes: dict = field(default_factory=dict)
    dislikes: dict = field(default_factory=dict)
    constraints: dict = field(default_factory=dict)
    history: list = field(default_factory=list)

    def apply(self, extracted, strategy="immediate", feedback_weight=1.0):
        self.history.append(extracted["raw"])
        if strategy == "immediate":
            weight = 1.0
        elif strategy == "weighted":
            weight = feedback_weight
        else:
            weight = 1.0
        for item in extracted.get("likes", []):
            self.likes[item] = min(3.0, self.likes.get(item, 0.0) + weight)
            self.dislikes.pop(item, None)
        for item in extracted.get("dislikes", []):
            self.dislikes[item] = min(3.0, self.dislikes.get(item, 0.0) + weight)
            self.likes.pop(item, None)
        for constraint in extracted.get("constraints", []):
            self.constraints[constraint["attribute"]] = constraint["value"]
        return self

    def to_dict(self):
        return {"likes": self.likes, "dislikes": self.dislikes, "constraints": self.constraints, "history": self.history}
