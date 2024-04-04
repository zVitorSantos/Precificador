import os
import subprocess
import requests
import zipfile
import sys
import shutil
from tqdm import tqdm

def update():
    try:
        # URL do arquivo no GitHub que contém a versão mais recente do CLI
        version_url = "https://raw.githubusercontent.com/zVitorSantos/Precificador/main/version.txt"

        # Faz uma solicitação GET para obter a versão mais recente
        response = requests.get(version_url)
        latest_version = response.text.strip()

        # Lê a versão atual do arquivo version.txt
        with open("version.txt", "r") as file:
            current_version = file.read().strip()

        # Verifica se já está na versão mais recente
        if current_version == latest_version:
            print("Você já está na versão mais recente.")
            input("\nPressione qualquer tecla para continuar...")
            # Abre o main.exe
            subprocess.Popen(["./main.exe"])
            sys.exit()

        # URL do arquivo .zip no GitHub que você deseja baixar
        file_url = f"https://github.com/zVitorSantos/Precificador/releases/download/v{latest_version}/Precificador-v{latest_version}.zip"

        # Faz uma solicitação GET para baixar o novo arquivo .zip
        response = requests.get(file_url, stream=True)

        # Obtém o tamanho total do arquivo
        total_size = int(response.headers.get('content-length', 0))

        # Cria a barra de progresso
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

        # Salva o novo arquivo .zip
        with open(f"Precificador-v{latest_version}.zip", "wb") as file:
            for data in response.iter_content(chunk_size=1024):
                progress_bar.update(len(data))
                file.write(data)

        progress_bar.close()

        # Descompacta o arquivo .zip
        with zipfile.ZipFile(f"Precificador-v{latest_version}.zip", 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Substitui o antigo arquivo .exe pelo novo
        os.remove("main.exe")
        os.rename(f"./Precificador-v{latest_version}/main.exe", "main.exe")

        # Atualiza a current_version no arquivo version.txt
        with open("version.txt", "w") as file:
            file.write(latest_version)

        # Deleta o que sobrou na pasta
        shutil.rmtree(f"./Precificador-v{latest_version}")

        # Deleta o .zip
        os.remove(f"Precificador-v{latest_version}.zip")

        print("Atualização concluída.")

        # Abre o novo main.exe
        subprocess.Popen(["main.exe"])
        
        sys.exit()
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a nova versão: {e}")
        
    input("\nPressione qualquer tecla para continuar...")

update()