from transformers import pipeline
import torch

torch.mps.empty_cache()
# Load a text generation model from Hugging Face (Llama 2 or Mistral)
# generator = pipeline("text-generation", model="meta-llama/Llama-2-7b-chat-hf")
# Set device to CPU instead of MPS (Mac Metal GPU)
device = torch.device("cpu")  # Force CPU usage
# generator = pipeline("text-generation", model="deepseek-ai/deepseek-llm-7b-chat", device=device)
# lighter model
# generator = pipeline("text-generation", model="gpt2", device=device)
generator = pipeline(
    "text-generation",
    model="deepseek-ai/deepseek-llm-7b-chat",
    torch_dtype=torch.float16,
    device=device
)




def optimize_prompt(query):
    """Suggests optimized prompts for better retrieval using a Hugging Face model"""
    prompt = f"Generate optimized variations of the query for better retrieval:\nQuery: {query}\nVariations:"
    response = generator(prompt, max_length=50, num_return_sequences=1)
    return response[0]["generated_text"].strip()
