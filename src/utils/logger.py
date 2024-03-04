from datetime import datetime
import os
import logging

currency_path_log_folder = f'log/{datetime.now().year}/{datetime.now().month}'

if not os.path.exists(currency_path_log_folder):
    os.makedirs(currency_path_log_folder)

logging.basicConfig(level=logging.INFO)
logging.basicConfig(filename=f'{currency_path_log_folder}/{datetime.now().day}.txt')
logging.Formatter(fmt=' %(name)s : %(levelname)-8s : %(message)s')

logger = logging
