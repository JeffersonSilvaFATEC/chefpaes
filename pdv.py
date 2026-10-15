import mysql.connector
import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chefpaes" #nome do banco de dados

)

# print("Conexão bem-sucedida ao banco de dados!", conn.is_connected()) mensagem de conexão
cursor = conn.cursor()
cursor.execute("SELECT * FROM produtos") #seleciona todos os produtos do banco de dados
produtos = cursor.fetchall() #armazena os resultados da consulta em uma variável

print("\n--- PRODUTOS ---")

for produto in produtos:
    id_, nome, categoria_id, preco, estoque = produto
    print(f"{id_} - {nome} |  Preço: R$ {preco:.2f} - Estoque: {estoque}")

# entrada = input("\nDigite o ID do produto: ")

# cursor = conn.cursor()
# cursor.execute("SELECT * FROM produtos WHERE id = %s", (entrada,))
# produto = cursor.fetchone()
# cursor.close()

# if produto is None:
#     print("Produto não encontrado.")
# else:
#     id_, nome, categoria_id, preco, estoque = produto
#     print(f"\nProduto selecionado: {nome} | Preço: R$ {preco:.2f} - Estoque: {estoque}")



#cadastrando o produto pelo menu, caso o produto não esteja
# cadastrado no banco de dados,
# o atendente pode cadastrar o produto antes de finalizar a venda

def cadastrar_produto(conn):
    print("\n--- CADASTRAR PRODUTO ---")
    nome = input("Nome do produto: ").strip()
    if nome == "":
        print("Nome do produto não pode ser vazio.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    print("\n--- CATEGORIAS ---")
    for categoria in categorias:
        print(categoria)


    try:
        categoria_id = int(input("ID da categoria: "))
        preco = float(input("Preço do produto (ex: 6.99): ").replace(",", "."))
        estoque = int(input("Quantidade inicial: "))

    except ValueError:
        print("Entrada inválida. Certifique-se de digitar números válidos para categoria, preço e estoque.")
        cursor.close()
        return


    if preco < 0 or estoque < 0:
        print("Preço e estoque não podem ser negativos.")
        cursor.close()
        return

    try:
        cursor.execute(
            "INSERT INTO produtos (nome, categoria_id, preco, estoque) VALUES (%s, %s, %s, %s)",
            (nome, categoria_id, preco, estoque)

        )
        conn.commit()
        print(f"Produto '{nome}' cadastrado com ID {cursor.lastrowid} com sucesso!")
    except mysql.connector.Error as erro:
        conn.rollback()
        print(f"Erro ao cadastrar o produto: {erro}")
    finally:
        cursor.close()

#alterando o preço e estoque
def alterar_produto(conn):
    print("\n--- ALTERAR PRODUTO ---")
    entrada = input("Digite o ID do produto que deseja alterar: ").strip()
    if not entrada.isdigit():
        print("ID do produto inválido.")
        return

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (int(entrada),))
        produto = cursor.fetchone()
        if produto is None:
            print("Produto não encontrado.")
            return

        id_produto, nome, categoria_id, preco_atual, estoque_atual = produto
        print(
            f"Produto selecionado: {nome} | Preço: R$ {preco_atual:.2f} "
            f"\n- Estoque: {estoque_atual}"
        )
        try:
            preco = float(input("Novo preço (ex: 5.60): ").replace(",", "."))
            estoque = int(input("Novo estoque: "))
            print(f"Novo preço: {preco:.2f}, Novo estoque: {estoque}")
        except ValueError:
            print("Entrada inválida. Digite um preço e um estoque válidos.")
            return

        if preco <= 0 or estoque < 0:
            print("Preço e estoque não podem ser negativos.")
            return

        cursor.execute(
            "UPDATE produtos SET preco = %s, estoque = %s WHERE id = %s",
            (preco, estoque, id_produto)
        )
        conn.commit()
        print(f"Produto '{nome}' alterado com sucesso!")
    except mysql.connector.Error as erro:
        conn.rollback()
        print(f"Erro ao alterar o produto: {erro}")
    finally:
        cursor.close()

