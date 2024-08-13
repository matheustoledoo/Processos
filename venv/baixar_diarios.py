from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import time
import os
from PyPDF2 import PdfFileReader

# Caminho para o ChromeDriver
chrome_driver_path = "C:/Program Files/ChromeDev/chrome-win64/chromedriver.exe"


# Configurando o WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL do TJSP
url = "https://dje.tjsp.jus.br/cdje/index.do;jsessionid=904E03097EDCF133765EE6CB860DFD6B.cdje2"

# Diretório para salvar os arquivos PDF
save_dir = "downloads_tjsp"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Palavras-chave para filtrar nos PDFs
palavras_chave = ["assistente técnico", "imóveis", "perícia"]

# Função para baixar PDFs dos cadernos selecionados
def baixar_caderno(caderno_text):
    # Selecionando o caderno
    select_caderno = Select(driver.find_element(By.ID, "caderno"))
    select_caderno.select_by_visible_text(caderno_text)

    # Selecionando a seção "Cível"
    select_secao = Select(driver.find_element(By.ID, "secao"))
    select_secao.select_by_visible_text("Cível")

    # Clicar no botão "Consultar"
    consultar_button = driver.find_element(By.XPATH, "//input[@value='Consultar']")
    consultar_button.click()

    # Esperar o resultado carregar
    time.sleep(5)

    # Procurar pelos links de download dos PDFs e baixá-los
    links_de_download = driver.find_elements(By.PARTIAL_LINK_TEXT, "Download")
    for link in links_de_download:
        pdf_url = link.get_attribute('href')
        baixar_pdf(pdf_url)

    # Navegar de volta à página inicial para selecionar o próximo caderno
    driver.get(url)
    time.sleep(2)

# Função para baixar o PDF
def baixar_pdf(pdf_url):
    response = driver.get(pdf_url)
    pdf_path = os.path.join(save_dir, pdf_url.split('/')[-1])

    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(response.content)
    
    print(f"PDF salvo em: {pdf_path}")
    
    # Filtrar as palavras-chave no PDF baixado
    filtrar_palavras_chave(pdf_path)

# Função para filtrar palavras-chave nos PDFs
def filtrar_palavras_chave(pdf_path):
    reader = PdfFileReader(pdf_path)
    found_keywords = {}

    for page_num in range(reader.getNumPages()):
        page = reader.getPage(page_num)
        text = page.extract_text()
        for palavra in palavras_chave:
            if palavra.lower() in text.lower():
                if palavra not in found_keywords:
                    found_keywords[palavra] = []
                found_keywords[palavra].append(page_num)

    if found_keywords:
        print(f"Palavras-chave encontradas em {pdf_path}: {found_keywords}")
    else:
        print(f"Nenhuma palavra-chave encontrada em {pdf_path}")

# Lista dos cadernos que queremos baixar
cadernos_para_baixar = [
    "caderno 3 - Judicial - 1ª Instância - Capital - Parte I",
    "caderno 3 - Judicial - 1ª Instância - Capital - Parte II",
    "caderno 4 - Judicial - 1ª Instância - Interior - Parte I",
    "caderno 4 - Judicial - 1ª Instância - Interior - Parte II",
    "caderno 4 - Judicial - 1ª Instância - Interior - Parte III"
]

# Iterando sobre cada caderno para baixá-los
for caderno in cadernos_para_baixar:
    baixar_caderno(caderno)

# Fechar o navegador ao final
driver.quit()
 