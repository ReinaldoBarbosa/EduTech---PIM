import customtkinter as ctk
from cryptography.fernet import Fernet
import json

# Carrega os dados
with open("teste.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

# Configuração aparência
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

# Função para criptografar senha (não utilizada no momento)
chave_secreta = Fernet.generate_key()
fernet = Fernet(chave_secreta)

# Criar a janela principal
app = ctk.CTk()
app.title('EduTec')
app.geometry('400x400')

frame_niveis = ctk.CTkFrame(app)

# Função para limpar o input
def limpa_input(event):
    event.delete(0, 'end')

    caracteres_minimas.configure(text_color='red')
    letra_maiuscula.configure(text_color='red')
    letra_minuscula.configure(text_color='red')
    numeros.configure(text_color='red')
    caracteres_especiais.configure(text_color='red')

# Função para trocar de tela
def trocar_tela(tela):
    frame_login.pack_forget()
    frame_cadastro.pack_forget()
    frame_niveis.pack_forget()
    tela.pack(pady=20, padx=20)

    resultado_cadastro.configure(text='')
    resultado_login.configure(text='')

# Verificar força da senha em tempo real
def verificar_senha(*args):
    senha = campo_senha_cadastro.get()

    caracteres_minimas.configure(text_color='green' if len(senha) >= 8 else 'red')
    letra_maiuscula.configure(text_color='green' if any(char.isupper() for char in senha) else 'red')
    letra_minuscula.configure(text_color='green' if any(char.islower() for char in senha) else 'red')
    numeros.configure(text_color='green' if any(char.isdigit() for char in senha) else 'red')
    caracteres_especiais.configure(text_color='green' if any(char in "!@#$%^&*()_+" for char in senha) else 'red')

# Função para cadastro
def cadastro():
    nome = campo_usuario_cadastro.get()
    senha = campo_senha_cadastro.get()

    try:
        with open('teste.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'Usuarios': []}

    if nome == "" or senha == "":
        resultado_cadastro.configure(text="Preencha todos os campos!", text_color='red')
        return

    for usuario in dados['Usuarios']:
        if usuario['nome'] == nome:
            resultado_cadastro.configure(text='Usuário já existe!', text_color='red')
            return

    dados['Usuarios'].append({
        'nome': nome,
        'senha': senha
    })

    with open('teste.json', 'w', encoding='utf-8') as arq:
        json.dump(dados, arq, indent=4, ensure_ascii=False)

    trocar_tela(frame_login)
    limpa_input(campo_usuario_cadastro)
    limpa_input(campo_senha_cadastro)

    resultado_cadastro.configure(text='Usuário cadastrado com sucesso!', text_color='green')

# Função para login
def login():
    usuario = campo_usuario.get()
    senha = campo_senha.get()

    try:
        with open('teste.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'Usuarios': []}

    if usuario == "" or senha == "":
        resultado_login.configure(text='Usuario ou Senha incorretos.', text_color='red')
        return

    for user in dados['Usuarios']:
        if user['nome'] == usuario and user['senha'] == senha:
            frame_login.pack_forget()
            TelaCursos(app)
            limpa_input(campo_usuario)
            limpa_input(campo_senha)
            return

    resultado_login.configure(text='Usuário ou senha incorretos.', text_color='red')


class TelaCursos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text="Escolha a matéria:").pack(pady=10)

        for materia in dados["Materias"]:
            ctk.CTkButton(self, text=materia["nome"],
                          command=lambda m=materia: self.ir_para_niveis(m)).pack(pady=5)

        # Botão de sair
        self.botao_sair = ctk.CTkButton(self, text="❌ Sair", command=self.sair)
        self.botao_sair.pack(pady=10)

    def ir_para_niveis(self, materia):
        self.pack_forget()
        TelaNiveis(app, materia)

    def sair(self):
        # Fecha a aplicação (alternativamente, você pode fazer algo como voltar para a tela inicial)
        app.quit()  # Fecha a aplicação (caso deseje sair)


class TelaNiveis(ctk.CTkFrame):
    def __init__(self, master, materia):
        super().__init__(master)
        self.materia = materia
        self.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text=f"Matéria: {materia['nome']}").pack(pady=10)
        ctk.CTkLabel(self, text="Escolha o nível:").pack(pady=5)

        for nivel in materia["niveis"]:
            ctk.CTkButton(self, text=nivel["nivel"],
                          command=lambda n=nivel: self.ir_para_opcoes(n)).pack(pady=5)

    def ir_para_opcoes(self, nivel):
        self.pack_forget()
        TelaOpcoes(app, self.materia, nivel)


class TelaOpcoes(ctk.CTkFrame):
    def __init__(self, master, materia, nivel):
        super().__init__(master)
        self.materia = materia
        self.nivel = nivel
        self.pack(fill="both", expand=True)

        ctk.CTkLabel(self, text=f"{materia['nome']} - {nivel['nivel']}", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self, text="O que você deseja fazer?").pack(pady=10)

        ctk.CTkButton(self, text="📘 Ver conteúdo", command=self.ver_conteudo).pack(pady=5)
        ctk.CTkButton(self, text="🧠 Responder Quiz", command=self.iniciar_quiz).pack(pady=5)

    def ver_conteudo(self):
        self.pack_forget()
        TelaConteudo(app, self.materia, self.nivel)

    def iniciar_quiz(self):
        self.pack_forget()
        TelaQuiz(app, self.materia, self.nivel)  # Corrigido: Passar 'nivel' corretamente para TelaQuiz


class TelaConteudo(ctk.CTkFrame):
    def __init__(self, master, materia, nivel):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        ctk.CTkLabel(self, text=f"Conteúdo - {materia['nome']} ({nivel['nivel']})", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=10)

        texto = ctk.CTkTextbox(self, wrap="word", width=500, height=200)
        texto.insert("1.0", nivel["descricao"])
        texto.configure(state="disabled")
        texto.pack(pady=10)

        ctk.CTkButton(self, text="🧠 Iniciar Quiz",
                      command=lambda: self.iniciar_quiz(nivel)).pack(pady=5)

    def iniciar_quiz(self, nivel):
        self.pack_forget()
        TelaQuiz(app, self.materia, nivel)  # Corrigido: Passar 'nivel' corretamente para TelaQuiz


class TelaQuiz(ctk.CTkFrame):
    def __init__(self, master, materia, nivel):
        super().__init__(master)
        self.questoes = nivel["questoes"]  # Usar 'nivel' para pegar as questões
        self.materia = materia
        self.index = 0
        self.pontuacao = 0  # Contador de acertos
        self.pack(fill="both", expand=True)
        self.label_pergunta = ctk.CTkLabel(self, text="", wraplength=500)
        self.label_pergunta.pack(pady=20)
        self.botoes = []

        for i in range(3):
            botao = ctk.CTkButton(self, text="", command=lambda i=i: self.responder(i))
            botao.pack(pady=5)
            self.botoes.append(botao)

        # Botão de voltar para cursos
        self.botao_voltar = ctk.CTkButton(self, text="🔙 Voltar para Cursos", command=self.voltar_para_cursos)
        self.botao_voltar.pack_forget()  # Inicialmente escondido

        # Escondendo o botão de avançar
        self.botao_avancar = ctk.CTkButton(self, text="➡ Avançar para o Próximo Nível", command=self.avancar_para_nivel_seguinte)
        self.botao_avancar.pack_forget()  # Inicialmente escondido
        
        self.mostrar_questao()

    def mostrar_questao(self):
        if self.index < len(self.questoes):
            q = self.questoes[self.index]
            self.label_pergunta.configure(text=q["enunciado"])
            self.botoes[0].configure(text=q["alternativa_a"])
            self.botoes[1].configure(text=q["alternativa_b"])
            self.botoes[2].configure(text=q["alternativa_c"])
        else:
            # Fim do quiz, exibe apenas o botão de voltar para cursos
            resultado = f"Fim do Quiz! Sua pontuação: {self.pontuacao}/{len(self.questoes)}"
            self.label_pergunta.configure(text=resultado)
            for botao in self.botoes:
                botao.pack_forget()

            # Mostra apenas o botão de voltar para cursos
            self.botao_voltar.pack(pady=10)

    def responder(self, i):
        q = self.questoes[self.index]
        resposta_correta = q["resposta"]

        if (i == 0 and resposta_correta == "alternativa_a") or \
           (i == 1 and resposta_correta == "alternativa_b") or \
           (i == 2 and resposta_correta == "alternativa_c"):
            self.pontuacao += 1
            resultado = "Resposta correta! ✅"
        else:
            resultado = f"Resposta errada! ❌ A resposta correta era: {q[resposta_correta]}"  # Corrigido aqui

        self.index += 1
        self.label_pergunta.configure(text=resultado)
        self.after(1000, self.mostrar_questao)  # Espera 1 segundo antes de mostrar a próxima questão

    def voltar_para_cursos(self):
        self.pack_forget()
        TelaCursos(app)  # Aqui é o que acontece ao clicar no botão de voltar para cursos

    def avancar_para_nivel_seguinte(self):
        pass  # A função foi desnecessária, pois removemos o botão de avançar



# ---------------- Tela de Login -----------------
frame_login = ctk.CTkFrame(app)

ctk.CTkLabel(frame_login, text="Usuário").pack(pady=5)
campo_usuario = ctk.CTkEntry(frame_login, placeholder_text="Digite o Usuario")
campo_usuario.pack(pady=5)

ctk.CTkLabel(frame_login, text="Senha").pack(pady=5)
campo_senha = ctk.CTkEntry(frame_login, placeholder_text="Digite sua Senha", show='*')
campo_senha.pack(pady=5)

resultado_login = ctk.CTkLabel(frame_login, text="")
resultado_login.pack(pady=10)

ctk.CTkButton(frame_login, text="Login", command=login).pack(pady=5)
ctk.CTkButton(frame_login, text="Cadastrar", command=lambda: trocar_tela(frame_cadastro)).pack(pady=5)

# ---------------- Tela de Cadastro -----------------
frame_cadastro = ctk.CTkFrame(app)

ctk.CTkLabel(frame_cadastro, text="Nome de Usuário").pack(pady=5)
campo_usuario_cadastro = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite um nome")
campo_usuario_cadastro.pack(pady=5)

ctk.CTkLabel(frame_cadastro, text="Senha").pack(pady=5)
campo_senha_cadastro = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite uma senha", show='*')
campo_senha_cadastro.pack(pady=5)

caracteres_minimas = ctk.CTkLabel(frame_cadastro, text="Mínimo 8 caracteres")
caracteres_minimas.pack(pady=0)

letra_maiuscula = ctk.CTkLabel(frame_cadastro, text="Letra Maiúscula")
letra_maiuscula.pack(pady=0)

letra_minuscula = ctk.CTkLabel(frame_cadastro, text="Letra Minúscula")
letra_minuscula.pack(pady=0)

numeros = ctk.CTkLabel(frame_cadastro, text="Números")
numeros.pack(pady=0)

caracteres_especiais = ctk.CTkLabel(frame_cadastro, text="Caracter Especial")
caracteres_especiais.pack(pady=0)

resultado_cadastro = ctk.CTkLabel(frame_cadastro, text="")
resultado_cadastro.pack(pady=10)

ctk.CTkButton(frame_cadastro, text="Cadastrar", command=cadastro).pack(pady=5)
ctk.CTkButton(frame_cadastro, text="Voltar ao Login", command=lambda: trocar_tela(frame_login)).pack(pady=5)

campo_senha_cadastro.bind("<KeyRelease>", verificar_senha)

# Inicia na tela de login
trocar_tela(frame_login)

# Executa o app
app.mainloop()
