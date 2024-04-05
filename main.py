import json
import os
import sys
import requests
import subprocess

def set_console_size():
    os.system("mode con: cols=70 lines=23")
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
    produtos = carregar_produtos()
    
    def produto_existe(referencia):
                    for produto in produtos:
                        if produto["referencia"] == referencia:
                            return True
                    return False
                
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
            while True:
                clear_screen()
                for produto in produtos:
                    clear_screen()
                    print("Ref:", produto["referencia"])
                opcao_produto = input("\n1. Atualizar Produto.\n2. Excluir Produto\n3. Gerar Relatório\n4. Voltar\n\nEscolha: ").upper()

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
                                break
                    elif opcao_produto == "3":
                        clear_screen()
                        referencia = input("Digite a referência da peça que deseja gerar o relatório: ")
                        if produto_existe(referencia):
                            for produto in produtos:
                                if produto["referencia"] == referencia:
                                    gerar_relatorio([produto])
                                    break
                        else:
                            print("Referência do produto não encontrada.")
                            opcao = input("Deseja inserir outra referência (1) ou voltar (2)? ")
                            if opcao == "2":
                                break
                    elif opcao_produto == "4":
                        break
        elif opcao == "3":
            while True:
                clear_screen()
                print("Configurações\n")
                print("1. Valores Padrões")
                print("2. Info")
                print("3. Voltar")
                opcao_config = input("\nEscolha uma opção: ")
                clear_screen()
                if opcao_config == "1":
                    # Aqui você pode adicionar o código para manipular os valores padrões
                    pass
                elif opcao_config == "2":
                    show_info()
                    input("\nPressione qualquer tecla para continuar...")
                elif opcao_config == "3":
                    break

        elif opcao == "4":
            clear_screen()
            break
        
def salvar_produto(produto):
    try:
        with open('produtos.json', 'r') as f:
            produtos = json.load(f)
    except FileNotFoundError:
        produtos = []
    produtos.append(produto)
    with open('produtos.json', 'w') as f:
        json.dump(produtos, f, indent=4)
        
def excluir_produto(referencia):
    clear_screen()
    produtos = carregar_produtos()
    produto = next((produto for produto in produtos if produto['referencia'] == referencia), None)
    if produto is None:
        print("Produto não encontrado.")
        return
    confirmacao = input(f"Tem certeza de que deseja excluir o produto {produto['nome']}? (s/n): ")
    if confirmacao.lower() != 's':
        print("Exclusão cancelada.")
        return
    produtos = [produto for produto in produtos if produto['referencia'] != referencia]
    with open('produtos.json', 'w') as f:
        json.dump(produtos, f, indent=4)
    print(f"Produto {produto['nome']} excluído com sucesso.")

