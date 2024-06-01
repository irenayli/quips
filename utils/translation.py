from typing import Any
import logging

import torch
import fasttext
from huggingface_hub import hf_hub_download
from transformers import AutoProcessor, SeamlessM4TForTextToText

log = logging.getLogger(__name__)


DEVICE = 'cuda'
LID_MODEL_ID = 'facebook/fasttext-language-identification'
TRANSLATION_MODEL_ID = 'facebook/hf-seamless-m4t-large'

# load LID model
lid_model_path = hf_hub_download(repo_id=LID_MODEL_ID, filename='model.bin')
lid_model = fasttext.load_model(lid_model_path)
# load translation model & tokenizer
tokenizer = AutoProcessor.from_pretrained(TRANSLATION_MODEL_ID, device_map = DEVICE, use_fast = False)
model = SeamlessM4TForTextToText.from_pretrained(TRANSLATION_MODEL_ID, device_map = DEVICE)


def identify_language(text: str, model: Any = lid_model) -> str:
    # predict, outputs:((prediction, probablity))
    lid_prediction = model.predict(text)

    # extract iso lang code from prediction
    lid = lid_prediction[0][0]
    detected_source_lang = lid[lid.rfind('__')+2:lid.rfind('_')]  

    log.info('Detected language <%s>. Text: %s', detected_source_lang, text)

    return detected_source_lang


def translate(text: str, target_language: str, source_language: str = None) -> str:
    target_language = target_language or identify_language(text)
    input_tokens = tokenizer(text, src_lang=source_language, return_tensors='pt').to(torch.device(DEVICE))
    output_tokens = model.generate(**input_tokens, tgt_lang=target_language)
    translated_text = tokenizer.decode(output_tokens[0].tolist(), skip_special_tokens=True)

    log.info('Translated from <%s> to <%s>.\nOriginal: <%s>\nTranslated: <%s>', source_language, target_language, translated_text, text)

    return translated_text