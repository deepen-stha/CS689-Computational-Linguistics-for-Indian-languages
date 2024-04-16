def get_transliteration_model(source_script, target_script,indic_to_hindi_xlite_engine, hindi_to_indic_xlite_engine):
    if str.lower(target_script) == "english":
        if str.lower(source_script) == "hindi":
            return hindi_to_indic_xlite_engine, "hi", False
        elif str.lower(source_script) == "nepali":
            return hindi_to_indic_xlite_engine, "ne", False
        elif str.lower(source_script) == "malyalam":
            return hindi_to_indic_xlite_engine, "ml", False
        else:
            #  if target_script isn't english and source_script isn't english then
            print("other language not supported yet")
            exit(-1)
    else:
        if str.lower(target_script) == "hindi":
            return indic_to_hindi_xlite_engine, "hi", True
        elif str.lower(target_script) == "nepali":
            return indic_to_hindi_xlite_engine, "ne", True
        elif str.lower(target_script) == "malyalam":
            return indic_to_hindi_xlite_engine, "ml", True
        else:
            print("other language not supported yet")
            exit(-1)

def predict_transliteration(word, model, language, prediction_count,is_roman):
    if is_roman:
        prediction = model.translit_word(word, topk=prediction_count)
        return prediction[language]
    else:
        return model.translit_word(word, lang_code=language, topk=prediction_count)
