## **1\. Objetivo**

**O projeto** tem como objetivo **desenvolver um pipeline de dados automatizado e escalável**, que integra as interações dos usuários de um grupo no Telegram com a **AWS**, utilizando **serviços serverless** para maximizar a eficiência e reduzir os custos.

**Fluxo de Dados**: o processo começa com um **bot no Telegram**, que coleta informações dos usuários e as envia para o **API Gateway**. Essas informações são então processadas por uma **função Lambda** e armazenadas no **Amazon S3**.

A partir deste ponto, o **Amazon EventBridge** monitora o bucket do S3 e **aciona automaticamente um novo processo de ETL** sempre que novos dados são carregados. Esse processo, realizado por uma segunda **função Lambda**, transforma os dados e os armazena em outro bucket do S3, tornando-os **prontos para consultas**.

Na fase final, utilizamos o **Amazon Athena** para realizar consultas SQL diretamente nos dados transformados, permitindo **análises robustas sem a necessidade de mover os dados para um banco de dados separado**.

Este **pipeline serverless** fornece uma solução flexível e eficiente para empresas que buscam ingerir, processar e analisar grandes volumes de dados de maneira **custo-efetiva**, sem a complexidade de uma infraestrutura tradicional.

### **1.1. TLDR**

 - **Fontes**:
  - Documentação Telegram Bot API [link](https://core.telegram.org/bots/api).
  - Documentação Telegram Application [link](https://core.telegram.org/api/obtaining_api_id).
  - Amazon Web Services [link](https://aws.amazon.com/pt/).
