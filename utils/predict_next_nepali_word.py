import random
# from initialization import nepali_model

# function to find the best next word for nepali language
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
        nS = 7 if len(candidates)>6 else len(candidates)
        return random.sample(candidates[::-1],nS)
    
    candidate_index = int((random.randint(0, len(candidates)))//3)
    return candidates[candidate_index if prev != () and prev[-1] != "<s>" else i] 


def nextNepaliWord(mySent,nepali_model):
    prev = tuple(mySent.split()[-2:])
    suggest = best_candidate(nepali_model, prev, 0, without=[], gen=False)
    if type(suggest) == int:
        return ["No suggestions"]
    suggestions = [f"{mySent} {sugg[0]} : {sugg[1]}" for sugg in suggest]
    return suggestions  # Return a list of strings