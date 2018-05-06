# Dragon of Justice

[![Build Status](https://travis-ci.org/ricardochaves/dragon-of-justice.svg?branch=master)](https://travis-ci.org/ricardochaves/dragon-of-justice) [![Maintainability](https://api.codeclimate.com/v1/badges/e7961a934e4e617f72f6/maintainability)](https://codeclimate.com/github/ricardochaves/dragon-of-justice/maintainability) [![Coverage Status](https://coveralls.io/repos/github/ricardochaves/dragon-of-justice/badge.svg)](https://coveralls.io/github/ricardochaves/dragon-of-justice) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3f29f0f45f6a404e8b1ae731a90ed03d)](https://www.codacy.com/app/ricardochaves/dragon-of-justice?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ricardochaves/dragon-of-justice&amp;utm_campaign=Badge_Grade) [![Issue Stats](http://issuestats.com/github/ricardochaves/dragon-of-justice/badge/pr)](http://issuestats.com/github/ricardochaves/dragon-of-justice) [![Issue Stats](http://issuestats.com/github/ricardochaves/dragon-of-justice/badge/issue)](http://issuestats.com/github/ricardochaves/dragon-of-justice) [![Updates](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/shield.svg)](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/) [![Python 3](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/python-3-shield.svg)](https://pyup.io/repos/github/ricardochaves/dragon-of-justice/)



# Como funciona

O projeto é apenas um bot do telegram que interage com o [Serenata de Amor](https://serenata.ai/) e armazena algumas coisas do usuário no banco de dados para ajudar na usabilidade.

# Para usar

Faça o clone do projeto:
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

Você precisa criar um bot no Telegram e adicionar o token no seu arquivo ```.env```. Para criar um token você pode ver a [documentação oficial do Telegran](https://core.telegram.org/bots#3-how-do-i-create-a-bot).

Para usar o docker, você precisa criar um diretório ```./data/db``` para mapear o volume do MongoDB ou apenas retire o volume do ```docker-compose.yml```

Agora basta usar ```docker-compose up``` e seu bot já vai responder.
