import pickle
from transformers import pipeline
import fasttext.util

def initialize_model():
    """
    Initialize the nepali_model global variable.
    """
    translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", tokenizer="facebook/nllb-200-distilled-600M")

    with open('model.pkl', 'rb') as file:
        nepali_model = pickle.load(file)
        return nepali_model, translator

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