# Ponderada 3


## Vídeo


## Explicação

O foco desta ponderada estava em desenvolver um sistema backend em microsserviçoes. Para isso, foram criados três serviços: auth, de autenticação para login e cadastro, database, para rodar o banco de dados e image-processing, para receber a imagem e processá-la. Ao rodar o docker compose, esses serviços são lançados e se tornam disponíveis para que o frontend acesse as rotas. O login é feito utilizando token, sendo assim necessário o token para poder acessar a página de submeter a imagem. Ao submeter a imagem, entra um simbolo de loading que retorna a imagem, assim que processada pelo backend.

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
