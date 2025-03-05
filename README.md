Este Back-end foi feito com python e flask.

## Funcionalidades  

* Criação e gestão de produtos.
* Gera QRCODE conforme o valor e o produto selecionado sem vinculos a bancos.
* Validações de pagamentos(Simula o pagamento confirmado).
* Possue estatísticas de vendas com fechamento mensal e anual.
* Painel de acompanhamento para visualização de pagamentos realizados/pendentes.
* Autenticação de login com hierarquia de admin e users.

  Para utilizar o system você deve o clone do repositorio usando o comando abaixo:

  `` git clone https://github.com/Emmanuel194/simple-ecommerceBack.git ``

  Após realizar o clone no seu na pasta raiz do projeto execute o seguinte comando para criar um ambiente virutal

  `` python -m venv venv ``
  
  após criado ative o mesmo:

  ``venv\Scripts\activate``

  assim que o ambiente virtual estiver criado baixe as depêndecias usando `` pip install `` ou até mesmo ``pip install -r requirements.txt`` caso não consiga.
  
  Após as configurações basicas você precisa também configurar variáveis de ambiente.

  Uma delas é o Db que foi feito em SQlite, nesse caso voce precisa usar ``flask db upgrade`` para fazer as migrações do DB.

  E também configurar o .env na raiz do projeto, sendo assim você consegue rodar o back-end no seu ambiente utilizando o comando ``python run.py``
  

  ## 🛠 Testando a API com Postman

Para testar as rotas desta API, utilize a collection do Postman disponível abaixo:

 [🔗 Acesse a Collection do Postman](undefined/workspace/e-commerce-simple/collection/29723495-f3d910c7-2760-4b78-b69f-b850b3d0b1e4?action=share&creator=29723495)

