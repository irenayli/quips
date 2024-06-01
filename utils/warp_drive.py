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
    source_language: str
) -> str:
    # get relevant rows
    language_data = lang_similarites[lang_similarites['ISO_1'] == source_language]
    # transform to data space
    similarity_target = transform_to_data_space(slider_value, language_data['Similarity'].values)
    # find closest language
    language_data['distance_to_target'] = abs(language_data['Similarity'] - similarity_target)
    target_language = language_data[language_data['distance_to_target'] == min(language_data['distance_to_target'].values)]['ISO_2'].values[0]  # TODO: improve
    
    return target_language