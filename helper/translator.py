from deep_translator import GoogleTranslator

def translate(source, target, text):
    return GoogleTranslator(source=source, target=target).translate(text)