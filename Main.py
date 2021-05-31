import random
import time
import config
import hashlib

#Função para ler a base origem
def LerBase(ArquivoBase):
    with open(ArquivoBase) as arquivo:
        linhas = arquivo.readlines()

    return linhas

#Função que gera a base segura (convertida)
def GerarBaseSegura(ArquivoBaseSeguraSaida, linhas, salt):
    arquivo = open(ArquivoBaseSeguraSaida, "w")

    for linha in linhas:
        linhaSplit = linha.split('|')
        usuario = linhaSplit[1]
        senha = linhaSplit[2]
        string = f"{usuario}{senha}{salt}"
        hash = hashlib.sha256(string.encode('utf-8')).hexdigest()

        arquivo.write(f"|{usuario}|{hash}|\n")
    arquivo.close()


#Função para autenticar os usuários da base pela senha
def AutenticarUsuarioBase(linhasBase, usuario, senha):
    valido = (x for x in linhasBase if linhasBase.split('|')[1] == usuario and linhasBase.split('|')[2] == senha)

    if valido is not None:
        return True
    else:
        return False

#Função para autenticar os usuários da base pela hash
def AutenticarUsuarioBaseSegura(linhasBase, usuario, hash, salt):
    string = f"{usuario}{hash}{salt}"
    hash = hashlib.sha256(string.encode('utf-8')).hexdigest()
    valido = (x for x in linhasBase if linhasBase.split('|')[1] == usuario and linhasBase.split('|')[2] == hash)

    if valido is not None:
        return True
    else:
        return False

#Principal
def main():
    ArquivoBaseEntrada = config.ArquivoBaseEntrada
    ArquivoBaseSeguraSaida = config.ArquivoBaseSeguraSaida
    Salt = config.Salt

    linhasBase = LerBase(ArquivoBaseEntrada)
    tamanhoBase = len(linhasBase)
    ini = time.time()
    GerarBaseSegura(ArquivoBaseSeguraSaida, linhasBase, Salt)
    fim = time.time()
    print("Tempo para gerar base segura: ", fim - ini, " segundos.")

    linhasBaseSegura = LerBase(ArquivoBaseSeguraSaida)

    aux = int(tamanhoBase / 2)  # 50% da base
    print(f"Quantidade de validações para teste: {aux} usuários.")
    ini = time.time()
    for i in range(0, aux):
        index = random.randint(0, tamanhoBase - 1)
        linha = linhasBase[index]
        linhaSplit = linha.split('|')
        usuario = linhaSplit[1]
        senha = linhaSplit[2]

        AutenticarUsuarioBase(linhasBase, usuario, senha)

    fim = time.time()
    print("Tempo para execução da validação por senha: ", fim - ini, " segundos.")
    ini = time.time()
    for i in range(0, aux):
        index = random.randint(0, tamanhoBase - 1)
        linha = linhasBase[index]
        linhaSplit = linha.split('|')
        usuario = linhaSplit[1]
        hash = linhaSplit[2]

        AutenticarUsuarioBaseSegura(linhasBaseSegura, usuario, hash, Salt)
    fim = time.time()
    print("Tempo para execução da validação por hash: ", fim - ini, " segundos.")

main()
