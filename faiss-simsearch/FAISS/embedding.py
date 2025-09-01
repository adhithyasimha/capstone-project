from transformers import RobertaTokenizer, RobertaModel
import torch
import numpy as np

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {device}")

tokenizer = RobertaTokenizer.from_pretrained("microsoft/graphcodebert-base")
model = RobertaModel.from_pretrained("microsoft/graphcodebert-base").to(device)
model.eval()

def get_embedding(text: str):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]  # [CLS]
        norm_embedding = cls_embedding.squeeze().cpu().numpy()
        norm_embedding = norm_embedding / np.linalg.norm(norm_embedding)
        return norm_embedding
