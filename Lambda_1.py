import os
import json
import logging
from datetime import datetime, timezone, timedelta
import boto3


def lambda_handler(event: dict, context: dict) -> dict:

  # Variáveis de ambiente
  BUCKET = os.environ["AWS_S3_BUCKET"]
  TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

  # Variáveis lógicas (configuração de fuso horário (SP UTC-3))
  tzinfo = timezone(offset=timedelta(hours=-3))
  date = datetime.now(tzinfo).strftime('%Y-%m-%d')
  timestamp = datetime.now(tzinfo).strftime('%Y%m%d%H%M%S%f')

  filename = f"{timestamp}.json"
  file_path = f"/tmp/{filename}"

  # Código principal
  client = boto3.client("s3")

  try:
    # Carrega a mensagem recebida do Telegram
    message = json.loads(event["body"])
    chat_id = message["message"]["chat"]["id"]

    # Verifica se a menssagem é do grupo certo pelo "chat_id ", e escreve a menssagem
    if chat_id == TELEGRAM_CHAT_ID:
      with open(file_path, mode="w", encoding="utf8") as fp:
        json.dump(message, fp)
      client.upload_file(file_path, BUCKET, f"telegram/context_date={date}/{filename}")
    else:
        logging.warning(f"Mensagem de chat_id {chat_id} ignorada. Origem incorreta.")
        return dict(statusCode="403")

  except Exception as exc:
      logging.error(msg=exc)
      return dict(statusCode="500")

  else:
      return dict(statusCode="200")