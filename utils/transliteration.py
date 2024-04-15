from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import fasttext.util
from constants.constants import *

def transliterate_word(word, from_script, to_script):
    """ Transliterates a word from the source script to the target script. """
    return transliterate(word, from_script, to_script)

def get_similar_words(word, model, k=5):
    """
    Get k similar words to the given word using the loaded fastText model.
    
    Args:
    word (str): The word for which similar words are to be found.
    model (fasttext.FastText._FastText): The loaded fastText model.
    k (int): The number of similar words to return.

    Returns:
    list: A list of tuples, each containing a similar word and its similarity score.
    """
    similar_words = model.get_nearest_neighbors(word, k)
    return similar_words

def get_sanscript(script):
    if script == Malyalam:
        return sanscript.MALAYALAM
    elif script == Hindi:
        return sanscript.DEVANAGARI
    elif script == English:
        return sanscript.ITRANS
    elif script == Nepali:
        return script # sanscript doesn't have any support for nepali
    else:
        return sanscript.DEVANAGARI
    
def get_model(source_sanscript,hindi_model,malyalam_model,nepali_model):
    """
    function to check and get the requried model for fasttext
    """
    if source_sanscript == sanscript.DEVANAGARI:
        return hindi_model
    elif source_sanscript == Nepali:
        return nepali_model
    else:
        return malyalam_model