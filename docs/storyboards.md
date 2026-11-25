# ClarifyRec interaction storyboards

These are interaction walkthroughs for the current prototype. The example dialogue is reproducible through the Streamlit chat. The recommendation catalogue is a small illustrative dataset, not a live MovieLens integration.

## 1. Ambiguous correction

| Step | User action | System response / feedback |
|---|---|---|
| 1 | “I want something lighter.” | Detects the phrase “lighter” as ambiguous. |
| 2 | User sees three numbered interpretations. | Asks whether “lighter” means less emotionally intense, more humorous, or less serious. |
| 3 | “I mean more humorous.” | Resolves the pending question and adds comedy as a positive preference. |
| 4 | User inspects profile and results. | Updated profile and ranked catalogue are displayed. |

## 2. Contradictory or revised preference

| Step | User action | System response / feedback |
|---|---|---|
| 1 | “I dislike comedy.” | Adds comedy to dislikes. |
| 2 | “Actually, I like comedy.” | Removes comedy from dislikes and adds it to likes. |
| 3 | User inspects profile. | The latest explicit polarity is visible. Unrelated preferences remain. |

## 3. Clear correction

| Step | User action | System response / feedback |
|---|---|---|
| 1 | “I don't want a tragic ending.” | Recognises an explicit ending constraint. |
| 2 | System updates profile immediately. | Does not ask an unnecessary clarification question. |
| 3 | User views recommendations. | Tragic-ending catalogue entries receive a strong penalty. |

**Status note:** Storyboards document interactions supported by the prototype's current rule-based logic. They are not recordings of a user study.
