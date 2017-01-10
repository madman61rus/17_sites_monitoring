import argparse
import requests
import datetime
import whois
from urllib.parse import urlparse


def load_urls4check(path):
    try:
        with open(path) as file:
            return file.read().splitlines()
    except IOError:
        return None


def is_server_respond_with_200(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return None


def get_domain_expiration_date(domain_name):
    who = whois.query(urlparse(domain_name).netloc)
    return who.expiration_date


def print_results(url, respond_200, expiration):
    if respond_200 is None:
        return None

    if respond_200 and expiration > 31:
        message = 'OK Ответ от сервера {} - 200, кол-во оставшихся дней - {}'
        print(message.format(url, expiration))
    else:
        message = 'Внимание! Ответ от сервера {} не 200, кол-во оставшихся дней - {}'
        print(message.format(url, expiration))


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('-f', '--file', required=True)
    arguments = args.parse_args()
    urls = load_urls4check(arguments.file)
    for url in urls:
        response = is_server_respond_with_200(url)
        if response is None:
            print('Внимание ! Домен {} не найден'.format(url))
        else:
            days = get_domain_expiration_date(url) - datetime.datetime.now()
            print_results(url, response, days.days)
