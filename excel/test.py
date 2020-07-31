import requests

for i in range(100, 1000):
    url = f"https://enreg.reestri.gov.ge/main.php?c=app&m=show_legal_person&legal_code_id=10561011&enteredCaptcha={i}"
    page = requests.get(url)
    print(page.content)