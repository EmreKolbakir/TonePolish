# tone_rewriter.py

import os
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from dotenv import load_dotenv
import torch

load_dotenv()

class ToneRewriter:
    def __init__(self):
        model_name = "NousResearch/Nous-Hermes-2-Mistral-7B-DPO"
        hf_token = os.getenv("HF_TOKEN")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype=torch.float16,
            token=hf_token
        )

        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )

    def rewrite(self, text, tone="friendly"):
        tone_guides = {
            "friendly": "Make it warm, polite, and natural. Slightly casual but still professional.",
            "confident": "Make it self-assured, clear, and direct, without sounding arrogant.",
            "humble": "Make it modest, thankful, and respectful, while staying to the point.",
            "formal": "Make it fully formal and grammatically correct. Avoid contractions and casual phrases."
        }

        prompt = f"""Rewrite the following sentence in a {tone} tone for professional communication. {tone_guides[tone]}

Input: {text}
Rewritten:"""

        try:
            output = self.pipe(
                prompt,
                max_new_tokens=100,
                temperature=0.7,
                top_p=0.95,
                do_sample=True
            )[0]["generated_text"]
            rewritten = output.split("Rewritten:")[-1].strip()
            return {"rewritten": rewritten}
        except Exception as e:
            return {"error": str(e)}
