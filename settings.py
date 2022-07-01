import dotenv, os


load_dotenv()

netgear_options = {
    "address": os.environ["CLIENT_IP"],
    "port": os.environ["CLIENT_PORT"],
    "protocol": "tcp",
    "logging": True,
    "pattern": 1
}
