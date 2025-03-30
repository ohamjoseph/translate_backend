from transformers import pipeline, AutoModelForCausalLM
import pickle
import os

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import pipeline

from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForSeq2SeqLM

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_id = "aikunu/fintune-moore2fr-nllb-200-distilled-600M"


from transformers import BitsAndBytesConfig

# quant_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type="nf4",   # ou "fp4", selon le modèle
#     bnb_4bit_use_double_quant=True,
#     bnb_4bit_compute_dtype="float16",  # ou bfloat16 si ton GPU le supporte
# )
#
#
# model = AutoModelForCausalLM.from_pretrained(
#     model_id,
#     quantization_config=quant_config,
#     device_map="auto"  # permet de charger sur le bon device (ex : CUDA)
# )

model_onnx = ORTModelForSeq2SeqLM.from_pretrained(os.path.join(BASE_DIR, "onnx_model"), use_cache=False)

tokenizer = AutoTokenizer.from_pretrained(model_id)

# translator = pipeline("translation", model=model, tokenizer=tokenizer)

# Chemin correct du modèle (dans le même dossier que hugging_face.py)
model_name = os.path.join(BASE_DIR, "cid.plk")



#trans_pipe = pipeline("translation", model=model_id, src_lang="mos_Latn", tgt_lang="fra_Latn")

def translation(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model_onnx.generate(**inputs)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


with open(model_name, 'rb') as f:
    model = pickle.load(f)