import os

# Caminho da pasta com as imagens
caminho_pasta = 'D://pai//imagens'

# Lista apenas arquivos com extensão de imagem
extensoes_validas = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp')
arquivos = [f for f in os.listdir(caminho_pasta) if f.lower().endswith(extensoes_validas)]

# Ordena os arquivos para manter uma sequência consistente
arquivos.sort()

# Renomeia os arquivos
for i, nome_antigo in enumerate(arquivos, start=1):

    extensao = os.path.splitext(nome_antigo)[1].upper()  # mantém a extensão original
    novo_nome = f"foto {i}.JPG"  # pode mudar a extensão se quiser forçar .JPG
    caminho_antigo = os.path.join(caminho_pasta, nome_antigo)
    caminho_novo = os.path.join(caminho_pasta, novo_nome)
    os.rename(caminho_antigo, caminho_novo)

print("Renomeação concluída!")
