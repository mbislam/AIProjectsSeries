from deep_translator import GoogleTranslator

print("Welcome to Language Translator!")

text = input("Enter text to translate: ")
source = input(
    "Source language code (en, es, fr, ar, bn): "
)
target = input(
    "Target language code (en, es, fr, ar, bn): "
)

try:
    translated = GoogleTranslator(
        source=source,
        target=target
    ).translate(text)

    print("\nTranslated Text:")
    print(translated)

except Exception as e:
    print("Translation failed.")
    print("Error:", e)