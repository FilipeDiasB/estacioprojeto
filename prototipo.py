import sqlite3

def create_database():
    conn = sqlite3.connect('estoque_vendas.db')
    cursor = conn.cursor()
2
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        quantidade INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        quantidade INTEGER,
        data_venda DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (produto_id) REFERENCES produtos (id)
    )
    ''')

    conn.commit()
    conn.close()

create_database()

def adicionar_produto(nome, preco, quantidade):
    conn = sqlite3.connect('estoque_vendas.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO produtos (nome, preco, quantidade)
    VALUES (?, ?, ?)
    ''', (nome, preco, quantidade))

    conn.commit()
    conn.close()

def atualizar_produto(produto_id, nome=None, preco=None, quantidade=None):
    conn = sqlite3.connect('estoque_vendas.db')
    cursor = conn.cursor()

    if nome:
        cursor.execute('''
        UPDATE produtos
        SET nome = ?
        WHERE id = ?
        ''', (nome, produto_id))

    if preco:
        cursor.execute('''
        UPDATE produtos
        SET preco = ?
        WHERE id = ?
        ''', (preco, produto_id))

    if quantidade is not None:
        cursor.execute('''
        UPDATE produtos
        SET quantidade = ?
        WHERE id = ?
        ''', (quantidade, produto_id))

    conn.commit()
    conn.close()

def listar_produtos():
    conn = sqlite3.connect('estoque_vendas.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

    conn.close()
    return produtos

def remover_produto(produto_id):
    conn = sqlite3.connect('estoque_vendas.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))

    conn.commit()
    conn.close()

def registrar_venda(produto_id, quantidade):
    conn = sqlite3.connect('estoque_vendas.db')
    cursor = conn.cursor()

    cursor.execute('SELECT quantidade FROM produtos WHERE id = ?', (produto_id,))
    produto = cursor.fetchone()

    if produto and produto[0] >= quantidade:
        cursor.execute('''
        INSERT INTO vendas (produto_id, quantidade)
        VALUES (?, ?)
        ''', (produto_id, quantidade))

        cursor.execute('''
        UPDATE produtos
        SET quantidade = quantidade - ?
        WHERE id = ?
        ''', (quantidade, produto_id))

        conn.commit()
        print(f"Venda registrada com sucesso!")
    else:
        print(f"Erro: Quantidade insuficiente em estoque!")

    conn.close()

def listar_vendas():
    conn = sqlite3.connect('estoque_vendas.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT vendas.id, produtos.nome, vendas.quantidade, vendas.data_venda
    FROM vendas
    JOIN produtos ON vendas.produto_id = produtos.id
    ''')
    vendas = cursor.fetchall()

    conn.close()
    return vendas


def menu():
    while True:
        print("\nSistema de Gestão de Estoque e Vendas")
        print("1. Adicionar Produto")
        print("2. Atualizar Produto")
        print("3. Listar Produtos")
        print("4. Remover Produto")
        print("5. Registrar Venda")
        print("6. Listar Vendas")
        print("7. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome do Produto: ")
            preco = float(input("Preço do Produto: "))
            quantidade = int(input("Quantidade em Estoque: "))
            adicionar_produto(nome, preco, quantidade)
            print("Produto adicionado com sucesso!")
        elif escolha == '2':
            produto_id = int(input("ID do Produto a atualizar: "))
            nome = input("Novo nome (deixe em branco para manter o atual): ")
            preco = input("Novo preço (deixe em branco para manter o atual): ")
            quantidade = input("Nova quantidade (deixe em branco para manter a atual): ")

            atualizar_produto(
                produto_id,
                nome if nome else None,
                float(preco) if preco else None,
                int(quantidade) if quantidade else None
            )
            print("Produto atualizado com sucesso!")
        elif escolha == '3':
            produtos = listar_produtos()
            print("\nProdutos em Estoque:")
            for produto in produtos:
                print(f"ID: {produto[0]}, Nome: {produto[1]}, Preço: {produto[2]}, Quantidade: {produto[3]}")
        elif escolha == '4':
            produto_id = int(input("ID do Produto a remover: "))
            remover_produto(produto_id)
            print("Produto removido com sucesso!")
        elif escolha == '5':
            produto_id = int(input("ID do Produto vendido: "))
            quantidade = int(input("Quantidade vendida: "))
            registrar_venda(produto_id, quantidade)
        elif escolha == '6':
            vendas = listar_vendas()
            print("\nRelatório de Vendas:")
            for venda in vendas:
                print(f"ID: {venda[0]}, Produto: {venda[1]}, Quantidade: {venda[2]}, Data: {venda[3]}")
        elif escolha == '7':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()

