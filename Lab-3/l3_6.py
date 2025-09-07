import pandas as pd

# Load your CSV with metrics
df = pd.read_csv("bug_fix_commits_with_all_metrics.csv")

# Cyclomatic Complexity (CC) change
cc_mean = df["CC_Change"].mean()
cc_std = df["CC_Change"].std()
cc_min = df["CC_Change"].min()
cc_max = df["CC_Change"].max()

# Maintainability Index (MI) change
mi_mean = df["MI_Change"].mean()
mi_std = df["MI_Change"].std()
mi_min = df["MI_Change"].min()
mi_max = df["MI_Change"].max()

# Lines of Code (LOC) change
loc_mean = df["LOC_Change"].mean()
loc_std = df["LOC_Change"].std()
loc_min = df["LOC_Change"].min()
loc_max = df["LOC_Change"].max()

# Print summary
print("Cyclomatic Complexity (CC) Change Distribution:")
print(f"Mean: {cc_mean:.4f}, Std: {cc_std:.4f}, Min: {cc_min}, Max: {cc_max}\n")

print("Maintainability Index (MI) Change Distribution:")
print(f"Mean: {mi_mean:.4f}, Std: {mi_std:.4f}, Min: {mi_min}, Max: {mi_max}\n")

print("Lines of Code (LOC) Change Distribution:")
print(f"Mean: {loc_mean:.2f}, Std: {loc_std:.2f}, Min: {loc_min}, Max: {loc_max}")
