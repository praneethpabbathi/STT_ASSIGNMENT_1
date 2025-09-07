import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModel
from sacrebleu import sentence_bleu
import numpy as np

df = pd.read_csv("bug_fix_commits_with_metrics.csv")

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")
model.eval()

# ---- Function to get embeddings for a code string ----
def get_code_embedding(code_str):
    if pd.isna(code_str) or code_str.strip() == "":
        return None
    inputs = tokenizer(code_str, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        # Take the [CLS] token embedding as representation
        cls_embedding = outputs.last_hidden_state[:,0,:].squeeze()
    return cls_embedding

# ---- Compute semantic similarity between before/after ----
def semantic_similarity(before, after):
    emb1 = get_code_embedding(before)
    emb2 = get_code_embedding(after)
    if emb1 is None or emb2 is None:
        return np.nan
    # Cosine similarity
    cos_sim = torch.nn.functional.cosine_similarity(emb1, emb2, dim=0)
    return cos_sim.item()

# ---- Compute token similarity using BLEU ----
def token_similarity(before, after):
    if pd.isna(before) or pd.isna(after):
        return np.nan
    # SacreBLEU expects references as list of lists
    bleu_score = sentence_bleu(after, [before])
    return bleu_score.score / 100.0  # scale 0-1

df["Semantic_Similarity"] = df.apply(lambda row: semantic_similarity(row["Source Before"],
                                                                    row["Source After"]), axis=1)
df["Token_Similarity"] = df.apply(lambda row: token_similarity(row["Source Before"],
                                                               row["Source After"]), axis=1)

df.to_csv("bug_fix_commits_with_all_metrics.csv", index=False)
print("Semantic similarity, token similarity, and classifications computed and saved.")
