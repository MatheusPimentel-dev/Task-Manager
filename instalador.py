import subprocess
import os

arquivo = 'requirements.txt'

# Abrir e ler o arquivo linha por linha
with open(arquivo, 'rb') as file:
    conteudo_binario = file.read()
    conteudo_texto = conteudo_binario.decode('utf-16')
    
    for linha in conteudo_texto.splitlines():
        # Remover espaços em branco no início e no fim da linha
        linha = linha.strip()

        # print(linha)
        quantidade_letras = sum(1 for char in linha if char.isalpha())
        if quantidade_letras == 0 or  linha == 'ÿþ':
            continue
        
        if os.name == 'nt':
            comando = ['py','-m', 'pip', 'install', linha]
        else:
            comando = ['python3','-m', 'pip', 'install', linha]

        # print(comando)
        subprocess.run(comando)