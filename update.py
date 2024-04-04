import os
import requests
import zipfile
import shutil

def update():
    try:
        # URL do arquivo no GitHub que contém a versão mais recente do CLI
        version_url = "https://raw.githubusercontent.com/zVitorSantos/Precificador/main/version.txt"

        # Faz uma solicitação GET para obter a versão mais recente
        response = requests.get(version_url)
        latest_version = response.text.strip()

        # URL do arquivo .zip no GitHub que você deseja baixar
        file_url = f"https://github.com/zVitorSantos/Precificador/releases/download/v{latest_version}/Precificador.zip"

        print("Baixando a nova versão...")

        # Faz uma solicitação GET para baixar o novo arquivo .zip
        response = requests.get(file_url)

        # Salva o novo arquivo .zip
        with open("Precificador.zip", "wb") as file:
            file.write(response.content)

        # Descompacta o arquivo .zip
        with zipfile.ZipFile("Precificador.zip", 'r') as zip_ref:
            zip_ref.extractall(".")

        # Substitui o antigo arquivo .exe pelo novo
        os.remove("main.exe")
        os.rename("./Precificador/main.exe", "main.exe")

        # Atualiza a current_version no arquivo version.txt
        with open("version.txt", "w") as file:
            file.write(latest_version)

        # Deleta o que sobrou na pasta Precificador
        shutil.rmtree("Precificador")

        print("Atualização concluída.")
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a nova versão: {e}")

update()