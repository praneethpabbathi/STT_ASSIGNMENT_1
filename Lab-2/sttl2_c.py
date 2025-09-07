import csv
from pydriller import Repository

repo_url = "https://github.com/pythonprofilers/memory_profiler.git"

output_file = "/Users/praneethpabbathi/bug_fixes.csv"

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

with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # CSV header
    writer.writerow(["Hash", "Message", "Parent Hashes", "Is Merge Commit?", "Modified Files"])
    # Traverse commits in the repo
    for commit in Repository(repo_url).traverse_commits():
        msg = commit.msg.lower()
        
        # Check if commit message contains any bug-fixing keyword
        if any(keyword in msg for keyword in bug_keywords):
            parent_hashes = commit.parents         
            modified_files = [m.filename for m in commit.modified_files]  

            # Write row to CSV
            writer.writerow([
                commit.hash,
                commit.msg.strip(),
                parent_hashes,
                commit.merge,
                modified_files
            ])

print(f"Bug-fixing commits saved to {output_file}")
