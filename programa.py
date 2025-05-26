import os
import platform
import time
import ast

def main():
    limpar_terminal()

    while True:
        print("🔧 Bem-vindo ao Programa de Diagnóstico de Falhas em Circuitos Lógicos 🔧\n")
        print("Escolha uma das opções abaixo:\n")
        print("  0 - ❌ Sair do programa")
        print("  1 - 🧮 Gerar Tabela Verdade de um Circuito")
        print("  2 - 🩺 Diagnosticar Falhas com Tabela Verdade Defeituosa\n")

        opcao = input("Digite o número da opção desejada: ")

        match opcao:
            case '0':
                print('\nTerminando programa.', end='')
                for i in range(2):
                    time.sleep(1)
                    print('.', end='')
                time.sleep(1)
                limpar_terminal()
                break
            case '1':
                try:
                    caminho_do_circuito = input('\nInsira o caminho para o arquivo com a descrição do circuito: ')
                    if not verificar_circuito(caminho_do_circuito):
                        raise ValueError('Descrição do circuito inválida')
                    
                    circuito = eval(open(caminho_do_circuito).read())
                    tv = obter_tv(circuito)

                    caminho_da_tv = input('Insira o caminho onde será salvo a tv: ')
                    salvar_tv(caminho_da_tv, tv)

                    print('TV salva em ' + caminho_da_tv, end='')
                except FileNotFoundError:
                    print('Arquivo não encontrado', end='')
                except ValueError as e:
                    print(e, end='')
            case '2':
                try:
                    caminho_da_tv = input('\nInsira o caminho para a tv defeituosa: ')
                    tv_defeituosa = recuperar_tv(caminho_da_tv)

                    caminho_do_circuito = input('Insira o caminho do circuito: ')

                    if not verificar_circuito(caminho_do_circuito):
                        raise ValueError('Circuito inválido')
                    
                    circuito = eval(open(caminho_do_circuito).read())
                    
                    variacoes_correspondentes = obter_variacoes_correspondentes(circuito, tv_defeituosa)

                    if len(variacoes_correspondentes) > 0:
                        print('\nPossíveis falhas que geram a Tabela Verdade defeituosa: ')
                        for indice, cod_variacao in enumerate(variacoes_correspondentes):
                            print('- ' +  obter_descricao_da_falha(cod_variacao, circuito['gates']))
                    else:
                        print('Essa tv não pode ser desse circuito', end='')
                except ValueError as e:
                    print(e, end='')
                except FileNotFoundError:
                    print('Arquivo não encontrado', end='')
            case _:
                print('Opção inválida', end='')
        
        input()
        limpar_terminal()

def limpar_terminal():
    os.system("cls" if platform.system() == "Windows" else "clear") 

def obter_tv(circuito):
    entradas_e_saidas = circuito['entradas'] + circuito['saidas']
    tv = {}

    for sinal in entradas_e_saidas:
        tv[sinal] = []

    for i in range(2 ** len(circuito['entradas'])):
        todos_os_sinais = obter_entradas(circuito['entradas'], i)
        
        for gate in circuito['gates']:
            gate_info = circuito[gate]

            if isinstance(gate_info[-1], bool):
                todos_os_sinais[gate_info[1]] = gate_info[-1]
            else:
                entradas_do_gate = []
                for nome_da_entrada in gate_info[2:]:
                    if not nome_da_entrada in todos_os_sinais:
                        raise ValueError(f'{nome_da_entrada} não existi antes da execução de {gate}')
                    
                    entradas_do_gate.append(todos_os_sinais[nome_da_entrada])

                todos_os_sinais[gate_info[1]] = calcular_saida(gate_info[0], entradas_do_gate)
            
        for sinal in entradas_e_saidas:
            if not sinal in todos_os_sinais:
                raise ValueError(f'Nenhum valor foi atribuido a {sinal}')
            
            tv[sinal].append(todos_os_sinais[sinal])

    return tv

def obter_entradas(entradas, numero_da_linha):
    binario = bin(numero_da_linha)[2:]

    binario = binario.rjust(len(entradas), '0')

    valores_das_entradas = {}

    for i in range(len(entradas)):
        valores_das_entradas[entradas[i]] = binario[i] == '1'

    return valores_das_entradas

