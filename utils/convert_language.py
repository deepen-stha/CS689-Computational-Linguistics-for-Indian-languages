from constants.constants import Malyalam_Language,Nepali_Language

def translate_malyalam_to_nepali(text,translator):
    # Translate Malyalam to Nepali
    return translator(text, src_lang=Malyalam_Language, tgt_lang=Nepali_Language)[0]['translation_text']

def translate_nepali_to_malyalam(text,translator):
    # Translate Nepali to Malyalam
    return translator(text, src_lang=Nepali_Language, tgt_lang=Malyalam_Language)[0]['translation_text']