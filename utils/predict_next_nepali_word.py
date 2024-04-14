import random

def best_candidate(nepali_model, prev, i, without=[], gen=True):
    """Choose the most likely next token given the previous (n-1) tokens.
    Args:
        prev (tuple of str): the previous n-1 tokens of the sentence (bigram).
        i (int): which candidate to select if not the most probable one.
        without (list of str): tokens to exclude from the candidates list.
        gen (bool): True if function is used for sentence generation, else false
    Returns:
        A tuple with the next most probable token and its corresponding probability.
    """

    blacklist  = ["<UNK>"] + without
    if len(prev)==1: # case when prev consist of single string(starting token <s>)
      candidates = ((ngram[1], prob) for ngram, prob in nepali_model.items() if ngram[0]==prev[0])
    else:
      candidates = ((ngram[-1], prob) for ngram, prob in nepali_model.items() if ngram[:-1]==prev)
      candidates = filter(lambda candidate: candidate[0] not in blacklist, candidates)
    candidates = sorted(candidates, key=lambda candidate: candidate[1], reverse=True)
    
    n_candidates = len(candidates)
    if  n_candidates == 0:
        return ("</s>", 1)
    
    # if the task is not to generate sentence, we will return multiple word suggestions
    if not gen:
        nS = 5 if len(candidates)>4 else len(candidates)
        return random.sample(candidates[::-1],nS)
    
    candidate_index = int((random.randint(0, len(candidates)))//3)
    return candidates[candidate_index if prev != () and prev[-1] != "<s>" else i] 


def nextNepaliWord(request_sentence,nepali_model, prediction_count):
    """
    Generate word suggestions for completing a Nepali sentence using a predictive model.
    
    :param sentence: The input sentence string for which to predict the next words.
    :param nepali_model: The predictive model used for generating word suggestions.
    :param prediction_count: The number of predictions to return.
    :return: A list of suggested words.
    """
    previous_word = tuple(request_sentence.split()[-2:])
    word_suggestions = best_candidate(nepali_model, previous_word, 0, without=[], gen=False)
    if type(word_suggestions) == int:
        return ["No suggestions"]
    final_suggestions = []
    for i in range(len(word_suggestions)):
       final_suggestions.append(f"{word_suggestions[i][0]}")
        
    return final_suggestions