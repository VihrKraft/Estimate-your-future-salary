import requests
from tools import predict_salary
from itertools import count


def get_hh_vacancies(programming_languages):
    area = 1
    per_page = 100
    url = 'https://api.hh.ru/vacancies'
    vacancies_statistic = {}
    for programming_language in programming_languages:
        salary_sum = 0
        vacancies_processed = 0
        for page in count(0, 1):
            payload = {
                'text': programming_language,
                'area': area,
                'page': page,
                'per_page': per_page,
            }
            response = requests.get(url, params=payload)
            pages = response.json()['pages']-1
            if page >= pages:
                break
            response.raise_for_status()
            vacancies_found = response.json()['found']
            vacancies = response.json()['items']
            for vacancy in vacancies:
                vacancy_salary = vacancy['salary']
                if vacancy_salary and vacancy_salary['currency'] == 'RUR':
                    salary = predict_salary(vacancy_salary['from'], vacancy_salary['to'])
                    salary_sum = salary_sum+salary
                    if salary != 0:
                        vacancies_processed += 1
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
        