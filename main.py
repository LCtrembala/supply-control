import sqlite3

conn = sqlite3.connect('suprimentos.db')
conn.execute('PRAGMA foreign_keys = ON')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS categoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS fornecedor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT NOT NULL
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS produto (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco REAL NOT NULL,
        ativo INTEGER NOT NULL DEFAULT 1,
        categoria_id INTEGER,
        fornecedor_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categoria(id),
        FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id)
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS movimentacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('ENTRADA', 'SAIDA')),
        quantidade INTEGER NOT NULL CHECK (quantidade > 0),
        data_hora TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
        observacao TEXT,
        FOREIGN KEY (produto_id) REFERENCES produto(id)
    )
''')
conn.commit()


# leitura com validação

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
        texto = input(mensagem).strip()
        if ',' in texto:
            texto = texto.replace('.', '').replace(',', '.')
        try:
            valor = float(texto)
        except ValueError:
            print('Erro: digite um número válido (ex.: 12,50).')
            continue
        if valor < minimo:
            print(f'Erro: o valor deve ser no mínimo {minimo}.')
            continue
        return valor


# categoria

def cadastrar_categoria():
    nome = ler_texto('Nome da categoria: ')
    try:
        cur.execute('INSERT INTO categoria (nome) VALUES (?)', (nome,))
        conn.commit()
        print('Categoria cadastrada com sucesso!')
    except sqlite3.IntegrityError:
        print('Erro: já existe uma categoria com esse nome.')


def listar_categorias():
    cur.execute('SELECT id, nome FROM categoria ORDER BY nome')
    categorias = cur.fetchall()
    if not categorias:
        print('Nenhuma categoria cadastrada...')
    else:
        print('Categorias cadastradas:')
        for id_, nome in categorias:
            print(f'ID: {id_} | Nome: {nome}')


def escolher_categoria():
    cur.execute('SELECT id, nome FROM categoria ORDER BY nome')
    categorias = cur.fetchall()
    if not categorias:
        print('(Nenhuma categoria cadastrada, o produto ficará sem categoria.)')
        return None
    print('Categorias disponíveis:')
    for id_, nome in categorias:
        print(f' {id_} - {nome}')
    ids_validos = [c[0] for c in categorias]
    while True:
        escolha = ler_inteiro('Digite o ID da categoria (0 para nenhuma): ')
        if escolha == 0:
            return None
        if escolha in ids_validos:
            return escolha
        print('Erro: ID inexistente.')


# fornecedor

def cadastrar_fornecedor():
    nome = ler_texto('Nome do fornecedor: ')
    telefone = ler_texto('Telefone do fornecedor: ')
    cur.execute(
        'INSERT INTO fornecedor (nome, telefone) VALUES (?, ?)',
        (nome, telefone)
    )
    conn.commit()
    print('Fornecedor cadastrado com sucesso!')


def listar_fornecedores():
    cur.execute('SELECT id, nome, telefone FROM fornecedor ORDER BY nome')
    fornecedores = cur.fetchall()
    if not fornecedores:
        print('Nenhum fornecedor cadastrado...')
    else:
        print('Fornecedores cadastrados:')
        for id_, nome, telefone in fornecedores:
            print(f'ID: {id_} | Nome: {nome} | Telefone: {telefone}')


def escolher_fornecedor():
    cur.execute('SELECT id, nome FROM fornecedor ORDER BY nome')
    fornecedores = cur.fetchall()
    if not fornecedores:
        print('(Nenhum fornecedor cadastrado, o produto ficará sem fornecedor.)')
        return None
    print('Fornecedores disponíveis:')
    for id_, nome in fornecedores:
        print(f' {id_} - {nome}')
    ids_validos = [f[0] for f in fornecedores]
    while True:
        escolha = ler_inteiro('Digite o ID do fornecedor (0 para nenhum): ')
        if escolha == 0:
            return None
        if escolha in ids_validos:
            return escolha
        print('Erro: ID inexistente.')


# produto

def cadastrar_produto():
    print('Informe os dados do produto:')
    descricao = ler_texto('Qual a descrição do produto?: ')
    quantidade = ler_inteiro('Qual a quantidade dele?: ')
    preco = ler_decimal('Qual o valor da última compra dele?: ')
    categoria_id = escolher_categoria()
    fornecedor_id = escolher_fornecedor()

    cur.execute(
        '''INSERT INTO produto (descricao, quantidade, preco, categoria_id, fornecedor_id)
           VALUES (?, ?, ?, ?, ?)''',
        (descricao, quantidade, preco, categoria_id, fornecedor_id)
    )
    produto_id = cur.lastrowid

    if quantidade > 0:
        cur.execute(
            'INSERT INTO movimentacao (produto_id, tipo, quantidade, observacao) VALUES (?, ?, ?, ?)',
            (produto_id, 'ENTRADA', quantidade, 'Estoque inicial')
        )
    conn.commit()

    codigo = f'COD-{produto_id:03d}'
    print(f'Produto cadastrado com sucesso!\nCódigo: {codigo}\nDescrição: {descricao}\nQuantidade: {quantidade}\nÚltimo preço: {preco}')


def listar_produtos():
    cur.execute('''
        SELECT p.id, p.descricao, p.quantidade, p.preco,
               COALESCE(c.nome, 'Sem categoria'),
               COALESCE(f.nome, 'Sem fornecedor')
        FROM produto p
        LEFT JOIN categoria c ON c.id = p.categoria_id
        LEFT JOIN fornecedor f ON f.id = p.fornecedor_id
        WHERE p.ativo = 1
    ''')
    produtos = cur.fetchall()
    if not produtos:
        print('Nenhum produto cadastrado...')
    else:
        print('Lista de produtos cadastrados:')
        for id_, descricao, quantidade, preco, categoria, fornecedor in produtos:
            print(f'ID: COD-{id_:03d} | Nome: {descricao} | Qtd: {quantidade} | Preço: {preco} | Categoria: {categoria} | Fornecedor: {fornecedor}')


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
    print('Editar produto:\n 1 - Nome\n 2 - Preço\n 3 - Categoria\n 4 - Fornecedor\n 0 - Voltar')
    print('(Para alterar a quantidade, use o menu Estoque.)')
    input_op = input('Selecione a opção que deseja editar: ').strip()

    if input_op == '1':
        novo = ler_texto('Digite o nome correto do produto: ')
        cur.execute('UPDATE produto SET descricao = ? WHERE id = ?', (novo, id_))
    elif input_op == '2':
        novo = ler_decimal('Digite o novo preço do produto: ')
        cur.execute('UPDATE produto SET preco = ? WHERE id = ?', (novo, id_))
    elif input_op == '3':
        novo = escolher_categoria()
        cur.execute('UPDATE produto SET categoria_id = ? WHERE id = ?', (novo, id_))
    elif input_op == '4':
        novo = escolher_fornecedor()
        cur.execute('UPDATE produto SET fornecedor_id = ? WHERE id = ?', (novo, id_))
    elif input_op == '0':
        print('Voltando ao menu...')
        return
    else:
        print('Opção inválida. Voltando ao menu...')
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


# estoque

def registrar_movimentacao():
    resultado = procurar_codigo()
    if not resultado:
        print('Produto não encontrado!')
        return

    id_, descricao, quantidade_atual, preco = resultado
    print(f'Produto localizado -- ID: COD-{id_:03d} | Nome: {descricao} | Estoque atual: {quantidade_atual}')
    print('Tipo de movimentação:\n 1 - Entrada\n 2 - Saída\n 0 - Voltar')
    escolha = input('Selecione uma opção: ').strip()

    if escolha == '1':
        tipo = 'ENTRADA'
    elif escolha == '2':
        tipo = 'SAIDA'
    elif escolha == '0':
        print('Voltando ao menu...')
        return
    else:
        print('Opção inválida. Voltando ao menu...')
        return

    quantidade = ler_inteiro('Quantidade: ', minimo=1)

    if tipo == 'SAIDA' and quantidade > quantidade_atual:
        print(f'Erro: estoque insuficiente. Disponível: {quantidade_atual}')
        return

    if tipo == 'ENTRADA':
        novo_saldo = quantidade_atual + quantidade
    else:
        novo_saldo = quantidade_atual - quantidade

    observacao = input('Observação (opcional): ').strip() or None

    cur.execute('UPDATE produto SET quantidade = ? WHERE id = ?', (novo_saldo, id_))
    cur.execute(
        'INSERT INTO movimentacao (produto_id, tipo, quantidade, observacao) VALUES (?, ?, ?, ?)',
        (id_, tipo, quantidade, observacao)
    )
    conn.commit()
    print(f'Movimentação registrada! Novo estoque de {descricao}: {novo_saldo}')


def historico_movimentacoes():
    resultado = procurar_codigo()
    if not resultado:
        print('Produto não encontrado!')
        return

    id_, descricao, quantidade, preco = resultado
    cur.execute('''
        SELECT data_hora, tipo, quantidade, COALESCE(observacao, '-')
        FROM movimentacao
        WHERE produto_id = ?
        ORDER BY id DESC
    ''', (id_,))
    movimentos = cur.fetchall()

    print(f'Histórico de COD-{id_:03d} - {descricao} (estoque atual: {quantidade})')
    if not movimentos:
        print('Nenhuma movimentação registrada.')
    else:
        for data_hora, tipo, qtd, obs in movimentos:
            print(f'{data_hora} | {tipo} | Qtd: {qtd} | Obs: {obs}')


# menus

def menu_produtos():
    while True:
        print('\n--- PRODUTOS ---')
        print(' 1 - Cadastrar Produto\n 2 - Listar Produtos\n 3 - Procurar Produto\n 4 - Editar Produto\n 5 - Excluir Produto\n 0 - Voltar')
        op = input('Digite uma opção: ').strip()

        if op == '1':
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
            break
        else:
            print('Erro! Selecione novamente alguma das opções citadas acima:')


def menu_categorias():
    while True:
        print('\n--- CATEGORIAS ---')
        print(' 1 - Cadastrar Categoria\n 2 - Listar Categorias\n 0 - Voltar')
        op = input('Digite uma opção: ').strip()

        if op == '1':
            cadastrar_categoria()
        elif op == '2':
            listar_categorias()
        elif op == '0':
            break
        else:
            print('Erro! Selecione novamente alguma das opções citadas acima:')


def menu_fornecedores():
    while True:
        print('\n--- FORNECEDORES ---')
        print(' 1 - Cadastrar Fornecedor\n 2 - Listar Fornecedores\n 0 - Voltar')
        op = input('Digite uma opção: ').strip()

        if op == '1':
            cadastrar_fornecedor()
        elif op == '2':
            listar_fornecedores()
        elif op == '0':
            break
        else:
            print('Erro! Selecione novamente alguma das opções citadas acima:')


def menu_estoque():
    while True:
        print('\n--- ESTOQUE ---')
        print(' 1 - Registrar Entrada/Saída\n 2 - Ver Histórico de um Produto\n 0 - Voltar')
        op = input('Digite uma opção: ').strip()

        if op == '1':
            registrar_movimentacao()
        elif op == '2':
            historico_movimentacoes()
        elif op == '0':
            break
        else:
            print('Erro! Selecione novamente alguma das opções citadas acima:')


# programa principal

print('Seja muito bem vindo ao sistema\n -- CONTROLE DE SUPRIMENTOS --')
nome_usuario = input('Por favor, digite seu nome: ').strip()
print(f'É um prazer ter você aqui, {nome_usuario}!')
print('==' * 10)
print('   SUPPLY CONTROL')
print('==' * 10)

while True:
    print('\n--- MENU PRINCIPAL ---')
    print(' 1 - Produtos\n 2 - Categorias\n 3 - Fornecedores\n 4 - Estoque\n 0 - Sair')
    op = input('Digite uma opção: ').strip()

    if op == '1':
        menu_produtos()
    elif op == '2':
        menu_categorias()
    elif op == '3':
        menu_fornecedores()
    elif op == '4':
        menu_estoque()
    elif op == '0':
        print('Até logo!')
        break
    else:
        print('Erro! Selecione novamente alguma das opções citadas acima:')