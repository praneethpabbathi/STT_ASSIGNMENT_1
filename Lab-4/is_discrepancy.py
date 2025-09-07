import pandas as pd

input_csv = "lab4_dataset.csv"
output_csv = "lab4_dataset_with_discrepancy.csv"

df = pd.read_csv(input_csv)

def compare_stripped(row):
    myers = str(row["diff_myers"]).strip().replace("\r\n", "\n").replace("\r", "\n")
    hist  = str(row["diff_hist"]).strip().replace("\r\n", "\n").replace("\r", "\n")
    return "No" if myers == hist else "Yes"

df["Discrepancy"] = df.apply(compare_stripped, axis=1)

df.to_csv(output_csv, index=False)
print(f"Discrepancy column updated → {output_csv}")


