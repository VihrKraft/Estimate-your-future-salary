import requests
from itertools import count
from tools import predict_salary


def get_sj_vacancies(programming_languages, secret_key):
    town = 4
    per_page = 100
    url = 'https://api.superjob.ru/2.0/vacancies/'
    vacancies_statistic = {}
    for programming_language in programming_languages:
        salary_sum = 0
        vacancies_processed = 0
        vacancies_found = 0
        headers = {
            'X-Api-App-Id': secret_key,
        }
        for page in count(0, 1):
            payload = {
                'town': town,
                'keyword': programming_language,
                'page': page,
                'count': per_page,
            }
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            vacancies_found = response.json()['total']
            vacancies = response.json()['objects']
            for vacancy in vacancies:
                if vacancy['currency'] == 'rub':
                    salary = predict_salary(vacancy['payment_from'], vacancy['payment_to'])
                    salary_sum = salary_sum+salary
                    if salary != 0:
                        vacancies_processed += 1
            more = response.json()['more']
            if not more:
                break
        try:
            average_salary = int(salary_sum/vacancies_processed)
        except ZeroDivisionError:
            average_salary = 0
        vacancies_statistic[programming_language] = {
            "vacancies_found": vacancies_found,
            "vacancies_processed": vacancies_processed,
            "average_salary": average_salary,
        }
    return vacancies_statistic