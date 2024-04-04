import os
import shutil
import subprocess

# Cria os executáveis
subprocess.run(["py", "-m", "PyInstaller", "--onefile", "--icon=main.ico", "--specpath", "./spec", "--distpath", "./dist", "main.py"])
subprocess.run(["py", "-m", "PyInstaller", "--onefile", "--icon=update.ico", "--specpath", "./spec", "--distpath", "./dist", "update.py"])

# Lê a versão do arquivo version.txt
with open("version.txt", "r") as file:
    version = file.read().strip()
    
# Caminho para o arquivo zip
zip_file_path = f"./dist/Precificador-v{version}.zip"

# Verifica se o arquivo zip já existe e, em caso afirmativo, exclui-o
if os.path.exists(zip_file_path):
    os.remove(zip_file_path)

# Cria o diretório Precificador v{version} dentro de dist se ele não existir
os.makedirs(f"./dist/Precificador-v{version}", exist_ok=True)

# Copia os executáveis e o version.txt para o diretório Precificador v{version}
shutil.copy("./dist/main.exe", f"./dist/Precificador-v{version}")
shutil.copy("./dist/update.exe", f"./dist/Precificador-v{version}")
shutil.copy("./version.txt", f"./dist/Precificador-v{version}")

# Cria um arquivo zip do diretório Precificador v{version} com o mesmo nome
shutil.make_archive(f"./dist/Precificador-v{version}", 'zip', "./dist", f"Precificador-v{version}")

# Exclui o diretório Precificador v{version}
shutil.rmtree(f"./dist/Precificador-v{version}")

# Exclui os arquivos exe
os.remove("./dist/main.exe")
os.remove("./dist/update.exe")