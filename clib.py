#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

# feitor por: mrxrobot
# v0.2

from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from termcolor import colored
from unicodedata import normalize

#modulos para executar comandos no sistema
import sys
import os
import time

# modulo para escolhar algo aleatorio, no caso, o user-agent
from random import choice



#define uma variavel contendo a mensagem de inicio programa
msg=colored("""                                     
                                      bbbbbbbb            
                     lllllll    iiii  b::::::b            
                     l:::::l   i::::i b::::::b            
                     l:::::l    iiii  b::::::b            
                     l:::::l           b:::::b            
    cccccccccccccccc  l::::l  iiiiiii  b:::::bbbbbbbbb    
  cc:::::::::::::::c  l::::l  i:::::i  b::::::::::::::bb  
 c:::::::::::::::::c  l::::l   i::::i  b::::::::::::::::b 
c:::::::cccccc:::::c  l::::l   i::::i  b:::::bbbbb:::::::b
c::::::c     ccccccc  l::::l   i::::i  b:::::b    b::::::b
c:::::c               l::::l   i::::i  b:::::b     b:::::b
c:::::c               l::::l   i::::i  b:::::b     b:::::b
c::::::c     ccccccc  l::::l   i::::i  b:::::b     b:::::b
c:::::::cccccc:::::c l::::::l i::::::i b:::::bbbbbb::::::b
 c:::::::::::::::::c l::::::l i::::::i b::::::::::::::::b 
  cc:::::::::::::::c l::::::l i::::::i b:::::::::::::::b  
    cccccccccccccccc llllllll iiiiiiii bbbbbbbbbbbbbbbb   {v}


""".format(v=colored("v0.2","green")),"red")

#define uma variavel contendo as informaçoes de ajuda
msg_help=colored("""
 _            _        
| |__    ___ | | _ __  
| '_ \  / _ \| || '_ \ 
| | | ||  __/| || |_) |
|_| |_| \___||_|| .__/ 
                |_|   
""","red") + colored("""
------------------------------
 Como pesquisar por um livro?
------------------------------ 

Para pesquisar por um livro informe o nome do livro ou nome do autor.

> nome do livro ou autor [enter]

-----------------------------
 Comandos dentro do programa 
-----------------------------
/h       --> Exibe este menu de ajuda.

/setd [/home/usuario/Downloads] --> configura um diretório padrão para armazenar os livros baixados.   

[v]oltar --> Volta ao menu anterior.
/q       --> Encerra o programa.

---------------------------------
 Como baixar o livro pesquisado? 
---------------------------------

Quando o usuário informar o nome do livro ou do autor, o programa 
vai iniciar a busca por livros correspondentes as informações passadas pelo 
usuário.
Quando a pesquisa terminar, será exibido em tela a lista dos livros encontrados,
juntamente com um número de identificação para cada link de download.
Para baixar o livro desejado, basta informar o número do link seguido de [enter]

""","yellow") 

# Agora é hora da brincadeira realmente começar
# Primeiro irei criar uma classe que terá os métodos e argumetos para 
# realizar o conexão entre o computador e o servidor onde estão os arquivos.

user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; explorer/3.5; Win7) KHTML/3.5.5 (like Gecko) (windows 7)',
        'Mozilla/5.0 (X11; U; unknow i686; en-US; rv:1.8.0.12) Gecko/20070731 unknow/dapper-security Firefox/1.5.0.12', 
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
]


def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')

def limpa():
    os.system("clear")
    print(msg)
    

#arquivo de configuração do diretorio de download
dconf = os.path.join(os.path.expanduser('~'),".clib-config")

#cores das opções do programa (quit, help, v, enter, exit)
e =colored('/q','red')
h = colored("/h","yellow")
vv=colored('v','green')
h = colored("/h","yellow")
enter=colored("enter","red")

