# Projeto Pessoal com Airflow para Docker

Este é um projeto do Airflow para Docker, o arquivo criado no docker-compose foi obtido no site oficial da documentação do Airflow, e pode ser consultado aqui:
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

No Docker Compose foi adicionado também mais uma imagem do PostgreSQL que servirá de um ambiente OLAP, para onde iremos fazer o carregamento dos dados extraídos e processados pelo Airflow.

Adicionei também ao arquivo configurações para o servidor SMTP, onde utilizei o Mailtrap para esta finalidade. Caso queira também utilizar o Mailtrap, segue o link do site:
https://mailtrap.io/

## Resumo sobre o projeto
O projeto consiste em ter um fluxo de ETL utilizando o Airflow para obter as taxas Ptax de cambio das moedas, extraindo, transformando e realizando o load no banco de dados. Este projeto também seguiu a metodologia Data Lake.

Sobre a DAG 'moeda':
Realizamos o acesso ao site citado acima, para extrair a tabela com todas as taxas Ptax, salvamos o arquivo em uma primeira camada 'Raw', em seguida realiza uma pequena transformação normalizando os dados, ou seja alterando os nomes das colunas, após isso é salvo em uma segunda camada chamada 'Trusted', que é o dado em um formato já confiável e pronto para ser aplicado uma regra de negócio por exemplo, em seguida utilizei um exemplo simples apenas para simular aplicando uma regra de negócio, filtrei para pegar as moedas apenas do tipo A e faço o carregamento dos dados no banco de dados, finalizando com um envio de email, notificando sobre a finalização da tarefa.

Abaixo a imagem da DAG e Envio do Email:

![Pipeline-airflow-dag](https://user-images.githubusercontent.com/55898372/200649864-55570b71-aa25-4f8e-a2dc-41213e0510ad.png)

![email-notificacao-airflow](https://user-images.githubusercontent.com/55898372/200649892-edfa572b-c471-4d14-a7c6-faaf31550c53.png)

# Utilizando o projeto

## Clonar o repositório
git clone https://github.com/sanchesfranklin/projeto-airflow-base.git

## No Linux
- Configurando o usuário correto para uso do Airflow: 
echo -e "AIRFLOW_UID=$(id -u)" > .env

## Inicializando a base de dados
docker-compose up airflow-init

## Executando o Airflow
docker-compose up -d

## Verificando se foi criado com sucesso
Executar o comando: docker container ps

## Abrindo a interface
http://localhost:8080

## Credenciais
- Login: airflow
- Senha: airflow


## Referências

https://airflow.apache.org/

https://levelup.gitconnected.com/creating-and-filling-a-postgres-db-with-docker-compose-e1607f6f882f


