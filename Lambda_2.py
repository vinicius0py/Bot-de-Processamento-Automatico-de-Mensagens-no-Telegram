import os
import json
import logging
import boto3
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timedelta, timezone

def lambda_handler(event: dict, context: dict) -> bool:
    # Variáveis de ambiente
    RAW_BUCKET = os.environ["AWS_S3_BUCKET"]
    ENRICHED_BUCKET = os.environ["AWS_S3_ENRICHED"]

    # Configuração do fuso horário e data
    tzinfo = timezone(offset=timedelta(hours=-3))
    date = (datetime.now(tzinfo) - timedelta(days=1)).strftime("%Y-%m-%d")
    timestamp = datetime.now(tzinfo).strftime("%Y%m%d%H%M%S%f")

    # Inicialização do cliente S3
    client = boto3.client("s3")
    table = None

    try:
        # Listar arquivos no bucket de dados brutos
        response = client.list_objects_v2(Bucket=RAW_BUCKET, Prefix=f"telegram/context_date={date}")

        # Processar cada arquivo listado
        for content in response["Contents"]:
            key = content["Key"]
            local_file_path = f"/tmp/{key.split('/')[-1]}"

            client.download_file(RAW_BUCKET, key, local_file_path)

            with open(local_file_path, mode="r", encoding="utf8") as fp:
                data = json.load(fp)["message"]

            parsed_data = parse_data(data=data)
            iter_table = pa.Table.from_pydict(mapping=parsed_data)

            # Concatenar as tabelas
            if table:
              table = pa.concat_tables([table, iter_table])
            else:
              table = iter_table
              iter_table = None

        # Persistir a tabela enriquecida em formato Parquet
        parquet_file_path = f"/tmp/{timestamp}.parquet"
        pq.write_table(table=table, where=parquet_file_path)
        client.upload_file(parquet_file_path, ENRICHED_BUCKET, f"telegram/context_date={date}/{timestamp}.parquet")
        return True

    except Exception as exc:
        logging.error(f"Erro ao processar os dados: {exc}")
        return False


def parse_data(data: dict) -> dict:

    # Obtendo a data e o timestamp atuais
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parsed_data = dict()

    # Extração de dados relevantes
    for key, value in data.items():
        if key == "from":
            for sub_key, sub_value in value.items():
                if sub_key in ["id", "is_bot", "first_name"]:
                    parsed_data[f"user_{sub_key}"] = [sub_value]
        elif key == "chat":
            for sub_key, sub_value in value.items():
                if sub_key in ["id", "type"]:
                    parsed_data[f"chat_{sub_key}"] = [sub_value]
        elif key in ["message_id", "date", "text"]:
            parsed_data[key] = [value]

    # Garantir que a "text" esteja presente
    if "text" not in parsed_data:
        parsed_data["text"] = [None]
    return parsed_data