class Connect:
    print(msg)
    def __init__(self, s, format_arq=".pdf"):
        # Comecei inicializado a classe com 2 argumetos
        # o primeiro 's', recebera o nome do livro
        # o segundo  'format_arq' define o formato do livro a ser baixado
    
        self.s = remover_acentos(s).replace("'", '')
        self.ext = format_arq
        self.verifica()

        if os.path.exists(dconf):
            with open(dconf, "r") as f:
                self.dd = f.readline().strip('\r\n')
                if self.dd[-1] != "/": self.dd += "/"

                if os.access(self.dd, os.F_OK) and os.access(self.dd, os.W_OK):
                    self.dd = self.dd

                else:
                    limpa()
                    print(colored("Falha ao adicioar diretório %s" %(colored(self.dd,"green")),"red"))
                    time.sleep(6)
                    
                    limpa()
                    print(colored("Configurando diretório temporário para armazenar os arquivos...","red"))
                    time.sleep(6)

                    if os.access("/tmp/", os.W_OK):
                        limpa()
                        print(colored("Diretório onde os livros serão salvos: %s" %(colored("/tmp/","green")),"red"))
                        time.sleep(6)
                        
                        self.dd = "/tmp/"
                        self.writeconfig()
                    else:
                        print(colored("Não foi possivel configurar o diretório de download!","red"))
                        self.volta()
        else:
            self.dd = "/tmp/"
            self.writeconfig()
    
    def writeconfig(self):
        with open(dconf, "w") as f:
            if self.dd[-1] != "/": self.dd += "/"
            if os.access(self.dd, os.F_OK) and os.access(self.dd, os.W_OK):
                print(colored("Novo diretório configurado com sucesso!","red"))
                time.sleep(4)
                f.write(self.dd)
            
            else:
                limpa()
                print(colored("Falha ao adicoiar diretório %s" %(colored(self.dd,"green")),"red"))
                time.sleep(6)
                
                limpa()
                print(colored("Configurando diretório temporário para armazenar os arquivos...","red"))
                time.sleep(6)

                if os.access("/tmp/", os.W_OK):
                    limpa()
                    print(colored("Diretório onde os livros serão salvos: %s" %(colored("/tmp/","green")),"red"))
                    time.sleep(6)
                    self.dd = "/tmp/"
                    f.write(self.dd)
    
                else:
                    print(colored("Não foi possivel configurar o diretório de download!","red"))
                    self.volta()

    
    def volta(self):
        os.system("clear")
        print(msg)

        try:
            Connect(str(input(f"Insira o nome do livro ou [{h}] para ajuda ou [{e}] para sair.\n> ").strip(" "))).down()  

        except KeyboardInterrupt:
            sys.exit(0)

    def verifica(self):
        if self.s == "/h":
            os.system("clear")
            print(msg_help)

            try:
                input(f"> Voltar para o menu principal [{enter}]")

            except KeyboardInterrupt:
                sys.exit(0)
            self.volta()


        elif self.s == "/q":
            sys.exit(0)


        elif self.s == "-h":
            print("Usage: clib.py [-hv] [/setd] STRING") 
            sys.exit(0)


        elif self.s == "-v":
            print("clib v0.2 by mrxrobot\n\nhttps://notabug.org/mrxrobot_/clib\n\n")
            sys.exit(0)


        elif self.s.startswith("-"):
            print("Opção inválida")
            sys.exit(0)


        elif self.s.split(" ")[0] == "/setd": 
            self.dd = self.s.split(" ")[1]
            self.writeconfig()
            self.volta()


        elif self.s.startswith("/"):
            print(colored("Opção inválida!", "red"))
            time.sleep(4)
            self.volta()


        elif self.s == "":
            print(colored("Erro, informe pelo menos o nome do livro ou do autor!\n","red"))
            time.sleep(5)
            self.volta()

        else:
            if teste == None:
                self.s = self.s.strip(" ").replace(' ', '+').replace('"', "")
            elif teste == "arg":
                self.s = self.s.strip(" ").replace(' ', '+').replace('"', "")
        return True

    def down(self):
        if self.verifica():
            os.system("clear")
            print(msg)
            try:
                print("Pesquisando por {s}".format(s=colored("'{s}'".format(s=self.s.replace('+', ' ')),"yellow")))
                self.links = []
                self.lista = {}
                self.url = f"http://lelivros.bid/?x=0&y=0&s={self.s}"
            
                self.req = Request(
                self.url,
                data=None,
                headers={'User-Agent': choice(user_agents)})
            
                self.resp = urlopen(self.req).read()
                self.soup = BeautifulSoup(self.resp, "html.parser")
            
                self.links = [x.get('href') for x in self.soup.find_all('a', {'class':' button product_type_simple'})]          
            except KeyboardInterrupt:
                sys.exit(0)

            i = 0
            self.nome = []
            for j in self.links:
                self.lista[ str(i)] = str(j)
                self.nome.append(str(self.soup.find_all(
                    'li', {'class':'post-17105 product type-product status-publish has-post-thumbnail hentry first instock'
                        })[i].find('a').find('h3').text))
 
                i += 1
            
            os.system("clear")
            print(msg)
            
            def lista_livro_d():
                cores = ['magenta', 'cyan']
                l = 0
                
                if len(self.lista) > 0:
                    print("\n{n}\t\t{livro}".format(n=colored("Numero","red"), livro=colored("Livro\n","red")))
                    for x in  self.lista:
                        #nome = self.lista[x].split("/"+self.lista[x].split('/')[4].split('-')[0] + "-")[1][:-1]
                        print("[" + colored(str(x), cores[l]) + "]\t\t" + colored(self.nome[int(x)].upper(), cores[l]))
                        l += 1
                        if l == len(cores):
                            l = 0
                        
                    print(" ")
                else:   
                    print(colored("Livro não encontrado!".upper(), "red"))

                    try:
                        input(f"> Voltar para o menu principal [{enter}]")

                    except KeyboardInterrupt:
                        sys.exit(0)
                    self.volta()

            lista_livro_d()
            try:
                self.op = str(input(f'\n\nInforme o número do download ou [{e}] para sair [{vv}]oltar\n> '))
                
            except KeyboardInterrupt:
                sys.exit(0)


            def reporthook(blocknum, blocksize, totalsize):
                readsofar = blocknum * blocksize
                if totalsize > 0:
                    percent =readsofar * 1e2 / totalsize
                    s = "\rBaixando:\t{a}\t:\t%5.0f%% %*d".format(a=self.nome[int(self.op)]) % (
                            percent, len(str(totalsize)), readsofar)
                    sys.stderr.write(s)

                    if readsofar >= totalsize:
                        sys.stderr.write("\n")
                else:
                    sys.stderr.write("read %d\n" %(readsofar,))

            
            def testa():
                while self.op != "/q" and self.op != "v":
                    if self.op.isalpha(): break
                    if self.op not in self.lista.keys(): break

                    self.req = Request(
                    self.lista[ str(self.op) ],
                    data=None,
                    headers={'User-Agent':choice(user_agents)}
                    )
                    self.resp = urlopen( self.req).read()
                    self.soup = BeautifulSoup( self.resp, "html.parser" )
                    self.d = [
                            x.get('href').split('&')[0] 
                            for x in self.soup.find_all('div', {'class':'links-download'})[0].find_all('a') 
                            if x.get('href') not in "javascript:void(0);" 
                            ]
                   
                    os.system("clear")
                    print(msg)
                    lista_livro_d()

                    try:
                        urlretrieve(self.d[0], self.dd + self.nome[int(self.op)] + self.ext, reporthook)
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except:
                        print("Erro no download!")
                    os.system("clear")
                    print(msg)
                    lista_livro_d()
                    print("{a} {b}\n\n".format( a=colored("\nArquivo salvo em: ", "green"), b=colored(self.dd + self.nome[int(self.op)] + self.ext, "red") ) )
                    time.sleep(10)
                    os.system("clear")
                    print(msg)
                    lista_livro_d()
                    try:
                        self.op = str(input(f'\n\nInforme o número do download ou [{e}] para sair [{vv}]voltar\n> '))
                    except KeyboardInterrupt:
                        sys.exit(0)
                
                if self.op == "/q": sys.exit(0)
                elif self.op == "v": self.volta()
                else: 
                    print(colored("Opção inválida", "red"))
                    time.sleep(3)
                    os.system("clear")
                    print(msg)
                    lista_livro_d()
                            
                    try:
                        self.op = str(input(f'\n\nInforme o número do download ou [{e}] para sair [{vv}]voltar\n> '))
                    except KeyboardInterrupt:
                        sys.exit(0)
                    
                    testa()
            testa()
            
if len(sys.argv) < 2:
    teste = None
    try:
        op=str(input(f"Insira o nome do livro ou [{h}] para ajuda ou [{e}] para sair.\n> ")).strip(" ")

    except KeyboardInterrupt:
        sys.exit(0)
    
    download = Connect(op)
    download.down()

else:
    teste = "arg"
    arg = []

    for i in range(int(len(sys.argv))):
        arg.append(sys.argv[i])
    
    op = " ".join(arg[1:])
    download = Connect(op)
    download.down()

