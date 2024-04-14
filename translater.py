from googletrans import Translator


def translate_text(text):
    translator = Translator()
    result = translator.translate(text, src='en', dest='ru')
    return result.text
