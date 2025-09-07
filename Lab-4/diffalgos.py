import csv
import subprocess
from pydriller import Repository

repo_paths = [
    "/Users/praneethpabbathi/lab4_repos/androguard",
    "/Users/praneethpabbathi/lab4_repos/deeppavlov",
    "/Users/praneethpabbathi/lab4_repos/deap"
    ]

output_csv = "lab4_dataset.csv"

def extract_diff(repo_dir, parent_sha, commit_sha, filepath, algorithm):
    cmd = [
        "git", "-C", repo_dir, "diff",
        f"--diff-algorithm={algorithm}",
        "-w", "--ignore-blank-lines",
        parent_sha, commit_sha, "--", filepath
    ]
    process = subprocess.run(cmd, text=True, capture_output=True)
    return process.stdout.strip()

with open(output_csv, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([
        "old_file_path", "new_file_path",
        "commit_SHA", "parent_SHA",
        "commit_message", "diff_myers", "diff_hist"
    ])

    for repo in repo_paths:
        print(f"\nAnalyzing repository: {repo}")
        for commit in Repository(repo).traverse_commits():
            
            if len(commit.parents) != 1:
                continue
            
            parent = commit.parents[0]
            
            for mod in commit.modified_files:
                old_file = mod.old_path or ""
                new_file = mod.new_path or ""
                target_file = new_file if new_file else old_file

                try:
                    diff_m = extract_diff(repo, parent, commit.hash, target_file, "myers")
                    diff_h = extract_diff(repo, parent, commit.hash, target_file, "histogram")

                    writer.writerow([
                        old_file, new_file,
                        commit.hash, parent,
                        commit.msg.replace("\n", " ").strip(),
                        diff_m, diff_h
                    ])
                except Exception as e:
                    print(f"Skipped {target_file} in {commit.hash}: {e}")
