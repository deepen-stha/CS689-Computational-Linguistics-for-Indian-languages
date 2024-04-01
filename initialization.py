import pickle
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def initialize_model():
    """
    Initialize the nepali_model global variable.
    """
    # Load the tokenizer and model (this currently support 11 Indian languages but not Nepali)
    tokenizer = AutoTokenizer.from_pretrained("ai4bharat/IndicBART", do_lower_case=False, use_fast=False, keep_accents=True)
    indicBARTModel = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/IndicBART")
    print("tokenizer and IndicBART model loaded")

    with open('model.pkl', 'rb') as file:
        nepali_model = pickle.load(file)
        print("Nepali Model loaded successfully")
        return tokenizer, indicBARTModel, nepali_model
