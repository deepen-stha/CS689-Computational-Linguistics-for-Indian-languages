from constants.constants import *
def common_error_response(error_code,error_message):
    return {
        "error": {
            "message": error_message,
            "code": error_code
        }
    }

def validate_transliteration_body(word,prediction_count,source_script,target_script):
    if word == "":
        return "word is required in the request body."
    
    if prediction_count == 0:
        return "prediction count is required in the request body."
    
    if source_script == "" or target_script == "":
        return "both source and target scripts are required in the request body."
    
    if str.lower(source_script) != English and str.lower(target_script) != English:
        return "indic to indic transliteration isnot supported yet."
    
    return ""
