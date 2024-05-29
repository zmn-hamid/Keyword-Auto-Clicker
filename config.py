import configparser

config = configparser.ConfigParser()
config.read("pv_config.ini")

DOMAINS_PATH = config.get("paths", "domains_path")
KEYWORDS_PATH = config.get("paths", "keywords_path")


REMOVE_SEARCHES = ["People also ask", "Videos", "Images", "Places", "Related searches"]
