import multiprocessing
import sys
import os

from pymongo.errors import ConnectionFailure
from multiprocessing import Pool
from pymongo import MongoClient
from loguru import logger
from time import time


def set_logger(logger_):
    global logger
    logger = logger_

def multiple_mdb_connection(stck_nmbr):
    logger.opt(colors=True).info(f'{multiprocessing.current_process().name} <c>///</c> {stck_nmbr}')


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level='DEBUG', format="<g>{time:YYYY-MM-DD HH:mm:ss}</g> | <m>{level}</m> | {message}", enqueue=True)
    
    try:
        client=MongoClient('mongodb://travis:test@127.0.0.1:27017/')
        db=client['mydb_test']
        list_of_db = client.list_database_names()
        if "mydb_test" in list_of_db:
            logger.debug(f'Exits')  
    except:
        logger.opt(colors=True).debug(f'<y>No connection</y>')



    begin_time_general_process = time()

    with Pool(processes=8, initializer=set_logger, initargs=(logger,)) as pool:
        pool.map(multiple_mdb_connection, range(10))

    end_time_general_process = time()
    logger.opt(colors=True).debug('Processing time: <c>{:02d}:{:02d}:{:02d}</c>'.format(
        int(end_time_general_process - begin_time_general_process) // 3600, 
        (int(end_time_general_process - begin_time_general_process) % 3600 // 60), 
        int(end_time_general_process - begin_time_general_process) % 60))
    logger.info("Done")