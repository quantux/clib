#!/usr/bin/env python3.6
# -*- encoding: utf-8 -*-

# feitor por: mrxrobot

from urllib.request import urlopen
from urllib.request import Request
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from termcolor import colored
from unicodedata import normalize
import progressbar
import sys
import os
import time


# Limpar a tela
os.system("clear")

#define uma variavel contendo a mensagem de inicio programa
msg=colored("""
  
       _  _  _     
  ___ | |(_)| |__  
 / __|| || || '_ \ 
| (__ | || || |_) |
 \___||_||_||_.__/ {v}
 
        """.format(v=colored("v0.1","green")),"red")


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
/help    --> Exibe este menu de ajuda.
[v]oltar --> Volta ao menu anterior.
/quit    --> Encerra o programa.

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



def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII','ignore').decode('ASCII')



class Connect:
    print(msg)
    def __init__(self, s, format_arq="pdf"):
        # Comecei inicializado a classe com 2 argumetos
        # o primeiro 's', recebera o nome do livro
        # o segundo  'format_arq' define o formato do livro a ser baixado
    
        self.s = remover_acentos(s)
        self.ext = format_arq
        self.verifica()
    
    def volta(self):
        os.system("clear")
        print(msg)
        Connect(str( input("Insira o nome do livro ou [{h}] para ajuda ou [{e}] para sair.\n> ". \
        format(h = colored("/help","yellow"), e = colored("/quit", "red") ) )  \
        ).strip(" ")).down()  

    def verifica(self):
        if self.s == "/help":
            os.system("clear")
            print(msg_help)
            input("> Voltar para o menu principal [{enter}]".format(enter=colored("enter","red")))
            self.volta()

        elif self.s == "/quit":
            sys.exit(0)

        elif self.s == "--help":
            os.system("clear")
            print(msg_help)
            sys.exit(0)

        elif self.s == "--version":
            print("clib v0.1 developed by mrxrobot!\nhttps://notabug.org/mrxrobot_/clib.git\n\n")
            sys.exit(0)

        elif self.s.startswith("-"):
            print("Opção inválida")
            sys.exit(0)

        elif self.s == "":
            print(colored("Erro, informe pelo menos o nome do livro ou do autor!\n","red"))
            time.sleep(5)
            self.volta()

        else:
            if teste == None:
                if len(self.s.split(" ")) > 1: self.s = "".join( self.s.replace(" ", "+") )
                else: selfs = self.s
                if self.s[-1] in "+": self.s = self.s[:-1]
            
            elif teste == "arg":
                if len(self.s.split(" ")) > 1: self.s = "".join( self.s.replace(" ", "+") )
                else: self.s = self.s
                if self.s[-1] in "+": self.s = self.s[:-1]

        return True

    def down(self):
        if self.verifica():
            os.system("clear")
            print(msg)
            print("Pesquisando por {s}".format(s=colored("'{s}'".format(s=self.s.replace('+', ' ')),"yellow")))
            self.links = []
            self.lista = {}
            self.url = "http://lelivros.bid/?x=0&y=0&s={ss}".format(ss=self.s)
            
            self.req = Request(
            self.url,
            data=None,
            headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            
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
                input("> Voltar para o menu principal [{enter}]".format(enter=colored("enter","red")))
                self.volta()
            
            self.op = str(input('\n\nInforme o numero do download ou [{ee}] para sair [{vv}]oltar\n> '.format(ee=colored('/quit','red'),vv=colored('v','green'))))
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

            while self.op != "/quit" and self.op != "v" and self.op != "h":
                
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
                headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
            
                self.resp = urlopen( self.req).read()
                self.soup = BeautifulSoup( self.resp, "html.parser" )
                self.d = "http://" + self.soup.find_all("script")[0].get_text().split("//")[2].split("&")[0]
                self.name = self.d.split("/")[-1].replace("%20","_").split("?")[0] + "." + self.ext
                print(colored("\nBaixando livro: ", "green") + colored(str(self.name)))
                urlretrieve(self.d, self.name, reporthook)
                print("{a} {b}\n\n".format( a=colored("\nArquivo salvo em: ", "green"), b=colored( str( os.getcwd() ) + "/" + self.name, "yellow") ) )
                self.op = str(input('\n\nInforme o numero do download ou [{ee}] para sair [{vv}]voltar\n> '.format(ee=colored('/quit','red'),vv=colored('v','green'))))

            if self.op == "/quit":
                sys.exit(0)
            elif self.op == "v":
                os.system("clear")
                self.volta()
            else:
                print("Opção invalida!")



if len(sys.argv) < 2:
    teste = None
    op=str( input("Insira o nome do livro ou [{h}] para ajuda ou [{e}] para sair.\n> ". \
            format(h = colored("/help","yellow"), e = colored("/quit", "red") ) )  \
            ).strip(" ")

    
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

