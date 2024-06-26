import os
import shutil
import subprocess

def build_executable(source_file, icon_file, output_path):
    """Função para construir um executável com PyInstaller."""
    subprocess.run(["py", "-m", "PyInstaller", "--onefile", f"--icon={icon_file}", "--specpath", "./spec", "--distpath", output_path, source_file])

def create_zip_folder(version):
    """Função para criar um arquivo ZIP com a versão especificada."""
    dist_folder = "./dist"
    version_folder = f"{dist_folder}/Precificador-v{version}"
    zip_file_path = f"{dist_folder}/Precificador-v{version}.zip"

    # Verifica se o arquivo ZIP já existe e o exclui, se necessário
    if os.path.exists(zip_file_path):
        os.remove(zip_file_path)

    # Cria o diretório Precificador v{version} dentro de dist se não existir
    os.makedirs(version_folder, exist_ok=True)

    # Copia os executáveis e o version.txt para o diretório Precificador v{version}
    shutil.copy(f"{dist_folder}/main.exe", version_folder)
    shutil.copy(f"{dist_folder}/update.exe", version_folder)
    shutil.copy("./version.txt", version_folder)

    # Cria um arquivo ZIP do diretório Precificador v{version} com o mesmo nome
    shutil.make_archive(version_folder, 'zip', dist_folder, f"Precificador-v{version}")

    # Exclui o diretório Precificador v{version} após a criação do ZIP
    shutil.rmtree(version_folder)

    # Exclui os executáveis após a criação do ZIP
    os.remove(f"{dist_folder}/main.exe")
    os.remove(f"{dist_folder}/update.exe")

def main():
    try:
        # Define o nome do arquivo principal, ícone e diretório de saída
        main_source_file = "main.py"
        update_source_file = "update.py"  
        main_icon_file = "main.ico"
        update_icon_file = "update.ico"  
        output_path = "./dist"

        # Constrói o executável principal
        build_executable(main_source_file, main_icon_file, output_path)

        # Constrói o executável de atualização
        build_executable(update_source_file, update_icon_file, output_path) 

        # Lê a versão do arquivo version.txt
        with open("version.txt", "r") as file:
            version = file.read().strip()

        # Cria um arquivo ZIP com a versão atual
        create_zip_folder(version)

        print("Processo de construção e empacotamento concluído com sucesso.")

    except Exception as e:
        print(f"Erro durante a construção e empacotamento: {e}")

if __name__ == "__main__":
    main()
