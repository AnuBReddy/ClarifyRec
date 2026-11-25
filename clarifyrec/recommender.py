from .catalog import MOVIES

def score_movie(movie, profile):
    score = 0.0
    features = set(movie["genres"] + movie["mood"] + movie["themes"] + [movie["pacing"], movie["ending"]])
    for feature, weight in profile.likes.items():
        if feature in features: score += 2.0 * weight
    for feature, weight in profile.dislikes.items():
        if feature in features: score -= 2.5 * weight
    ending = profile.constraints.get("ending")
    if ending == "not tragic" and movie["ending"] == "tragic": score -= 100
    if ending in ("happy", "tragic") and movie["ending"] != ending: score -= 2
    return score

def recommend(profile, limit=5, exclude_ids=None):
    exclude_ids = set(exclude_ids or [])
    ranked = sorted((m for m in MOVIES if m["id"] not in exclude_ids), key=lambda m: (score_movie(m, profile), -m["year"]), reverse=True)
    return [{**m, "score": round(score_movie(m, profile), 2)} for m in ranked[:limit]]
