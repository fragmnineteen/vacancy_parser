from flask import Flask, render_template, request
from main import get_vacancies
import psycopg2

app = Flask(__name__)

host = 'db'
user = "postgres"
password = "1"
db_name = 'vacancies'

def fetch_vacancies(keyword=None, city=None, employer=None):
    connection = None

    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name    
        )
        connection.autocommit = True
        
        sql_query = "SELECT id, name, url, employer, salary, area FROM vacancies_table"
        conditions = []
        values = []

        if keyword:
            conditions.append("name ILIKE %s")
            values.append(f"%{keyword}%")
        if city:
            conditions.append("area ILIKE %s")
            values.append(f"%{city}%")
        if employer:
            conditions.append("employer ILIKE %s")
            values.append(f"%{employer}%")

        if conditions:
            sql_query += " WHERE " + " AND ".join(conditions)

        with connection.cursor() as cursor:
            cursor.execute(sql_query, values)
            vacancies = cursor.fetchall()

        return vacancies
        
    except Exception as ex:
        print("[INFO] Error while fetching vacancies from PostgreSQL", ex)
        return []
    
    finally:
        if connection:
            connection.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form.get('search_keyword')
        if keyword:
            get_vacancies(keyword)
        else:
            get_vacancies("")
        vacancies = fetch_vacancies()
        return render_template('index.html', vacancies=vacancies)
    else:
        vacancies = fetch_vacancies()
        return render_template('index.html', vacancies=vacancies)

@app.route('/filter', methods=['POST'])
def filter_vacancies():
    keyword = request.form.get('keyword')
    city = request.form.get('city')
    employer = request.form.get('employer')

    vacancies = fetch_vacancies(keyword=keyword, city=city, employer=employer)
    return render_template('index.html', vacancies=vacancies)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
