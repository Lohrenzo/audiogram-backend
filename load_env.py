import json
import os
from dotenv import load_dotenv

load_dotenv()


def update_zappa_settings():
    # Load .env variables
    env_vars = {
        "DB_ENGINE": os.environ.get("DB_ENGINE"),
        "DB_HOST": os.environ.get("DB_HOST"),
        "DB_NAME": os.environ.get("DB_NAME"),
        "DB_USER": os.environ.get("DB_USER"),
        "DB_PASSWORD": os.environ.get("DB_PASSWORD"),
        "DB_PORT": os.environ.get("DB_PORT"),
        "DEBUG": os.environ.get("DEBUG"),
        "SECRET_KEY": os.environ.get("SECRET_KEY"),
        "USE_S3_STATIC": os.environ.get("USE_S3_STATIC"),
        "AWS_STORAGE_BUCKET_NAME": os.environ.get("AWS_STORAGE_BUCKET_NAME"),
        "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID"),
        "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "AWS_DEFAULT_ACL": os.environ.get("AWS_DEFAULT_ACL"),
    }

    # Load existing Zappa settings
    with open("zappa_settings.json", "r") as file:
        zappa_settings = json.load(file)

    # Update environment variables in Zappa settings
    zappa_settings["production"]["environment_variables"] = env_vars

    # print(zappa_settings)

    # Save updated Zappa settings
    with open("zappa_settings.json", "w") as file:
        json.dump(zappa_settings, file, indent=4)


if __name__ == "__main__":
    update_zappa_settings()
