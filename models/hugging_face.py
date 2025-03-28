from transformers import pipeline
import pickle
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Chemin correct du modèle (dans le même dossier que hugging_face.py)
model_name = os.path.join(BASE_DIR, "cid.plk")

model_id = "aikunu/fintune-moore2fr-nllb-200-distilled-600M"
trans_pipe = pipeline("translation", model=model_id, src_lang="mos_Latn", tgt_lang="fra_Latn")


with open(model_name, 'rb') as f:
    model = pickle.load(f)