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


def cadastrar_produto():
    print('Informe os dados do produto:')
    descricao = input('Qual a descrição do produto?: ').strip()
    quantidade = int(input('Qual a quantidade dele?: '))
    preco = float(input('Qual o valor da última compra dele?: '))

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
        novo = input('Digite o nome correto do produto: ').strip()
        cur.execute('UPDATE produto SET descricao = ? WHERE id = ?', (novo, id_))
    elif input_op == '2':
        novo = int(input('Digite a quantidade correta do produto: '))
        cur.execute('UPDATE produto SET quantidade = ? WHERE id = ?', (novo, id_))
    elif input_op == '3':
        novo = float(input('Digite o novo preço do produto: '))
        cur.execute('UPDATE produto SET preco = ? WHERE id = ?', (novo, id_))
    elif input_op == '0':
        print('Voltando ao menu principal...')
        return
    else:
        print('Opção inválida. Voltando ao menu principal...')
        return

    conn.commit()
    print('Produto atualizado com sucesso!')


print('Seja muito bem vindo ao sistema\n -- CONTROLE DE SUPRIMENTOS --')
nome_usuario = input('Por favor, digite seu nome: ').strip()
print(f'É um prazer ter você aqui, {nome_usuario}!')
print('Selecione algumas das opções do nosso menu abaixo: ')
print('==' * 10)
print('   SUPPLY CONTROL')
print('==' * 10)

while True:
    print(' 1 - Cadastrar Produto\n 2 - Listar Produtos\n 3 - Procurar Produto\n 4 - Editar Produto\n 0 - Sair ')
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
    elif op == '0':
        print('Até logo!')
        break
    else:
        print('Erro! Selecione novamente alguma das opções citadas acima:')