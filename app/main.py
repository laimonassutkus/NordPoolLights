import logging
from datetime import datetime

from config import Config
from mi_cloud import MiCloud
from nord_pool_price import NordPoolPrice

logger = logging.getLogger()
logger.setLevel("DEBUG")

# Load application's configuration, such as credentials, and so on.
CONFIG = Config()


def handler(event, context) -> None:
    prices = NordPoolPrice.get_prices(country=CONFIG.country, vat_percentage=CONFIG.vat_percentage)

    current_hour = datetime.now().hour
    current_price = prices[current_hour]

    plug = MiCloud(
        username=CONFIG.username,
        password=CONFIG.password
    ).get_smart_plug(CONFIG.mi_device_id)

    if current_price < CONFIG.price_threshold:
        plug.on()
    else:
        plug.off()
