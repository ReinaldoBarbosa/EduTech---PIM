import customtkinter as ctk
from cryptography.fernet import Fernet
import json
import time

# Configuração aparência
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

# Função para criptografar senha
chave_secreta = Fernet.generate_key()
fernet = Fernet(chave_secreta)

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
    frame_principal.pack_forget()
    tela.pack(pady=20, padx=20)

    resultado_cadastro.configure(text='')
    resultado_login.configure(text='')

# Verificar força da senha em tempo real
def verificar_senha(*args):
    senha = campo_senha_cadastro.get()

    if len(senha) >= 8:
        caracteres_minimas.configure(text_color='green')
    else:
        caracteres_minimas.configure(text_color='red')

    if any(char.isupper() for char in senha):
        letra_maiuscula.configure(text_color='green')
    else:
        letra_maiuscula.configure(text_color='red')

    if any(char.islower() for char in senha):
        letra_minuscula.configure(text_color='green')
    else:
        letra_minuscula.configure(text_color='red')

    if any(char.isdigit() for char in senha):
        numeros.configure(text_color='green')
    else:
        numeros.configure(text_color='red')

    if any(char in "!@#$%^&*()_+" for char in senha):
        caracteres_especiais.configure(text_color='green')
    else:
        caracteres_especiais.configure(text_color='red')

# Função para cadastro
def cadastro():
    nome = campo_usuario_cadastro.get()
    senha = campo_senha_cadastro.get()

    # Carrega ou cria o arquivo JSON
    try:
        with open('teste.json', 'r', encoding='utf-8') as arq:
            dados = json.load(arq)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {'Usuarios': []} 


    # Verifica campos vazios
    if nome == "" or senha == "":
        resultado_cadastro.configure(text="Preencha todos os campos!", text_color='red')
        return
    

    # Verifica se o usuário já existe
    for usuario in dados['Usuarios']:
        if usuario['nome'] == nome:
            resultado_cadastro.configure(text='Usuário já existe!', text_color='red')
            return   


    # Adiciona novo usuário
    dados['Usuarios'].append({
        'nome': nome,
        'senha': senha
    })

    # Salva no JSON
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

    # Verifica o login
    for user in dados['Usuarios']:
        if user['nome'] == usuario and user['senha'] == senha:
            abrir_tela_principal()
            limpa_input(campo_usuario)
            limpa_input(campo_senha)
            return           
    resultado_login.configure(text='Usuário ou senha incorretos.', text_color='red')

# Função para abrir a tela principal após login
def abrir_tela_principal():
    trocar_tela(frame_principal)
    texto_bem_vindo.configure(text=f"Bem-vindo, {campo_usuario.get()}!")

# Função para abrir a tela de questões
def abrir_questoes(materia):
    global questoes, indice_questao, pontuacao

    questoes = materia['questoes']
    indice_questao = 0
    pontuacao = 0
    botao_a.pack(pady=5)
    botao_b.pack(pady=5)
    botao_c.pack(pady=5)

    exibir_questao()
    trocar_tela(frame_questoes)

# Exibe cada questão
def exibir_questao():
    global indice_questao

    if indice_questao < len(questoes):
        questao_atual = questoes[indice_questao]

        texto_questao.configure(text=questao_atual['enunciado'], text_color='gray')
        botao_a.configure(text=questao_atual['alternativa_a'])
        botao_b.configure(text=questao_atual['alternativa_b'])
        botao_c.configure(text=questao_atual['alternativa_c'])
    else:
        texto_questao.configure(text=f"Você acertou {pontuacao} de {len(questoes)} questões!", text_color='gray')
        botao_a.pack_forget()
        botao_b.pack_forget()
        botao_c.pack_forget()
        botao_voltar.pack(pady=5)

# Verificar resposta
def verificar_resposta(resposta):
    global indice_questao, pontuacao

    if resposta == questoes[indice_questao]['resposta']:
        texto_questao.configure(text="Correto ✅", text_color='green')
        pontuacao += 1
    else:
        texto_questao.configure(text="Incorreto ❌", text_color='red')

    app.update()  # Atualiza a tela para mostrar o resultado
    time.sleep(2)  # Delay de 2 segundos
    
    indice_questao += 1
    exibir_questao()

def voltar_para_inicio():
    frame_questoes.pack_forget() 
    botao_voltar.pack_forget()
    trocar_tela(frame_principal)  # Isso seria uma função que redefine o layout inicial do quiz


# Criar a janela principal
app = ctk.CTk()
app.title('EduTec')
app.geometry('400x400')

# ---------------- Tela de Login -----------------
frame_login = ctk.CTkFrame(app)

ctk.CTkLabel(frame_login, text="Usuário").pack(pady=5)
campo_usuario = ctk.CTkEntry(frame_login, placeholder_text="Digite o Usuario")
campo_usuario.pack(pady=5)

ctk.CTkLabel(frame_login, text="Senha").pack(pady=5)
campo_senha = ctk.CTkEntry(frame_login, placeholder_text="Digite sua Senha" ,show='*')
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
campo_senha_cadastro = ctk.CTkEntry(frame_cadastro, placeholder_text="Digite uma senha" ,show='*')
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

# Conecta a função de verificação em tempo real
campo_senha_cadastro.bind("<KeyRelease>", verificar_senha)
# ----------------- Tela de Questões -----------------
frame_questoes = ctk.CTkFrame(app)
texto_questao = ctk.CTkLabel(frame_questoes, text="")
texto_questao.pack(pady=10)

botao_a = ctk.CTkButton(frame_questoes, text="", command=lambda: verificar_resposta('alternativa_a'))
botao_a.pack(pady=5)

botao_b = ctk.CTkButton(frame_questoes, text="", command=lambda: verificar_resposta('alternativa_b'))
botao_b.pack(pady=5)

botao_c = ctk.CTkButton(frame_questoes, text="", command=lambda: verificar_resposta('alternativa_c'))
botao_c.pack(pady=5)

botao_voltar = ctk.CTkButton(frame_questoes, text="Voltar para incio", command=lambda: voltar_para_inicio())
botao_voltar.pack_forget()

# ---------------- Tela Principal -----------------
frame_principal = ctk.CTkFrame(app)

texto_bem_vindo = ctk.CTkLabel(frame_principal, text="", font=('Arial', 18))
texto_bem_vindo.pack(pady=20)

# Tenta abrir o arquivo JSON
try:
    with open('teste.json', 'r', encoding='utf-8') as arq:
        dados = json.load(arq)
except (FileNotFoundError, json.JSONDecodeError):
    dados = {'Materias': []}  # Garantir que exista uma chave 'Materias'

# Iterar sobre as matérias
for materia in dados['Materias']:
    # Criar botão para cada matéria
    ctk.CTkButton(frame_principal, text=materia['nome'], command=lambda m=materia: abrir_questoes(m)).pack(pady=10)


ctk.CTkButton(frame_principal, text="Sair", command=lambda: trocar_tela(frame_login)).pack(pady=10)

# Inicia na tela de login
trocar_tela(frame_login)

# Executa o app
app.mainloop()