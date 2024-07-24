from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")
# DB_NAME = env.str("DB_NAME")
# DB_USER = env.str("DB_USER")
# DB_PASSWORD = env.str("DB_PASSWORD")
# DB_HOST = env.str("DB_HOST")
# DB_PORT = env.int("DB_PORT")
# PAYMENT_TOKEN = env.str("PAYMENT_TOKEN")
