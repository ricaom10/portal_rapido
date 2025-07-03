usuarios = {}

def create_user(nome, senha):
    usuarios[nome] = senha

def get_user(nome):
    return usuarios.get(nome)
