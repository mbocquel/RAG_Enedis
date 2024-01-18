import requests

# Fonction pour se connecter et récupérer les cookies de session
def login(username, password):
    url_login = "https://sandiego.eggdonorconnect.com/Account/Login"

    login_data = {
        'ReturnUrl': '/Recipient/DonorDashboardMatching',
        '__RequestVerificationToken': 'dB5WlNVIl6kzuGCytq5AEHqoKCcw1DOfkPUsoFGs8rfeuI7uflTxYSBOSLB-YyoIU_2olR14nf_K5DSJJSFD0wWkjpwh-nFW_vYCGxohXyA1',
        'Email': username,
        'Password': password,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://sandiego.eggdonorconnect.com/Account/Login?ReturnUrl=%2FRecipient%2FDonorDashboardMatching',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'fr',
    }

    cookies = {
        'ARRAffinity': '8d7c727bc6a90d8676d983aa4d7b32e217762d1d50c7efa9da32d1731fc8ec75',
        'ARRAffinitySameSite': '8d7c727bc6a90d8676d983aa4d7b32e217762d1d50c7efa9da32d1731fc8ec75',
        '__RequestVerificationToken': 'Ll_Qkn1ZqKpp_VwwRRCdQDIlqaBs7g-aLgFynA5M3ZlUCBNDXqS7aL7u7PLW76MwCcuuyTyIsjjll6HXLsS2vBQdY3LDLYM9VNIluKqphko1',
        '_gcl_au': '1.1.310311742.1705590155',
        '_ga_P7R0X0HSX8': 'GS1.1.1705590154.1.0.1705590154.60.0.0',
        '_ga': 'GA1.2.291451522.1705590155',
        '_gid': 'GA1.2.1407580339.1705590155',
        '_gat_gtag_UA_17694912_3': '1',
        '_gat_UA-17694912-3': '1',
        '_fbp': 'fb.1.1705590155750.500187230',
        '_gali': 'btnLogin',
    }

    # Effectuer la requête de connexion
    response = requests.post(url_login, data=login_data, headers=headers, cookies=cookies)

    # Vérifier si la connexion a réussi (en fonction du code de statut HTTP)
    if response.status_code == 200:
        print("Connexion réussie !")
        # print(response.text)
    else:
        print(f"Échec de la connexion. Code de statut HTTP : {response.status_code}")
        return None


