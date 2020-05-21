# Bem vindo ao JW Admin

Esse sistema foi criado para a gestão de territórios e saídas de campo para congregações das Testemunhas de Jeová.

## Instruções para rodar localmente

1. [Instale a versão 3+ do Python](https://realpython.com/installing-python/)
2. [Instale o PIP](https://pip.pypa.io/en/stable/installing/)
3. [Crie e ative seu virtualenv](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
4. Após clonar o repo, vá à pasta do projeto e execute `pip install -r requirements.txt` no seu terminal
5. Ainda na pasta do projeto execute `python manage.py makemigrations` no seu terminal
6. Ainda na pasta do projeto execute `python manage.py migrate` no seu terminal
7. Ainda na pasta do projeto execute `python manage.py runserver` no seu terminal
8. Você deve poder acessar o projeto no seu browser
