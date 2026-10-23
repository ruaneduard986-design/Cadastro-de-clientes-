import sqlite3

class Database:
    def __init__(self, db_name="clientes.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT,
                idade INTEGER
            )
        """)
        self.conn.commit()

    def inserir(self, nome, email, telefone, idade):
        self.cursor.execute("""
            INSERT INTO clientes (nome, email, telefone, idade)
            VALUES (?, ?, ?, ?)
        """, (nome, email, telefone, idade))
        self.conn.commit()

    def listar(self):
        self.cursor.execute("SELECT * FROM clientes ORDER BY id")
        return self.cursor.fetchall()

    def buscar(self, termo):
        self.cursor.execute("""
            SELECT * FROM clientes
            WHERE nome LIKE ? OR email LIKE ?
            ORDER BY id
        """, (f"%{termo}%", f"%{termo}%"))
        return self.cursor.fetchall()

    def atualizar(self, id_cliente, nome, email, telefone, idade):
        self.cursor.execute("""
            UPDATE clientes
            SET nome=?, email=?, telefone=?, idade=?
            WHERE id=?
        """, (nome, email, telefone, idade, id_cliente))
        self.conn.commit()

    def deletar(self, id_cliente):
        self.cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
        self.conn.commit()

    def fechar(self):
        self.conn.close()