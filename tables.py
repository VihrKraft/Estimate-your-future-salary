from terminaltables import AsciiTable
from HeadHunter import get_hh_vacancies
from SuperJob import get_sj_vacancies
from dotenv import load_dotenv
import os

def create_job_table(vacancies_statistic):
    table = [
        ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата'],
    ]
    for programming_language in vacancies_statistic:
        vacancies_statistic_programming_language = [programming_language, vacancies_statistic[programming_language]['vacancies_found'], vacancies_statistic[programming_language]['vacancies_processed'], vacancies_statistic[programming_language]['average_salary']]
        table.append(vacancies_statistic_programming_language)
    table = AsciiTable(table)
    print(table.table)


def main():
    load_dotenv()
    sj_secret_key = os.getenv('SUPERJOB_SECRET_KEY')
    programming_languages = ['Python', 'JavaScript', 'Java', 'Ruby:', 'PHP', 'C++', 'C#', 'C']
    vacancies_statistic_hh = get_hh_vacancies(programming_languages)
    create_job_table(vacancies_statistic_hh)
    vacancies_statistic_sj = get_sj_vacancies(programming_languages, sj_secret_key)
    create_job_table(vacancies_statistic_sj)

if __name__ == '__main__':
    main()