def calcular_saida(operacao, entradas):
    match operacao.lower():
        case 'and':
            if len(entradas) < 2:
                raise ValueError('Quatidade de entradas não suportada na operação AND')
            return all(entradas)
        case 'or':
            if len(entradas) < 2:
                raise ValueError('Quatidade de entradas não suportada na operação OR')
            return any(entradas)
        case 'not':
            if len(entradas) != 1:
                raise ValueError('Quatidade de entradas não suportada na operação NOT')
            return not entradas[0]
        case 'nand':
            if len(entradas) < 2:
                raise ValueError('Quatidade de entradas não suportada na operação NAND')
            return not all(entradas)
        case 'nor':
            if len(entradas) < 2:
                raise ValueError('Quatidade de entradas não suportada na operação NOR')
            return not any(entradas)
        case 'xor':
            if len(entradas) < 2:
                raise ValueError('Quatidade de entradas não suportada na operação XOR')
            return (not entradas[0] and entradas[1] or entradas[0] and not entradas[1])
        case 'xnor':
            if len(entradas) != 2:
                raise ValueError('Quatidade de entradas não suportada na operação XNOR')
            return (not entradas[0] and not entradas[1] or all(entradas))
        case _:
            raise ValueError(f'{operacao} não é uma operação válida')

def salvar_tv(nome_do_arquivo, tv):
    chaves = list(tv.keys())
    cabecalho = '\t'.join(chaves) + '\n'
    
    arquivo = open(nome_do_arquivo, 'w')
    arquivo.write(cabecalho)

    linhas = list(zip(*tv.values()))
    for linha in linhas:
        arquivo.write('\t'.join(('1' if valor else '0') for valor in linha) + '\n')
    
    arquivo.close()

def recuperar_tv(caminho_da_tv):
    arquivo = open(caminho_da_tv)
    entradas_e_saidas = arquivo.readline().split()

    if len(entradas_e_saidas) < 2:
        raise ValueError('TV inválida')
    
    tv = {}

    for sinal in entradas_e_saidas:
        tv[sinal] = []

    for linha in arquivo:
        sinais = linha.split()

        if len(sinais) != len(entradas_e_saidas):
            raise ValueError('TV inválida')
        
        for i in range(len(entradas_e_saidas)):
            if not sinais[i] in ('1', '0'):
                raise ValueError('TV inválida')

            tv[entradas_e_saidas[i]].append(sinais[i] == '1')
    
    arquivo.close()

    return tv
  
def obter_variacao_do_circuito(circuito, codigo):
    gates = circuito['gates']

    ternario = tern(codigo)
    ternario = ternario.rjust(len(gates), '0')

    for i, nome_do_gate in enumerate(gates):
        if isinstance(circuito[nome_do_gate][-1], bool):
            match ternario[i]:
                case '0':
                    circuito[nome_do_gate].pop()
                case '1':
                    circuito[nome_do_gate][-1] = False
                case '2':
                    circuito[nome_do_gate][-1] = True
        else:
            if ternario[i] != '0':
                circuito[nome_do_gate].append(ternario[i] == '2')
        
    return circuito

def tern(num):
    if num == 0:
        return '0'
    
    ternario = ''

    while num > 0:
        ternario = str(num % 3) + ternario
        num = int(num / 3)

    return ternario

def obter_variacoes_correspondentes(circuito, tv):
    variacoes_correspondentes = []

    for cod in range(3 ** len(circuito['gates'])):
        if tv == obter_tv(obter_variacao_do_circuito(circuito, cod)):
            variacoes_correspondentes.append(cod)

    return variacoes_correspondentes

def obter_descricao_da_falha(codigo, gates):
    descricao = ''

    if codigo == 0:
        return 'circuito sadio'
    
    ternario = tern(codigo)
    ternario = ternario.rjust(len(gates), '0')

    descricao = ''

    for i, nome_do_gate in enumerate(gates):
        if ternario[i] != '0':
            descricao = descricao + f'{nome_do_gate} preso em {int(ternario[i]) - 1}, '

    descricao = descricao[:-2]
    descricao = ' e'.join(descricao.rsplit(',', 1))

    return descricao

def verificar_circuito(caminho_arquivo):
    try:
        with open(caminho_arquivo) as arquivo:
        
            circuito = ast.literal_eval(arquivo.read())
            arquivo.close()

            if not isinstance(circuito, dict):
                return False
            
            chaves_obrg = ['entradas', 'saidas', 'gates']

            if not all(chave in circuito for chave in chaves_obrg):
                return False
            
            if not all(gate in circuito for gate in circuito['gates']):
                return False
            
            return True

    except (SyntaxError, ValueError):
        return False

if __name__ == '__main__':
    main()
