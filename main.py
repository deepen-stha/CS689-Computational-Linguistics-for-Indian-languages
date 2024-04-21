import json
from flask import Flask, request
from utils.predict_next_nepali_word import nextNepaliWord
from utils.convert_language import translate_malyalam_to_nepali,translate_nepali_to_malyalam
from initialization import *
from flask_cors import CORS
import sys
from utils.similar_word import *
from utils.transliterate import *
from utils.common import common_error_response,validate_transliteration_body

app = Flask(__name__)
CORS(app)

# Load the model one time only at the beginning of the program
nepali_model, translator = initialize_model()

# load the fasttext model one time only
# hindi_model, malyalam_model,nepali_fasttext_model  = initialize_fasttext_model()

# loading the ai4bharat-transliteration model
indic_to_hindi_xlite_engine, hindi_to_indic_xlite_engine = intializeXlitEngine()

# adding route for predicting next word
@app.route('/predict_next_word', methods=['POST'])
def predict_next_word_api():
    data = request.get_json()
    context = data['context']
    prediction_count = data['prediction-count']
    nepali_word = translate_malyalam_to_nepali(context, translator)
    prediction = nextNepaliWord(nepali_word, nepali_model, prediction_count)
    malyalam_predicted_word = []
    for pred in prediction:
        malyalam_predicted_word.append(translate_nepali_to_malyalam(pred, translator))

    json_response = json.dumps({"predictions": malyalam_predicted_word}, ensure_ascii=False)
    return json_response

# adding route for predicting next word for nepali language
@app.route('/predict_next_nepali_word', methods=['POST'])
def predict_next_nepali_word_api():
    data = request.get_json()
    context = data['context']
    prediction_count = data['prediction-count']

    prediction = nextNepaliWord(context, nepali_model, prediction_count)
    json_response = json.dumps({"predictions": prediction}, ensure_ascii=False)
    return json_response

# # adding route for similar word
# @app.route('/similar-word', methods=['POST'])
# def perform_transliteration():
#     data = request.get_json()
#     context = data['context']
#     prediction_count = data['prediction-count']
#     source_script = data['source-script']
#     source_sanscript = get_sanscript(source_script)

#     fasttext_model = get_fasttext_model(source_sanscript,hindi_model,malyalam_model,nepali_fasttext_model)
#     similar_words = get_similar_words(context, fasttext_model, prediction_count)
#     predictions = []
#     for score, word in similar_words:
#         predictions.append(word)
#     json_response = json.dumps({"predictions": predictions}, ensure_ascii=False)
#     return json_response

# adding route for transliterate
@app.route('/transliterate', methods=['POST'])
def perform_transliteration():
    data = request.get_json()
    word = data['word']
    prediction_count = data['prediction-count']
    source_script = data['source-script']
    target_script = data['target-script']

    # validating the request body for transliteration
    message = validate_transliteration_body(word, prediction_count, source_script, target_script)
    if message != "":
        return common_error_response(400, message)
    
    # getting the model to use and then perform prediction using it
    xlite_engine, lang_code, is_roman = get_transliteration_model(source_script,target_script, indic_to_hindi_xlite_engine, hindi_to_indic_xlite_engine)
    prediction = predict_transliteration(word, xlite_engine, lang_code, prediction_count,is_roman)
    json_response = json.dumps({"predictions": prediction}, ensure_ascii=False)
    return json_response
    

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        app.run(port=8080)

    # elif len(sys.argv) > 1 and sys.argv[1] == "similar-word":
    #     word = input("Enter a word which you want to transliterate: ")
    #     prediction_count = int(input("Enter the number of predictions to generate: "))
    #     source_script = input("Enter the source script:  ")
    #     # target_script = input("Enter the target script")
    #     source_sanscript = get_sanscript(source_script)
    #     fasttext_model = get_fasttext_model(source_sanscript,hindi_model,malyalam_model,nepali_fasttext_model)
    #     # transliterated_word = transliterate_word(word, source_script, target_script)
    #     similar_words = get_similar_words(word, fasttext_model, 5)
    #     predictions = []
    #     for score, word in similar_words:
    #         predictions.append(word)
    #     print(predictions)

    elif len(sys.argv) > 1 and sys.argv[1] == "transliteration":
        word = input("Enter a word which you want to transliterate: ")
        prediction_count = int(input("Enter the number of predictions to generate: "))
        source_script = input("Enter the source script:  ")
        target_script = input("Enter the target script: ")
        # validating the input for transliteration
        message = validate_transliteration_body(word, prediction_count, source_script, target_script)
        if message != "":
            print("error: "+message)
            exit(-1)
        
        # getting the model to use and then perform prediction using it
        xlite_engine, lang_code, is_roman = get_transliteration_model(source_script,target_script, indic_to_hindi_xlite_engine, hindi_to_indic_xlite_engine)
        prediction = predict_transliteration(word, xlite_engine, lang_code, prediction_count,is_roman)
        print(prediction)

    else:
        # Interactively get input from the terminal
        word = input("Enter a word to predict next words for: ")
        prediction_count = int(input("Enter the number of predictions to generate: "))
        language = input("Enter the language:  ")
        if language == "nepali":
            prediction = nextNepaliWord(word, nepali_model, prediction_count)
        else:
            nepali_word = translate_malyalam_to_nepali(word, translator)
            nepali_predictions = nextNepaliWord(nepali_word, nepali_model, prediction_count)
            predictions = []
            for pred in nepali_predictions:
                predictions.append(translate_nepali_to_malyalam(pred, translator))

        print("Predictions:", predictions)