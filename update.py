import os
import subprocess
import requests
import zipfile
import sys
import shutil
from datetime import timedelta
import progressbar

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
        total_size = int(response.headers.get('content-length', 0))
        
        # Nome do arquivo de saída
        output_file = f"Precificador-v{latest_version}.zip"

        # Inicializa a barra de progresso
        downloaded = 0
        chunk_size = 1024 

        widgets = [
            progressbar.Percentage(),
            ' ',        
            progressbar.Bar(marker='=', left='[', right=']'), 
            ' ',
            progressbar.FileTransferSpeed(unit='B'), 
            ' | ',
            progressbar.FormatLabel('%(value).2f/%(max_value).2f MB'),
        ]
        
        # Abre o arquivo de saída para escrita em modo binário
        with open(output_file, "wb") as file:
            # Inicializa a barra de progresso com o tamanho total esperado em MB
            with progressbar.ProgressBar(max_value=total_size / (1024 * 1024), widgets=widgets) as pbar:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    downloaded += len(data)
                    pbar.update(downloaded / (1024 * 1024))

        # Verifica se o arquivo foi baixado completamente
        if downloaded != total_size:
            print("\nErro: O download do arquivo não foi concluído com sucesso.")
            input("\nPressione qualquer tecla para continuar...")
            sys.exit()
        
        # Verifica o tamanho do arquivo baixado
        downloaded_file_size = os.path.getsize(output_file)
        if downloaded_file_size != total_size:
            print("\nErro: O tamanho do arquivo baixado não corresponde ao tamanho esperado.")
            input("\nPressione qualquer tecla para continuar...")
            sys.exit()
        
        # Descompacta o arquivo .zip
        with zipfile.ZipFile(output_file, 'r') as zip_ref:
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