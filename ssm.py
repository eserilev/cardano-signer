import boto3

def get_client(service: str):
    from botocore.config import Config

    config = Config(retries=dict(max_attempts=20))
    client = boto3.client(service, config=config)
    return client

def get_ssm_key(key_name: str, decript: bool):
    client = get_client(service="ssm")
    decrypted_param = client.get_parameter(Name=key_name, WithDecryption=decript)

    parameter_meta = decrypted_param.get("Parameter")

    key_name = parameter_meta.get("Name")
    decrypted_param = parameter_meta.get("Value")

    return key_name, decrypted_param
