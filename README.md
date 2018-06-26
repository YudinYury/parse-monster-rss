# parse-monster-rss
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

запуск скрипта
python parse_on_rss.py
в результате в текущей папке появится файл vacancies.txt
