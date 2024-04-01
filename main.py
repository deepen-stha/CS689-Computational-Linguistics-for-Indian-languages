# Importing all the required packages
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("ai4bharat/IndicBART", do_lower_case=False, use_fast=False, keep_accents=True)
model = AutoModelForSeq2SeqLM.from_pretrained("ai4bharat/IndicBART")

# adding route for predicting next word
@app.route('/predict_next_word', methods=['POST'])
def predict_next_word_api():
    data = request.get_json()
    word = data['word']
    print("requested word ",word)
    next_word = predict_next_word(tokenizer, model, word)
    return jsonify({"predicted_next_word": next_word})

def predict_next_word(tokenizer, model, word):
    # Some initial mapping
    bos_id = tokenizer._convert_token_to_id_with_added_voc("<s>")
    eos_id = tokenizer._convert_token_to_id_with_added_voc("</s>")
    pad_id = tokenizer._convert_token_to_id_with_added_voc("<pad>")
    
    inp = tokenizer(word, add_special_tokens=False, return_tensors="pt", padding=True).input_ids
    
    model_output = model.generate(inp, use_cache=True, num_beams=4, max_length=20, min_length=1, 
                                  early_stopping=True, pad_token_id=pad_id, bos_token_id=bos_id, eos_token_id=eos_id, 
                                  decoder_start_token_id=tokenizer._convert_token_to_id_with_added_voc("<2en>"))
    
    decoded_output = tokenizer.decode(model_output[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return decoded_output
    
if __name__ == "__main__":
    app.run(port=8080)
