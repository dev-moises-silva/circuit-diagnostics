
# Diagnóstico de Falhas em Circuitos Lógicos

Este projeto tem como objetivo simular o comportamento de circuitos lógicos e diagnosticar possíveis falhas do tipo *stuck-at* (porta lógica presa em 0 ou 1), com base em uma Tabela Verdade defeituosa.

## ▶️ Como Executar

Certifique-se de ter o Python 3 instalado.

No terminal, execute o script principal:

```bash
python programa.py
```

## 📋 Menu de Opções

O programa apresenta um menu interativo com diferentes funcionalidades.

---

### ✅ Opção 1 – Gerar a Tabela Verdade do Circuito

O usuário deverá fornecer o **caminho de um arquivo contendo a descrição do circuito** no formato de um dicionário Python.

Em seguida, o usuário deverá informar o **nome do arquivo e o caminho** onde deseja **salvar a Tabela Verdade gerada**.

Essa funcionalidade pode ser usada tanto para gerar a Tabela Verdade correta do circuito quanto para criar uma base que poderá ser **manualmente modificada** (por exemplo, para simular defeitos) e depois reutilizada na **Opção 2**, para fins de teste.

#### 🧾 Exemplo de descrição do circuito:

```python
{
    'entradas': ['A', 'B', 'C'],
    'saidas': ['Y'], 
    'gates': ['g1', 'g2', 'g3'],
    'g1': ['nand', 'y1', 'A', 'B'],
    'g2': ['not', 'y2', 'C'],
    'g3': ['and', 'Y', 'B', 'y1', 'y2']
}
```

O programa suporta gates com as seguintes portas lógicas: **AND, NAND, OR, NOR, NOT, XOR e NXOR**

#### 💾 Exemplo de Tabela Verdade gerada:

```
A	B	C	Y
0	0	0	0
0	0	1	0
0	1	0	1
0	1	1	0
1	0	0	0
1	0	1	0
1	1	0	0
1	1	1	0
```

> Essa Tabela Verdade pode ser salva e modificada para ser usada como entrada da Opção 2, simulando defeitos manualmente.

#### ⚠️ Ordem das portas lógicas (`gates`)

A lista `'gates'` **deve seguir a ordem de execução**. Se uma porta usa a saída de outra, ela **deve vir depois**.

Exemplo correto:

```python
'gates': ['g1', 'g2', 'g3']
```

Exemplo incorreto:

```python
'gates': ['g3', 'g1', 'g2']  # ❌ g3 usa saídas ainda não definidas
```

#### 🛠️ Simulação de falhas

Para simular uma falha do tipo *stuck-at*, adicione um valor booleano ao fim da lista do gate:

- `True`: saída presa em 1
- `False`: saída presa em 0

```python
'g2': ['not', 'y2', 'C', True]
'g3': ['and', 'Y', 'B', 'y1', 'y2', False]
```

---

### ✅ Opção 2 – Diagnóstico de Falhas com Tabela Verdade Defeituosa

Nesta opção, o programa tenta descobrir quais falhas possíveis em um circuito lógico poderiam produzir uma Tabela Verdade defeituosa fornecida pelo usuário.

#### 📥 Entradas necessárias:

1. **Arquivo com a descrição do circuito** – mesmo formato de descrição de circuito usado na Opção 1.
2. **Arquivo com a Tabela Verdade defeituosa** - mesmo formato de tv gerado pela Opção 1.

> A Tabela Verdade usada aqui pode ser criada com a **Opção 1**, salva em arquivo, e depois alterada manualmente para simular falhas.

#### 🧾 Exemplo de Tabela Verdade defeituosa:

```
A	B	C	Y
0	0	0	0
0	0	1	0
0	1	0	0
0	1	1	0
1	0	0	0
1	0	1	0
1	1	0	0
1	1	1	0
```

O programa:

1. Lê o circuito e gera variações simulando falhas (preso em 0 ou 1).
2. Compara com a Tabela Verdade defeituosa fornecida.
3. Informa quais falhas poderiam explicar o comportamento observado.

#### ✅ Saída esperada:

```
Falhas possíveis que geram a Tabela Verdade defeituosa:
- g3 preso em 0
- g2 preso em 0
```

---

## ✅ Requisitos

- Python 3.x
- Nenhuma biblioteca externa necessária (usa apenas a biblioteca padrão do Python)

## 📄 Licença

Este projeto é de uso livre para fins acadêmicos e educacionais.
