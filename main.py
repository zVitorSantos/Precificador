import json
import os
import sys
import requests
import subprocess
import pandas as pd
import time

# imports to import/export functions
# from tkinter import Tk
# from tkinter.filedialog import askopenfilename, asksaveasfilename
# from datetime import datetime

# *TODO: Preparar para salvar os produtos em um banco de dados
# *TODO: Finalizar formulário de importação/exportação de produtos

def set_console_size():
    os.system("mode con: cols=75")
set_console_size()
    
def check_for_updates():
    try:
        # URL do arquivo no GitHub que contém a versão mais recente do CLI
        version_url = "https://raw.githubusercontent.com/zVitorSantos/Precificador/main/version.txt"

        # Faz uma solicitação GET para obter a versão mais recente
        response = requests.get(version_url)
        latest_version = response.text.strip()

        try:
            # Tenta ler a versão atual do arquivo version.txt local
            with open("version.txt", "r") as file:
                current_version = file.read().strip()
        except FileNotFoundError:
            # Se o arquivo version.txt não for encontrado, define a versão atual como 0
            current_version = "0"

        # Compara a versão mais recente com a versão atual
        if latest_version > current_version:
            print("Uma nova versão está disponível. Atualizando...\n")
            # Inicia o update.exe
            subprocess.Popen(['update.exe'])
            # Termina o main.exe
            sys.exit()
        else:
            print("Versão mais recente.")
            
    except requests.exceptions.RequestException as e:
        print(f"Erro ao verificar atualizações: {e}")
        input("\nPressione qualquer tecla para continuar...")

check_for_updates()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    verificar_config()
      
    while True:
        clear_screen()
        print("Programa de Precificação de Produtos\n")
        print("1. Cadastrar Produto")
        print("2. Produtos Cadastrados")
        print("3. Configurações")
        print("4. Sair")
        opcao = input("\nEscolha uma opção: ")
        clear_screen()
        if opcao == "1":
            precificar_produto()
        elif opcao == "2":
            exibir_cadastrados()
        elif opcao == "3":
            while True:
                clear_screen()
                print("Configurações\n")
                print("1. Valores Padrões")
                print("2. Importar/Exportar(não finalizada)")
                print("3. Info")
                print("4. Voltar")
                opcao_config = input("\nEscolha uma opção: ")
                clear_screen()
                if opcao_config == "1":
                    alterar_configuracoes()
                elif opcao_config == "2":
                    importar_exportar()
                elif opcao_config == "3":
                    show_info()
                elif opcao_config == "4":
                    break
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
                    time.sleep(2)

        elif opcao == "4":
            clear_screen()
            break
        
def verificar_config():
    # Verifique se o arquivo config.json existe
    if not os.path.exists('config.json'):
        # Se não existir, crie o arquivo com valores padrão
        config = {
            'config_acresimos': {
                'imposto': 12.0,
                'frete': 5.0,
                'comissao': 5.0,
                'lucro': 10.0
            },
            'config_calcular': {
                'mao_de_obra': 0.04,
                'custo_injecao': 100.00,
                'custo_pintura_metalizada': 50,
                'custo_pintura_normal': 40
            },
            'materiais': {
                'PP': 12.15,
                'ABS': 13.03,
                'TPU': 33.10,
                'PVC': 15.47
            }
        }
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
def salvar_produto(produto):
    try:
        with open('produtos.json', 'r') as f:
            produtos = json.load(f)
    except FileNotFoundError:
        produtos = []
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON.")
        return
    except Exception as e:
        print(f"Erro desconhecido: {e}")
        return

    produtos.append(produto)

    try:
        with open('produtos.json', 'w') as f:
            json.dump(produtos, f, indent=4)
    except Exception as e:
        print(f"Erro ao escrever no arquivo: {e}")
        
