# normalization
import pandas as pd

lang_keys = pd.read_csv('data/valid_languages.csv')
lang_similarites = pd.read_csv('data/language_similarities.csv')


def check_language_valid(lang_code: str) -> bool:
    return lang_code in set(lang_similarites['ISO_1'].values)


def transform_to_data_space(slider_value, data_values, slider_min = 3, slider_max = 80):
    # normalize slider
    normalized_slider_value = (slider_value- slider_min) / (slider_max - slider_min)

    # transform to similarity space
    similarity_min = min(data_values)
    similarity_max = max(data_values)
    similarity_target = similarity_min + normalized_slider_value * (similarity_max - similarity_min)

    return similarity_target


def get_target_language(
    slider_value: float, 
    src_lang: str,
    req_target_lang: str
) -> str:
    # get relevant rows
    
    language_data = lang_similarites[
        ((lang_similarites['ISO_1'] == req_target_lang) | (lang_similarites['ISO_2'] == req_target_lang)) &
        (lang_similarites['ISO_1'] != src_lang) &
        (lang_similarites['ISO_2'] != src_lang)
    ]

    # transform to data space
    similarity_target = transform_to_data_space(slider_value, language_data['Similarity'].values)
    # find closest language
    target_language = lang_similarites.iloc[(lang_similarites['Similarity']-similarity_target).abs().argsort()[0]]['ISO_2']
    
    return target_language
