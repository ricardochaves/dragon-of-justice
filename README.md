# Dragon of Justice

[![Build Status](https://travis-ci.org/ricardochaves/dragon-of-justice.svg?branch=master)](https://travis-ci.org/ricardochaves/dragon-of-justice) [![Maintainability](https://api.codeclimate.com/v1/badges/e7961a934e4e617f72f6/maintainability)](https://codeclimate.com/github/ricardochaves/dragon-of-justice/maintainability) [![Coverage Status](https://coveralls.io/repos/github/ricardochaves/dragon-of-justice/badge.svg)](https://coveralls.io/github/ricardochaves/dragon-of-justice) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3f29f0f45f6a404e8b1ae731a90ed03d)](https://www.codacy.com/app/ricardochaves/dragon-of-justice?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ricardochaves/dragon-of-justice&amp;utm_campaign=Badge_Grade) [![Updates](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/shield.svg)](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/) [![Python 3](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/python-3-shield.svg)](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/)

___

Um chatbot (atualmente com suporte ao Telegram) que utiliza parte da stack do  [Serenata de Amor](https://serenata.ai/) para identificar atividades suspeitas de deputados federais.

O objetivo do projeto é dar poder a qualquer pessoa / organização de criar o seu próprio chatbot fazendo com que mais e mais pessoas tenha acesso a informações que vão ajuda-las a cobrar os seus deputados.

## Para desenvolver

Faça um clone do projeto

```
git clone git@github.com:ricardochaves/dragon-of-justice.git
```

Entre na pasta

```
cd dragon-of-justice
```

Crie um arquivo ```.env``` baseado no ```example.env```

```
cp example.env .env
```

### Crie um bot no telegram

Atualmente o bot só tem suporte para o telegram, mas ele está sendo desenvolvido com a ideia de se plugar mais bots ao bot core.

Você precisa criar um bot no Telegram e adicionar o token no seu arquivo ```.env```. Para criar um token você pode ver a [documentação oficial do Telegran](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

### MongoDB

Se você quiser manter os dados persistidos no banco de dados crie um diretório ```./data/db``` e adicione o volume no ```docker-compose.yml```. Ele vai ficar parecido com o exemplo abaixo.

```
services:
  mongodb:
    image: mongo:3.6.0
    ports:
      - "27017:27017"
    volumes:
      - ./data/db:/data/db
```

Para rodar o projeto basta executar ```docker-compose up```

### Testes

Para executar os testes:

```
docker-compose run bot nosetests
```

Se você gosta de ver os testes durante o desenvolvimento use o watch

```
docker-compose run bot nosetests --with-watch
```

Existe a opção de usar com converage

```
docker-compose run bot nosetests --with-watch --with-coverage --cover-package=.
```

### Code Climate

Para evitar que o PR tenha problemas com o Code Climate você pode rodar ele localmente primeiro.
Primeiro instale o CLI. Veja como instalar [aqui](https://github.com/codeclimate/codeclimate#packages)

Após a instalação baixe as imagens do docker dos plugins, no diretório root faça:

```
codeclimate engines:install
```

Isso pode demorar...

Depois que ele baixar as imagens execute:

```
codeclimate analyze
```

O resultado esperado é:

```
>>codeclimate analyze
Starting analysis
Running structure: Done!
Running duplication: Done!
Running pep8: Done!
Running markdownlint: Done!

Analysis complete! Found 0 issues.
```
