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
        client=MongoClient('mongodb://travis:test@127.0.0.1:27017/mydb')
        logger.opt(colors=True).debug(f'<c>{client.list_database_names()}</c>')
        collection = client['contacts'] 
  
        emp_rec1 = { 
                "name":"Mr.Geek", 
                "eid":24, 
                "location":"delhi"
                } 
        emp_rec2 = { 
                "name":"Mr.Shaurya", 
                "eid":14, 
                "location":"delhi"
                } 
        
        # Insert Data 
        rec_id1 = collection.insert_one(emp_rec1) 
        rec_id2 = collection.insert_one(emp_rec2) 
        
        logger.info(f'Data inserted with record ids {rec_id1} & {rec_id2}') 
        
        # Printing the data inserted 
        cursor = collection.find() 
        for record in cursor: 
            logger.info(f'{record}')
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