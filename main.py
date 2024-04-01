import json
from flask import Flask, request, jsonify
from utils.predict_next_nepali_word import nextNepaliWord
from initialization import initialize_model

app = Flask(__name__)

# Load the model one time only at the beginning of the program
tokenizer, indicBARTModel, nepali_model = initialize_model()

# adding route for predicting next word
@app.route('/predict_next_word', methods=['POST'])
def predict_next_word_api():
    data = request.get_json()
    word = data['word']
    print("requested word ",word)
    next_word = predict_next_word(tokenizer, indicBARTModel, word)
    return jsonify({"predicted_next_word": next_word})

# adding route for predicting next word for nepali language
@app.route('/predict_next_nepali_word', methods=['POST'])
def predict_next_nepali_word_api():
    data = request.get_json()
    word = data['word']
    print("requested word ",word)
    prediction = nextNepaliWord(word, nepali_model)
    # Convert list of strings to JSON format
    json_response = json.dumps({"predictions": prediction}, ensure_ascii=False)
    return json_response

# function to predict next word for 11 indian languages except Nepali
def predict_next_word(tokenizer, indicBARTModel, word):
    # Some initial mapping
    bos_id = tokenizer._convert_token_to_id_with_added_voc("<s>")
    eos_id = tokenizer._convert_token_to_id_with_added_voc("</s>")
    pad_id = tokenizer._convert_token_to_id_with_added_voc("<pad>")
    
    inp = tokenizer(word, add_special_tokens=False, return_tensors="pt", padding=True).input_ids
    
    model_output = indicBARTModel.generate(inp, use_cache=True, num_beams=4, max_length=20, min_length=1, 
                                  early_stopping=True, pad_token_id=pad_id, bos_token_id=bos_id, eos_token_id=eos_id, 
                                  decoder_start_token_id=tokenizer._convert_token_to_id_with_added_voc("<2en>"))
    
    decoded_output = tokenizer.decode(model_output[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return decoded_output

if __name__ == "__main__":
    app.run(port=8080)
