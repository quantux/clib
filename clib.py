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

# Limpar a tela
os.system("clear")

#define uma variavel contendo a mensagem de inicio programa
msg=colored("""
  
       _  _  _     
  ___ | |(_)| |__  
 / __|| || || '_ \ 
| (__ | || || |_) |
 \___||_||_||_.__/ {v}
 
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


#cores das opções do programa (quit, help, v, enter, exit)
e =colored('/q','red')
h = colored("/h","yellow")
vv=colored('v','green')
h = colored("/h","yellow")
enter=colored("enter","red")

class Connect:
    print(msg)
    def __init__(self, s, format_arq="pdf"):
        # Comecei inicializado a classe com 2 argumetos
        # o primeiro 's', recebera o nome do livro
        # o segundo  'format_arq' define o formato do livro a ser baixado
    
        self.s = remover_acentos(s)
        self.ext = format_arq
        self.verifica()

        if os.path.exists("config"):
            with open("config", "r") as f:
                self.dd = f.readline().strip('\r\n')
                if not self.dd.endswith("/"): self.dd += "/"

                if os.path.exists(self.dd):
                    self.dd = self.dd

                else:
                    self.dd = os.getcwd() + "/"
                    self.writeconfig()
        else:
            self.dd = os.getcwd() + "/"
            self.writeconfig()
    
    def writeconfig(self):
        with open("config", "w") as f:
            if self.dd[-1] != "/": self.dd += "/"

            if os.path.exists(self.dd):
                f.write(self.dd)
            else:
                self.dd = os.getcwd() + "/"
                f.write(self.dd)

            print(colored("Novo diretorio de download configurado! %s" %self.dd, "red"))
            time.sleep(4)
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
            os.system("clear")
            print(msg_help)
            sys.exit(0)


        elif self.s == "-v":
            print("clib v0.2 developed by mrxrobot!\n\nhttps://notabug.org/mrxrobot_/clib.git\n\n")
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
                self.s = self.s.strip(" ").replace(' ', '+')
            elif teste == "arg":
                self.s = self.s.strip(" ").replace(' ', '+')
        return True

    def down(self):
        if self.verifica():
            os.system("clear")
            print(msg)
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
            
            for link in self.soup.find_all("a"):
                if str(link.get('href')).endswith("/"):
                    if self.ext in str(link.get('href')).split('/')[-2].split('-'):
                        self.links.append(link.get('href'))
                    elif self.ext in str(link.get("href")).split('/')[-1].split('-'):
                        self.links.append(link.get("href"))
                    else:
                        continue

          
            i = 0
            for j in set(self.links):
                self.lista[ str(i)] = str(j)
                i += 1

            os.system("clear")
            print(msg)
                    
            if len(self.lista) > 0:
                print("\n{n}\t\t{livro}".format(n=colored("Numero","red"), livro=colored("Livro\n","red")))
                for x in self.lista:
                    print("[" + colored(str(x), "green") + "]\t\t" + colored(self.lista[x].split("/"+self.lista[x].split('/')[4].split('-')[0] + "-")[1][:-1], "yellow"))
            else:   
                print(colored("Livro não encontrado!".upper(), "red"))

                try:
                    input(f"> Voltar para o menu principal [{enter}]")

                except KeyboardInterrupt:
                    sys.exit(0)
                self.volta()


            try:
                self.op = str(input(f'\n\nInforme o número do download ou [{e}] para sair [{vv}]oltar\n> '))

            except KeyboardInterrupt:
                sys.exit(0)


            def reporthook(blocknum, blocksize, totalsize):
                readsofar = blocknum * blocksize
                if totalsize > 0:
                    percent =readsofar * 1e2 / totalsize
                    s = "\rProgresso do download: %5.0f%% %*d" % (
                            percent, len(str(totalsize)), readsofar)
                    sys.stderr.write(s)

                    if readsofar >= totalsize:
                        sys.stderr.write("\n")
                else:
                    sys.stderr.write("read %d\n" %(readsofar,))

            try:
                while self.op != "/q" and self.op != "v":
                
                    try:
                        self.url = self.lista[ str(self.op)]

                    except:
                        print("Opção inválida")
                        time.sleep(3)
                        os.system("clear")
                        self.down()

                    self.req = Request(
                        self.lista[ str(self.op) ],
                        data=None,
                        headers={'User-Agent':choice(user_agents)}
                    )
                    self.resp = urlopen( self.req).read()
                    self.soup = BeautifulSoup( self.resp, "html.parser" )

                    self.d = "http://" + self.soup.find_all("script")[0].get_text().split("//")[2].split("&")[0]
                    self.name = self.d.split("/")[-1].replace("%20","_").split("?")[0] + "." + self.ext
                    
                    print(colored("\nBaixando livro: ", "green") + colored(str(self.name)))
                    urlretrieve(self.d, self.dd + self.name, reporthook)
                    print("{a} {b}\n\n".format( a=colored("\nArquivo salvo em: ", "green"), b=colored(self.dd + self.name, "yellow") ) )
                    try:
                        self.op = str(input(f'\n\nInforme o número do download ou [{e}] para sair [{vv}]voltar\n> '))
                    except KeyboardInterrupt:
                        sys.exit(0)

                if self.op == "/q":
                    sys.exit(0)
                elif self.op == "v":
                    os.system("clear")
                    self.volta()
                else:
                    print("Opção invalida!")

            except KeyboardInterrupt:
                sys.exit(0)


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

