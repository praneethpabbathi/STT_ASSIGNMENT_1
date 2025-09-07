import csv
import re
from pydriller import Repository
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

repo_url = "https://github.com/pythonprofilers/memory_profiler.git"
output_file = "bug_fixes_diffs_llm.csv"

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

tokenizer = AutoTokenizer.from_pretrained("mamiksik/CommitPredictorT5")
model = AutoModelForSeq2SeqLM.from_pretrained("mamiksik/CommitPredictorT5")

def get_llm_message(commit_msg, diff):
    """Generate commit message from diff using CommitPredictorT5"""
    input_text = f"Original message: {commit_msg}\nDiff:\n{diff}\nRectify:"
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(**inputs, max_length=64)
    llm_msg = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return llm_msg

# Manually chosen precision heuristic 
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
def rectify_message(dev_msg, llm_msg, filename):
    dev_msg = dev_msg.strip()
    llm_msg = llm_msg.strip() if llm_msg else ""

    # If developer message is precise, keep it
    if is_precise(dev_msg):
        return dev_msg  

    # If LLM gave a usable message, prefer it
    if llm_msg and llm_msg.lower() != "unknown":
        if filename not in llm_msg:
            return f"{llm_msg} in {filename}"
        return llm_msg

    # Fallback default
    return f"Bug fix in {filename}"


with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Hash",
        "Developer Message",
        "Filename",
        "Source Before",
        "Source After",
        "Diff",
        "LLM Inference",
        "Rectified Message"
    ])

    for commit in Repository(repo_url).traverse_commits():
        msg = commit.msg.strip()
        if any(keyword in msg.lower() for keyword in bug_keywords):
            for mod in commit.modified_files:
                before_text = mod.source_code_before.replace("\n", "\\n") if mod.source_code_before else ""
                after_text = mod.source_code.replace("\n", "\\n") if mod.source_code else ""
                diff_text = mod.diff.replace("\n", "\\n") if mod.diff else ""

                # LLM inference
                llm_message = get_llm_message(msg, diff_text)

                # Rectification logic applied here
                rectified = rectify_message(msg, llm_message, mod.filename)

                writer.writerow([
                    commit.hash,
                    msg,
                    mod.filename,
                    before_text,
                    after_text,
                    diff_text,
                    llm_message,
                    rectified
                ])

print(f"Bug-fix diffs with LLM + Rectified messages saved to {output_file}")

