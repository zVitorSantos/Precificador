import requests
import os
import subprocess

def check_for_updates():
    # URL do arquivo no GitHub que contém a versão mais recente do seu aplicativo
    version_url = "https://raw.githubusercontent.com/username/repo/master/version.txt"

    # URL do arquivo .exe no GitHub que você deseja baixar se houver uma nova versão
    file_url = "https://github.com/username/repo/releases/download/v1.0.1/app.exe"

    # Versão atual do seu aplicativo
    current_version = "1.0.0"

    # Faz uma solicitação GET para obter a versão mais recente
    response = requests.get(version_url)
    latest_version = response.text.strip()

    # Compara a versão mais recente com a versão atual
    if latest_version > current_version:
        print("Uma nova versão está disponível. Atualizando...")

        # Faz uma solicitação GET para baixar o novo arquivo .exe
        response = requests.get(file_url)

        # Substitui o antigo arquivo .exe pelo novo
        with open("app_new.exe", "wb") as file:
            file.write(response.content)

        # Renomeia o antigo arquivo .exe e substitui pelo novo
        os.rename("app.exe", "app_old.exe")
        os.rename("app_new.exe", "app.exe")

        print("Atualização concluída.")

    # Inicia o aplicativo principal
    subprocess.run(["app.exe"])

check_for_updates()