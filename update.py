import os
import requests

def update():
    try:
        # URL do arquivo no GitHub que contém a versão mais recente do CLI
        version_url = "https://raw.githubusercontent.com/zVitorSantos/Precificador/main/version.txt"

        # Faz uma solicitação GET para obter a versão mais recente
        response = requests.get(version_url)
        latest_version = response.text.strip()

        # URL do arquivo .exe no GitHub que você deseja baixar
        file_url = f"https://github.com/zVitorSantos/Precificador/releases/download/v{latest_version}/main.exe"

        print("Baixando a nova versão...")

        # Faz uma solicitação GET para baixar o novo arquivo .exe
        response = requests.get(file_url)

        # Substitui o antigo arquivo .exe pelo novo
        with open("main_new.exe", "wb") as file:
            file.write(response.content)

        # Substitui o antigo arquivo .exe pelo novo
        os.rename("main_new.exe", "main.exe")

        # Atualiza a current_version no arquivo version.txt
        with open("version.txt", "w") as file:
            file.write(latest_version)

        print("Atualização concluída.")
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a nova versão: {e}")

update()