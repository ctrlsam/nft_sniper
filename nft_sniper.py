import os
from time import sleep
import logging
from rich.logging import RichHandler
from src import *
import config


def output_op(opportunity):
    print('** Opportunity Found **')
    print(f'NFT: {opportunity.name} | FP diff: {opportunity.profit}')


def setup_logging():
    level = os.environ.get("LOG_LEVEL", "INFO")

    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(message)s',
        datefmt='[%X]',
        handlers=[RichHandler()]
    )

    return logging.getLogger('rich')


if __name__ == '__main__':
    logger = setup_logging()

    scrapers = []

    # Add collections from Magic Eden
    for collections in config.providers.get('MagicEden').get('collections'):
        scrapers.append(MagicEden(collections))

    scan_interval = 5  # seconds
    scanning = True

    while scanning:
        for collection in scrapers:
            opps = collection.get_opportunities()
            for op in opps:
                output_op(op)

        logger.info(f'scan complete, waiting for {scan_interval}s')
        sleep(scan_interval)
