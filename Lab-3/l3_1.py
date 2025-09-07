
import pandas as pd
import os 
import numpy as np 
from collections import Counter 

df = pd.read_csv("/Users/praneethpabbathi/bug_fixes_diffs_llm.csv")

commit_count = df["Hash"].nunique()
file_count = df["Filename"].nunique()


# Average number of files touched per commit
files_per_commit = df.groupby("Hash")["Filename"].nunique()
avg_files_per_commit = files_per_commit.mean()


# Bug-fix type distribution
fix_type_stats = df["LLM Inference"].value_counts()

# Top 10 frequently modified files
frequent_files = df["Filename"].value_counts().head(10)

# Top 10 file extensions
df["Ext"] = df["Filename"].apply(lambda x: os.path.splitext(str(x))[1])
frequent_exts = df["Ext"].value_counts().head(10)

# Print outputs
print("=== Baseline Descriptive Statistics ===")
print(f"Number of commits: {commit_count}")
print(f"Number of unique files: {file_count}")
print(f"Average files changed per commit: {avg_files_per_commit:.2f}")

print("\n=== Fix Type Distribution ===")
print(fix_type_stats)

print("\n=== Top 10 Modified Files ===")
print(frequent_files)

print("\n=== Top 10 File Extensions ===")
print(frequent_exts)
