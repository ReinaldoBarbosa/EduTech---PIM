import customtkinter as ctk
import json
import os
import re
import time
import random
import smtplib
from tkinter import messagebox
from email.mime.text import MIMEText
from email.utils import formataddr
import hashlib

# Carrega os dados
with open("teste.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Configurações iniciais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# App principal
app = ctk.CTk()
app.title("EduTech")
app.geometry("800x500")
app.resizable(False, False)

usuario_log = ''

def informar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Controle da tela atual
tela_atual = None
def trocar_tela(nova_tela_class):
    global tela_atual
    if tela_atual is not None:
        tela_atual.destroy()
    tela_atual = nova_tela_class(app) 
    tela_atual.place(relx=0.5, rely=0.5, anchor="center")

# Funções auxiliares
def on_focus_in_senha(entry, bloco):
    entry.configure(border_color="#0945f3")
    bloco.place(x=entry.winfo_x(), y=entry.winfo_y() - 160)

def on_focus_out_senha(entry, bloco):
    entry.configure(border_color="#2a2d2e")
    bloco.place_forget()

def on_focus_in(entry):
    entry.configure(border_color="#0945f3")

def on_focus_out(entry):
    entry.configure(border_color="#2a2d2e")

def enviar_email_confirmacao(destinatario, codigo, nome_usuario):
    remetente = "edutech.unip@gmail.com"
    senha = "lwzf ivjy qvxz maod"  # Gere em https://myaccount.google.com/apppasswords

    assunto = "Código de Verificação - EduTech"
    corpo_html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #0945f3; text-align: center;">EduTech - Confirmação de E-mail</h2>
                <p style="font-size: 16px; color: #333;">
                    Olá <strong>{nome_usuario}</strong>,<br><br>
                    Obrigado por se cadastrar na <strong>EduTech</strong>! Para continuar, confirme seu endereço de e-mail:
                </p>
                <p style="font-size: 16px; color: #333; text-align: center;">
                    <span style="color: #0945f3;">{destinatario}</span>
                </p>
                <p style="font-size: 16px; color: #333; text-align: center; margin-top: 20px;">
                    Seu código de verificação:
                </p>
                <div style="text-align: center; margin: 10px 0 30px 0;">
                    <span style="font-size: 28px; color: #0945f3; font-weight: bold; letter-spacing: 4px;">{codigo}</span>
                </div>
                <p style="font-size: 14px; color: #555;">
                    Caso você não tenha solicitado este cadastro, apenas ignore este e-mail.<br><br>
                    Atenciosamente,<br>
                    Equipe EduTech
                </p>
            </div>
        </body>
    </html>
    """

    msg = MIMEText(corpo_html, 'html')
    msg["Subject"] = assunto
    msg["From"] = formataddr(("Escola Tecnológica", remetente))
    msg["To"] = destinatario

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remetente, senha)
            servidor.send_message(msg)
        return True
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return False

# Tela de Login
class TelaLogin(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=357, height=400, fg_color="#1A1A1A")

        ctk.CTkLabel(self, text="Login", text_color="#0945f3", font=("Roboto", 20, "bold")).place(x=150, y=30)

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Nome de Usuário", width=300, border_color="#2a2d2e", font=("Roboto", 14))
        self.entry1.place(x=25, y=85)

        ctk.CTkLabel(self, text="O campo nome de usuário é de caráter obrigatório", text_color="green", font=("Roboto", 8)).place(x=25, y=115)

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Senha do Usuário", width=300, border_color="#2a2d2e", font=("Roboto", 14), show="*")
        self.entry2.place(x=25, y=155)

        ctk.CTkLabel(self, text="O campo de senha é de caráter obrigatório", text_color="green", font=("Roboto", 8)).place(x=25, y=185)

        ctk.CTkCheckBox(self, text="Lembrar-se de mim sempre", fg_color="#0945f3").place(x=25, y=215)

        ctk.CTkButton(self, text='LOGIN', fg_color='#0945f3', hover_color='#072bc7', width=300, cursor="hand2", command=self.login).place(x=25, y=265)

        ctk.CTkButton(self, text='CADASTRO', fg_color='#0945f3', hover_color='#072bc7', width=300, cursor="hand2", command=lambda: trocar_tela(TelaEscolhaPerfil)).place(x=25, y=310)

    def login(self):
        email = self.entry1.get()
        senha = self.entry2.get()

        if not os.path.exists("usuarios.json"):
            messagebox.showerror("Erro", "Nenhum usuário cadastrado ainda!")
            return

        with open("usuarios.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        usuarios = dados["Usuarios"]
        senha_digitada_hash = hashlib.sha256(senha.encode()).hexdigest()
        for usuario in usuarios:
            if usuario["email"] == email and usuario["senha"] == senha_digitada_hash:
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")

                # Atualiza acessos
                usuario["acessos"] = usuario.get("acessos", 0) + 1

                # Salva o horário de login (timestamp)
                usuario["ultimo_login"] = time.time()

                # Salva o JSON atualizado
                with open("usuarios.json", "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=4, ensure_ascii=False)

                # Salva o nome do usuário logado se precisar usar depois
                global usuario_log
                usuario_log = usuario["nome"]

                trocar_tela(lambda master: TelaPainel(master, usuario_log))
                return

        messagebox.showerror("Erro", "Email ou senha incorretos.")

class TelaEscolhaPerfil(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#1A1A1A", width=400, height=300)

        ctk.CTkLabel(self, text="Como você deseja se cadastrar?", font=("Roboto", 18, "bold"), text_color="#0945f3").place(x=50, y=30)

        ctk.CTkButton(self, text="🎓\n Sou Aluno", width=140, height=100, fg_color="#1f1f1f", command=self.ir_para_aluno).place(x=40, y=90)
        ctk.CTkButton(self, text="👨‍🏫\n Sou Professor", width=140, height=100, fg_color="#1f1f1f", command=self.ir_para_professor).place(x=220, y=90)

        ctk.CTkButton(self, text="Voltar", width=300, fg_color="#3a3a3a", hover_color="#0945f3", command=self.voltar).place(x=50, y=220)

    def ir_para_aluno(self):
        trocar_tela(lambda master: TelaCadastro(master, "aluno"))

    def ir_para_professor(self):
        trocar_tela(lambda master: TelaCadastro(master, "professor"))

    def voltar(self):
        trocar_tela(TelaLogin)

# Tela de Cadastro
class TelaCadastro(ctk.CTkFrame):
    def __init__(self, master, status):
        super().__init__(master, width=357, height=400, fg_color="#1A1A1A")
        self.status = status

        ctk.CTkLabel(self, text="Cadastro", text_color="#0945f3", font=("Roboto", 20, "bold")).place(x=130, y=30)

        self.entry1 = ctk.CTkEntry(self, placeholder_text="Nome de Usuário", width=300, font=("Roboto", 14))
        self.entry1.place(x=25, y=85)
        ctk.CTkLabel(self, text="O campo nome de usuário é obrigatório", text_color="green", font=("Roboto", 8)).place(x=25, y=115)

        self.entry2 = ctk.CTkEntry(self, placeholder_text="Email do Usuário", width=300, font=("Roboto", 14))
        self.entry2.place(x=25, y=155)
        ctk.CTkLabel(self, text="O campo senha é obrigatório", text_color="green", font=("Roboto", 8)).place(x=25, y=185)

        self.entry3 = ctk.CTkEntry(self, placeholder_text="Senha do Usuário", width=300, font=("Roboto", 14), show="*")
        self.entry3.place(x=25, y=225)

        self.lembrar_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self, text="Aceito os Termos e Políticas", variable=self.lembrar_var, fg_color="#0945f3").place(x=25, y=275)

        ctk.CTkButton(self, text="CADASTRAR", width=140, fg_color='#0945f3', hover_color='#072bc7', command=self.cadastrar).place(x=25, y=320)
        ctk.CTkButton(self, text="VOLTAR", width=140, fg_color='#3a3a3a', hover_color='#5a5a5a', command=self.voltar_login).place(x=185, y=320)

        # Bloco com requisitos da senha
        self.bloco_requisitos = ctk.CTkFrame(self, width=250, height=150, corner_radius=10, border_width=1, border_color="#ccc")

        requisitos_texto = [
            "Mínimo de 8 caracteres", "Letra maiúscula", "Letra minúscula", "Número", "Caractere especial"
        ]
        self.labels_requisitos = []
        for i, texto in enumerate(requisitos_texto):
            label = ctk.CTkLabel(self.bloco_requisitos, text="❌ " + texto, text_color="#fff", font=("Roboto", 12))
            label.place(x=10, y=10 + i * 25)
            self.labels_requisitos.append(label)

        # Eventos de foco
        self.entry1.bind("<FocusIn>", lambda e: on_focus_in(self.entry1))
        self.entry1.bind("<FocusOut>", lambda e: on_focus_out(self.entry1))

        self.entry2.bind("<FocusIn>", lambda e: on_focus_in(self.entry2))
        self.entry2.bind("<FocusOut>", lambda e: on_focus_out(self.entry2))

        self.entry3.bind("<KeyRelease>", self.validar_senha)
        self.entry3.bind("<FocusIn>", lambda e: on_focus_in_senha(self.entry3, self.bloco_requisitos))
        self.entry3.bind("<FocusOut>", lambda e: on_focus_out_senha(self.entry3, self.bloco_requisitos))

    def validar_senha(self, event=None):
        senha = self.entry3.get()
        requisitos = [
            (len(senha) >= 8, "Mínimo de 8 caracteres"),
            (any(c.isupper() for c in senha), "Letra maiúscula"),
            (any(c.islower() for c in senha), "Letra minúscula"),
            (any(c.isdigit() for c in senha), "Número"),
            (re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha) is not None, "Caractere especial")
        ]
        for i, (valido, texto) in enumerate(requisitos):
            self.labels_requisitos[i].configure(text=("✔️ " if valido else "❌ ") + texto, text_color="green" if valido else "#fff")

    def cadastrar(self):
        nome = self.entry1.get()
        email = self.entry2.get()
        senha = self.entry3.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Atenção", "Todos os campos são obrigatórios.")
            return

        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showerror("Erro", "E-mail inválido.")
            return

        if not (
            len(senha) >= 8 and
            any(c.isupper() for c in senha) and
            any(c.islower() for c in senha) and
            any(c.isdigit() for c in senha) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha)
        ):
            messagebox.showerror("Erro", "A senha não atende aos requisitos.")
            return

        usuarios = {}
        if os.path.exists("usuarios.json"):
            with open("usuarios.json", "r", encoding="utf-8") as f:
                usuarios = json.load(f)

        if 'Usuarios' in usuarios and any(u["email"] == email for u in usuarios['Usuarios']):
            messagebox.showerror("Erro", "Usuário já cadastrado com esse e-mail.")
            return

        # Gerar código e enviar
        codigo = str(random.randint(100000, 999999))
        enviado = enviar_email_confirmacao(email, codigo, nome)

        if enviado:
            messagebox.showinfo("Verificação", f"Um código foi enviado para {email}.")
            trocar_tela(lambda master: TelaVerificacaoCodigo(master, nome, email, senha, codigo, self.status))
        else:
            messagebox.showerror("Erro", "Não foi possível enviar o e-mail. Verifique sua conexão ou tente outro e-mail.")

    def voltar_login(self):
        trocar_tela(TelaLogin)

class TelaVerificacaoCodigo(ctk.CTkFrame):
    def __init__(self, master, nome, email, senha, codigo, status):
        super().__init__(master, width=357, height=400, fg_color="#1A1A1A")

        self.nome = nome
        self.email = email
        self.senha = informar_senha(senha)
        self.codigo_esperado = codigo
        self.status = status

        ctk.CTkLabel(self, text="Verificação de E-mail", font=("Roboto", 20, "bold"), text_color="#0945f3").place(x=70, y=40)

        ctk.CTkLabel(self, text="Digite o código enviado para seu e-mail:", text_color="white").place(x=40, y=100)

        self.entry_codigo = ctk.CTkEntry(self, placeholder_text="Código de verificação", width=250)
        self.entry_codigo.place(x=50, y=140)

        ctk.CTkButton(self, text="VERIFICAR", command=self.verificar_codigo, fg_color="#0945f3", hover_color="#072bc7").place(x=100, y=200)

    def verificar_codigo(self):
        if self.entry_codigo.get() == self.codigo_esperado:
            usuarios = {}
            if os.path.exists("usuarios.json"):
                with open("usuarios.json", "r", encoding="utf-8") as f:
                    usuarios = json.load(f)

            if 'Usuarios' not in usuarios:
                usuarios['Usuarios'] = []

            usuarios['Usuarios'].append({
                "nome": self.nome,
                "email": self.email,
                "senha": self.senha,
                "Progresso": 0,
                "Pontuacao": 0,
                "Rank": "Bronze",
                "acessos": 0,
                "tempo_total_min": 0,
                "status": self.status,
                "materias": {}
            })

            with open("usuarios.json", "w", encoding="utf-8") as f:
                json.dump(usuarios, f, indent=4)

            messagebox.showinfo("Sucesso", "Cadastro confirmado!")
            trocar_tela(TelaLogin)
        else:
            messagebox.showerror("Erro", "Código incorreto. Verifique seu e-mail.")

# Tela Principal
class TelaPainel(ctk.CTkFrame):

    def __init__(self, master, usuario_log):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")
        self.usuario_log = usuario_log  # Armazena o usuário logado
        self.cor_texto = "blue"
        self.cor_fundo = "#1f1f1f"

        # Título personalizado
        frame_bem_vindo = ctk.CTkFrame(self, fg_color="transparent")
        frame_bem_vindo.place(x=34, y=30)

        label_prefixo = ctk.CTkLabel(
            frame_bem_vindo,
            text="Seja Bem Vindo, ",
            font=("Roboto", 24, "bold"),
            text_color="#D3D3D3"
        )
        label_prefixo.pack(side="left")

        self.label_nome = ctk.CTkLabel(
            frame_bem_vindo,
            text="Usuário!",
            font=("Roboto", 24, "bold"),
            text_color=self.cor_texto
        )
        self.label_nome.pack(side="left")

        # Construção da interface conforme status do usuário
        self.construir_tela()

        # Botão de sair
        ctk.CTkButton(
            self,
            text="← Sair",
            width=229,
            height=38,
            fg_color=self.cor_fundo,
            hover_color="#2c2c2c",
            compound="right",
            corner_radius=6,
            command=self.logout
        ).place(x=34, y=320)

        # Botão Ver Cursos
        ctk.CTkButton(
            self,
            text="Ver Cursos",
            width=229,
            height=38,
            fg_color=self.cor_fundo,
            hover_color="#2c2c2c",
            text_color=self.cor_texto,
            compound="right",
            corner_radius=6,
            command=self.curso
        ).place(x=297, y=320)

        # Atualiza as informações do usuário
        self.atualizar_informacoes_usuario()

    def construir_tela(self):
        usuario = self.carregar_dados_usuario(self.usuario_log)

        if usuario:
            if usuario['status'] == 'aluno':
                self.telaAluno()
            elif usuario['status'] == 'professor':
                self.telaProfessor()

    def telaAluno(self):
        # Caixa de progresso
        self.seu_progresso = ctk.CTkFrame(self, width=140, height=97, fg_color="#212121")
        self.seu_progresso.place(x=34, y=99)

        ctk.CTkLabel(self.seu_progresso, text="Seu\nProgresso", font=("Roboto", 10)).place(relx=0.5, rely=0.2, anchor="center")
        self.label_porcentagem = ctk.CTkLabel(self.seu_progresso, text="0%", font=("Roboto", 20, "bold"))
        self.label_porcentagem.place(relx=0.5, rely=0.7, anchor="center")

        # Caixa de pontuação
        self.pontuacao = ctk.CTkFrame(self, width=140, height=97, fg_color="#212121")
        self.pontuacao.place(x=208, y=99)

        ctk.CTkLabel(self.pontuacao, text="Pontuação", font=("Roboto", 10)).place(relx=0.5, rely=0.2, anchor="center")
        self.pontuacao_aluno = ctk.CTkLabel(self.pontuacao, text="0", font=("Roboto", 20, "bold"))
        self.pontuacao_aluno.place(relx=0.5, rely=0.7, anchor="center")

        # Caixa de nível
        self.nivel_atual = ctk.CTkFrame(self, width=140, height=97, fg_color="#212121")
        self.nivel_atual.place(x=384, y=99)

        ctk.CTkLabel(self.nivel_atual, text="Seu Nível\nAtual", font=("Roboto", 10)).place(relx=0.5, rely=0.2, anchor="center")
        self.nivel = ctk.CTkLabel(self.nivel_atual, text="BRONZE", font=("Roboto", 20, "bold"))
        self.nivel.place(relx=0.5, rely=0.7, anchor="center")

    def telaProfessor(self):
        ctk.CTkButton(
            self,
            text="Novo Curso",
            width=140,
            height=97,
            fg_color=self.cor_fundo,
            hover_color="#2c2c2c",
            text_color=self.cor_texto,
            compound="right",
            corner_radius=6,
            command=self.cadastrar_curso
        ).place(x=208, y=99)

    def carregar_dados_usuario(self, usuario_log):
        with open("usuarios.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        for usuario in dados["Usuarios"]:
            if usuario["nome"] == usuario_log:
                return usuario
        return None

    def atualizar_informacoes_usuario(self):
        usuario = self.carregar_dados_usuario(self.usuario_log)

        if usuario:
            self.label_nome.configure(text=f"{usuario['nome']}!")

            progresso = usuario.get("progresso", 0)
            if hasattr(self, "label_porcentagem"):
                self.label_porcentagem.configure(text=f"{progresso}%")

            pontuacao = usuario.get("pontuacao", 0)
            if hasattr(self, "pontuacao_aluno"):
                self.pontuacao_aluno.configure(text=str(pontuacao))

            nivel = usuario.get("nivel", "BRONZE")
            if hasattr(self, "nivel"):
                self.nivel.configure(text=nivel)

    def curso(self):
        self.place_forget()
        trocar_tela(lambda master: TelaCursos(master))

    def cadastrar_curso(self):
        self.place_forget()
        trocar_tela(lambda master: CadastroCurso(master))

    def logout(self):
        usuario = self.carregar_dados_usuario(self.usuario_log)

        if usuario and "ultimo_login" in usuario:
            tempo_uso = time.time() - usuario["ultimo_login"]
            minutos = round(tempo_uso / 60)
            usuario["tempo_total_min"] = usuario.get("tempo_total_min", 0) + minutos

            with open("usuarios.json", "r", encoding="utf-8") as f:
                dados = json.load(f)

            for u in dados["Usuarios"]:
                if u["nome"] == self.usuario_log:
                    u.update(usuario)
                    break

            with open("usuarios.json", "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)

        trocar_tela(TelaLogin)
# Tela Cursos
class TelaCursos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")
        self.grid(row=0, column=0, sticky="nsew")

        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        titulo = ctk.CTkLabel(self, text="Cursos Disponíveis", font=("Roboto", 20, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Carregar as matérias do JSON
        with open("teste.json", "r", encoding="utf-8") as f:
            materias = json.load(f)

        colunas = 2
        for i, materia in enumerate(materias):
            linha = (i // colunas) + 1
            coluna = i % colunas

            botao = ctk.CTkButton(
                self,
                text=materia["nome"],
                width=242,
                height=38,
                fg_color="#1f1f1f",
                text_color="#FFFFFF",
                hover_color="#2C2C2C",
                corner_radius=5,
                command=lambda m=materia: self.ir_para_niveis(m)
            )
            botao.grid(row=linha, column=coluna, padx=10, pady=10)

        total_linhas = (len(materias) + 1) // 2 + 1
        botao_voltar = ctk.CTkButton(self, text="Voltar",width=242,
                height=38,
                fg_color="#1f1f1f",
                text_color="#FFFFFF",
                hover_color="#2C2C2C",
                corner_radius=5, command=self.sair)
        botao_voltar.grid(row=total_linhas, column=0, columnspan=2, pady=20)

    def ir_para_niveis(self, materia):
        materia_nome = materia["nome"]

        # Carregar os dados dos usuários
        with open("usuarios.json", "r", encoding="utf-8") as f:
            usuarios = json.load(f)["Usuarios"]

        # Verifica se o usuário logado tem essa matéria
        for usuario in usuarios:
            if usuario["nome"] == usuario_log:
                if "materias" not in usuario:
                    usuario["materias"] = {}

                # Adiciona a matéria se ainda não existir
                if materia_nome not in usuario["materias"]:
                    usuario["materias"][materia_nome] = {
                        "niveis_acessados": {
                            "Iniciante": {
                                "desbloqueado": True
                            },
                            "Intermediario": {
                                "desbloqueado": False
                            },
                            "Avancado": {
                                "desbloqueado": False
                            }
                        }
                    }

                break

        # Salva no JSON dos usuários
        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump({"Usuarios": usuarios}, f, indent=4)

        # Vai para a tela de níveis
        self.pack_forget()
        trocar_tela(lambda app: TelaNiveis(app, materia))

    def sair(self):
        self.grid_forget()
        trocar_tela(lambda master: TelaPainel(master, usuario_log))

class CadastroCurso(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")
        self.pack_propagate(False)

        self.nome_var = ctk.StringVar()

        ctk.CTkLabel(self, text="Nome do Curso:").pack(pady=(10, 0))
        ctk.CTkEntry(self, textvariable=self.nome_var, width=400).pack(pady=(0, 10))

        self.tabs = ctk.CTkTabview(self, width=530, height=250)
        self.tabs.pack()

        self.niveis = ["Iniciante", "Intermediario", "Avancado"]
        self.descricoes = {}
        self.questoes = {}

        for nivel in self.niveis:
            tab = self.tabs.add(nivel)
            self._criar_scroll_com_formulario(tab, nivel)

        ctk.CTkButton(self, text="Salvar Curso", command=self.salvar).pack(pady=10)

    def _criar_scroll_com_formulario(self, parent, nivel):
        container = ctk.CTkFrame(parent)
        container.pack(fill="both", expand=True)

        canvas = ctk.CTkCanvas(container, width=510, height=230, bg="#1A1A1A", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(container, orientation="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollable_frame = ctk.CTkFrame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Formulário dentro do scroll
        self.descricoes[nivel] = ctk.CTkTextbox(scrollable_frame, height=60, width=490, border_width=1, corner_radius=6, wrap="word", font=("Arial", 14))
        ctk.CTkLabel(scrollable_frame, text="Descrição do Conteúdo:").pack(anchor="w", padx=5)
        self.descricoes[nivel].pack(pady=5, padx=5)

        self.questoes[nivel] = []

        for i in range(3):
            frame_q = ctk.CTkFrame(scrollable_frame)
            frame_q.pack(pady=5, fill="x", padx=5)

            enunciado = ctk.StringVar()
            alt_a = ctk.StringVar()
            alt_b = ctk.StringVar()
            alt_c = ctk.StringVar()
            resposta = ctk.StringVar(value="alternativa_a")

            ctk.CTkLabel(frame_q, text=f"Questão {i+1} - Enunciado:").pack(anchor="w")
            ctk.CTkEntry(frame_q, textvariable=enunciado, width=490).pack()
            ctk.CTkLabel(frame_q, text="Alternativas:").pack(anchor="w")
            ctk.CTkEntry(frame_q, textvariable=alt_a, placeholder_text="a)").pack()
            ctk.CTkEntry(frame_q, textvariable=alt_b, placeholder_text="b)").pack()
            ctk.CTkEntry(frame_q, textvariable=alt_c, placeholder_text="c)").pack()

            ctk.CTkLabel(frame_q, text="Resposta correta:").pack(anchor="w")
            ctk.CTkOptionMenu(frame_q, values=["alternativa_a", "alternativa_b", "alternativa_c"],
                              variable=resposta).pack()

            self.questoes[nivel].append({
                "enunciado": enunciado,
                "alternativa_a": alt_a,
                "alternativa_b": alt_b,
                "alternativa_c": alt_c,
                "resposta": resposta
            })

    def salvar(self):
        nome = self.nome_var.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Informe o nome do curso.")
            return

        dados = {
            "nome": nome,
            "niveis": []
        }

        for nivel in self.niveis:
            descricao = self.descricoes[nivel].get("1.0", "end").strip()
            questoes_formatadas = []

            for q in self.questoes[nivel]:
                questoes_formatadas.append({
                    "enunciado": q["enunciado"].get(),
                    "alternativa_a": q["alternativa_a"].get(),
                    "alternativa_b": q["alternativa_b"].get(),
                    "alternativa_c": q["alternativa_c"].get(),
                    "resposta": q["resposta"].get()
                })

            dados["niveis"].append({
                "nivel": nivel,
                "descricao": descricao,
                "questoes": questoes_formatadas
            })

        # Tenta carregar os cursos existentes
        caminho_arquivo = "teste.json"
        if os.path.exists(caminho_arquivo):
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                try:
                    cursos = json.load(f)
                except json.JSONDecodeError:
                    cursos = []
        else:
            cursos = []

        # Adiciona o novo curso à lista
        cursos.append(dados)

        # Salva todos os cursos de volta no arquivo
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(cursos, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Sucesso", "Curso salvo com sucesso!")
        trocar_tela(lambda master: TelaPainel(master, usuario_log))

# Tela Niveis
class TelaNiveis(ctk.CTkFrame):
    def __init__(self, master, materia):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")  # Fundo escuro
        self.materia = materia
        self.pack(expand=True) 

        # Carregar os dados dos usuários
        with open("usuarios.json", "r") as f:
            dados = json.load(f)
        
        global usuario_log
        # Encontrar o usuário logado
        usuario_logado = next(
            usuario for usuario in dados["Usuarios"] if usuario["nome"] == usuario_log)

        # Título da matéria
        titulo = ctk.CTkLabel(self, text=self.materia['nome'].capitalize(), font=("Roboto", 20, "bold"))
        titulo.place(x=34, y=20)

        # Posições dos botões
        posicoes = [
            (34, 80),
            (287, 80),
            (34, 140)
        ]

        # Obter os níveis acessados como dicionário
        niveis_acessados = usuario_logado["materias"].get(self.materia["nome"], {}).get("niveis_acessados", {})

        for i, (nivel_nome, nivel_info) in enumerate(niveis_acessados.items()):
            desbloqueado = nivel_info.get("desbloqueado", False)
            cor_texto = "blue" if desbloqueado else "#212121"
            estado = "normal" if desbloqueado else "disabled"
            cor_fundo = "#1f1f1f" if desbloqueado else "#212121"

            btn = ctk.CTkButton(
                self,
                text=nivel_nome.capitalize(),
                width=229,
                height=38,
                fg_color=cor_fundo,
                hover_color="#2c2c2c" if desbloqueado else cor_fundo,
                text_color=cor_texto,
                compound="right",
                corner_radius=6,
                state=estado,
                command=lambda n=nivel_nome: self.ir_para_opcoes(n)
            )

            x, y = posicoes[i]
            btn.place(x=x, y=y)

        # Botão de voltar
        btn_voltar = ctk.CTkButton(
                self,
                text="Voltar",
                width=229,
                height=38,
                fg_color=cor_fundo,
                hover_color="#2c2c2c",
                text_color="#A5A5A5",
                compound="right",
                corner_radius=6,
                command=self.voltar
            )
        btn_voltar.place(x=34, y=320)

    def ir_para_opcoes(self, nivel):
        self.pack_forget()
        trocar_tela(lambda app: TelaOpcoes(app, self.materia, nivel))


    def voltar(self):
        self.pack_forget()
        trocar_tela(TelaCursos)

# Tela de Opções
class TelaOpcoes(ctk.CTkFrame):
    def __init__(self, master, materia, nivel):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")
        self.materia = materia
        self.nivel = nivel

        cor_fundo = "#1f1f1f"
        cor_hover = "#2c2c2c"
        cor_texto = "#A5A5A5"
        cor_texto2 = "blue"

        titulo = ctk.CTkLabel(
            self, 
            text=f"{materia['nome']} - {self.nivel.capitalize()}", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        titulo.place(x=35, y=47)

        sub = ctk.CTkLabel(
            self,
            text="O que você deseja fazer?",
            font=ctk.CTkFont(size=14),
            text_color=cor_texto
        )

        sub.place(x=35, y=85)

        btn_conteudo = ctk.CTkButton(
            self,
            text="📘 Ver conteúdo",
            width=242,
            height=38,
            fg_color=cor_fundo,
            hover_color=cor_hover,
            text_color=cor_texto2,
            corner_radius=6,
            command=lambda n=nivel: self.ir_para_conteudo(n) 
        )
        btn_conteudo.place(x=35, y=132)

        btn_quiz = ctk.CTkButton(
            self,
            text="🧠 Responder Quiz",
            width=242,
            height=38,
            fg_color=cor_fundo,
            hover_color=cor_hover,
            text_color=cor_texto,
            corner_radius=6,
            command=self.responder_quiz
        )
        btn_quiz.place(x=287, y=132)

        ctk.CTkButton(
            self,
            text="← Voltar",
            width=242,
            height=38,
            fg_color="#1f1f1f",
            hover_color="#2c2c2c",
            command=self.voltar
        ).place(x=35, y=320)

        btn_voltat = ctk.CTkButton(
            self,
            text="Voltar",
            width=242,
            height=38,
            fg_color=cor_fundo,
            hover_color=cor_hover,
            text_color=cor_texto,
            corner_radius=6
        )
        btn_voltat.place(x=34, y=520)

    def ir_para_conteudo(self, nivel):
        self.pack_forget()
        trocar_tela(lambda app: TelaConteudo(app, self.materia, nivel))   

    def responder_quiz(self):
        self.place_forget()
        trocar_tela(lambda app: TelaQuiz(app, self.materia, self.nivel)) 

    def voltar(self):
        self.place_forget()
        trocar_tela(lambda app: TelaNiveis(app, self.materia))    

# Tela Conteudo
class TelaConteudo(ctk.CTkFrame):
    def __init__(self, master, materia, nivel):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")
        self.materia = materia
        self.nivel = nivel

        cor_fundo = "#1f1f1f"
        cor_hover = "#2c2c2c"
        cor_texto = "#A5A5A5"
        cor_botao_ativo = "#007bff"

        # Título
        titulo = ctk.CTkLabel(
            self,
            text="Conteúdo",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="white"
        )
        titulo.place(x=35, y=47)

        # Buscar o conteúdo do nível
        texto_conteudo = "Conteúdo não encontrado."
        for nivel_dict in materia.get("niveis", []):
            if nivel_dict["nivel"].lower() == nivel.lower():
                texto_conteudo = nivel_dict.get("descricao", texto_conteudo)
                break

        # Caixa de texto
        self.texto = ctk.CTkTextbox(
            self,
            width=485,
            height=208,
            fg_color="#2A2A2A",
            text_color="white",
            font=ctk.CTkFont(size=13),
            wrap="word"
        )
        self.texto.insert("1.0", texto_conteudo)
        self.texto.configure(state="disabled")
        self.texto.place(x=35, y=99)

        # Botão Voltar
        ctk.CTkButton(
            self,
            text="← Voltar",
            width=229,
            height=38,
            fg_color=cor_fundo,
            hover_color=cor_hover,
            text_color=cor_texto,
            corner_radius=6,
            command=self.voltar
        ).place(x=35, y=334)

        # Botão Responder Quiz
        ctk.CTkButton(
            self,
            text="Responder Quiz →",
            width=229,
            height=38,
            fg_color=cor_fundo,
            hover_color=cor_hover,
            text_color="blue",
            corner_radius=6,
            command=self.responder_quiz
        ).place(x=290, y=334)


    def voltar(self):
        self.place_forget()
        trocar_tela(lambda app: TelaOpcoes(app, self.materia, self.nivel))

    def responder_quiz(self):
        self.place_forget()
        trocar_tela(lambda app: TelaQuiz(app, self.materia, self.nivel))

# Tela Quiz
class TelaQuiz(ctk.CTkFrame):
    def __init__(self, master, materia, nivel):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")
        self.materia = materia
        self.nivel = nivel
        self.questao_atual = 0
        self.resposta_selecionada = ctk.StringVar()
        self.checkboxes = []
        self.acerto = 0
        self.erro = 0

        # Busca questão no JSON
        self.questoes = self.get_questoes()

        self.create_widgets()

    def get_questoes(self):
        for n in self.materia['niveis']:
            if n['nivel'].lower() == self.nivel.lower():
                return n['questoes']
        return []

    def create_widgets(self):
        if not self.questoes:
            ctk.CTkLabel(self, text="Nenhuma questão encontrada.", text_color="red").place(relx=0.5, rely=0.5, anchor="center")
            ctk.CTkButton(
            self,
            text="← Voltar",
            width=130,
            fg_color="#1f1f1f",
            hover_color="#2c2c2c",
            command=self.voltar
        ).place(x=34, y=99)
            return

        questao = self.questoes[self.questao_atual]

        ctk.CTkLabel(self, text=f"Questão {self.questao_atual + 1}", 
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white").place(x=34, y=46, anchor="w")

        # Caixa da pergunta com borda azul
        self.frame_pergunta = ctk.CTkFrame(
            self,
            width=485,
            height=59,
            fg_color="#212121",
            corner_radius=5
        )
        self.frame_pergunta.place(x=34, y=88)
        self.frame_pergunta.pack_propagate(False)  # Impede redimensionamento automático

        ctk.CTkLabel(
            self.frame_pergunta,
            text=questao["enunciado"],
            wraplength=485,
            justify="left",
            text_color="white"
        ).pack(padx=10, pady=10)
        def selecionar_unico(valor):
            self.resposta_selecionada.set(valor)
            for cb in self.checkboxes:
                if cb.cget("onvalue") != valor:
                    cb.deselect()

        y_offset = 0.45
        for key in ["alternativa_a", "alternativa_b", "alternativa_c"]:
            cb = ctk.CTkCheckBox(
                master=self,
                text=questao[key],
                onvalue=key,
                offvalue="",
                variable=ctk.StringVar(),  # variável independente para visual
                text_color="white",
                command=lambda k=key: selecionar_unico(k)
            )
            cb.place(x=34, rely=y_offset, anchor="w")
            self.checkboxes.append(cb)
            y_offset += 0.13

        # Botões
        ctk.CTkButton(
            self,
            text="← Voltar",
            width=229,
            height=38,
            fg_color="#1f1f1f",
            hover_color="#2c2c2c",
            command=self.voltar
        ).place(x=34, y=334)

        ctk.CTkButton(
            self,
            text="Responder →",
            width=229,
            height=38,
            fg_color="blue",
            hover_color="#0056b3",
            command=self.responder
        ).place(x=281, y=334)

    def responder(self):
        resposta = self.resposta_selecionada.get()
        correta = self.questoes[self.questao_atual]["resposta"]
        

        if resposta == correta:
            print("Resposta correta!")
            self.acerto +=1
        else:
            print("Resposta incorreta!")
            self.erro +=1

        # Avançar ou encerrar
        self.questao_atual += 1
        if self.questao_atual < len(self.questoes):
            for widget in self.winfo_children():
                widget.destroy()
            self.create_widgets()
        else:
            trocar_tela(lambda app: TelaResultado(app, self.materia, self.nivel, usuario_log, self.acerto, self.erro))


    def voltar(self):
        self.place_forget()
        trocar_tela(lambda app: TelaOpcoes(app, self.materia, self.nivel))

# Tela Resultado do Quiz
class TelaResultado(ctk.CTkFrame):
    def __init__(self, master, materia, nivel_atual, nome_usuario, acertos, erros):
        super().__init__(master, width=555, height=400, fg_color="#1A1A1A")
        self.materia = materia
        self.nivel = nivel_atual

        # Título
        ctk.CTkLabel(self, text="Quiz Concluído", font=ctk.CTkFont(size=22, weight="bold"), text_color="white")\
            .place(x=209, y=46)

        # Caixa do resultado
        self.frame_resultado = ctk.CTkFrame(self, fg_color="#1A1A1A", border_color="gray", border_width=1, corner_radius=10, width=485, height=208)
        self.frame_resultado.place(x=35, y=99)

        if acertos >= 3:
            ctk.CTkLabel(self.frame_resultado, text=f"PARABÉNS, {nome_usuario.upper()}!", font=ctk.CTkFont(size=18, weight="bold"), text_color="blue")\
                .place(relx=0.5, rely=0.2, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text="Você concluiu uma nova etapa", font=ctk.CTkFont(size=16), text_color="white")\
                .place(relx=0.5, rely=0.4, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text=f"Acertou {acertos}", font=ctk.CTkFont(size=16), text_color="green")\
                .place(relx=0.5, rely=0.6, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text=f"Errou {erros}", font=ctk.CTkFont(size=16), text_color="red")\
                .place(relx=0.5, rely=0.75, anchor="center")
            # Botão Avançar
            ctk.CTkButton(self, text="Avançar Nível →", width=229, height=38,command=lambda: self.avancar(self.materia, self.nivel),
                        fg_color="blue", text_color="white", hover_color="#003cb3")\
                .place(x=290, y=334)
        elif acertos == 2:
            ctk.CTkLabel(self.frame_resultado, text=f"BOM TRABALHO, {nome_usuario.upper()}!", font=ctk.CTkFont(size=18, weight="bold"), text_color="blue")\
                .place(relx=0.5, rely=0.2, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text="Falta pouco para dominar esse nível!", font=ctk.CTkFont(size=16), text_color="white")\
                .place(relx=0.5, rely=0.4, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text=f"Acertou {acertos}", font=ctk.CTkFont(size=16), text_color="green")\
                .place(relx=0.5, rely=0.6, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text=f"Errou {erros}", font=ctk.CTkFont(size=16), text_color="red")\
                .place(relx=0.5, rely=0.75, anchor="center")
            # Botão Avançar
            ctk.CTkButton(self, text="Repetir Quiz", width=229, height=38, command=self.repetir,
                        fg_color="blue", text_color="white", hover_color="#003cb3")\
                .place(x=290, y=334)
        else:
            ctk.CTkLabel(self.frame_resultado, text=f"NÃO DESISTA, {nome_usuario.upper()}!", font=ctk.CTkFont(size=18, weight="bold"), text_color="blue")\
                .place(relx=0.5, rely=0.2, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text="Cada erro é uma chance de aprender!", font=ctk.CTkFont(size=16), text_color="white")\
                .place(relx=0.5, rely=0.4, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text=f"Acertou {acertos}", font=ctk.CTkFont(size=16), text_color="green")\
                .place(relx=0.5, rely=0.6, anchor="center")

            ctk.CTkLabel(self.frame_resultado, text=f"Errou {erros}", font=ctk.CTkFont(size=16), text_color="red")\
                .place(relx=0.5, rely=0.75, anchor="center")  
            # Botão Avançar
            ctk.CTkButton(self, text="Repetir Quiz", width=229, height=38, command=self.repetir,
                        fg_color="blue", text_color="white", hover_color="#003cb3")\
                .place(x=290, y=334)  
        
        

        # Botão Voltar
        ctk.CTkButton(self, text="← Voltar", width=229, height=38, command=self.voltar,
                      fg_color="#2C2C2C", hover_color="#3A3A3A")\
            .place(x=35, y=334)


    def voltar(self):
        self.place_forget()
        trocar_tela(lambda app: TelaOpcoes(app, self.materia, self.nivel))

    def repetir(self):
        self.place_forget()
        trocar_tela(lambda app: TelaQuiz(app, self.materia, self.nivel))
   

    def avancar(self, materia, nivel_atual):
        materia_nome = materia["nome"]
        niveis_ordem = ["Iniciante", "Intermediario", "Avancado"]

        try:
            proximo_indice = niveis_ordem.index(nivel_atual) + 1
            proximo_nivel = niveis_ordem[proximo_indice]
        except IndexError:
            messagebox.showinfo("Fim de Curso", "Você já está no nível mais avançado.")
            return

        with open("usuarios.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        for usuario in dados["Usuarios"]:
            if usuario["nome"] == usuario_log:
                if "materias" not in usuario:
                    usuario["materias"] = {}

                if materia_nome not in usuario["materias"]:
                    usuario["materias"][materia_nome] = {
                        "niveis_acessados": {
                            nivel_atual: {"desbloqueado": True},
                            proximo_nivel: {"desbloqueado": False}
                        }
                    }

                niveis = usuario["materias"][materia_nome]["niveis_acessados"]

                if proximo_nivel in niveis:
                    niveis[proximo_nivel]["desbloqueado"] = True
                else:
                    niveis[proximo_nivel] = {"desbloqueado": True}

                break

        with open("usuarios.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Nível Liberado", f"O nível '{proximo_nivel}' foi desbloqueado com sucesso!")
        
        self.pack_forget()
        trocar_tela(lambda app: TelaOpcoes(app, self.materia, proximo_nivel))  

# Início da aplicação
trocar_tela(TelaLogin)
app.mainloop()