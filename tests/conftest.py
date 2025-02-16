import logging

# ignore logs from azure, openai and httpx
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
