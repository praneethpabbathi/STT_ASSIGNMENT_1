import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dataset = pd.read_csv("lab4_dataset_with_discrepancy.csv")


def get_file_category(path):
    if pd.isna(path):
        return "Other"
    path_lower = str(path).lower()
    if "test" in path_lower:
        return "Test Code"
    elif "readme" in path_lower:
        return "README"
    elif "license" in path_lower:
        return "LICENSE"
    elif path_lower.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.rb', '.go', '.cs', '.php')):
        return "Source Code"
    else:
        return "Other"

dataset["file_type"] = dataset["old_file_path"].apply(get_file_category)

file_categories = ["Source Code", "Test Code", "README", "LICENSE"]

stats_summary = {}
for cat in file_categories:
    files_in_cat = dataset[dataset["file_type"] == cat]
    total_files = len(files_in_cat)
    mismatches = len(files_in_cat[files_in_cat["Discrepancy"] == "Yes"])
    mismatch_percentage = (mismatches / total_files * 100) if total_files > 0 else 0

    stats_summary[cat] = {
        "Total": total_files,
        "Mismatches": mismatches,
        "Mismatch %": mismatch_percentage
    }

stats_df = pd.DataFrame(stats_summary).T

print("="*60)
print("FILE MISMATCH REPORT")
print("="*60)
print(stats_df.round(2))
print()

for cat in file_categories:
    vals = stats_summary[cat]
    print(f"• {cat:<12}: {vals['Mismatches']} mismatches / {vals['Total']} files ({vals['Mismatch %']:.1f}%)")

fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# 1. Bar chart of mismatches
mismatch_counts = [stats_summary[cat]["Mismatches"] for cat in file_categories]
bars = axes[0, 0].bar(file_categories, mismatch_counts, color=['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4'])
axes[0, 0].set_title("Mismatch Counts by File Type", fontweight="bold", fontsize=14)
axes[0, 0].set_ylabel("Count")
axes[0, 0].grid(axis="y", alpha=0.3)
for bar, val in zip(bars, mismatch_counts):
    axes[0, 0].text(bar.get_x() + bar.get_width()/2, val + 0.5, str(val), ha="center", fontweight="bold")

# 2. Mismatch percentages
mismatch_percents = [stats_summary[cat]["Mismatch %"] for cat in file_categories]
bars = axes[0, 1].bar(file_categories, mismatch_percents, color=['#ff8a80', '#80cbc4', '#81c784', '#ffb74d'])
axes[0, 1].set_title("Mismatch Rates (%)", fontweight="bold", fontsize=14)
axes[0, 1].set_ylabel("Percentage")
axes[0, 1].grid(axis="y", alpha=0.3)
for bar, val in zip(bars, mismatch_percents):
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, val + 0.1, f"{val:.1f}%", ha="center", fontweight="bold")

# 3. File type distribution
# Values for pie chart
total_files = [stats_summary[cat]["Total"] for cat in file_categories]
colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']

# Explode small slice(s) to highlight them (e.g., LICENSE)
explode = [0, 0, 0, 0.2]  # Source, Test, README, LICENSE

# Draw pie chart
wedges, texts, autotexts = axes[1, 0].pie(
    total_files,
    labels=file_categories,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    explode=explode,
    wedgeprops={'edgecolor': 'white'},
    pctdistance=0.75,    # percentage distance from center
    labeldistance=1.05   # label distance from center
)

# Add legend outside pie to avoid overlapping
axes[1, 0].legend(wedges, file_categories, title="File Types", loc="center left", bbox_to_anchor=(1, 0.5))

# Title
axes[1, 0].set_title("File Type Distribution", fontweight="bold", fontsize=14)

# Make percentages readable
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')



# 4. Matches vs Mismatches
indices = np.arange(len(file_categories))
matches = [stats_summary[cat]["Total"] - stats_summary[cat]["Mismatches"] for cat in file_categories]
mismatches = [stats_summary[cat]["Mismatches"] for cat in file_categories]
axes[1, 1].bar(indices - 0.2, matches, 0.4, label="Matches", color="lightgreen")
axes[1, 1].bar(indices + 0.2, mismatches, 0.4, label="Mismatches", color="lightcoral")
axes[1, 1].set_xticks(indices)
axes[1, 1].set_xticklabels(file_categories, rotation=30, ha="right")
axes[1, 1].set_ylabel("Number of Files")
axes[1, 1].set_title("Matches vs Mismatches", fontweight="bold", fontsize=14)
axes[1, 1].legend()
axes[1, 1].grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

# --- Overall summary ---
total_files_analyzed = sum(stats_summary[cat]["Total"] for cat in file_categories)
total_mismatches_found = sum(stats_summary[cat]["Mismatches"] for cat in file_categories)
overall_rate = (total_mismatches_found / total_files_analyzed * 100) if total_files_analyzed > 0 else 0

print("\n" + "="*60)
print("FINAL SUMMARY")
print("="*60)
print(f"Total Files Processed : {total_files_analyzed}")
print(f"Total Mismatches      : {total_mismatches_found}")
print(f"Overall Mismatch Rate : {overall_rate:.2f}%\n")

for cat in file_categories:
    vals = stats_summary[cat]
    print(f"{cat:<12}: {vals['Mismatches']:>4} / {vals['Total']:>5} ({vals['Mismatch %']:.1f}%)")
