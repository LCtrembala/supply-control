import sqlite3

conn = sqlite3.connect('suprimentos.db')
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL,
        ativo INTEGER NOT NULL DEFAULT 1
    )
''')
conn.commit()


def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print('Erro: este campo não pode ficar vazio.')


def ler_inteiro(mensagem, minimo=0):
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print('Erro: digite um número inteiro (ex.: 10).')
            continue
        if valor < minimo:
            print(f'Erro: o valor deve ser no mínimo {minimo}.')
            continue
        return valor


def ler_decimal(mensagem, minimo=0):
    while True:
        try:
            valor = float(input(mensagem).replace(',', '.'))
        except ValueError:
            print('Erro: digite um número válido (ex.: 12.50).')
            continue
        if valor < minimo:
            print(f'Erro: o valor deve ser no mínimo {minimo}.')
            continue
        return valor


def cadastrar_produto():
    print('Informe os dados do produto:')
    descricao = ler_texto('Qual a descrição do produto?: ')
    quantidade = ler_inteiro('Qual a quantidade dele?: ')
    preco = ler_decimal('Qual o valor da última compra dele?: ')

    cur.execute(
        'INSERT INTO produto (descricao, quantidade, preco) VALUES (?, ?, ?)',
        (descricao, quantidade, preco)
    )
    conn.commit()

    codigo = f'COD-{cur.lastrowid:03d}'
    print(f'Produto cadastrado com sucesso!\nCódigo: {codigo}\nDescrição: {descricao}\nQuantidade: {quantidade}\nÚltimo preço: {preco}')


def listar_produtos():
    cur.execute('SELECT id, descricao, quantidade, preco FROM produto WHERE ativo = 1')
    produtos = cur.fetchall()
    if not produtos:
        print('Nenhum produto cadastrado...')
    else:
        print('Lista de produtos cadastrados:')
        for id_, descricao, quantidade, preco in produtos:
            print(f'ID: COD-{id_:03d} | Nome: {descricao} | Qtd: {quantidade} | Preço: {preco}')


def procurar_codigo():
    codigo = input('Digite o código do produto: ').strip().upper().replace('COD-', '')
    if not codigo.isdigit():
        return None
    cur.execute(
        'SELECT id, descricao, quantidade, preco FROM produto WHERE id = ? AND ativo = 1',
        (int(codigo),)
    )
    return cur.fetchone()  # devolve (id, descricao, quantidade, preco) ou None


def editar_produto():
    resultado = procurar_codigo()
    if not resultado:
        print('Produto não encontrado!')
        return

    id_, descricao, quantidade, preco = resultado
    print(f'Produto localizado -- ID: COD-{id_:03d} | Nome: {descricao} | Qtd: {quantidade} | Preço: {preco}')
    print('Editar produto:\n 1 - Nome\n 2 - Quantidade\n 3 - Preço\n 0 - Voltar')
    input_op = input('Selecione a opção que deseja editar: ').strip()

    if input_op == '1':
        novo = ler_texto('Digite o nome correto do produto: ')
        cur.execute('UPDATE produto SET descricao = ? WHERE id = ?', (novo, id_))
    elif input_op == '2':
        novo = ler_inteiro('Digite a quantidade correta do produto: ')
        cur.execute('UPDATE produto SET quantidade = ? WHERE id = ?', (novo, id_))
    elif input_op == '3':
        novo = ler_decimal('Digite o novo preço do produto: ')
        cur.execute('UPDATE produto SET preco = ? WHERE id = ?', (novo, id_))
    elif input_op == '0':
        print('Voltando ao menu principal...')
        return
    else:
        print('Opção inválida. Voltando ao menu principal...')
        return

    conn.commit()
    print('Produto atualizado com sucesso!')


def excluir_produto():
    resultado = procurar_codigo()
    if not resultado:
        print('Produto não encontrado!')
        return

    id_, descricao, quantidade, preco = resultado
    print(f'Produto localizado -- ID: COD-{id_:03d} | Nome: {descricao} | Qtd: {quantidade} | Preço: {preco}')
    confirma = input('Deseja realmente excluir este produto? (s/n): ').strip().lower()

    if confirma == 's':
        cur.execute('UPDATE produto SET ativo = 0 WHERE id = ?', (id_,))
        conn.commit()
        print('Produto excluído com sucesso!')
    else:
        print('Operação cancelada.')


print('Seja muito bem vindo ao sistema\n -- CONTROLE DE SUPRIMENTOS --')
nome_usuario = input('Por favor, digite seu nome: ').strip()
print(f'É um prazer ter você aqui, {nome_usuario}!')
print('Selecione algumas das opções do nosso menu abaixo: ')
print('==' * 10)
print('   SUPPLY CONTROL')
print('==' * 10)

while True:
    print(' 1 - Cadastrar Produto\n 2 - Listar Produtos\n 3 - Procurar Produto\n 4 - Editar Produto\n 5 - Excluir Produto\n 0 - Sair ')
    op = input("Digite uma opção: ").strip()

    if op == "1":
        cadastrar_produto()
    elif op == '2':
        listar_produtos()
    elif op == '3':
        resultado = procurar_codigo()
        if resultado:
            print(f'Produto encontrado: ID: COD-{resultado[0]:03d} | Nome: {resultado[1]} | Qtd: {resultado[2]} | Preço: {resultado[3]}')
        else:
            print('Produto não encontrado!')
    elif op == '4':
        editar_produto()
    elif op == '5':
        excluir_produto()
    elif op == '0':
        print('Até logo!')
        break
    else:
        print('Erro! Selecione novamente alguma das opções citadas acima:')