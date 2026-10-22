# PDV Chefpães

O Projeto PDV ChefPães é para auxiliar a padaria que o meu pai 
possui na cidade de Tanabi. A padaria dele não possui sistema automatizado de registro de vendas e estoque

## Funcionalidades

- O PDV faz desde o registro de uma venda com um carrinho (adicionando mais de um produto), interligando com o estoque, baixando automaticamente a quantidade disponível para venda de determinados produtos da padaria.
- Efetua a inserção de produtos novos e também eventuais alteração de valores.
- Mostra o relatório diário de vendas da padaria.

## Tecnologias

- MySQL
- Python
- Biblioteca mysql-connector-python

## Banco de dados

estrutura consta no arquivo "chespaes.sql"

## Como rodar

1. Instalar o Python e MySQL
2. Executar no terminal o comando para instalar a biblioteca: pip install mysql-connector-python
3. Abra o arquivo chefpaes.sql no Workbench e o execute
4. Ajuste o 'CONFIG' no 'pdv.py' com o seu usuário e senha do MySQL.
5. Execute python pdv.py

## O que aprendi

1. Fazer corretamente as indentações dentro das funções, como o UPDATE fora do FOR, que só baixava o ultimo produto do carrinho.
2. A lógica do JOIN, GROUP BY, SUM e LIMIT do SQL para mostrar o ranking dos produtos mais vendidos do dia. O JOIN liga as tabelas itens_pedido, pedidos e produtos e o WHERE condiciona ao dia de hoje.
3. Commit e Rollback no registro de vendas, para gravar os pedidos, itens e baixa de estoque ou cancelar o registro da venda. O rollback desfaz tudo que foi registrado da venda até o momento e o Commit confirma tudo de uma vez no final.
___