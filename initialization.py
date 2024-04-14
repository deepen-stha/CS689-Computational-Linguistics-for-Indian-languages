import pickle
from transformers import pipeline

def initialize_model():
    """
    Initialize the nepali_model global variable.
    """
    translator = pipeline("translation", model="facebook/nllb-200-distilled-600M", tokenizer="facebook/nllb-200-distilled-600M")

    with open('model.pkl', 'rb') as file:
        nepali_model = pickle.load(file)
        print("Nepali Model loaded successfully")
        return nepali_model, translator
