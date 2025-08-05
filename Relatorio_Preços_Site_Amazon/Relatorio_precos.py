from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import time

# Configuração do navegador headless
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920,1080")

# Iniciar driver
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

# Termo de busca
produto = "notebook"

# Acessar Amazon
driver.get("https://www.amazon.com.br")
time.sleep(2)

# Buscar o produto
barra_busca = driver.find_element(By.ID, "twotabsearchtextbox")
barra_busca.send_keys(produto)
barra_busca.send_keys(Keys.ENTER)
time.sleep(3)

# Captura os dados
titulos = driver.find_elements(By.CSS_SELECTOR, "h2 span")
precos = driver.find_elements(By.CSS_SELECTOR, ".a-price-whole")

# Extrair textos e preços ANTES de fechar o navegador
resultados = []
for titulo, preco in zip(titulos, precos):
    try:
        nome = titulo.text.strip()
        valor = preco.text.strip().replace('.', '')  # Remove ponto de milhar
        preco_num = int(valor)  # Converte para número
        resultados.append((nome, preco_num))
    except Exception as e:
        print("Erro ao capturar produto:", e)

# Fecha o navegador
driver.quit()

# Ordena os resultados por preço (menor para maior)
resultados_ordenados = sorted(resultados, key=lambda x: x[1])

# Criar o PDF
nome_pdf = f"cotacao_amazon_{produto.replace(" ", "_")}.pdf"
pdf = canvas.Canvas(nome_pdf, pagesize=A4)
largura, altura = A4
y = altura - 50

pdf.setFont("Helvetica-Bold", 14)
pdf.drawString(50, y, f"Cotação Amazon - {produto} (Menor preço primeiro)")
y -= 30
pdf.setFont("Helvetica", 10)

for nome, preco in resultados_ordenados:
    # Formatação com ponto
    linha_completa = f"{nome} - R$ {preco:,}".replace(",", ".")
    linhas = simpleSplit(linha_completa, "Helvetica", 10, largura - 100)
    for linha in linhas:
        pdf.drawString(50, y, linha)
        y -= 15
        if y < 50:
            pdf.showPage()
            pdf.setFont("Helvetica", 10)
            y = altura - 50

pdf.save()

print(f"\n✅ PDF gerado com sucesso (ordenado por preço): {nome_pdf}")
