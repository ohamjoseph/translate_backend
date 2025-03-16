from transformers import pipeline
import pickle

model_id = "aikunu/fintune-moore2fr-nllb-200-distilled-600M"
trans_pipe = pipeline("translation", model=model_id, src_lang="mos_Latn", tgt_lang="fra_Latn")

model_name = "/home/hamed/PycharmProjects/translate_backend/models/cid.plk"

with open(model_name, 'rb') as f:
    model = pickle.load(f)