def excluir_produto(referencia):
    clear_screen()
    try:
        produtos = carregar_produtos()
    except Exception as e:
        print(f"Erro ao carregar produtos: {e}")
        return
    produto = next((produto for produto in produtos if produto['referencia'] == referencia), None)
    if produto is None:
        print("Produto não encontrado.")
        return
    confirmacao = input(f"Tem certeza de que deseja excluir o produto {produto['referencia']}? (s/n): ")
    if confirmacao.lower() != 's':
        print("Exclusão cancelada.")
        return
    produtos = [produto for produto in produtos if produto['referencia'] != referencia]
    try:
        with open('produtos.json', 'w') as f:
            json.dump(produtos, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar produtos: {e}")
        return
    print(f"Produto {produto['nome']} excluído com sucesso.")

def atualizar_produto(referencia):
    try:
        with open('produtos.json', 'r') as f:
            produtos = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Erro ao carregar produtos.")
        return

    for produto in produtos:
        if produto['referencia'] == referencia:
            while True:
                for i, resposta in enumerate(produto['respostas'], start=1):
                    clear_screen()
                    print(f"\nInformações da resposta {i}:\n")
                    print(f"1. Peso: {resposta['peso']} g")
                    print(f"2. Valor do material: R${resposta['valor_material']:.2f}")
                    print(f"3. Cavidades: {resposta['cavidades']}")
                    print(f"4. Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
                    print(f"5. Peças por satélite: {resposta['pecas_por_satelite']}")
                    print(f"6. Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 2 else 'Metalizada'}")
                    print(f"7. Imposto: {produto['acrescimos']['imposto']}%")
                    print(f"8. Frete: {produto['acrescimos']['frete']}%")
                    print(f"9. Comissão: {produto['acrescimos']['comissao']}%")
                    print(f"10. Lucro: {produto['acrescimos']['lucro']}%")
                    print(f"11. Voltar")

                # Pedir ao usuário para escolher qual informação ele quer alterar
                opcao = input("\nEscolha uma opção ou finalize: ")

                try:
                    if opcao == "1":
                        while True:
                            peso = float(input("Novo peso: "))
                            if 1 <= peso <= 1000:
                                resposta['peso'] = peso
                                break
                            else:
                                print("O peso deve estar entre 1 e 1000.")
                                time.sleep(3)
                    elif opcao == "2":
                        while True:
                            valor_material = float(input("Novo valor do material: R$"))
                            if 1 <= valor_material <= 10000:
                                resposta['valor_material'] = valor_material
                                break
                            else:
                                print("O valor do material deve estar entre 1 e 10000.")
                                time.sleep(3)
                    elif opcao == "3":
                        while True:
                            cavidades = int(input("Novas cavidades: "))
                            if 1 <= cavidades <= 10000:
                                resposta['cavidades'] = cavidades
                                break
                            else:
                                print("As cavidades devem estar entre 1 e 10000.")
                                time.sleep(3)
                    elif opcao == "4":
                        while True:
                            tempo_ciclo = float(input("Novo tempo de ciclo: "))
                            if 1 <= tempo_ciclo <= 100000:
                                resposta['tempo_ciclo'] = tempo_ciclo
                                break
                            else:
                                print("O tempo de ciclo deve estar entre 1 e 100000.")
                                time.sleep(3)
                    elif opcao == "5":
                        while True:
                            pecas_por_satelite = int(input("Novas peças por satélite: "))
                            if 1 <= pecas_por_satelite <= 10000:
                                resposta['pecas_por_satelite'] = pecas_por_satelite
                                break
                            else:
                                print("As peças por satélite devem estar entre 1 e 10000.")
                                time.sleep(3)
                    elif opcao == "6":
                        while True:
                            metalizado_ou_pintado = int(input("1. Metalizada\n2. Pintada\n\nEscolha uma opção:"))
                            if metalizado_ou_pintado in [1, 2]:
                                resposta['metalizado_ou_pintado'] = metalizado_ou_pintado
                                break
                            else:
                                print("Por favor, escolha 1 para Metalizada ou 2 para Pintada.")
                                time.sleep(3)
                    elif opcao in ["7", "8", "9", "10"]:
                        while True:
                            acrescimo = float(input("Novo " + ("imposto" if opcao == "7" else "frete" if opcao == "8" else "comissão" if opcao == "9" else "lucro") + ": "))
                            if 0 <= acrescimo <= 100:
                                produto['acrescimos'][("imposto" if opcao == "7" else "frete" if opcao == "8" else "comissao" if opcao == "9" else "lucro")] = acrescimo
                                break
                            else:
                                print("O valor deve estar entre 0 e 100.")
                                time.sleep(3)
                    elif opcao == "11":
                        break
                except ValueError:
                    print("Entrada inválida. Por favor, tente novamente.")
                    continue

            # Atualizar as informações do produto
            for resposta in produto['respostas']:
                custos = calcular(resposta)
                produto['custos'] = custos
                produto['custo_total'] = custos['custo_total']
                produto['valor_total'] = custos['valor_total']

            break

    try:
        with open('produtos.json', 'w') as f:
            json.dump(produtos, f, indent=4)
    except Exception as e:
        print(f"Erro ao salvar produtos: {e}")
        
def carregar_produtos():
    try:
        with open('produtos.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON.")
        return []
    
def exibir_cadastrados():
    voltar = False  
    while True:
        produtos = carregar_produtos()
        def produto_existe(referencia):
            for produto in produtos:
                if produto["referencia"] == int(referencia):
                    return True
            return False

        if not produtos:
            print("Nenhum produto cadastrado.")
            while True:
                opcao_produto = input("\n1. Cadastrar Produto.\n2. Voltar\n\nEscolha uma opção: ").upper()
                if opcao_produto == "1":
                    clear_screen()
                    precificar_produto()
                    break
                elif opcao_produto == "2":
                    break
                else:
                    print("Por favor, escolha uma opção válida.")
                    time.sleep(3)
        else:
            clear_screen()
            for produto in produtos:
                print("Ref:", produto["referencia"])
            opcao_produto = input("\n1. Atualizar Produto\n2. Excluir Produto\n3. Gerar Relatório\n4. Voltar\n\nEscolha: ").upper()
            while True:
                if opcao_produto == "1":
                    clear_screen()
                    referencia = input("Digite a referência da peça que deseja atualizar: ")
                    if produto_existe(referencia):
                        atualizar_produto(referencia)
                    else:
                        print("Referência do produto não encontrada.")
                        opcao = input("Deseja inserir outra referência (1) ou voltar (2)? ")
                        if opcao == "2":
                            clear_screen()
                            break
                elif opcao_produto == "2":
                    clear_screen()
                    referencia = input("Digite a referência da peça que deseja excluir: ")
                    if produto_existe(referencia):
                        excluir_produto(referencia)
                    else:
                        print("Referência do produto não encontrada.")
                        opcao = input("Deseja inserir outra referência (1) ou voltar (2)? ")
                        if opcao == "2":
                            clear_screen()
                            break
                elif opcao_produto == "3":
                    while True:
                        clear_screen()
                        referencia = input("Digite a referência para gerar o relatório,\nou digite (1) para voltar:\n\nReferência:")
                        if referencia.lower() == '1':
                            break
                        clear_screen()
                        if produto_existe(referencia):
                            for produto in produtos:
                                if produto["referencia"] == int(referencia):
                                    gerar_relatorio([produto])
                                    clear_screen()
                                    break
                        else:
                            print("Referência do produto não encontrada.")
                            opcao = input("Deseja inserir outra referência (1) ou voltar (2)? ")
                            if opcao == "2":
                                clear_screen()
                                break
                        
                elif opcao_produto == "4":
                    clear_screen()
                    voltar = True 
                    break
                else:
                    print("Opção inválida. Por favor, escolha uma opção válida.")
                    time.sleep(3)
                    break
            if voltar:
                break
            
def show_info():
    with open("version.txt", "r") as file:
        current_version = file.read().strip()
    print(f"Versão atual do programa: {current_version}")
    input("\nPressione qualquer tecla para voltar...")

def precificar_produto():
    while True:
        try:
            entrada = input("Digite a referência do produto ou (1) para voltar: ")
            if entrada.lower() == '1':
                return
            referencia = int(entrada)
            if referencia < 150:
                print("A referência deve ser igual ou maior que 150.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
            time.sleep(3)
            continue

    try:
        produtos = carregar_produtos()
    except Exception as e:
        print(f"Erro ao carregar produtos: {e}")
        return

    for produto in produtos:
        if produto['referencia'] == referencia:
            while True:
                clear_screen()
                opcao = input("Essa referência já existe.\n\n1. Atualizar produto\n2. Excluir produto\n3. Voltar\n\nEscolha uma opção: ").upper()
                if opcao == "1":
                    atualizar_produto(referencia)
                    return
                elif opcao == "2":
                    if excluir_produto(referencia):
                        return
                elif opcao == "3":
                    clear_screen()
                    return

    montado = None
    while montado is None:
        clear_screen()
        resposta = input("Tem mais de uma parte?\n1. Sim\n2. Não\n\nEscolha uma opção: ")
        if resposta in ['1', '2']:
            montado = resposta == '1'
        else:
            print("Resposta inválida. Por favor, digite 1 para Sim ou 2 para Não.")
            time.sleep(3)

    produtos = []
    respostas_result = [] 
    custos_result = []  
    if montado:
        num_partes = None
        while num_partes is None:
            clear_screen()
            try:
                resposta = int(input("Quantas partes o produto possui? "))
                if 2 <= resposta <= 10:
                    num_partes = resposta
                else:
                    print("Resposta inválida. Por favor, digite um número entre 2 e 10.")
                    time.sleep(3)
            except ValueError:
                print("Entrada inválida. Por favor, digite um número inteiro.")
                time.sleep(3)
                continue
    
        clear_screen()
        custo_total_produto = 0
        for i in range(num_partes):
            print(f"\nPerguntas para a parte {i+1}")
            respostas = perguntas()
            respostas_result.append(respostas)
            custos = calcular(respostas)  
            custos_result.append(custos) 
            custo_total_produto += custos['custo_total']
    
        acrescimos_result = acrescimos()
        valor_total_produto = custo_total_produto * (1 + acrescimos_result["imposto"]/100)
        valor_total_produto = valor_total_produto * (1 + acrescimos_result["frete"]/100)
        valor_total_produto = valor_total_produto * (1 + acrescimos_result["comissao"]/100)
        valor_total_produto = valor_total_produto * (1 + acrescimos_result["lucro"]/100)
    
        produto = {
            "referencia": referencia,
            "montado": montado,
            "acrescimos": acrescimos_result,
            "respostas": respostas_result,
            "custos": custos_result,
            "custo_total": round(custo_total_produto, 4),
            "valor_total": round(valor_total_produto, 4)
        }
        produtos.append(produto)
    else:
        clear_screen()
        respostas = perguntas()
        respostas_result = [respostas]  
        custos = calcular(respostas)  
        custos_result = [custos]  
        acrescimos_result = acrescimos()
        custo_total_produto = custos['custo_total']
        valor_total_produto = custo_total_produto * (1 + acrescimos_result["imposto"]/100)
        valor_total_produto = valor_total_produto * (1 + acrescimos_result["frete"]/100)
        valor_total_produto = valor_total_produto * (1 + acrescimos_result["comissao"]/100)
        valor_total_produto = valor_total_produto * (1 + acrescimos_result["lucro"]/100)
        produto = {
            "referencia": referencia,
            "montado": montado,
            "acrescimos": acrescimos_result,
            "respostas": respostas_result,
            "custos": custos_result,
            "custo_total": round(custo_total_produto, 4),
            "valor_total": round(valor_total_produto, 4)
        }
        produtos.append(produto)

    while True:
        clear_screen()
        try:
            salvar_produto(produto)
        except Exception as e:
            print(f"Erro ao salvar produto: {e}")
            continue
        opcao = input("Cadastro concluído com Sucesso!\n\n1. Relatório da peça\n2. Voltar ao menu\n\nEscolha uma opção: ")
        if opcao == "1":
            clear_screen()
            gerar_relatorio(produtos)
        elif opcao == "2":
            clear_screen()
            break
        else:
            clear_screen()
            print("Resposta inválida. Por favor, escolha uma opção válida")
            time.sleep(3)

def perguntas():
    # Carregue os materiais do arquivo config.json
    with open('config.json', 'r') as f:
        config = json.load(f)
    materiais = {str(i+1): material for i, material in enumerate(config['materiais'].keys())}
    materiais[str(len(materiais) + 1)] = 'Outro'
    valores = config['materiais']

    # Perguntas que serão feitas para cada parte ou para o produto inteiro
    clear_screen()
    while True:
        clear_screen()
        try:
            peso = float(input("Peso(g): ").replace(',', '.'))
            break
        except ValueError:
            print("Por favor, insira um número válido.")
            time.sleep(3)
    clear_screen()
    print("Material")
    for key, value in sorted(materiais.items(), key=lambda item: item[0]):
        print(f"{key}. {value}")
    while True:
        material_escolhido = input("\n\nEscolha um material: ")
        if material_escolhido in materiais:
            if materiais[material_escolhido] == 'Outro':
                while True:
                    try:
                        valor_material = float(input("Insira o valor do material: "))
                        if valor_material >= 0:
                            valores['Outro'] = valor_material
                            break
                        else:
                            print("Por favor, insira um valor maior ou igual que 0.")
                    except ValueError:
                        print("Por favor, insira um número válido.")
            break
        else:
            print("Por favor, escolha um material válido.")
            time.sleep(3)
    material = materiais[material_escolhido]
    valor_material = valores[material]
    clear_screen()
    while True:
        clear_screen()
        try:
            cavidades = int(input("Quantas cavidades: "))
            if 0 <= cavidades <= 1000:
                break
            else:
                print("Por favor, insira um número entre 0 e 1000.")
                time.sleep(3)
        except ValueError:
            print("Por favor, insira um número válido.")
            time.sleep(3)
    clear_screen()
    while True:
        clear_screen()
        try:
            tempo_ciclo = int(input("Tempo de ciclo (segundos): "))
            break
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
            time.sleep(3)
    clear_screen()
    while True:
        clear_screen()
        try:
            pecas_por_satelite = int(input("Peças por satélite: "))
            break
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
            time.sleep(3)
    clear_screen()
    while True:
        clear_screen()
        metalizado_ou_pintado = int(input("A peça é Metalizada ou Pintada?\n1. Metalizada\n2. Pintada\n\nEscolha uma opção: "))
        if metalizado_ou_pintado in [1, 2]:
            break
        else:
            print("Por favor, insira 1 para Metalizada ou 2 para Pintada.")
            time.sleep(3)
    clear_screen()

    # Retorne um dicionário com as respostas
    return {
        "peso": peso,
        "valor_material": valores[material],
        "cavidades": cavidades,
        "tempo_ciclo": tempo_ciclo,
        "pecas_por_satelite": pecas_por_satelite,
        "metalizado_ou_pintado": metalizado_ou_pintado
    }
        
def acrescimos():
    # Carregue as configurações de acréscimos do arquivo config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Use os valores carregados como padrões
    imposto_padrao = config['config_acresimos']['imposto']
    frete_padrao = config['config_acresimos']['frete']
    comissao_padrao = config['config_acresimos']['comissao']
    lucro_padrao = config['config_acresimos']['lucro']
    
    # Perguntas sobre imposto, frete, comissão e lucro
    while True:
        imposto = input(f"Imposto (padrão {imposto_padrao}%): ")
        if not imposto:
            imposto = imposto_padrao
            break
        try:
            imposto = float(imposto)
            if 0 <= imposto <= 100:
                break
            else:
                print("Por favor, insira um número entre 0 e 100.")
                time.sleep(3)
        except ValueError:
            print("Por favor, insira um número válido.")
            time.sleep(3)
    while True:
        frete = input(f"Frete (padrão {frete_padrao}%): ")
        if not frete:
            frete = frete_padrao
            break
        try:
            frete = float(frete)
            if 0 <= frete <= 100:
                break
            else:
                print("Por favor, insira um número entre 0 e 100.")
                time.sleep(3)
        except ValueError:
            print("Por favor, insira um número válido.")
            time.sleep(3)
    while True:
        comissao = input(f"Comissão (padrão {comissao_padrao}%): ")
        if not comissao:
            comissao = comissao_padrao
            break
        try:
            comissao = float(comissao)
            if 0 <= comissao <= 100:
                break
            else:
                print("Por favor, insira um número entre 0 e 100.")
                time.sleep(3)
        except ValueError:
            print("Por favor, insira um número válido.")
            time.sleep(3)

    while True:
        lucro = input(f"Lucro (padrão {lucro_padrao}%): ")
        if not lucro:
            lucro = lucro_padrao
            break
        try:
            lucro = float(lucro)
            if 0 <= lucro <= 100:
                break
            else:
                print("Por favor, insira um número entre 0 e 100.")
                time.sleep(3)
        except ValueError:
            print("Por favor, insira um número válido.")
            time.sleep(3)

    # Crie um dicionário com os acréscimos
    acrescimos = {
        "imposto": imposto,
        "frete": frete,
        "comissao": comissao,
        "lucro": lucro
    }

    # Retorne o dicionário com os acréscimos
    return acrescimos

def calcular(respostas):
    # Carregue as configurações de cálculo do arquivo config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Calcule quantas peças são feitas em uma hora
    pecas_por_hora = round((3600 / respostas["tempo_ciclo"]) * respostas["cavidades"], 4)

    # Calcule o custo por peça
    custo_injecao = round(config['config_calcular']['custo_injecao'] / pecas_por_hora, 4)

    # Calcule o custo do material por hora
    peso_kg = respostas["peso"] / 1000
    custo_material = 0 if respostas["valor_material"] == 0 else round(peso_kg * respostas["valor_material"], 4)

    # Calcule o custo da pintura por peça
    if respostas["metalizado_ou_pintado"] == 1:
        custo_pintura = round(config['config_calcular']['custo_pintura_metalizada'] / respostas["pecas_por_satelite"], 4)
    else:
        custo_pintura = round(config['config_calcular']['custo_pintura_normal'] / respostas["pecas_por_satelite"], 4)

    # Use a mão de obra do arquivo de configuração
    mao_de_obra = config['config_calcular']['mao_de_obra']

    # Calcule o custo total e o valor total
    custo_total = round(custo_injecao + custo_material + custo_pintura + mao_de_obra, 4)
    valor_total = custo_total
    # Retorne um dicionário com o custo e o valor da peça
    return {
        "pecas_por_hora": pecas_por_hora,
        "custo_injecao": custo_injecao,
        "custo_material": custo_material,
        "custo_pintura": custo_pintura,
        "mao_de_obra": mao_de_obra,
        "custo_total": custo_total,
        "valor_total": valor_total
    }

def alterar_configuracoes():
    # Carregue as configurações atuais do arquivo config.json
    with open('config.json', 'r') as f:
        config = json.load(f)

    while True:
        clear_screen()
        print("Configurações\n")
        print("1. Alterar configurações de acréscimos")
        print("2. Alterar configurações de cálculo")
        print("3. Alterar configurações de materiais")
        print("4. Voltar")
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            while True:
                clear_screen()
                # Exibe todas as configurações de acréscimos
                for i, key in enumerate(config['config_acresimos'], start=1):
                    print(f"{i}. {key}: {config['config_acresimos'][key]}")
                # Permite ao usuário escolher qual configuração alterar
                opcao_acresimo = int(input("\nEscolha uma opção para alterar ou 0 para voltar: "))
                if opcao_acresimo != 0:
                    key = list(config['config_acresimos'].keys())[opcao_acresimo - 1]
                    novo_valor = input(f"{key} atualmente é {config['config_acresimos'][key]}. Digite um novo valor: ")
                    config['config_acresimos'][key] = float(novo_valor)
                else:
                    clear_screen()
                    break
        elif opcao == "2":
            while True:
                clear_screen()
                # Exiba todas as configurações de cálculo
                for i, key in enumerate(config['config_calcular'], start=1):
                    print(f"{i}. {key}: {config['config_calcular'][key]}")
                # Permite ao usuário escolher qual configuração alterar
                opcao_calculo = int(input("\nEscolha uma opção para alterar ou 0 para voltar: "))
                if opcao_calculo != 0:
                    key = list(config['config_calcular'].keys())[opcao_calculo - 1]
                    novo_valor = input(f"{key} atualmente é {config['config_calcular'][key]}. Digite um novo valor: ")
                    config['config_calcular'][key] = float(novo_valor)
                else:
                    clear_screen()
                    break
        elif opcao == "3":
            while True:
                clear_screen()
                # Exibe todas as configurações de materiais
                for i, key in enumerate(config['materiais'], start=1):
                    print(f"{i}. {key}: {config['materiais'][key]}")
                # Permite ao usuário escolher qual configuração alterar
                opcao_material = int(input("\nEscolha uma opção para alterar ou 0 para voltar: "))
                if opcao_material != 0:
                    key = list(config['materiais'].keys())[opcao_material - 1]
                    novo_valor = input(f"{key} atualmente é {config['materiais'][key]}. Digite um novo valor: ")
                    config['materiais'][key] = float(novo_valor)
                else:
                    clear_screen()
                    break
        elif opcao == "4":
            break
        else:
            print("Por favor, escolha uma opção válida.")
            time.sleep(3)

    # Grava as novas configurações no arquivo config.json
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

    print("Configurações atualizadas com sucesso.")
    time.sleep(3)
    
def adicionar_produto(produto):
    print("Essa função não está completa!")
    time.sleep(5)
    # # Verificar se a referência do produto já existe
    # produtos = carregar_produtos()
    # for p in produtos:
    #     if 'Referencia' in p and 'Referencia' in produto and p['Referencia'] == produto['Referencia']:
    #         print(f"Produto com referência {produto['Referencia']} já existe.")
    #         return
    # # Calcular as informações que faltam
    # for resposta in produto['respostas']:
    #     custos = calcular(resposta)
    #     resposta.update(custos)
    # # Adicionar o produto
    # produtos.append(produto)
    # salvar_produto(produtos) 
    # print(f"Produto com referência {produto['Referencia']} adicionado com sucesso.")
    # time.sleep(3)

def modelo_importacao():
    print("Essa função não está completa!")
    time.sleep(5)
    # # Definir as colunas do modelo
    # colunas = ['Referencia', 'Material', 'Peso', 'Cavidades', 'Tempo Ciclo', 'Peças por Satélite', 'Metalizado ou Pintado']
    # # Criar um DataFrame com dois exemplos de produtos
    # data = {
    #     'Referencia': ['EX1', 'EX2', 'EX2'],
    #     'Material': ['PP', 'PP', 'ABS'],
    #     'Peso': [0.005, 0.005, 0.001],
    #     'Cavidades': [24, 24, 50],
    #     'Tempo Ciclo': [15, 15, 8],
    #     'Peças por Satélite': [700, 700, 1289],
    #     'Metalizado ou Pintado': ['Metalizado', 'Metalizado', 'Pintado']
    # }
    # df = pd.DataFrame(data, columns=colunas)
    # # Abrir uma janela de diálogo para escolher onde salvar o arquivo
    # root = Tk()
    # root.withdraw()
    # root.attributes('-topmost', True)
    # arquivo = asksaveasfilename(defaultextension=".xlsx", initialfile="modelo_importacao", filetypes=[("Excel files", "*.xlsx")])
    # if not arquivo:  # Se o usuário cancelar a janela de diálogo
    #     return
    # # Salvar o DataFrame como um arquivo .xlsx
    # df.to_excel(arquivo, index=False)
    # clear_screen()
    # print("Modelo de importação criado com sucesso.")
    # root.destroy()

def importar_exportar():
    print("Essa função não está completa!")
    time.sleep(5)
    # # Carregue as configurações atuais do arquivo config.json
    # with open('config.json', 'r') as f:
    #     config = json.load(f)
        
    # opcao = input("1. Importar\n2. Exportar\n3. Voltar\n\nEscolha uma opção: ")
    # if opcao == "1":
    #     clear_screen()
    #     opcao_importacao = input("1. Baixar modelo de importação\n2. Importar arquivo\n\nEscolha uma opção: ")
    #     if opcao_importacao == "1":
    #         modelo_importacao()
    #         input("\nPressione Enter para continuar...")
    #     elif opcao_importacao == "2":
    #         clear_screen()
    #         root = Tk()
    #         root.withdraw()
    #         root.attributes('-topmost', True)
    #         arquivo = askopenfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    #         if not arquivo:
    #             return
            
    #         # Ler o arquivo Excel ou CSV
    #         if arquivo.endswith('.csv'):
    #             df = pd.read_csv(arquivo)
    #         elif arquivo.endswith('.xlsx'):
    #             df = pd.read_excel(arquivo)
    #         else:
    #             print("Formato de arquivo não suportado.")
    #             input("\nPressione Enter para continuar...")
    #             return
            
    #         # Use os valores carregados como padrões
    #         imposto_padrao = config['config_acresimos']['imposto']
    #         frete_padrao = config['config_acresimos']['frete']
    #         comissao_padrao = config['config_acresimos']['comissao']
    #         lucro_padrao = config['config_acresimos']['lucro']
            
    #         produtos = []
            
    #         # Iterar sobre os registros do DataFrame
    #         for index, row in df.iterrows():
    #             produto = {
    #                 "referencia": row['Referencia'],
    #                 "montado": False,
    #                 "acrescimos": {
    #                     "imposto": imposto_padrao,
    #                     "frete": frete_padrao,
    #                     "comissao": comissao_padrao,
    #                     "lucro": lucro_padrao
    #                 },
    #                 "respostas": [
    #                     {
    #                         "peso": row['Peso'],
    #                         "valor_material": config['materiais'][row['Material']],
    #                         "cavidades": row['Cavidades'],
    #                         "tempo_ciclo": row['Tempo Ciclo'],
    #                         "pecas_por_satelite": row['Peças por Satélite'],
    #                         "metalizado_ou_pintado": 1 if row['Metalizado ou Pintado'] == 'Metalizado' else 2
    #                     }
    #                 ],
    #                 "custos": {
    #                     "mao_de_obra": config['config_calcular']['mao_de_obra'],
    #                     "custo_injecao": config['config_calcular']['custo_injecao'],
    #                     "custo_pintura": config['config_calcular']['custo_pintura_metalizada'] if row['Metalizado ou Pintado'] == 'Metalizado' else config['config_calcular']['custo_pintura_normal'],
    #                     "custo_material": row['Peso'] * config['materiais'][row['Material']]
    #                 }
    #             }
                
    #             produto['custo_total'] = sum(produto['custos'].values())
    #             produto['valor_total'] = produto['custo_total'] * (1 + sum(produto['acrescimos'].values()) / 100)
                
    #             produtos.append(produto)
            
    #         # Adicionar os produtos processados ao sistema
    #         for produto in produtos:
    #             adicionar_produto(produto)
            
    #         root.destroy()
    #     else:
    #         clear_screen()
    #         print("Opção inválida.")
    #         input("\nPressione Enter para continuar...")
    # elif opcao == "2":
    #     clear_screen()
    #     # Obter a data e a hora atual e formatá-las como uma string
    #     arquivo = "Export"
    #     produtos = carregar_produtos()
    #     df = pd.json_normalize(produtos, record_path='respostas', meta=['referencia', 'montado', 'acrescimos', 'custos', 'custo_total', 'valor_total'])
    #     # Adicionar a extensão .csv ao nome do arquivo
    #     arquivo_csv = arquivo + '.csv'
    #     root = Tk()
    #     root.withdraw()
    #     root.attributes('-topmost', True) 
    #     arquivo_csv = asksaveasfilename(defaultextension=".csv", initialfile=arquivo_csv, filetypes=[("CSV files", "*.csv")])  # Mostra uma janela de diálogo 'Salvar como'
    #     if not arquivo_csv:
    #         return
    #     df.to_csv(arquivo_csv, index=False)
    #     root.destroy() 
    # elif opcao == "3":
    #     clear_screen()
    #     return
    # else:
    #     clear_screen()
    #     print("Opção inválida.")
    #     input("\nPressione Enter para continuar...")
    
def gerar_relatorio(produtos):
    while True:
        tipo_relatorio = input("Qual tipo de relatório você deseja?\n1. Parcial\n2. Completo\n3. Voltar\n\nEscolha uma opção: ")
        if tipo_relatorio == "1":
            relatorio_parcial(produtos)
            break
        elif tipo_relatorio == "2":
            relatorio_completo(produtos)
            break
        elif tipo_relatorio == "3":
            break
        else:
            print("Por favor, escolha uma opção válida.")
            time.sleep(3)

def relatorio_parcial(produtos):
    clear_screen()
    for i, produto in enumerate(produtos, start=1):
        print(f"Relatório do Produto {produto['referencia']}")
        for j, resposta in enumerate(produto['respostas'], start=1):
            print(f"\n{'Informações da Parte - ' + str(j) if produto['montado'] else 'Informações:'}\n")
            print(f"Peso: {resposta['peso']} g")
            print(f"Valor do material: R${resposta['valor_material']:.2f}")
            print(f"Cavidades: {resposta['cavidades']}")
            print(f"Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
            print(f"Peças por satélite: {resposta['pecas_por_satelite']}")
            print(f"Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 2 else 'Metalizada'}")
            for k, custo in enumerate(produto['custos'], start=1):
                if k == j:
                    if produto['montado']:
                        print(f"\nCusto da peça: R${custo['custo_total']:.2f}")
        print("\nAcréscimos:")
        print(f"Imposto: {produto['acrescimos']['imposto']}%")
        print(f"Frete: {produto['acrescimos']['frete']}%")
        print(f"Comissão: {produto['acrescimos']['comissao']}%")
        print(f"Lucro: {produto['acrescimos']['lucro']}%")
        print("\nTotais:")
        print(f"Custo total: R${produto['custo_total']:.2f}")
        print(f"Valor total: R${produto['valor_total']:.2f}")
    
    input("\nPressione Enter para continuar...")
    
def relatorio_completo(produtos):
    clear_screen()
    for i, produto in enumerate(produtos, start=1):
        print(f"Relatório Completo do Produto {produto['referencia']}")
        for j, resposta in enumerate(produto['respostas'], start=1):
            if produto['montado']:
                print(f"\nInformações da Parte - {j}\n")
            else:
                print("\nInformações:")
            print(f"Peso: {resposta['peso']} g")
            print(f"Valor do material: R${resposta['valor_material']:.2f}")
            print(f"Cavidades: {resposta['cavidades']}")
            print(f"Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
            print(f"Peças por satélite: {resposta['pecas_por_satelite']}")
            print(f"Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 2 else 'Metalizada'}")
            if produto['montado']:
                for k, custo in enumerate(produto['custos'], start=1):
                    if k == j:
                        print(f"\n{'Formação de custos da peça:' if produto['montado'] else 'Formação de custos:'}")
                        print(f"Peças por hora: {custo['pecas_por_hora']}")
                        print(f"Custo de injeção: R${custo['custo_injecao']:.2f}")
                        print(f"Custo do material: R${custo['custo_material']:.2f}")
                        print(f"Custo de pintura: R${custo['custo_pintura']:.2f}")
                        print(f"Mão de obra: R${custo['mao_de_obra']:.2f}")
                        print(f"Custo da peça: R${custo['custo_total']:.2f}")
            else:
                custo = produto['custos'][0] if isinstance(produto['custos'], list) else produto['custos']
                print(f"\nFormação de custos:")
                print(f"Peças por hora: {custo['pecas_por_hora']}")
                print(f"Custo de injeção: R${custo['custo_injecao']:.2f}")
                print(f"Custo do material: R${custo['custo_material']:.2f}")
                print(f"Custo de pintura: R${custo['custo_pintura']:.2f}")
                print(f"Mão de obra: R${custo['mao_de_obra']:.2f}")
                        
        print("\nAcréscimos:")
        print(f"Imposto: {produto['acrescimos']['imposto']}%")
        print(f"Frete: {produto['acrescimos']['frete']}%")
        print(f"Comissão: {produto['acrescimos']['comissao']}%")
        print(f"Lucro: {produto['acrescimos']['lucro']}%")
        print("\nTotais:")
        print(f"Custo total: R${produto['custo_total']:.2f}")
        print(f"Valor total: R${produto['valor_total']:.2f}")
    
    input("\nPressione Enter para continuar...")
    
menu()