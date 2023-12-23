import psycopg2

from config_data.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        self.__cur = self.conn.cursor()

    def execute_query_and_commit(self, query, values=None):
        with self.conn.cursor() as cursor:
            cursor.execute(query, values)
            self.conn.commit()

    def getQueryResult_fetchall(self, query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
            if res:
                return res
            return []

    def getQueryResult_fetchone(self, query):
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchone()
            if res:
                return res
            return None

    def exception_func(self, query, one=False):
        try:
            if one:
                return self.getQueryResult_fetchone(query)
            return self.getQueryResult_fetchall(query)
        except psycopg2.Error:
            print('Ошибка чтения из БД')
        return []

    def getRegions(self):
        query = """SELECT id, part_of_world FROM regions"""
        return self.exception_func(query)

    def getCountries(self, id_):
        query = f"""SELECT id, country FROM countries where id_part_of_world = '{id_}'"""
        return self.exception_func(query)

    def getCitites(self, id_):
        query = f"""SELECT id, city FROM cities where id_country = '{id_}'"""
        return self.exception_func(query)

    def getDesCity(self, id_):
        query = f"""SELECT code FROM cities WHERE id = '{id_}'"""
        return self.exception_func(query, one=True)

    def getDesRusCity(self, id_):
        query = f"""SELECT code FROM russian_cities WHERE id = '{id_}'"""
        return self.exception_func(query, one=True)

    def getRusCity(self, id_):
        query = f"""SELECT city FROM russian_cities WHERE id = '{id_}'"""
        return self.exception_func(query)

    def getRussianCitiesFirstChar(self):
        query = f"""SELECT DISTINCT LEFT(city, 1) from russian_cities"""
        return self.exception_func(query)

    def getRussianCities(self, first_char):
        query = f"""SELECT id, city FROM russian_cities where left(city, 1) = '{first_char}'"""
        return self.exception_func(query)

bot_database = Database()

# Инициализируем "базу данных"
users_db = {}

# Создаем шаблон заполнения словаря с пользователями
user_dict_template = {
    'departure_city': '',
    'destination_city': '',
    'date': ''
}
