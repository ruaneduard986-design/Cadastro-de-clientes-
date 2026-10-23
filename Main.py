
import tkinter as tk
from tkinter import ttk, messagebox
from Database import Database

class AppCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Cadastro de Clientes")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        self.db = Database()
        self.id_selecionado = None

        self.criar_widgets()
        self.carregar_dados()

    # ------------------ INTERFACE ------------------
    def criar_widgets(self):
        # Título
        titulo = tk.Label(
            self.root, text="Cadastro de Clientes",
            font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2c3e50"
        )
        titulo.pack(pady=10)

        # Frame do formulário
        frame_form = tk.LabelFrame(
            self.root, text=" Dados do Cliente ",
            font=("Arial", 11, "bold"), bg="#f0f0f0", padx=10, pady=10
        )
        frame_form.pack(fill="x", padx=20, pady=5)

        # Nome
        tk.Label(frame_form, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_nome = tk.Entry(frame_form, width=50)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        # Email
        tk.Label(frame_form, text="Email:", bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = tk.Entry(frame_form, width=50)
        self.entry_email.grid(row=1, column=1, padx=5, pady=5)

        # Telefone
        tk.Label(frame_form, text="Telefone:", bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_telefone = tk.Entry(frame_form, width=50)
        self.entry_telefone.grid(row=2, column=1, padx=5, pady=5)

        # Idade
        tk.Label(frame_form, text="Idade:", bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_idade = tk.Entry(frame_form, width=50)
        self.entry_idade.grid(row=3, column=1, padx=5, pady=5)

        # Frame dos botões
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=10)

        tk.Button(frame_botoes, text=" Cadastrar", width=12,
                  bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  command=self.cadastrar).grid(row=0, column=0, padx=5)

        tk.Button(frame_botoes, text=" Atualizar", width=12,
                  bg="#f39c12", fg="white", font=("Arial", 10, "bold"),
                  command=self.atualizar).grid(row=0, column=1, padx=5)

        tk.Button(frame_botoes, text=" Excluir", width=12,
                  bg="#c0392b", fg="white", font=("Arial", 10, "bold"),
                  command=self.excluir).grid(row=0, column=2, padx=5)

        tk.Button(frame_botoes, text=" Limpar", width=12,
                  bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"),
                  command=self.limpar_campos).grid(row=0, column=3, padx=5)

        # Frame de busca
        frame_busca = tk.Frame(self.root, bg="#f0f0f0")
        frame_busca.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_busca, text="Buscar:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left")
        self.entry_busca = tk.Entry(frame_busca, width=40)
        self.entry_busca.pack(side="left", padx=5)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.buscar())

        # Tabela (Treeview)
        frame_tabela = tk.Frame(self.root)
        frame_tabela.pack(fill="both", expand=True, padx=20, pady=10)

        colunas = ("ID", "Nome", "Email", "Telefone", "Idade")
        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=10)

        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.column("ID", width=50)
        self.tree.column("Nome", width=200)
        self.tree.column("Email", width=200)

        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Clique na tabela preenche formulário
        self.tree.bind("<<TreeviewSelect>>", self.selecionar_registro)

    # ------------------ AÇÕES ------------------
    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        idade = self.entry_idade.get().strip()

        if not nome or not email:
            messagebox.showwarning("Aviso", "Nome e Email são obrigatórios!")
            return

        try:
            idade_int = int(idade) if idade else None
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número!")
            return

        self.db.inserir(nome, email, telefone, idade_int)
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        self.limpar_campos()
        self.carregar_dados()

    def atualizar(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela!")
            return

        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        idade = self.entry_idade.get().strip()

        if not nome or not email:
            messagebox.showwarning("Aviso", "Nome e Email são obrigatórios!")
            return

        try:
            idade_int = int(idade) if idade else None
        except ValueError:
            messagebox.showerror("Erro", "Idade deve ser um número!")
            return

        self.db.atualizar(self.id_selecionado, nome, email, telefone, idade_int)
        messagebox.showinfo("Sucesso", "Cliente atualizado!")
        self.limpar_campos()
        self.carregar_dados()

    def excluir(self):
        if not self.id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela!")
            return

        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?"):
            self.db.deletar(self.id_selecionado)
            messagebox.showinfo("Sucesso", "Cliente excluído!")
            self.limpar_campos()
            self.carregar_dados()

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.id_selecionado = None
        self.tree.selection_remove(self.tree.selection())

    def carregar_dados(self, registros=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if registros is None:
            registros = self.db.listar()

        for row in registros:
            self.tree.insert("", "end", values=row)

    def buscar(self):
        termo = self.entry_busca.get().strip()
        if termo:
            registros = self.db.buscar(termo)
        else:
            registros = self.db.listar()
        self.carregar_dados(registros)

    def selecionar_registro(self, event):
        selecionado = self.tree.selection()
        if not selecionado:
            return

        valores = self.tree.item(selecionado[0], "values")
        self.id_selecionado = valores[0]

        self.limpar_campos_sem_id()
        self.entry_nome.insert(0, valores[1])
        self.entry_email.insert(0, valores[2])
        self.entry_telefone.insert(0, valores[3])
        self.entry_idade.insert(0, valores[4])
        self.id_selecionado = valores[0]

    def limpar_campos_sem_id(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)


# ------------------ EXECUÇÃO ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = AppCadastro(root)
    root.mainloop()