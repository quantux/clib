# clib *v0.1*

### Informação

O projeto não tem nenhum fim lucrativo e é 100% livre.
O único objetivo aqui é contribuir com software livre para a comunidade.

### O que é o clib?

O **clib** é uma ferramenta CLI para a obtenção de livros em formato pdf, utilizando como fonte o site lelivros.com.
Utilizando de vários algoritos de análise de código html, o software faz uma busca pelo livro informado pelo usuário e, se encontrar, faz o download do mesmo.
É livre e está lançado sob a [Unlicense] (http://unlicense.org).

### Como instalar o clib? 

Dependências:

```
python3.6
pip3.6
git

```
Módulos:

```

beautifulsoup4==4.6.0
bs4==0.0.1
progressbar2==3.34.3
python-utils==2.2.0
six==1.11.0
termcolor==1.1.0
urllib5==5.0.0

```

Instalação:

```
$ git clone https://notabug.org/mrxrobot_/clib.git

$ cd clib

$ su root -c "pip3 install -r requirements.txt" 

```

Se estiver utilizando o Windows, pode apenas usar o conteúdo dentro das aspas duplas, sem o **su root -c**. O **requirements.txt** é um arquivo de texto que contém os modulos do python que serão necessários para o funcionamento do software.


### E agora?

Após ter completado a instalação, pode-se utilizar o clib assim:

```

$ clib

```

### Algumas imagens que descrevem o funcionamento do software:

![Started program](https://a.uguu.se/MKqChAB3lsMZ_1-tela-de-inicio.jpg)

![Started program](https://a.uguu.se/g58haOjblrWI_2-inserindo-o-nome-do-livro.jpg)

![Started program](https://a.uguu.se/ZFXdqwBCag1U_3-livro-encontrado.jpg)

![Started program](https://a.uguu.se/TuHXZlVEhcdT_4-escolhendo-o-livro.jpg)

![Started program](https://a.uguu.se/Xyru6ZkRPexF_5-baixando-o-livro.jpg)

![Started program](https://a.uguu.se/Nlh4zRKibcQ2_6-download-concluido.jpg)


### Como contribuir 

Você pode contribuir de várias maneiras: reportando bugs, aprimorando o código-fonte, fazendo sugestões, etc. 
Forkeie o projeto e mande o seu pull request! 
