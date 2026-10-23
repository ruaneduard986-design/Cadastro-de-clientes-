 import sqlite3

class Database:
    def __init__(self, db_name="clientes.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.criar_tabela()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao conectar ao banco de dados: {e}")

    def criar_tabela(self):
        """Cria a tabela clientes com constraints de validação."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    telefone TEXT,
                    idade INTEGER CHECK(idade >= 0 AND idade <= 150)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Erro ao criar tabela: {e}")

    def inserir(self, nome, email, telefone=None, idade=None):
        """Insere um novo cliente. Lança sqlite3.IntegrityError se email já existir."""
        try:
            self.cursor.execute("""
                INSERT INTO clientes (nome, email, telefone, idade)
                VALUES (?, ?, ?, ?)
            """, (nome, email, telefone, idade))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            self.conn.rollback()
            raise IntegrityError(f"Email já cadastrado ou violação de constraint: {e}")
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Erro ao inserir cliente: {e}")

    def listar(self):
        """Lista todos os clientes ordenados por ID."""
        try:
            self.cursor.execute("SELECT * FROM clientes ORDER BY id")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao listar clientes: {e}")

    def buscar(self, termo):
        """Busca clientes por nome ou email contendo o termo."""
        try:
            self.cursor.execute("""
                SELECT * FROM clientes
                WHERE nome LIKE ? OR email LIKE ?
                ORDER BY id
            """, (f"%{termo}%", f"%{termo}%"))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao buscar clientes: {e}")

    def obter_por_id(self, id_cliente):
        """Obtém um cliente específico pelo ID."""
        try:
            self.cursor.execute(
                "SELECT * FROM clientes WHERE id=?",
                (id_cliente,)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao buscar cliente por ID: {e}")

    def atualizar(self, id_cliente, nome, email, telefone=None, idade=None):
        """Atualiza um cliente existente. Verifica se email já existe para outro ID."""
        try:
            # Verifica se email já está sendo usado por outro registro
            self.cursor.execute(
                "SELECT id FROM clientes WHERE email=? AND id!=?",
                (email, id_cliente)
            )
            if self.cursor.fetchone():
                raise IntegrityError("Email já está em uso por outro cliente.")

            self.cursor.execute("""
                UPDATE clientes
                SET nome=?, email=?, telefone=?, idade=?
                WHERE id=?
            """, (nome, email, telefone, idade, id_cliente))
            self.conn.commit()
        except sqlite3.IntegrityError:
            self.conn.rollback()
            raise
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Erro ao atualizar cliente: {e}")

    def deletar(self, id_cliente):
        """Deleta um cliente pelo ID."""
        try:
            self.cursor.execute("DELETE FROM clientes WHERE id=?", (id_cliente,))
            self.conn.commit()
            if self.cursor.rowcount == 0:
                raise ValueError("Cliente não encontrado.")
        except sqlite3.Error as e:
            self.conn.rollback()
            raise RuntimeError(f"Erro ao deletar cliente: {e}")

    def validar_email(self, email):
        """Valida formato básico de email."""
        import re
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao, email):
            raise ValueError("Formato de email inválido.")
        return True

    def validar_idade(self, idade):
        """Valida que idade está dentro de uma faixa razoável."""
        if idade is None:
            return True  # Permite idade nula
        if not isinstance(idade, int):
            raise ValueError("Idade deve ser um número inteiro.")
        if idade < 0 or idade > 150:
            raise ValueError("Idade deve estar entre 0 e 150 anos.")
        return True

    def verificar_duplicacao(self, email, id_excluir=None):
        """Verifica se email já existe na base, exceto se id_excluir for fornecido."""
        try:
            if id_excluir:
                self.cursor.execute(
                    "SELECT id FROM clientes WHERE email=? AND id!=?",
                    (email, id_excluir)
                )
            else:
                self.cursor.execute(
                    "SELECT id FROM clientes WHERE email=?",
                    (email,)
                )
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao verificar duplicação: {e}")

    def fechar(self):
        """Fecha a conexão com o banco de dados."""
        try:
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            raise RuntimeError(f"Erro ao fechar conexão: {e}")