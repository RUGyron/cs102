import config
import telebot
import requests
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.token)

"""

@bot.message_handler(content_types=["text"])
def repeater(message):  # Название функции не играет никакой роли, в принципе
     bot.send_message(message.chat.id, message.text)

"""


def get_page(week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group='K3140')
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")
    if type(day) == list:
        day = day[0]
    # Получаем таблицу с расписанием на день недели
    schedule_table = soup.find("table", attrs={"id": "1day"})
    if day == '/monday' or day == '/sunday' or day == '/Monday' or day == '/Sunday':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    elif day == '/tuesday' or day == '/Tuesday':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    elif day == '/wednesday' or day == '/Wednesday':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    elif day == '/thursday' or day == '/Thursday':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    elif day == '/friday' or day == '/Friday':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    elif day == '/saturday' or day == '/Saturday':
        schedule_table = soup.find("table", attrs={"id": "6day"})
    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n') for lesson in lessons_list]
    lessons_list = [''.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
                               'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
def get_day(message):
    if len(message.text.split()) == 2:
        day, week = message.text.split()
        web_page = get_page(week)
    else:
        day = message.text.split()
        web_page = get_page()
    times_lst, locations_lst, lessons_lst = get_schedule(web_page, day)

    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
