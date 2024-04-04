import os
import shutil
import subprocess

# Cria os executáveis
subprocess.run(["py", "-m", "PyInstaller", "--onefile", "--icon=main.ico", "--specpath", "./spec", "--distpath", "./dist/main", "--workpath", "./build/main", "main.py"])
subprocess.run(["py", "-m", "PyInstaller", "--onefile", "--icon=update.ico", "--specpath", "./spec", "--distpath", "./dist/update", "--workpath", "./build/update", "update.py"])

# Cria o diretório Precificador se ele não existir
os.makedirs("Precificador", exist_ok=True)

# Copia os executáveis e o version.txt para o diretório Precificador
shutil.copy("./dist/main/main.exe", "./Precificador")
shutil.copy("./dist/update/update.exe", "./Precificador")
shutil.copy("./version.txt", "./Precificador")

# Lê a versão do arquivo version.txt
with open("version.txt", "r") as file:
    version = file.read().strip()

# Cria um arquivo zip do diretório Precificador com a versão no nome
shutil.make_archive(f"Precificador-v{version}/Precificador", 'zip', ".")

# Exclui o diretório Precificador
shutil.rmtree("Precificador")