from transformers import AutoModel, AutoTokenizer
import torch

device = torch.device("mps" if torch.has_mps else "cuda" if torch.cuda.is_available() else "cpu")
    
if device.type == "cuda":
    model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, torch_dtype=torch.float16)
else:
    model = AutoModel.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True, low_cpu_mem_usage=True)
        
model.to(device)
tokenizer = AutoTokenizer.from_pretrained('openbmb/MiniCPM-Llama3-V-2_5', trust_remote_code=True)
model.eval()