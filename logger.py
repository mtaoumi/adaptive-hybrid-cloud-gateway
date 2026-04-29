import logging
import os

# create logs folder if it doesn't exist
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/gateway.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def log_routing(message, route, reason):
    logging.info(f"Message: {message} | Route: {route} | Reason: {reason}")
