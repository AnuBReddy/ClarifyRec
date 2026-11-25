"""Small deterministic smoke comparison; not a human-subject study."""
import csv, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from clarifyrec.strategies import ImmediateUpdater, WeightedUpdater, ClarifyRec

SCENARIOS = [
    ["I like romance", "I want something lighter"],
    ["I like comedy", "Actually, I want something serious rather than comedy"],
    ["I like romance", "I don't want a tragic ending"],
]
CLASSES = [("immediate", ImmediateUpdater), ("weighted", WeightedUpdater), ("clarifyrec", ClarifyRec)]
rows=[]
for name, cls in CLASSES:
    clarification_count=0; resolved=0; outputs=0
    for scenario in SCENARIOS:
        engine=cls()
        for utterance in scenario:
            result=engine.process(utterance)
            if result["status"] == "clarification_pending":
                clarification_count += 1
                reply="1"
                result=engine.process(reply)
                resolved += int(result["status"] == "resolved")
        outputs += 1
    rows.append({"strategy":name,"scenarios":outputs,"clarification_prompts":clarification_count,"simulated_resolutions":resolved,"note":"Deterministic software smoke test only; not evidence of user satisfaction or general recommendation quality."})
out=os.path.join(os.path.dirname(__file__),"comparison_smoke_results.csv")
with open(out,"w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
print(f"Wrote {out}")
for r in rows: print(r)
