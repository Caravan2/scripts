def CheckPhone(prefix):
    Silknet = ["514", "555", "557", "558", "577", "593", "570", "578", "791"]
    Magticom = ["551", "591", "595", "596", "598", "599", "790"]
    Beeline = ["568", "571", "574", "592", "597", "579"]
    Globalcell = ["559"]

    if prefix in Silknet:
        provider = "Silknet"
    elif prefix in Magticom:
        provider = "Magticom"
    elif prefix in Beeline:
        provider = "Beeline"
    elif prefix in Globalcell:
        provider = "Globalcell"
    elif "32" in prefix:
        provider = "Government (Tbilisi)"
    elif "422" in prefix:
        provider = "Government (Batumi)"
    elif "431" in prefix:
        provider = "Government (Kutaisi)"
    elif "341" in prefix:
        provider = "Government (Rustavi)"
    elif "358" in prefix:
        provider = "Government (Bolnisi)"
    elif "372" in prefix:
        provider = "Government (Gardabani)"
    elif "413" in prefix:
        provider = "Government (Senaki)"
    elif "411" in prefix:
        provider = "Government (Samtredia)"
    elif "419" in prefix:
        provider = "Government (Chokhatauri)"
    elif "426" in prefix:
        provider = "Government (Kobuleti)"
    elif "436" in prefix:
        provider = "Government (Tskaltubo)"
    elif "479" in prefix:
        provider = "Government (Chiatura)"
    elif "492" in prefix:
        provider = "Government (Zestafoni)"
    elif "493" in prefix:
        provider = "Government (Poti)"
    elif "496" in prefix:
        provider = "Government (Ozurgeti)"
    elif "497" in prefix:
        provider = "Government (Tkibuli)"
    elif "353" in prefix:
        provider = "Government (Gurjaani)"
    elif "370" in prefix:
        provider = "Government (Gori)"
    elif "357" in prefix:
        provider = "Government (Marneuli)"
    elif "415" in prefix:
        provider = "Government (Zugdidi)"
    elif "367" in prefix:
        provider = "Government (Borjomi)"
    elif "365" in prefix:
        provider = "Government (Akhaltsikhe)" 
    elif "350" in prefix:
        provider = "Government (Telavi)"
    elif "351" in prefix:
        provider = "Government (Sagarejo)"
    elif "354" in prefix:
        provider = "Government (Lagodekhi)"
    elif "355" in prefix:
        provider = "Government (Sighnaghi)"
    else:
        provider = None
    
    
    return provider