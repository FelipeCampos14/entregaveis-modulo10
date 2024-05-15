# Ponderada 2

## Vídeo


## Explicação
Para o backend foram criado dois models, um para users, que será utilizado futuramente para autenticação, e um de ToDos, correpondente a ponderada atual.
Foram então criadas rotas de CRUD para cada, as quais são acessadas por widgets no front-end. O front-end em flutter foi desenvolvido apenas para acessar as rotas de CRUD, sendo capaz de criar, listar, atualizar e apagar tarefas. Ao criar uma tarefa, ela é lista logo abaixo. É possível atualizá-las e apagá-las por meio dos botões que aparecem á direita, respectivamente. 
Para armazenar os dados, foi utilizado sqlite pela praticidade

## Como executar

É necessário apenas subir os containers de cada serviço da aplicação:

```
docker compose up --build
```
