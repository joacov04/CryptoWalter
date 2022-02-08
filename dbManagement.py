import sqlite3

conn = sqlite3.connect('data.db')
curs = conn.cursor()


def insert_user(name, api, api_secret):
    '''Inserts a new user into the database'''
    with conn:
        curs.execute("INSERT INTO api VALUES (:user, :api_key, :secret_api)", {'user': name, 'api_key': api, 'secret_api': api_secret})


def get_api(user):
    '''Returns id, api_key and secret_api matching with the discord username'''
    with conn:
        curs.execute("SELECT * FROM api WHERE user=:user", {'user': user})
        return curs.fetchone()


def get_user(api):
    '''Returns id, username and secret_api matching with the api_key'''
    with conn:
        curs.execute("SELECT * FROM api WHERE api_key=:api", {'api': api})
        return curs.fetchone()


def get_only_api(user):
    '''Returns api_key matching with the discord username'''
    with conn:
        curs.execute("SELECT api_key FROM api WHERE user=:user", {'user': user})
        return curs.fetchone()


def get_only_user(api):
    '''Returns username matching with the api_key'''
    with conn:
        curs.execute("SELECT user FROM api WHERE api_key=:api", {'api': api})
        return curs.fetchone()


def get_all_data():
    '''Returns all data from the database'''
    with conn:
        curs.execute("SELECT * FROM api")
