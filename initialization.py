import fasttext.util
from ai4bharat.transliteration import XlitEngine

def initialize_fasttext_model():
    """
    function to initialise the fasttext model
    """
    # downloading fasttext model for hindi, malyalam and nepali
    fasttext.util.download_model('hi', if_exists='ignore')
    fasttext.util.download_model('ml', if_exists='ignore')
    fasttext.util.download_model('ne', if_exists='ignore')

    # Load the pre-trained model
    hindi_model = fasttext.load_model('cc.hi.300.bin')
    malyalam_model = fasttext.load_model('cc.ml.300.bin')
    nepali_model = fasttext.load_model('cc.ne.300.bin')
    return hindi_model, malyalam_model,nepali_model

def intializeXlitEngine():
    indic_to_hindi_xlite_engine = XlitEngine(["hi", "ml","ne"], beam_width=6)
    hindi_to_indic_xlite_engine = XlitEngine(src_script_type="indic", beam_width=10, rescore=False) # indic script(eg: namaste)
    return indic_to_hindi_xlite_engine, hindi_to_indic_xlite_engine



