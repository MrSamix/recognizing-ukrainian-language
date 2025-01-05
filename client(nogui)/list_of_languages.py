import json
# from faster_whisper import WhisperModel

def get_native_name(code):
    with open("languages.json", "r", encoding="utf-8") as file:
        languages = json.load(file)
    for lang in languages:
        if lang["code"] == code:
            return lang["native"]
    return code # test -> None


def get_code_by_native_name(name):
    with open("languages.json", "r", encoding="utf-8") as file:
        languages = json.load(file)
    for lang in languages:
        if lang["native"] == name:
            return lang["code"]
    return None # test -> None



list_of_avaibable_languages_codes = ['af', 'am', 'ar', 'as', 'az', 'ba', 'be', 'bg', 'bn', 'bo', 'br', 'bs', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'gl', 'gu', 'ha', 'haw', 'he', 'hi', 'hr', 'ht', 'hu', 'hy', 'id', 'is', 'it', 'ja', 'jw', 'ka', 'kk', 'km', 'kn', 'ko', 'la', 'lb', 'ln', 'lo', 'lt', 'lv', 'mg', 'mi', 'mk', 'ml', 'mn', 'mr', 'ms', 'mt', 'my', 'ne', 'nl', 'nn', 'no', 'oc', 'pa', 'pl', 'ps', 'pt', 'ro', 'ru', 'sa', 'sd', 'si', 'sk', 'sl', 'sn', 'so', 'sq', 'sr', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'tk', 'tl', 'tr', 'tt', 'uk', 'ur', 'uz', 'vi', 'yi', 'yo', 'zh', 'yue']


list_of_avaibable_languages_native = ["Auto"]
for code in list_of_avaibable_languages_codes:
    list_of_avaibable_languages_native.append(get_native_name(code))


def return_list_of_avaibable_languages_native():
    return list_of_avaibable_languages_native