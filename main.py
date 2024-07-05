import requests
import psycopg2

host = 'db'
user = "postgres"
password = "1"
db_name = 'vacancies'


def create_vacancies_table():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS vacancies_table (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                employer TEXT NOT NULL,
                salary TEXT NOT NULL,
                area TEXT NOT NULL
            )
            """
            cursor.execute(create_table_query)

    except Exception as ex:
        print("[INFO] Error while creating vacancies_table:", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def clear_vacancies_table():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        with connection.cursor() as cursor:
            clear_table_query = """
            DROP TABLE IF EXISTS vacancies_table CASCADE;
            """
            cursor.execute(clear_table_query)

        create_vacancies_table()

    except Exception as ex:
        print("[INFO] Error while clearing vacancies_table:", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def database_insertion(data_to_insert):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        sql_query = """
        INSERT INTO vacancies_table (id, name, url, employer, salary, area)
        VALUES (%s, %s, %s, %s, %s, %s);
        """

        with connection.cursor() as cursor:
            cursor.execute(sql_query, data_to_insert)

    except Exception as ex:
        print("[INFO] Error while inserting into vacancies_table:", ex)
    finally:
        if connection:
            connection.close()
            print("[INFO] PostgreSQL connection closed")


def get_vacancies(keyword):
    clear_vacancies_table()

    url = "https://api.hh.ru/vacancies"
    params = {
        "text": keyword,
        "per_page": 40,
    }
    headers = {
        "User-Agent": "Your User Agent",
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        vacancies = data.get("items", [])
        for vacancy in vacancies:
            vacancy_id = vacancy.get("id")
            vacancy_area = vacancy.get("area").get('name')
            vacancy_title = vacancy.get("name")
            vacancy_url = vacancy.get("alternate_url")
            company_name = vacancy.get("employer", {}).get("name")
            salary_info = vacancy.get("salary")
            if salary_info:
                salary_value = f'{salary_info.get("from", "")} - {salary_info.get("to", "")} {salary_info.get("currency", "")}'
            else:
                salary_value = 'Заработная плата не указана'
            data_to_insert = [vacancy_id, vacancy_title, vacancy_url, company_name, salary_value, vacancy_area]
            database_insertion(data_to_insert)
    else:
        print(f"Request failed with status code: {response.status_code}")


if __name__ == "__main__":
    create_vacancies_table()