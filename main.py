import json
from flask import Flask, request

from initialization import *
from flask_cors import CORS
import sys
from utils.similar_word import *
from utils.transliterate import *
from utils.common import common_error_response,validate_transliteration_body

app = Flask(__name__)
CORS(app)

# loading the ai4bharat-transliteration model
indic_to_hindi_xlite_engine, hindi_to_indic_xlite_engine = intializeXlitEngine()

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