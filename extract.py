from bs4 import BeautifulSoup

# Charger le contenu du fichier HTML
with open('test.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Utiliser BeautifulSoup pour analyser le HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Liste pour stocker les informations des donneurs
donors_info = []

# Parcourir chaque balise de donneur
for donor_div in soup.find_all('div', class_='activeDonor'):
    donor_info = {}

    # Extraire des informations spécifiques de chaque donneur
    donor_info['donor_code'] = donor_div.select_one('.donorCode').text.strip()
    donor_info['age'] = donor_div.select_one('.question:contains("Age")').find_next(class_='answer').text.strip()
    donor_info['repeat_donor'] = donor_div.select_one('.question:contains("Repeat Donor")').find_next(class_='answer').text.strip()
    donor_info['compensation'] = donor_div.select_one('.question:contains("Compensation")').find_next(class_='answer').text.strip()
    donor_info['education'] = donor_div.select_one('.question:contains("Education")').find_next(class_='answer').text.strip()

    donors_info.append(donor_info)

# Afficher les informations des donneurs
for donor in donors_info:
    print(donor)
