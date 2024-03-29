import requests
from bs4 import BeautifulSoup
import random

def extrair_dados(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        imgs_produtos = soup.find_all('img', class_='u-block x-product-list__image')
        
        dados = []
        for img_produto in imgs_produtos:
            imagem_url = img_produto['src']
            titulo = img_produto.get('alt') or imagem_url.split('/')[-1].split('.')[0].replace('-', ' ').title()
            preco = round(random.uniform(20, 80), 2)
            
            dados.append({
                'nome': titulo,
                'descricao': titulo,  # Utilizando o título como descrição por enquanto
                'imagem': "https://socalskateshop.com/mm5/"+imagem_url,
                'valor': preco,
                'tamanho': 'P M G'
            })
        
        return dados
    else:
        print("Erro ao acessar a página:", response.status_code)
        return None

# URL do site que você quer extrair os dados
url = 'https://socalskateshop.com/featured-products.html?CatListingOffset=48&Offset=48&Per_Page=48&Sort_By=newest'

# Chama a função para extrair os dados da URL
dados_extraidos = extrair_dados(url)

# Exibe os dados extraídos
if dados_extraidos:
    for produto in dados_extraidos:
        # Fazendo uma solicitação POST para a API
        try:
            resposta = requests.post('https://e-commerce-prod.onrender.com/api/produtos', json=produto)
            if resposta.status_code == 200:
                print(f"Dados do produto '{produto['nome']}' enviados com sucesso!")
            else:
                print(f"Falha ao enviar dados do produto '{produto['nome']}' - Código de status {resposta.status_code}")
        except Exception as e:
            print(f"Erro ao enviar dados do produto '{produto['nome']}': {e}")
else:
    print("Não foi possível extrair os dados.")