from transformers import RobertaTokenizer, RobertaModel
import torch
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[INFO] Using device: {device}")

tokenizer = RobertaTokenizer.from_pretrained("microsoft/graphcodebert-base")
model = RobertaModel.from_pretrained("microsoft/graphcodebert-base").to(device)
model.eval()

def get_embedding(text: str):
    logger.info(f"Generating embedding for text: {text[:100]}...")
    
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=512
    )
    inputs = {k: v.to(device) for k, v in inputs.items()}
    
    logger.info(f"Tokenized input shape: {inputs['input_ids'].shape}")

    with torch.no_grad():
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :]  # [CLS]
        logger.info(f"Raw CLS embedding shape: {cls_embedding.shape}")
        
        norm_embedding = cls_embedding.squeeze().cpu().numpy()
        logger.info(f"CPU embedding shape: {norm_embedding.shape}")
        
        norm_embedding = norm_embedding / np.linalg.norm(norm_embedding)
        logger.info(f"Normalized embedding norm: {np.linalg.norm(norm_embedding)}")
        
        return norm_embedding
