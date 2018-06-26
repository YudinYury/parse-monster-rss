'''Тестовое задание на вакансию Data Miner:
Написать парсер на https://www.monster.com/
Какие данные собирать: необходимо собрать текста описания
вакансий.
Пример ссылки на вакансию: https://job-
openings.monster.com/Advisory-Financial-Services-Oracle-
Accounts-Payable-Senior-Associate-New-York-NY-US-
PWC/22/c6e97461-efec-40e2-a6b4-77bb4330a271

Текста необходимо записывать в файл, каждое описание новой
вакансии на отдельной строке.
Код необходимо опубликовать на github.com с кратким readme
как запустить парсер.
Парсер должен быть написан на языке Python.

К сайту есть доступ через rss
http://rss.jobsearch.monster.com/rssquery.ashx
им и воспользуемся в уточненном формате
http://rss.jobsearch.monster.com/rssquery.ashx/?q='python'

Оставил несколько принтов - если их "включить", то работа программы станет нагляднее - будет видно что не зависла.
'''

from html.parser import HTMLParser
import logging
import requests
import re


# levels (from low to high): DEBUG -> INFO -> WARNING -> ERROR -> CRITICAL.
logging.basicConfig(level=logging.ERROR, format='[line:%(lineno)d]# %(asctime)s * %(levelname)s *** %(message)s')


class MonsterRssPageParser(HTMLParser):
    # этот класс для парсинга RSS выдачи и получения ссылок на вакансии
    def __init__(self):
        HTMLParser.__init__(self)
        self.vacancies_list = []
        self.title = None
        self.description = None
        self.link = None
        self.pub_date = None
        self.data = ''
        self.start_item = False
        self.start_title = False
        self.start_description = False
        self.start_link = False
        self.start_pub_date = False
        self.start_search = False
        self.start_save_data = False

    def print_vacancies_list(self):
        print(f'class: vacancies_list = {self.vacancies_list}')

    def get_vacancies_list(self):
        return self.vacancies_list

    def handle_starttag(self, tag, attrs):
        if tag == 'item':
            logging.debug("Start  :", tag)
            self.start_search = True
            return

        if not self.start_search:
            return

        logging.debug("Start  :", tag)
        # logging.debug(f'AAAAAAAAAAAAAAAAAAAAAAAAA     Нашеееел !!!')
        self.start_search = True

        if self.start_search and tag == 'title':
            self.start_title = True

        if self.start_search and tag == 'description':
            self.start_description = True

        if self.start_search and tag == 'link':
            self.start_link = True

        if self.start_search and tag == 'pubdate':
            self.start_pub_date = True

    def handle_endtag(self, tag):
        if not self.start_search:
            return
        logging.info("End   :", tag)
        logging.info("End   :", tag)
        if tag == 'item':
            new_vacancy = {
                'title': self.title,
                'description': self.description,
                'link': self.link,
                'pub_date': self.pub_date
            }
            logging.debug(f"Make new_vacancy: {new_vacancy}")
            self.vacancies_list.append(new_vacancy)
            self.start_search = False
            self.start_save_data = False
            self.start_item = False
            self.title = None
            self.description = None
            self.link = None
            self.pub_date = None
            logging.info('End of search')
            return
        if self.start_search and tag == 'title':
            self.start_title = False
            return
        if self.start_search and tag == 'description':
            self.start_description = False
            return
        if self.start_search and tag == 'link':
            self.start_link = False
            return
        if self.start_search and tag == 'pubDate':
            self.start_pub_date = False
            return

    def handle_data(self, data):
        if not self.start_search:
            return
        logging.debug("DATA  :", data)
        logging.debug("self.start_title  :", self.start_title)
        logging.debug("self.start_description  :", self.start_description)
        if self.start_title:
            self.title = data
            logging.info(f'handle_data start_title = {self.title}')
        if self.start_description:
            self.description = data
            logging.info(f'handle_data start_description = {data}')
        if self.start_link:
            self.link = data
            logging.info(f'handle_data start_link = {data}')
        if self.start_pub_date:
            self.pub_date = data
            logging.info(f'handle_data start_link = {data}')


class MonsterVacancyPageParser(HTMLParser):
    # этот класс для парсинга непосредственно страницы вакансии и получения описания вакансии
    # для парсинга примера из задания достаточно этого класса
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = ''
        self.start_search = False
        self.start_save_data = False

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            # logging.info(f'AAAAAAAAAAAAAAAAAAAAAAAAA     Нашеееел !!!')
            self.start_search = True

        if len(attrs):
            logging.debug(f'tag.attrs = {attrs}')
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'detail-content':
                    self.start_search = True


    def handle_endtag(self, tag):
        logging.info("End   :", tag)
        if tag == '/div':
            self.start_search = False
            self.start_save_data = False
            logging.info('End of search')

    def handle_data(self, data):
        if self.start_search:
            if data == 'About the Job':
                self.start_save_data = True
                return

            if self.start_save_data and len(data) > 2:
                if is_valid_text(data):
                    self.data += data

            if self.start_save_data and data == 'Want more jobs like this?': #  'View more info'
                self.start_save_data = False

def get_html(page_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    return requests.get(page_url, headers = headers)


def parce_vacancy_page(url):
    logging.info(f'start parcing for {url}')
    vacancy_parser = MonsterVacancyPageParser()
    vacancy_parser.feed(get_html(url).text)
    return vacancy_parser.data


def is_valid_text(text):
    words = re.findall(r'\w+', text)
    if len(words) == 0:
        return False
    if len(words) > 1 or len(words[0]) > 2:
        return True
    return False


def save_vacancies_to_file(self, file_name):
    print(f'Save searches vacancies file {file_name}')
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write('\n'.join(self.links))


def del_view_more_info(text):
    match = re.search(r'View more info', text)
    if not match:
        return text
    idx = match.span()[0]
    text = text[:idx]
    text = re.sub("^\s+|\n|\r|\s+$", '', text) # удаляю пробелы в начале и конце строки и символы переноса строки
    return text

def _main():
    key_word = 'python'
    file_name = 'vacancies.txt'

    logging.info(f'start parcing RSS')
    parser = MonsterRssPageParser()
    parser.feed(get_html(f'http://rss.jobsearch.monster.com/rssquery.ashx/?q="{key_word}"').text)
    vacancies_list = parser.get_vacancies_list()
    # print('Find vacancies in Monster.com for keyword "{}": founded {}'.format(key_word, len(vacancies_list)))

    num = 0
    vacancies_list_for_file = []
    for vacancy in vacancies_list:
        num += 1
        url = vacancy['link']
        title =  vacancy['title']
        description = del_view_more_info(parce_vacancy_page(url))
        # print()
        # print(f'title vacancy #{num}: {title}')
        # print(f'description: {description}')

        # если использовать строку кода, которая чуть ниже, то текст в файле будет более читаемым
        # vacancies_list_for_file.append('title: ' + title + '\n' + 'description: ' + description)

        # если использовать эту строку кода, то все описания вакансий будут
        vacancies_list_for_file.append(description)
        # if num > 3:
        #     break

    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('\n'.join(vacancies_list_for_file))


if __name__ == "__main__":
    _main()

