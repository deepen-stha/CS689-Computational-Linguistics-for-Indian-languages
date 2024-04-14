import json
from flask import Flask, request
from utils.predict_next_nepali_word import nextNepaliWord
from utils.convert_language import translate_malyalam_to_nepali,translate_nepali_to_malyalam
from initialization import initialize_model
from flask_cors import CORS
import sys

app = Flask(__name__)
CORS(app)

# Load the model one time only at the beginning of the program
nepali_model, translator = initialize_model()

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

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        app.run(port=8080)
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