from db_config import *
from imports import *
from aiomysql import ProgrammingError, IntegrityError, DataError, OperationalError, InterfaceError, InternalError

async def create_database():
    try:
        connect = await aiomysql.connect(host=DB_HOST,
                                         password=DB_PASSWORD,
                                         user=DB_USER,
                                         port=DB_PORT,
                                         autocommit=True)
        csr = await connect.cursor()
        await csr.execute('CREATE DATABASE IF NOT EXISTS Sophia')
        return connect
    except InternalError:
        log(f'Error creating database!')
    finally:
        await csr.close()

async def create(connect):
    try:
        csr = await connect.cursor()
        await csr.execute('USE Sophia')
        await csr.execute('CREATE TABLE IF NOT EXISTS SophiaTable ('
                          'id int PRIMARY KEY AUTO_INCREMENT,'
                          'role varchar(128),'
                          'content varchar(8092))')
    except OperationalError:
        log('Server is not available!')
        reconnect = await create_database()
    except InternalError:
        log(f'Error connecting database!')
    finally:
        await csr.close()

async def include(connect, role, content):
    try:
        csr = await connect.cursor()
        await csr.execute('USE Sophia')
        await csr.execute('INSERT IGNORE INTO SophiaTable (role, content)'
                          'VALUES (%s, %s)', 
                          (role, content))
    except OperationalError:
        log('Server is not available!')
        reconnect = await create_database()
    except ProgrammingError:
        log(f'Invalid syntax')
    except DataError:
        log('Invalid length data!')
    except IntegrityError:
        log('An error was detected in the data while loading!')
    except InterfaceError:
        log('Connection to database is refused!')
    finally:
        await csr.close()
        
async def select_data(connect, role, content):
    try:
        csr = await connect.cursor()
        await csr.execute('USE Sophia')
        await csr.execute('SELECT * FROM SophiaTable (' 
                          'SELECT role, content FROM messages'
                          'ORDER BY id DESC'
                          'LIMIT 40)')
        role = await csr.fetchall()
        content = await csr.fetchall()
        return role, content
    except OperationalError:
        log('Server is not available!')
        reconnect = await create_database()
    except ProgrammingError:
        log('Incorrect a data!')
    finally:
        await csr.close()