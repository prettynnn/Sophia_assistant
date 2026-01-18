from .db_config import *
from aiomysql import ProgrammingError, IntegrityError, DataError, OperationalError, InterfaceError, InternalError
from others.config import log

import aiomysql

async def connector_to_server():
    connect = await aiomysql.connect(host=DB_HOST,
                                     password=DB_PASSWORD,
                                     user=DB_USER,
                                     port=DB_PORT,
                                     autocommit=True)
    return connect
        
async def create_database(connect):
    try:
        csr = await connect.cursor()
        await csr.execute('CREATE DATABASE IF NOT EXISTS SophiaBase')
    except InternalError:
        log(f'Error creating database!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()

async def create_table(connect):
    try:
        csr = await connect.cursor()
        await csr.execute('USE SophiaBase')
        await csr.execute('CREATE TABLE IF NOT EXISTS SophiaTable ('
                          'id INT PRIMARY KEY AUTO_INCREMENT, '
                          'users BIGINT, '
                          'roles TEXT, '
                          'contents TEXT)')
                          
    except OperationalError:
        log('Server is not available!')
    except InternalError:
        log(f'Error connecting database!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()
async def include_in_table(connect, user, role, content):
    try:
        csr = await connect.cursor()
        await csr.execute('USE SophiaBase')
        await csr.execute('INSERT IGNORE INTO SophiaTable (users, roles, contents) '
                          'VALUES (%s, %s, %s)', 
                          (user, 
                           role, 
                           content))
    except OperationalError:
        log('Server is not available!')
    except ProgrammingError:
        log(f'Invalid syntax')
    except DataError:
        log('Invalid length data!')
    except IntegrityError:
        log('An error was detected in the data while loading!')
    except InterfaceError:
        log('Connection to database is refused!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()
        
async def select_data_from_table(connect, user, role, content):
    try:
        csr = await connect.cursor()
        await csr.execute('USE SophiaBase')
        await csr.execute('SELECT users FROM SophiaTable '
                          'WHERE users = %s '
                          'AND roles = %s '
                          'AND contents = %s '
                          'ORDER BY id DESC '
                          'LIMIT 50', 
                          (user, 
                           role, 
                           content))
        results = await csr.fetchall()
        if results != None:
            return results
        else:
            return []
    except OperationalError:
        log('Server is not available!')
    except ProgrammingError:
        log('Incorrect a data!')
    finally:
        if csr is None:
            return
        else:
            await csr.close()
