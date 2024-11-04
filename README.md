# Bot de Processamento Automático de Mensagens no Telegram

### Autor: [Vinícius Oliveira](https://www.linkedin.com/in/vinicius-oliveira-p1/)

---

## Descrição

Este projeto desenvolve um pipeline de dados automatizado e escalável que processa e armazena interações de usuários de um grupo no Telegram utilizando serviços serverless da AWS. A solução é focada em eficiência e custo-benefício, evitando a necessidade de uma infraestrutura tradicional e permitindo o armazenamento e consulta dos dados diretamente na nuvem.

## Objetivo

O objetivo do projeto é coletar mensagens de um grupo no Telegram e integrá-las em um pipeline de dados na AWS, com um fluxo automatizado para o processamento e análise dos dados. A arquitetura utiliza uma combinação de serviços serverless que incluem:

- **Telegram Bot API** para captura das interações
- **AWS API Gateway** para gerenciamento de solicitações
- **AWS Lambda** para processamento dos dados
- **Amazon S3** para armazenamento
- **Amazon EventBridge** para monitoramento e acionamento de novos processos de ETL
- **Amazon Athena** para consultas SQL diretas nos dados armazenados

Essa estrutura permite um pipeline de ingestão, transformação e análise de dados otimizado para empresas que buscam uma solução flexível e econômica.

## Funcionamento

O pipeline funciona com o seguinte fluxo de dados:

1. **Coleta de Dados**: Um bot no Telegram captura as mensagens dos usuários e as envia para o **API Gateway**.
2. **Processamento Inicial**: A mensagem é recebida pelo **API Gateway** e encaminhada para uma **função Lambda**, que processa e armazena o conteúdo no **Amazon S3**.
3. **Transformação dos Dados**: Com o Amazon EventBridge monitorando o bucket do S3, um novo processo de ETL é acionado automaticamente quando novos dados são detectados. Esse processo de ETL, realizado por outra função Lambda, transforma os dados brutos e os organiza para consultas futuras.
4. **Análise dos Dados**: Utilizando o **Amazon Athena**, é possível realizar consultas SQL diretamente no bucket do S3, permitindo análises detalhadas dos dados sem a necessidade de transferi-los para um banco de dados tradicional.

## Principais Ferramentas e Tecnologias

- **Telegram Bot API**: Integração com o Telegram para captura de mensagens.
- **AWS API Gateway**: Gerencia e expõe endpoints para comunicação do bot.
- **AWS Lambda**: Realiza processamento serverless em cada etapa do pipeline.
- **Amazon S3**: Armazena os dados brutos e transformados.
- **Amazon EventBridge**: Monitora eventos e aciona o processo de ETL automaticamente.
- **Amazon Athena**: Permite consultas SQL diretamente no S3 para análise de dados.

## Pré-Requisitos

- Credenciais e configurações de API do Telegram.
- Conta na AWS com permissões para os serviços mencionados.
- Configurações de IAM para permissões de acesso aos serviços AWS.

## Configuração e Execução

1. **Configuração do Bot do Telegram**: Siga as instruções na [Documentação do Telegram Bot API](https://core.telegram.org/bots/api) para configurar o bot.
2. **Configuração na AWS**:
   - Crie e configure os serviços no console da AWS conforme descrito na arquitetura do projeto.
   - Configure o API Gateway, funções Lambda, e buckets do S3 conforme necessário.

3. **Execução do Pipeline**:
   - Após a configuração, o pipeline será acionado automaticamente a cada nova mensagem capturada pelo bot.
   - Os dados processados estarão disponíveis para consulta no Amazon Athena.

## Fontes

- [Documentação Telegram Bot API](https://core.telegram.org/bots/api)
- [Documentação Telegram Application](https://core.telegram.org/api/obtaining_api_id)
- [Amazon Web Services](https://aws.amazon.com/pt/)

