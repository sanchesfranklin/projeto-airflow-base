# Projeto base do Airflow para Docker
Este é um projeto base do Airflow para Docker, o arquivo criado no docker-compose foi obtido no site oficial da documentação do Airflow, e pode ser consultado aqui:
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Para facilitar foi criado este repositório onde pode apenas executar simples passos abaixo e você terá um container Docker  com o Airflow pronto para estudos e explorar a ferramenta.

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
