from langdetect import detect, detect_langs

lang = detect_langs("Русскоязычный Mенеджер по Продажам")

print(lang)