# Ponderada 4


## Vídeo

[Screencast from 18-06-2024 09:06:51.webm](https://github.com/FelipeCampos14/entregaveis-modulo10/assets/99193547/0b7580f5-1a1d-4866-b21c-29e1e50bf37c)


## Explicação

O foco desta ponderada foi criar gateway para a api, que foi feito com nginx, adicionar um sistema de logs, que registra os eventos do usuário. Além disso foi criado um frontend mobile para interagir com os eventos da aplicação. Ao acessar, basta fazer login e depois interagir com os ToDos. Ao rodar o docker compose da aplicação, o serviços de database, backend e gateway são lançados.

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
