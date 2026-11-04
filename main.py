produto = [] #lista vazia chamada produto, que vai armazenar os produtos cadastrados

def gerar_codigo():
    # usa o tamanho atual da lista para gerar o próximo código
    return f'COD-{len(produto) + 1:03d}'


def cadastrar_produto(): #Define uma função chamada cadastrar_produto, responsável por cadastrar um novo produto.
    print('Informe os dados do produto:')
    nome_produto = input('Qual descrição do produto?: ')
    quantidade = int(input('Qual quantidade dele?: '))
    preco = float(input('Qual valor da ultima compra dele?: '))

    codigo = gerar_codigo()  # gera o código antes de salvar
    produto.append([codigo, nome_produto, quantidade, preco])#Adiciona os dados do produto dentro da lista produto

    print(f'Produto cadastrado com sucesso!!\nCódigo: {codigo}\nDescrição: {nome_produto}\nQuantidade: {quantidade}\nUltimo preço: {preco} ')
    print(f'o {nome_produto} foi cadastrado com sucesso! Deseja adicionar outro?')


def listar_produtos():
    if len(produto) == 0:
        print('Nenhum produto cadastrado...')
    else:
        print('Lista de produtos cadastrados:')
        for codigo, nome, quantidade, preco in produto: #Percorre cada produto armazenado na lista produto e separa seus três valores nas variáveis nome, quantidade e preco
            print(f'ID: {codigo} | Nome: {nome} | Qtd: {quantidade} | Preço: {preco}')

def procurar_codigo():
    codigo = input('Digite o código do produto: ').strip()
    if codigo.isdigit():
        codigo = f'COD-{int(codigo):03d}'  # Formata o código para o padrão COD-xxx
    for item in produto:
        if item[0] == codigo:
            return item
    return None

def editar_produto():
    resultado = procurar_codigo()
    if resultado:
        print(f'Produto localizado -- ID: {resultado[0]} | Nome: {resultado[1]} | Qtd: {resultado[2]} | Preço: {resultado[3]}')
        print(f'Editar produto:\n 1 - Nome\n 2 - Quantidade\n 3 - Preço\n 0 - Voltar')
        input_op = input('Selecione a opção que deseja editar: ').strip()
        if input_op == '1':
            nome_novo = input('Digite o nome correto do produto:')
            resultado[1] = nome_novo
            print(f'Produto atualizado! \n ID: {resultado[0]} | Nome: {resultado[1]} | Qtd: {resultado[2]} | Preço: {resultado[3]}')
        elif input_op == '2':
            quantidade_nova = int(input('Digite a quantidade correta do produto:'))
            resultado[2] = quantidade_nova
            print(f'Produto atualizado! \n ID: {resultado[0]} | Nome: {resultado[1]} | Qtd: {resultado[2]} | Preço: {resultado[3]}')
        elif input_op == '3':
            preco_novo = float(input('Digite o novo preço do produto:'))
            resultado[3] = preco_novo
            print(f'Produto atualizado! \n ID: {resultado[0]} | Nome: {resultado[1]} | Qtd: {resultado[2]} | Preço: {resultado[3]}')
        elif input_op == '0':
            print('Voltando ao menu principal...')
        else:
            print('Opção inválida. Voltando ao menu principal...')
    
print('Seja muito bem vindo ao sistema\n -- CONTROLE DE SUPRIMENTOS --')
#espaço
nome_usuario=input('Por favor, digite seu nome: ').strip() 
#espaço
print(f'É um prazer ter você aqui, {nome_usuario}!')
#espaço
print('Selecione algumas das opções do nosso menu abaixo: ')
#espaço
print('=='*10)
print('   SUPPLY CONTROL')
print('=='*10)
#espaço
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
            print(f'Produto encontrado: ID: {resultado[0]} | Nome: {resultado[1]} | Qtd: {resultado[2]} | Preço: {resultado[3]}')
        else:
            print('Produto não encontrado!')
    elif op == '4':
        editar_produto()
    elif op == '0':
        print('Até logo!')
        break  # sai do loop
    else:
        print('Erro! Selecione novamente alguma das opções citadas acima:')