import argparse
import requests
import datetime
import pythonwhois
from os import path

def load_urls4check(path):
    try:
        with open(path) as file:
            return [line for line in file.read().splitlines()]
    except IOError as error:
        print ('Не могу прочитать файл')
        return None


def is_server_respond_with_200(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        print('Сайт {} не существует'.format(url))
        return None

def get_domain_expiration_date(domain_name):
    who =  pythonwhois.get_whois(domain_name.split('//')[1])
    return who['expiration_date'][0]

def print_results(url, respond_200,expiration):
    if respond_200 == None:
        return None
    print(expiration,respond_200)

    if respond_200 == True and expiration > 31:
        print ('OK  Ответ от сервера {} - 200, количество оставшихся дней до окончания делегирования - {}'
               .format(url, expiration))
    else:
        print ('Внимание! Ответ от сервера {} - {}, количество оставшихся дней до окончания делегирования - {}'
               .format(url, respond_200, expiration))

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-f','--file', required=True)
    arguments = args.parse_args()
    urls=load_urls4check(arguments.file)
    for url in urls:
        days =  get_domain_expiration_date(url) - datetime.datetime.now()
        print_results(url, is_server_respond_with_200(url), days.days)

