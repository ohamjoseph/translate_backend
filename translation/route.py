from typing import Optional


from fastapi import APIRouter

from pydantic import BaseModel

from models.hugging_face import trans_pipe, model

router = APIRouter()


class TranslateText(BaseModel):
    text: str
    src_lang: Optional[str] = "mos_Latn"
    tgt_lang: Optional[str] = "fra_Latn"

@router.post("/translation")
def translate(translate_text: TranslateText):
    return trans_pipe(translate_text.text)

@router.get("/detection_langue")
def detection_langue(text: str):
    predict = model.predict([text])
    lang = predict[0]
    return lang