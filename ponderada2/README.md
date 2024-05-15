


# Ponderada 2

https://github.com/FelipeCampos14/entregaveis-modulo10/assets/99193547/f2b0e464-7e7b-4648-8075-f654cc7a9f3b

## Vídeo


## Explicação
Para o backend foram criado dois models, um para users, que será utilizado futuramente para autenticação, e um de ToDos, correpondente a ponderada atual.
Foram então criadas rotas de CRUD para cada, as quais são acessadas por widgets no front-end. O front-end em flutter foi desenvolvido apenas para acessar as rotas de CRUD, sendo capaz de criar, listar, atualizar e apagar tarefas. Ao criar uma tarefa, ela é lista logo abaixo. É possível atualizá-las e apagá-las por meio dos botões que aparecem á direita, respectivamente. Para armazenar os dados, foi utilizada a imagem do postgres, a qual foi mapeada no docker compose.

## Como executar


Primeiro é necessário subir o container do back-end:

```
docker compose up --build
```

Agora é necessário subir o emulador, para isso é necessário ter instalado android studio e flutter. Dado isso precisa-se:

```
flutter emulators
```

Após isso, é necessário lançar um dos emuladores escolhidos:

```
flutter emulators --launch <nomeDoEmulador>
```

E agora basta lançar a aplicação flutter:

```
flutter run
```