# Fonction pour accéder à une autre page en utilisant les cookies de session
def access_dashboard():

    url = "https://sandiego.eggdonorconnect.com/Recipient/_DonorDashboardMatching"

    # Données du formulaire (assurez-vous d'ajuster cela en fonction de ce que le serveur attend)
    form_data = {
        "CustomFilters": [],
        "SortBy": "Newest First",
        "Heritages": [],
        "OnlyShowRecipientFrozen": False,
        "OnlyShowRecipientFresh": False,
        "TertiaryStatuses": [],
        "IPPhotoIdForFacialMatching": None,
        "AffiliateClinicIdOverride": None,
        "ScriptsOnly": False,
        "tabNumber": "0",
        "ShowLiveBirthGuarantee": False,
        "EducationLevels": ["High School", "Some College", "Currently Enrolled in College", "Trade School", "2-Year Degree", "4-Year Degree", "Graduate Degree"],
        "AllEducationLevels": True,
        "ClinicField1": None,
        "BloodTypes": [],
        "AllBloodTypes": True,
        "DonorCodeSearch": None,
        "ClinicId": "9",
        "FreshOrFrozen": None,
        "AllEthnicities": True,
        "Ethnicities": [],
        "AdditionalClinicId": None,
        "useMetricSystem": False,
        "ContactOptions": [],
        "AllContactOptions": False,
        "PreviewAccessOnly": False,
        "KnownOnly": False,
        "RecipientId": "141318",
        "SplitOnly": None,
        "AllHeights": True,
        "minHeight": 59,
        "maxHeight": 74,
        "HairColors": [],
        "AllHair": False,
        "EyeColors": [],
        "AllEyes": False,
        "AllRaces": False,
        "Races": ["Jewish", "Middle Eastern", "Native American", "White / Caucasian"],
        "ProvenDonor": None
    } 

    # En-têtes de la requête
    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'fr',
        'Content-Type': 'application/json',
        'Referer': 'https://sandiego.eggdonorconnect.com/Recipient/DonorDashboardMatching',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        # Ajoutez d'autres en-têtes si nécessaire
    }

    # Cookies de la session (ajoutez tous les cookies nécessaires)
    cookies = {
        'ARRAffinity': '8d7c727bc6a90d8676d983aa4d7b32e217762d1d50c7efa9da32d1731fc8ec75',
        'ARRAffinitySameSite': '8d7c727bc6a90d8676d983aa4d7b32e217762d1d50c7efa9da32d1731fc8ec75',
        '__RequestVerificationToken': 'Ll_Qkn1ZqKpp_VwwRRCdQDIlqaBs7g-aLgFynA5M3ZlUCBNDXqS7aL7u7PLW76MwCcuuyTyIsjjll6HXLsS2vBQdY3LDLYM9VNIluKqphko1',
        '_gcl_au': '1.1.310311742.1705590155',
        '_ga_P7R0X0HSX8': 'GS1.1.1705590154.1.0.1705590154.60.0.0',
        '_ga': 'GA1.2.291451522.1705590155',
        '_gid': 'GA1.2.1407580339.1705590155',
        '_gat_gtag_UA_17694912_3': '1',
        '_gat_UA-17694912-3': '1',
        '_fbp': 'fb.1.1705590155750.500187230',
        '_gali': 'btnLogin',
        'SortBy3':'Newest First',
        'last_tab_number':'0',
        'HairColor':'',
        'TertiaryStatuses':'', 
        'EyeColor':'',
        'SplitOnly':'null', 
        'ClinicField1':'null', 
        'KnownOnly':'false',
        'minHeight':'59',
        'maxHeight':'74',
        'FreshFrozen':'null',
        'Ethnicities':'',
        'ProvenDonor':'null',
        'Contact':'',
        'Heritages':'',
        'BloodTypes':'', 
        'IPPhotoIdForFacialMatching':'null',
        'Races':'Jewish,Middle Eastern,Native American,White / Caucasian',
        'Education':'High School,Some College,Currently Enrolled in College,Trade School,2-Year Degree,4-Year Degree,Graduate Degree',
        'last_donor_clicked':'null',
        'CustomFilter_radioWillingtoDonateSameSex':'null',
        '.AspNet.ApplicationCookie':'Lh1Lw10Ype1nJoV92Yn6UHXjQpQs1t7LRZzTFldlFME6NyMLlEhxm1yGjk7AuwGz55qnMt-lfRxoi_XUQukL3vhyv3_25-bGIPqSUCRuBGDBEqxMAycJBUk53-xgUUT3R91X9fWOo2rghPc85d7UccXiJV_K9Pr4kX9MJLDDVZG57tjafsPqkC1HXlFI2G1-yV3wcVprsbAtxkw1sAIIX5ARGjTTczpddj5QP-c1GaXppT-RrRzWTUKoqInh4_S5CEzyjYnKt59r5hs3p2O36qy35-5OEekZkKVEWSwvCpo5g-NHANoF8-jx6P4MQB1AaEmHZIhdPrf1scuhNibul9FwcfN9ocY9WPIAO2RH828KmZRJkw2fExNXNWXkq8KBuj_Si4FYOXHZSwZXF01No4cFAWfGijyL86yNMGWovRHP28QtttSv2b9aMbvJ2P1z_IgwNWW8U4SVEUNI6ibYgD-x26z2WDekTzRkZy1HcqFO-3-pcxlu6Bxlt3x8C1ujdht9hrzif-__El-Ma-h2OA'
    }

    # Effectuer la requête POST
    response = requests.post(url, headers=headers, cookies=cookies, json=form_data)


    # Vérifier si l'accès à la page a réussi (en fonction du code de statut HTTP)
    if response.status_code == 200:
        # print("Accès à la page réussi 2!")
        print(response.text)  # Afficher le contenu de la page (à des fins de démonstration)
    else:
        print(f"Échec de l'accès à la page. Code de statut HTTP : {response.status_code}")

# Exemple d'utilisation
cookies_session = login('email', 'password')
access_dashboard()
