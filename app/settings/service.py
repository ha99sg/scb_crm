from sqlalchemy import select

from app.third_parties.oracle.base import SessionLocal
from app.third_parties.oracle.models.enviroment.model import DBS

ss = SessionLocal()
configs = ss.execute(
    select(
        DBS
    )
).scalars().all()

configs = {config.name: config.value for config in configs}

SERVICE = {
    "application": {
        "version": "1.0.0",
        "project_name": configs.get("PROJECT_NAME", "CRM"),
        "secret_key": configs.get("SECRET_KEY", ""),
        "debug": bool(configs.get("DEBUG", "") if configs.get("DEBUG", "") in ["True", "true", "1"] else False),
        "allowed_hosts": list(configs.get("ALLOWED_HOSTS", ["*"]))
    },
    "file": {
        "url": configs.get("SERVICE_FILE_URL"),
        "server-auth": configs.get("SERVICE_FILE_SERVICE_AUTH"),
        "authorization": "bearer 3",
        "service_file_cdn": configs.get("SERVICE_FILE_CDN")
    },
    "file-upload": {
        "file_limit": int(configs.get("FILE_LIMIT", 10)),
        "file_size_max": int(configs.get("FILE_SIZE_MAX", 5000000))
    },
    "ekyc": {
        "url": configs.get("SERVICE_EKYC_URL"),
        "x-transaction-id": "CRM_TEST",
        "authorization": f"bearer {configs.get('SERVICE_EKYC_BEARER_TOKEN')}",
        'otp': configs.get('SERVICE_EKYC_OTP'),
        'token': configs.get('SERVICE_EKYC_BEARER_TOKEN'),
        'server-auth': configs.get('SERVICE_EKYC_SERVER_TOKEN')
    },
    "template": {
        "url": configs.get("SERVICE_TEMPLATE_URL"),
        "server-auth": configs.get("SERVICE_TEMPLATE_SERVICE_AUTH")
    },
    "card": {
        "url": configs.get("SERVICE_CARD_URL"),
        "authorization": f"bearer {configs.get('SERVICE_CARD_BEARER_TOKEN')}",
        "x-transaction-id": "CRM_TEST"
    },
    "idm": {
        "host": configs.get("SERVICE_IDM_URL"),
        "headers": {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {configs.get("SERVICE_IDM_BEARER_TOKEN")}'
        },
        "service_name": "CRM"

    },
    "tms": {
        "url": configs.get("SERVICE_TEMPLATE_URL"),
        "headers": {
            'Content-Type': 'application/json',
            "server-auth": "BCQjyTXFB0TWJiLjKcuzAenpYsbXV5O0",
            "authorization": "Bearer 1"
        }
    },
    "gw": {
        "url": configs.get("SERVICE_GW_URL"),
        "email": configs.get("SERVICE_GW_EMAIL_DATA_INPUT__EMAIL_TO"),
        "sms_mobile": configs.get('SERVICE_GW_SMS_MOBILE')
    },
    "kafka": {
        "sasl_mechanism": configs.get("KAFKA_SASL_MECHANISM"),
        "bootstrap_servers": configs.get("KAFKA_BOOTSTRAP_SERVERS"),
        "security_protocol": configs.get("KAFKA_SECURITY_PROTOCOL"),
        "sasl_plain_username": configs.get("KAFKA_SASL_PLAIN_USERNAME"),
        "sasl_plain_password": configs.get("KAFKA_SASL_PLAIN_PASSWORD"),
        "producer_topic": configs.get("KAFKA_PRODUCER_TOPIC"),
        "message_max_bytes": configs.get("KAFKA_MESSAGE_MAX_BYTES"),
        "write_log": bool(configs.get("KAFKA_WRITE_LOG") if configs.get("KAFKA_WRITE_LOG") in ["True", "true", "1"] else False),
    },
    "redis": {
        "host": configs.get("REDIS_HOST"),
        "port": configs.get("REDIS_PORT"),
        "password": configs.get("REDIS_PASSWORD"),
        "database": configs.get("REDIS_DATABASE"),
    },
    "production": {
        "production_flag": bool(configs.get("PRODUCTION") if configs.get("PRODUCTION") in ["True", "true", "1"] else False)
    },
    "rabbitmq": {
        "host_name": configs.get("RABBITMQ_HOST_NAME"),
        "host_ip": configs.get("RABBITMQ_HOST_IP"),
        "vhost": configs.get("RABBITMQ_VHOST"),
        "mqtt_port": configs.get("RABBITMQ_MQTT_PORT"),
        "amqp_port": configs.get("RABBITMQ_AMQP_PORT"),
        "web_stomp_port": configs.get("RABBITMQ_WEB_STOMP_PORT"),
        "server_username": configs.get("RABBITMQ_SERVER_USERNAME"),
        "server_password": configs.get("RABBITMQ_SERVER_PASSWORD"),
        "client_username": configs.get("RABBITMQ_CLIENT_USERNAME"),
        "client_password": configs.get("RABBITMQ_CLIENT_PASSWORD")
    },
    "fileshare": {
        "tablet_banner_share_link": configs.get("FILESHARE_TABLET_BANNER_SHARE_LINK")
    },
    'sentry': {
        "host": configs.get("SENTRY_HOST"),
        "port": configs.get("SENTRY_PORT"),
        "client_key": configs.get("SENTRY_CLIENT_KEY"),
        "project_id": configs.get("SENTRY_PROJECT_ID")
    },
    "crm_app_url": configs.get("CRM_APP_URL")
}
