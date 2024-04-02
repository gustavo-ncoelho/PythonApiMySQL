import mysql.connector

class BancoDeDados:
    def __init__(self, db_config):
        self.db_config = db_config

    def conectar(self):
        return mysql.connector.connect(**self.db_config)

    def criar_tabelas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contatos (
                id INT PRIMARY KEY AUTO_INCREMENT,
                nome VARCHAR(50),
                perfil_linkedin VARCHAR(50)
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conexoes (
                id INT PRIMARY KEY AUTO_INCREMENT,
                contato1_id INT,
                contato2_id INT,
                FOREIGN KEY (contato1_id) REFERENCES contatos(id),
                FOREIGN KEY (contato2_id) REFERENCES contatos(id)
            );
        ''')

        conn.commit()
        conn.close()

class ContatoManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def adicionar_contato(self, nome, perfil_linkedin):
        try:
            conn = banco.conectar()
            cursor = conn.cursor()

            cursor.execute('''SELECT id FROM contatos 
                           WHERE nome = %s AND perfil_linkedin = %s''', 
                           (nome, perfil_linkedin))
            contato_id = cursor.fetchone()

            if contato_id:
                contato_id = contato_id[0]
                print("Perfil já cadastrado !!")
            else:
                cursor.execute('''INSERT INTO contatos (nome, perfil_linkedin) 
                               VALUES (%s, %s)''', 
                               (nome, perfil_linkedin))

            conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao adicionar contato: {err}")
        finally:
            if 'conn' in locals():
                conn.close()

    def alterar_contato(self, contato_id, novo_nome, novo_perfil_linkedin):
        try:
            conn = banco.conectar()
            cursor = conn.cursor()

            cursor.execute('''UPDATE contatos SET nome = %s, perfil_linkedin = %s 
                           WHERE id = %s''', 
                           (novo_nome, novo_perfil_linkedin, contato_id))

            conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao alterar contato: {err}")
        finally:
            if 'conn' in locals():
                conn.close()

    def listar_contatos(self):
        try:
            conn = banco.conectar()
            cursor = conn.cursor()

            cursor.execute("SELECT id, nome, perfil_linkedin FROM contatos")
            contatos = cursor.fetchall()

            for contato in contatos:
                print(f"ID: {contato[0]}, Nome: {contato[1]}, Perfil LinkedIn: {contato[2]}")

        except mysql.connector.Error as erro:
            print(f"Erro ao listar contatos: {erro}")
        finally:
            if 'conn' in locals():
                conn.close()
    
    def excluir_contato(self, contato_id):
        try:
            conn = banco.conectar()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM contatos WHERE id = %s", (contato_id,))

            conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao excluir contato: {err}")
        finally:
            if 'conn' in locals():
                conn.close()

class Menu:
    def __init__(self, contato_manager):
        self.contato_manager = contato_manager

    def exibir_menu(self):
        while True:
            print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=")
            print("\n1. Adicionar Contato")
            print("2. Alterar Contato")
            print("3. Listar Contatos")
            print("4. Excluir contato")
            print("0. Sair")
            print("......................")

            escolha = input("Escolha uma opção: ")

            if escolha == "1":
                nome = input("Nome do contato: ")
                perfil_linkedin = input("Perfil do LinkedIn: ")
                self.contato_manager.adicionar_contato(nome, perfil_linkedin)
            elif escolha == "2":
                contato_id = input("Digite o ID do contato que deseja alterar: ")
                novo_nome = input("Novo nome do contato: ")
                novo_perfil_linkedin = input("Novo perfil do LinkedIn: ")
                self.contato_manager.alterar_contato(contato_id, novo_nome, novo_perfil_linkedin)
            elif escolha == "3":
                self.contato_manager.listar_contatos()
            elif escolha == "4":
                contato_id = input("Digite o ID do contato que deseja deletar: ")
                self.contato_manager.excluir_contato(contato_id)
            elif escolha == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    db_config = {
        'user':'natanhmc',
        'password':'1q2w3e4r5t',
        'host':'db4free.net',
        'database':'linkedin123',
        'port':3306
    }

    banco = BancoDeDados(db_config)
    banco.criar_tabelas()

    contato_manager = ContatoManager(db_config)
    menu = Menu(contato_manager)
    menu.exibir_menu()