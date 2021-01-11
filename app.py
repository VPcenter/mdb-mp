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
    begin_time_general_process = time()
    try:
        client=MongoClient('mongodb://travis:test@127.0.0.1:27017/mydb')
        logger.opt(colors=True).debug(f'<c>{client.list_database_names()}</c>')
        db=client['mydb']
        collection = db['contacts'] 
        for idx in range(10):
            collection.insert_one({"name":"Mr.Geek","eid":idx})
        cursor=collection.find()
        logger.opt(colors=True).info(f'<g>Number of documents {collection.count_documents()}</g>')
        for record in cursor: 
            logger.info(f'{record}')
    except:
        logger.opt(colors=True).debug(f'<y>No connection</y>')
    

    with Pool(processes=8, initializer=set_logger, initargs=(logger,)) as pool:
        pool.map(multiple_mdb_connection, range(10))

    end_time_general_process = time()
    logger.opt(colors=True).debug('Processing time: <c>{:02d}:{:02d}:{:02d}</c>'.format(
        int(end_time_general_process - begin_time_general_process) // 3600, 
        (int(end_time_general_process - begin_time_general_process) % 3600 // 60), 
        int(end_time_general_process - begin_time_general_process) % 60))
    logger.info("Done")