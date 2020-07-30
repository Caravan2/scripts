import subprocess

split1 = ["mail.", "mx.", "mx1.", "mx2.", "mx3.", "mx4.", "smtp.", "relay.", "relay1.", "relay2."]

split2 = ["ge", "com", "net", "ru", "org", "io"]

def CheckMx(domain):
    try:
        batcmd=f"host -t mx {domain}"
        result = subprocess.check_output(batcmd, shell=True)
        result = result.decode()
        print(result)

        if "google" in result or "GOOGLE" in result:
            provider = "gmail.com"
            print("It uses ", provider)
        elif "zoho" in result:
            provider = "zoho.com"
            print("It uses ", provider)
        elif "wanex" in result:
            provider = "silknet.com"
            print("It uses ", provider)
        elif "outlook" in result:
            provider = "outlook.com"
            print("It uses ", provider)
        elif "yahoodns" in result:
            provider = "yahoo.com"
            print("It uses ", provider)
        elif "yandex" in result:
            provider = "yandex.ru"
            print("It uses ", provider)
        elif "mail.ru" in result:
            provider = "mail.ru"
            print("It uses ", provider)
        else:
            for each in split1:
                if each in result:
                    try:
                        result = result.split(each)[1]
                        for each2 in split2:
                            if each2 in result:
                                try:
                                    provider = result.split(each2)[0] + each2
                                    print("It uses ", provider)
                                    break
                                except:
                                    provider = None
                                    print("Does not have any provider")
                                    break
                            else:
                                provider = None
                                print("trying different extension")
                    except:
                        provider = None
                        print("Does not have any provider")
                        break
                    break
                else:
                    provider = None
                    print("Trying different mx prefix")
    except:
        provider = None
        
    print("PROVIDER IS: ", provider)
    return provider