def nova_venda(conn):

    carrinho = []
    total = 0

    while True:
        entrada = input("\nDigite o ID do produto (ENTER finalizar): ")
        if entrada == "":
            break
        #arrumando erros de digitação na hora da venda, caso o
        # usuário digite letras ou caracteres especiais, o programa 
        # não quebra e pede para digitar novamente
        if not entrada.isdigit():
            print("Digite apenas o número do ID.")
            continue
        
        

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (entrada,))
        produto = cursor.fetchone()
        cursor.close()

    #Volta para o inicio do loop, evitando adicionar um produto inexistente ao carrinho

        if produto is None:
            print("Produto não encontrado.")
            continue
        id_, nome, categoria_id, preco, estoque = produto

    #bloqueando produto repetido no carrinho
        ja_no_carrinho = False
        for item in carrinho:
            if item[0] == id_:
                ja_no_carrinho = True

        if ja_no_carrinho:
            print("O produto já está no carrinho.")
            continue
        #Validando a quantidade digitada pelo atendente
        try:
            quantidade = int(input(f"Quantidade de {nome}: "))
        except ValueError:
            print("Quantidade inválida. Digite apenas números.")
            continue
        #volta para o ID, sem adicionar o produto ao carrinho

        if quantidade <= 0:
            print("A quantidade precisa ser maior que zero.")
            continue

        if quantidade > estoque:
            print(f"Quantidade indisponível. Estoque atual: {estoque}")
            continue

        carrinho.append((id_, nome, quantidade, preco))
        total += preco * quantidade
        print(f"Adicionado! Total parcial: R$ {total:.2f}")

    print("\n--- CARRINHO ---")
    for id_, nome, quantidade, preco in carrinho:
        print(f"{quantidade}x {nome} - R$ {preco * quantidade:.2f}")
    print(f"\nTotal a pagar: R$ {total:.2f}")

    print("Itens no carrinho:", len(carrinho))

    if carrinho:
        confirmar = input("\nConfirmar a venda? (s/n): ")

        if confirmar.lower() == "s":
            #criando o cursor para conectar ao banco de dados
            cursor = conn.cursor()

            try:
                cursor.execute(
                    "INSERT INTO pedidos (data_pedido, valor_total) VALUES (NOW(), %s)",
                    (total,)
                )
                pedido_id = cursor.lastrowid

            #executando o comando SQL para inserir a venda na tabela de vendas
            #mostra o ID do pedido gerado automaticamente pelo banco de dados
            #é usado para ligar cada item ao pedido certo


                for id_, nome, quantidade, preco in carrinho:
                    cursor.execute(
                        "INSERT INTO itens_pedido(pedido_id, produto_id, quantidade, preco_unitario)"
                        "VALUES (%s, %s, %s, %s)",
                    (pedido_id, id_, quantidade, preco)
                )
                    #baixando o estoque do produto após a venda
                    cursor.execute(
                            "UPDATE produtos SET estoque = estoque - %s WHERE id = %s",
                            (quantidade, id_)
                    )
                    print(f"Baixou {quantidade} itens do produto {id_}")

                conn.commit() #confirmando/salvando a transação no banco
                print(f"Venda registrada com sucesso! Total: R$ {total:.2f}")

            except mysql.connector.Error as erro:
                conn.rollback()
                print(f"Erro ao gravar a venda, nada foi salvo: {erro}")

            finally:
                cursor.close()

            
        else:
            print("Venda cancelada.")

def listar_produtos(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    cursor.close()

    print("\n--- PRODUTOS ---")
    for produto in produtos:
        id_, nome, categoria_id, preco, estoque = produto
        print(f"{id_} - {nome} |  Preço: R$ {preco:.2f} - Estoque: {estoque}")

while True:
    print("\n===== PDV CHEFPAES =====")
    print("1 - Nova venda")
    print("2 - Listar produtos")
    print("3 - Cadastrar produto")
    print("4 - Alterar produto")
    print("0 - Sair")
    opcao = input("Escolha: ")

    if opcao == "1":
        nova_venda(conn)
    elif opcao == "2":
        listar_produtos(conn)
    elif opcao == "3":
        cadastrar_produto(conn)
    elif opcao == "4":
        alterar_produto(conn)
    elif opcao == "0":
        break
    else:
        print("Opção inválida.")

conn.close() 
print("Finalizado")