def carregar_produtos():
    try:
        with open('produtos.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def atualizar_produto(referencia):
    # Carregar os produtos do arquivo JSON
    with open('produtos.json', 'r') as f:
        produtos = json.load(f)

    # Encontrar o produto que corresponde à referência fornecida
    for produto in produtos:
        if produto['referencia'] == referencia:
            while True:
                for i, resposta in enumerate(produto['respostas'], start=1):
                    clear_screen()
                    print(f"\nInformações da resposta {i}:\n")
                    print(f"1. Peso: {resposta['peso']} kg")
                    print(f"2. Valor do material: R${resposta['valor_material']:.2f}")
                    print(f"3. Cavidades: {resposta['cavidades']}")
                    print(f"4. Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
                    print(f"5. Peças por satélite: {resposta['pecas_por_satelite']}")
                    print(f"6. Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 1 else 'Metalizada'}")
                    print(f"7. Imposto: {produto['acrescimos']['imposto']}%")
                    print(f"8. Frete: {produto['acrescimos']['frete']}%")
                    print(f"9. Comissão: {produto['acrescimos']['comissao']}%")
                    print(f"10. Lucro: {produto['acrescimos']['lucro']}%")
                    print(f"11. Finalizar")

                # Pedir ao usuário para escolher qual informação ele quer alterar
                opcao = input("\nEscolha uma opção ou finalize: ")

                if opcao == "1":
                    resposta['peso'] = float(input("Novo peso: "))
                elif opcao == "2":
                    resposta['valor_material'] = float(input("Novo valor do material: R$"))
                elif opcao == "3":
                    resposta['cavidades'] = int(input("Novas cavidades: "))
                elif opcao == "4":
                    resposta['tempo_ciclo'] = float(input("Novo tempo de ciclo: "))
                elif opcao == "5":
                    resposta['pecas_por_satelite'] = int(input("Novas peças por satélite: "))
                elif opcao == "6":
                    resposta['metalizado_ou_pintado'] = int(input("Metalizada ou Pintada (1 para Pintada, 0 para Metalizada): "))
                elif opcao == "7":
                    produto['acrescimos']['imposto'] = float(input("Novo imposto: "))
                elif opcao == "8":
                    produto['acrescimos']['frete'] = float(input("Novo frete: "))
                elif opcao == "9":
                    produto['acrescimos']['comissao'] = float(input("Nova comissão: "))
                elif opcao == "10":
                    produto['acrescimos']['lucro'] = float(input("Novo lucro: "))
                elif opcao == "11":
                    break

            # Atualizar as informações do produto
            for resposta in produto['respostas']:
                custos = calcular(resposta)
                produto['custos'] = custos
                produto['custo_total'] = custos['custo_total']
                produto['valor_total'] = custos['valor_total']

            break

    # Salvar os produtos atualizados no arquivo JSON
    with open('produtos.json', 'w') as f:
        json.dump(produtos, f, indent=4)
        
def show_info():
    with open("version.txt", "r") as file:
        current_version = file.read().strip()
    print(f"Versão atual do programa: {current_version}")

def precificar_produto():
    referencia = input("Digite a referência do produto: ")
    produtos = carregar_produtos()
    for produto in produtos:
        if produto['referencia'] == referencia:
            opcao = input("Essa referência já existe.\n\n1. Atualizar produto\n2. Excluir produto\n3. Voltar\n\nEscolha uma opção: ").upper()
            if opcao == "1":
                atualizar_produto(referencia)
                break
            elif opcao == "2":
                excluir_produto(referencia)
                return
            elif opcao == "3":
                break
    montado = None
    while montado is None:
        clear_screen()
        resposta = input("Tem mais de uma parte?\n1. Sim\n2. Não\n\nEscolha uma opção: ")
        if resposta in ['1', '2']:
            montado = resposta == '1'
        else:
            print("Resposta inválida. Por favor, digite 1 para Sim ou 2 para Não.")

    produtos = []
    respostas_result = [] 
    custos_result = []  
    if montado:
        num_partes = None
        while num_partes is None:
            clear_screen()
            resposta = int(input("\nQuantas partes o produto possui? "))
            if 2 <= resposta <= 10:
                num_partes = resposta
            else:
                print("Resposta inválida. Por favor, digite um número entre 2 e 10.")

        clear_screen()
        custo_total_produto = 0
        valor_total_produto = 0
        for i in range(num_partes):
            print(f"\nPerguntas para a parte {i+1}")
            respostas = perguntas()
            respostas_result.append(respostas)
            custos = calcular(respostas)  
            custos_result.append(custos) 
            custo_total_produto += custos['custo_total']
            valor_total_produto += custos['valor_total']
            acrescimos_result = acrescimos()
            custo_total_produto = custo_total_produto * (1 + acrescimos_result["imposto"]/100)
            custo_total_produto = custo_total_produto * (1 + acrescimos_result["frete"]/100)
            custo_total_produto = custo_total_produto * (1 + acrescimos_result["comissao"]/100)
            valor_total_produto = custo_total_produto * (1 + acrescimos_result["lucro"]/100)
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
        custo_total_produto = custos['custo_total'] * (1 + acrescimos_result["imposto"]/100)
        custo_total_produto = custo_total_produto * (1 + acrescimos_result["frete"]/100)
        custo_total_produto = custo_total_produto * (1 + acrescimos_result["comissao"]/100)
        valor_total_produto = custo_total_produto * (1 + acrescimos_result["lucro"]/100)
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
        opcao = input("Cadastro concluído com Sucesso!\n\n1. Relatório da peça\n2. Voltar ao menu\n\nEscolha uma opção: ")
        if opcao == "1":
            salvar_produto(produto)
            gerar_relatorio(produtos)
        elif opcao == "2":
            salvar_produto(produto)
            break
        
def perguntas():
    # Mapa de materiais e seus valores
    materiais = {
        "1": "PP",
        "2": "ABS",
        "3": "TPU",
        "4": "PVC"
    }

    # Mapa de valores dos materiais
    valores = {
        "PP": 12.15,
        "ABS": 13.03,
        "TPU": 33.10,
        "PVC": 15.47
    }

    # Perguntas que serão feitas para cada parte ou para o produto inteiro
    clear_screen()
    while True:
        clear_screen()
        try:
            peso = float(input("Peso (kg): ").replace(',', '.'))
            break
        except ValueError:
            print("Por favor, insira um número válido.")
    clear_screen()
    print("Material")
    for key, value in materiais.items():
        print(f"{key}. {value}")
    while True:
        material_escolhido = input("\n\nEscolha um material: ")
        if material_escolhido in materiais:
            break
        else:
            print("Por favor, escolha um material válido.")
    material = materiais[material_escolhido]
    clear_screen()
    while True:
        clear_screen()
        try:
            cavidades = int(input("Quantas cavidades: "))
            if 0 <= cavidades <= 1000:
                break
            else:
                print("Por favor, insira um número entre 0 e 1000.")
        except ValueError:
            print("Por favor, insira um número válido.")
    clear_screen()
    while True:
        clear_screen()
        try:
            tempo_ciclo = int(input("Tempo de ciclo (segundos): "))
            break
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
    clear_screen()
    while True:
        clear_screen()
        try:
            pecas_por_satelite = int(input("Peças por satélite: "))
            break
        except ValueError:
            print("Por favor, insira um número inteiro válido.")
    clear_screen()
    while True:
        clear_screen()
        metalizado_ou_pintado = int(input("Metalizado?\n1. Sim\n2. Não\n\nResposta: "))
        if metalizado_ou_pintado in [1, 2]:
            break
        else:
            print("Por favor, insira 1 para Sim ou 2 para Não.")
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
    # Perguntas sobre imposto, frete, comissão e lucro
    while True:
        imposto = input("Imposto (padrão 12%): ")
        if not imposto:
            imposto = 12.0
            break
        try:
            imposto = float(imposto)
            if 0 <= imposto <= 100:
                break
            else:
                print("Por favor, insira um número entre 0 e 100.")
        except ValueError:
            print("Por favor, insira um número válido.")
    while True:
        frete = input("Frete (padrão 5%): ")
        if not frete:
            frete = 5.0
            break
        try:
            frete = float(frete)
            if 0 <= frete <= 100:
                break
            else:
                print("Por favor, insira um número entre 0 e 100.")
        except ValueError:
            print("Por favor, insira um número válido.")
    while True:
        comissao = input("Comissão (padrão 5%): ")
        if not comissao:
            comissao = 5.0
            break
        try:
            comissao = float(comissao)
            if 0 <= comissao <= 100:
                break
            else:
                print("Por favor, insira um número entre 0 e 100.")
        except ValueError:
            print("Por favor, insira um número válido.")

    # Forçar a inserção de um lucro
    while True:
        lucro = input("Lucro (%): ")
        if lucro:
            try:
                lucro = float(lucro)
                if 0 <= lucro <= 100:
                    break
                else:
                    print("Por favor, insira um número entre 0 e 100.")
            except ValueError:
                print("Por favor, insira um número válido.")
        else:
            print("É obrigatório definir uma margem de lucro.")

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
    # Calcule quantas peças são feitas em uma hora
    pecas_por_hora = round((3600 / respostas["tempo_ciclo"]) * respostas["cavidades"], 4)

    # Calcule o custo por peça
    custo_injecao = round(100.00 / pecas_por_hora, 4)

    # Calcule o custo do material por hora
    custo_material = round(respostas["peso"] * respostas["valor_material"], 4)

    # Calcule o custo da pintura por peça
    if respostas["metalizado_ou_pintado"] == 1:
        custo_pintura = round(50 / respostas["pecas_por_satelite"], 4)
    else:
        custo_pintura = round(40 / respostas["pecas_por_satelite"], 4)

    # Defina a mão de obra como 0,04
    mao_de_obra = 0.04

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
    
def gerar_relatorio(produtos):
    while True:
        tipo_relatorio = input("\nQual tipo de relatório você deseja?\n1. Parcial\n2. Completo\n3. Voltar\n\nEscolha uma opção: ")
        if tipo_relatorio == "1":
            exibir_relatorio(produtos)
            break
        elif tipo_relatorio == "2":
            exibir_relatorio_completo(produtos)
            break
        elif tipo_relatorio == "3":
            break
        else:
            print("Por favor, escolha uma opção válida.")

def exibir_relatorio(produtos):
    clear_screen()
    for i, produto in enumerate(produtos, start=1):
        print(f"\nRelatório do Produto {produto['referencia']}")
        print("\nAcréscimos:")
        print(f"Imposto: {produto['acrescimos']['imposto']}%")
        print(f"Frete: {produto['acrescimos']['frete']}%")
        print(f"Comissão: {produto['acrescimos']['comissao']}%")
        print(f"Lucro: {produto['acrescimos']['lucro']}%")
        print("\nTotais:")
        print(f"Custo total: R${produto['custo_total']:.2f}")
        print(f"Valor total: R${produto['valor_total']:.2f}")
        for j, resposta in enumerate(produto['respostas'], start=1):
            if produto['montado']:
                print(f"\nInformações da Parte - {j}")
                print(f"Peso: {resposta['peso']} kg")
                print(f"Valor do material: R${resposta['valor_material']:.2f}")
                print(f"Cavidades: {resposta['cavidades']}")
                print(f"Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
                print(f"Peças por satélite: {resposta['pecas_por_satelite']}")
                print(f"Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 1 else 'Metalizada'}")
                print("\nTotal da Peça:")
                print(f"Custo da peça: R${resposta['custo_total']:.2f}")
                print(f"Valor da peça: R${resposta['valor_total']:.2f}")  
            else:
                print("\nInformações da Peça:")
                print(f"Peso: {resposta['peso']} kg")
                print(f"Valor do material: R${resposta['valor_material']:.2f}")
                print(f"Cavidades: {resposta['cavidades']}")
                print(f"Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
                print(f"Peças por satélite: {resposta['pecas_por_satelite']}")
                print(f"Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 1 else 'Metalizada'}")
                
    input("\nPressione Enter para continuar...")
    
def exibir_relatorio_completo(produtos):
    clear_screen()
    for i, produto in enumerate(produtos, start=1):
        print(f"\nRelatório Completo do Produto {produto['referencia']}")
        print("\nAcréscimos:")
        print(f"Imposto: {produto['acrescimos']['imposto']}%")
        print(f"Frete: {produto['acrescimos']['frete']}%")
        print(f"Comissão: {produto['acrescimos']['comissao']}%")
        print(f"Lucro: {produto['acrescimos']['lucro']}%")
        print("\nTotais:")
        print(f"Custo total: R${produto['custo_total']:.2f}")
        print(f"Valor total: R${produto['valor_total']:.2f}")
        for j, resposta in enumerate(produto['respostas'], start=1):
            if produto['montado']:
                print(f"\nInformações da Parte - {j}")
                print(f"Peso: {resposta['peso']} kg")
                print(f"Valor do material: R${resposta['valor_material']:.2f}")
                print(f"Cavidades: {resposta['cavidades']}")
                print(f"Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
                print(f"Peças por satélite: {resposta['pecas_por_satelite']}")
                print(f"Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 1 else 'Metalizada'}")
                print("\nTotal da Peça:")
                print(f"Custo da peça: R${resposta['custo_total']:.2f}")
                print(f"Valor da peça: R${resposta['valor_total']:.2f}")
                for custo in produto['custos']:
                    print("\nFormação de custos da peça:")
                    print(f"Peças por hora: {custo['pecas_por_hora']}")
                    print(f"Custo de injeção: R${custo['custo_injecao']:.2f}")
                    print(f"Custo do material: R${custo['custo_material']:.2f}")
                    print(f"Custo de pintura: R${custo['custo_pintura']:.2f}")
                    print(f"Mão de obra: R${custo['mao_de_obra']:.2f}")
            else:
                print("\nInformações:")
                print(f"Peso: {resposta['peso']} kg")
                print(f"Valor do material: R${resposta['valor_material']:.2f}")
                print(f"Cavidades: {resposta['cavidades']}")
                print(f"Tempo de ciclo: {resposta['tempo_ciclo']} segundos")
                print(f"Peças por satélite: {resposta['pecas_por_satelite']}")
                print(f"Metalizada ou Pintada: {'Pintada' if resposta['metalizado_ou_pintado'] == 1 else 'Metalizada'}")
                for custo in produto['custos']:
                    print("\nFormação de custos da peça:")
                    print(f"Peças por hora: {custo['pecas_por_hora']}")
                    print(f"Custo de injeção: R${custo['custo_injecao']:.2f}")
                    print(f"Custo do material: R${custo['custo_material']:.2f}")
                    print(f"Custo de pintura: R${custo['custo_pintura']:.2f}")
                    print(f"Mão de obra: R${custo['mao_de_obra']:.2f}")
                
    input("\nPressione Enter para continuar...")
    
menu()