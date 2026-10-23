
                import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import re
from Database import Database

class AppCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Clientes")
        self.root.geometry("900x650")
        self.root.configure(bg="#f8f9fa")
        self.root.resizable(True, True)

        # Configurar protocolo de fechamento seguro
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Inicializar banco
        self.db = None
        try:
            self.db = Database()
        except RuntimeError as e:
            messagebox.showerror("Erro Crítico", f"Não foi possível conectar ao banco de dados:\n{e}")
            self.root.destroy()
            return

        self.id_selecionado = None

        self.criar_widgets()
        self.carregar_dados()

    # ------------------ INTERFACE MINIMALISTA ------------------
    def criar_widgets(self):
        # Estilos modernos
        style = ttk.Style()
        style.theme_use('clam')

        # Cores
        PRIMARY_COLOR = "#4a6cf7"
        SUCCESS_COLOR = "#2ecc71"
        WARNING_COLOR = "#f39c12"
        DANGER_COLOR = "#e74c3c"
        NEUTRAL_COLOR = "#95a5a6"
        BG_COLOR = "#f8f9fa"
        FRAME_BG = "#ffffff"
        TEXT_COLOR = "#2c3e50"

        # Título
        titulo = tk.Label(
            self.root,
            text="Sistema de Cadastro",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        titulo.pack(pady=(20, 10))

        # Subtítulo
        subtitulo = tk.Label(
            self.root,
            text="Gerencie seus clientes de forma simples",
            font=("Segoe UI", 10),
            bg=BG_COLOR,
            fg="#7f8c8d"
        )
        subtitulo.pack(pady=(0, 20))

        # Frame do formulário (card estilizado)
        frame_form = tk.Frame(
            self.root,
            bg=FRAME_BG,
            relief="flat"
        )
        frame_form.pack(fill="x", padx=40, pady=10)

        # Border shadow effect simulado
        shadow_frame = tk.Frame(frame_form, bg="#e9ecef", height=2)
        shadow_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Container interno do form
        form_inner = tk.Frame(frame_form, bg=FRAME_BG)
        form_inner.pack(padx=30, pady=15)

        # Linha 1: Nome e Email lado a lado
        linha1 = tk.Frame(form_inner, bg=FRAME_BG)
        linha1.pack(fill="x", pady=5)

        tk.Label(linha1, text="Nome Completo", bg=FRAME_BG, font=("Segoe UI", 9), fg="#34495e").pack(side="left", padx=5)
        self.entry_nome = tk.Entry(linha1, width=45, font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_nome.pack(side="left", padx=5)

        linha2 = tk.Frame(form_inner, bg=FRAME_BG)
        linha2.pack(fill="x", pady=5)

        tk.Label(linha2, text="Email", bg=FRAME_BG, font=("Segoe UI", 9), fg="#34495e").pack(side="left", padx=5)
        self.entry_email = tk.Entry(linha2, width=45, font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_email.pack(side="left", padx=5)

        # Linha 2: Telefone e Idade lado a lado
        linha3 = tk.Frame(form_inner, bg=FRAME_BG)
        linha3.pack(fill="x", pady=5)

        tk.Label(linha3, text="Telefone", bg=FRAME_BG, font=("Segoe UI", 9), fg="#34495e").pack(side="left", padx=5)
        self.entry_telefone = tk.Entry(linha3, width=45, font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_telefone.pack(side="left", padx=5)

        linha4 = tk.Frame(form_inner, bg=FRAME_BG)
        linha4.pack(fill="x", pady=5)

        tk.Label(linha4, text="Idade", bg=FRAME_BG, font=("Segoe UI", 9), fg="#34495e").pack(side="left", padx=5)
        self.entry_idade = tk.Entry(linha4, width=45, font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_idade.pack(side="left", padx=5)

        # Separador
        separator = tk.Frame(self.root, bg="#e9ecef", height=2)
        separator.pack(fill="x", padx=40, pady=10)

        # Botões com ícones simulados
        frame_botoes = tk.Frame(self.root, bg=BG_COLOR)
        frame_botoes.pack(pady=10)

        botao_config = {
            "font": ("Segoe UI", 10, "bold"),
            "bd": 0,
            "cursor": "hand2",
            "padx": 20,
            "pady": 10
        }

        tk.Button(frame_botoes, text="Cadastrar", width=15,
                  bg=SUCCESS_COLOR, fg="white",
                  command=self.cadastrar, **botao_config).grid(row=0, column=0, padx=8)

        tk.Button(frame_botoes, text=" Atualizar", width=15,
                  bg=WARNING_COLOR, fg="white",
                  command=self.atualizar, **botao_config).grid(row=0, column=1, padx=8)

        tk.Button(frame_botoes, text=" Excluir", width=15,
                  bg=DANGER_COLOR, fg="white",
                  command=self.excluir, **botao_config).grid(row=0, column=2, padx=8)

        tk.Button(frame_botoes, text=" Limpar", width=15,
                  bg=NEUTRAL_COLOR, fg="white",
                  command=self.limpar_campos, **botao_config).grid(row=0, column=3, padx=8)

        # Separador
        separator2 = tk.Frame(self.root, bg="#e9ecef", height=2)
        separator2.pack(fill="x", padx=40, pady=10)

        # Frame de busca
        frame_busca = tk.Frame(self.root, bg=FRAME_BG)
        frame_busca.pack(fill="x", padx=40, pady=10)

        tk.Label(frame_busca, text="🔍 Buscar", bg=FRAME_BG, font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)
        self.entry_busca = tk.Entry(frame_busca, width=50, font=("Segoe UI", 10), bd=1, relief="solid")
        self.entry_busca.pack(side="left", padx=10)
        self.entry_busca.bind("<KeyRelease>", lambda e: self.buscar())

        # Tabela moderna
        frame_tabela = tk.Frame(self.root, bg=FRAME_BG)
        frame_tabela.pack(fill="both", expand=True, padx=40, pady=15)

        colunas = ("ID", "Nome", "Email", "Telefone", "Idade")
        
        # Estilo moderno da Treeview
        style.configure("Modern.Treeview",
                       background=FRAME_BG,
                       foreground=TEXT_COLOR,
                       fieldbackground=FRAME_BG,
                       borderwidth=0,
                       font=("Segoe UI", 9))
        style.configure("Modern.Treeview.Heading",
                       background="#ecf0f1",
                       foreground=TEXT_COLOR,
                       font=("Segoe UI", 9, "bold"),
                       borderwidth=0)
        style.map("Modern.Treeview",
                 background=[('selected', PRIMARY_COLOR), ('active', PRIMARY_COLOR)],
                 foreground=[('selected', 'white'), ('active', 'white')])

        self.tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings",
                                 style="Modern.Treeview", height=12)

        for i, col in enumerate(colunas):
            widths = [50, 200, 220, 120, 70]
            anchors = ["center", "w", "w", "center", "center"]
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[i], minwidth=widths[i], anchor=anchors[i])

        # Scrollbar customizada
        scrollbar_y = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        self.tree.bind("<<TreeviewSelect>>", self.selecionar_registro)

        # Status bar
        status_bar = tk.Label(
            self.root,
            text="Pronto",
            bd=1,
            relief="sunken",
            anchor="w",
            bg="#ecf0f1",
            fg="#7f8c8d",
            font=("Segoe UI", 8)
        )
        status_bar.pack(side="bottom", fill="x")
        self.status_bar = status_bar

        # Atalhos de teclado
        self.root.bind("<Control-n>", lambda e: self.limpar_campos())
        self.root.bind("<Control-f>", lambda e: self.entry_busca.focus_set())

    # ------------------ MÉTODO UNIFICADO DE LEITURA E VALIDAÇÃO ------------------
    def ler_formulario(self, permitir_edicao=False):
        """
        Lê os campos do formulário, valida e retorna os dados.
        Retorna tupla (nome, email, telefone, idade) ou None se inválido.
        
        Args:
            permitir_edicao: Se False, verifica se tem registro selecionado para edição
        """
        # Coletar valores
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_telefone.get().strip()
        idade_str = self.entry_idade.get().strip()

        # Validações básicas
        if not nome:
            messagebox.showwarning("Validação", "O campo 'Nome' é obrigatório.")
            self.entry_nome.focus_set()
            return None

        if not email:
            messagebox.showwarning("Validação", "O campo 'Email' é obrigatório.")
            self.entry_email.focus_set()
            return None

        # Validação de formato de email
        padrao_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(padrao_email, email):
            messagebox.showerror("Validação", "Formato de email inválido.\nExemplo: usuario@dominio.com")
            self.entry_email.focus_set()
            self.entry_email.select_range(0, tk.END)
            return None

        # Validação de idade
        idade = None
        if idade_str:
            try:
                idade = int(idade_str)
                if idade < 0 or idade > 150:
                    messagebox.showwarning("Validação", "Idade deve estar entre 0 e 150 anos.")
                    self.entry_idade.focus_set()
                    self.entry_idade.select_range(0, tk.END)
                    return None
            except ValueError:
                messagebox.showerror("Validação", "Idade deve ser um número inteiro.")
                self.entry_idade.focus_set()
                self.entry_idade.select_range(0, tk.END)
                return None

        # Para edição, verifica se há registro selecionado
        if permitir_edicao and not self.id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente na tabela para editar.")
            return None

        return (nome, email, telefone if telefone else None, idade)

    # ------------------ AÇÕES ------------------
    def cadastrar(self):
        """Cadastra um novo cliente."""
        dados = self.ler_formulario(permitir_edicao=False)
        if not dados:
            return

        nome, email, telefone, idade = dados

        try:
            # Verifica duplicação antes de tentar inserir
            if self.db.verificar_duplicacao(email):
                messagebox.showerror("Erro", "Este email já está cadastrado.")
                self.entry_email.focus_set()
                self.entry_email.select_range(0, tk.END)
                return

            self.db.inserir(nome, email, telefone, idade)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
            self.limpar_campos()
            self.carregar_dados()
            self.atualizar_status(f"Cadastro realizado: {nome}")

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este email já está cadastrado no sistema.")
            self.entry_email.focus_set()
        except RuntimeError as e:
            messagebox.showerror("Erro no Banco", f"Erro ao salvar no banco:\n{e}")
        except Exception as e:
            messagebox.showerror("Erro Desconhecido", f"Ocorreu um erro inesperado:\n{e}")

    def atualizar(self):
        """Atualiza um cliente existente."""
        dados = self.ler_formulario(permitir_edicao=True)
        if not dados:
            return

        nome, email, telefone, idade = dados

        try:
            self.db.atualizar(self.id_selecionado, nome, email, telefone, idade)
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
            self.limpar_campos()
            self.carregar_dados()
            self.atualizar_status(f"Atualização realizada: {nome}")

        except sqlite3.IntegrityError as e:
            msg = str(e) if "email" in str(e).lower() else "Violação de constraint no banco de dados."
            messagebox.showerror("Erro", "Email já está em uso por outro cliente.")
            self.entry_email.focus_set()
        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except RuntimeError as e:
            messagebox.showerror("Erro no Banco", f"Erro ao atualizar:\n{e}")
        except Exception as e:
            messagebox.showerror("Erro Desconhecido", f"Ocorreu um erro inesperado:\n{e}")

    def excluir(self):
        """Exclui um cliente."""
        if not self.id_selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente na tabela para excluir.")
            return

        # Confirmação
        resposta = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Deseja realmente excluir o cliente?\n\n"
            f"ID: {self.id_selecionado}\n"
            f"Esta ação não pode ser desfeita."
        )

        if not resposta:
            return

        try:
            nome = self.entry_nome.get().strip()
            self.db.deletar(self.id_selecionado)
            messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
            self.limpar_campos()
            self.carregar_dados()
            self.atualizar_status(f"Exclusão realizada: {nome}")

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except RuntimeError as e:
            messagebox.showerror("Erro no Banco", f"Erro ao excluir:\n{e}")
        except Exception as e:
            messagebox.showerror("Erro Desconhecido", f"Ocorreu um erro inesperado:\n{e}")

    def limpar_campos(self):
        """Limpa todos os campos do formulário."""
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)
        self.id_selecionado = None
        self.tree.selection_remove(self.tree.selection())
        self.atualizar_status("Campos limpos")

    def carregar_dados(self, registros=None):
        """Carrega dados na tabela."""
        # Limpar itens existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obter registros
        if registros is None:
            try:
                registros = self.db.listar()
            except RuntimeError as e:
                messagebox.showerror("Erro", f"Não foi possível carregar os dados:\n{e}")
                return

        # Inserir na tabela
        total = 0
        for row in registros:
            self.tree.insert("", "end", values=row)
            total += 1

        self.atualizar_status(f"{total} cliente(s) carregado(s)")

    def buscar(self):
        """Realiza busca nos registros."""
        termo = self.entry_busca.get().strip()

        try:
            if termo:
                registros = self.db.buscar(termo)
                self.carregar_dados(registros)
                self.atualizar_status(f"{len(registros)} resultado(s) para '{termo}'")
            else:
                self.carregar_dados()

        except RuntimeError as e:
            messagebox.showerror("Erro", f"Erro ao buscar:\n{e}")

    def selecionar_registro(self, event):
        """Preenche o formulário ao selecionar um registro na tabela."""
        selecionado = self.tree.selection()
        if not selecionado:
            return

        try:
            valores = self.tree.item(selecionado[0], "values")
            self.id_selecionado = valores[0]

            # Limpar e preencher
            self.limpar_campos_sem_id()
            self.entry_nome.insert(0, valores[1])
            self.entry_email.insert(0, valores[2])
            self.entry_telefone.insert(0, valores[3])
            self.entry_idade.insert(0, valores[4] if valores[4] else "")

            self.atualizar_status(f"Selecionado: {valores[1]}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar registro:\n{e}")

    def limpar_campos_sem_id(self):
        """Limpa campos sem resetar o ID selecionado."""
        self.entry_nome.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_idade.delete(0, tk.END)

    def atualizar_status(self, mensagem):
        """Atualiza a barra de status."""
        self.status_bar.config(text=mensagem)

    def on_closing(self):
        """Chamado ao fechar a janela - fecha conexão com segurança."""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do programa?"):
            try:
                if self.db:
                    self.db.fechar()
            except RuntimeError as e:
                messagebox.showwarning("Aviso", f"Erro ao fechar banco de dados:\n{e}")
            finally:
                self.root.destroy()


# ------------------ EXECUÇÃO ------------------
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AppCadastro(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Erro Crítico", f"Falha ao iniciar aplicação:\n{e}")