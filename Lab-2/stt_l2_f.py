import csv
import re
import pandas as pd
import matplotlib.pyplot as plt

input_file = "bug_fixes_diffs_llm.csv"

bug_keywords = [
    "fix", "fixed", "fixes", "bug", "crash",
    "solves", "resolves", "resolve", "issue", "regression",
    "fall back", "assertion", "coverity", "reproducible",
    "stack", "broken", "differential testing", "error",
    "hang", "test fix", "steps to reproduce", "failure",
    "leak", "stack trace", "heap overflow", "freeze",
    "problem", "overflow", "avoid", "workaround",
    "break", "stop"
]

def is_precise(msg, filename=None, threshold=3):
    if not msg:
        return False
    
    score = 0
    # 1. Filename mention
    if filename and filename.lower() in msg.lower():
        score += 1
    # 2. Starts with add/fix/update
    if re.match(r"^(add|fix|update)\b", msg.lower()):
        score += 1
    # 3. Contains bug keyword
    if any(keyword in msg.lower() for keyword in bug_keywords):
        score += 1
    # 4. Contains technical keyword
    if re.search(r"\.py|function|method|class|error|exception|crash|leak", msg.lower()):
        score += 1
    
    return score >= threshold

df = pd.read_csv(input_file)

# --- Add precision labels ---
df["Dev_Precise"] = df["Developer Message"].apply(is_precise)
df["LLM_Precise"] = df["LLM Inference"].apply(is_precise)
df["Rect_Precise"] = df["Rectified Message"].apply(is_precise)

# --- Compute hit rates ---
total = len(df)
dev_precise = df["Dev_Precise"].sum()
llm_precise = df["LLM_Precise"].sum()
rect_precise = df["Rect_Precise"].sum()

hit_rates = {
    "Developer": round(dev_precise / total * 100, 2),
    "LLM": round(llm_precise / total * 100, 2),
    "Rectifier": round(rect_precise / total * 100, 2),
}

print("=== Hit Rates (RQ1–RQ3) ===")
for k, v in hit_rates.items():
    print(f"{k}: {v}% precise")

df.to_csv("bug_fixes_eval.csv", index=False)

plt.bar(hit_rates.keys(), hit_rates.values())
plt.ylabel("Hit Rate (%)")
plt.title("Commit Message Precision Comparison")
plt.show()
