import requests
import os

os.system("chcp 65001")

def check_for_updates():
    # Lê a versão atual do arquivo version.txt local
    with open("version.txt", "r") as file:
        current_version = file.read().strip()
        
    # URL do arquivo no GitHub que contém a versão mais recente do CLI
    version_url = "https://raw.githubusercontent.com/zVitorSantos/Precificador/main/version.txt"

    # Faz uma solicitação GET para obter a versão mais recente
    response = requests.get(version_url)
    latest_version = response.text.strip()

    # URL do arquivo .exe no GitHub que você deseja baixar se houver uma nova versão
    file_url = f"https://github.com/zVitorSantos/Precificador/releases/download/v{latest_version}/main.exe"

    # Compara a versão mais recente com a versão atual
    if latest_version > current_version:
        print("Uma nova versão está disponível. Atualizando...")

        # Faz uma solicitação GET para baixar o novo arquivo .exe
        response = requests.get(file_url)

        # Substitui o antigo arquivo .exe pelo novo
        with open("main_new.exe", "wb") as file:
            file.write(response.content)

        # Substitui o antigo arquivo .exe pelo novo
        os.rename("main_new.exe", "main.exe")

        # Atualiza a current_version no script
        current_version = latest_version

        # Atualiza a current_version no arquivo version.txt
        with open("version.txt", "w") as file:
            file.write(current_version)

        print("Atualização concluída.")
    else:
        print("Você já está na versão mais recente.")

check_for_updates()