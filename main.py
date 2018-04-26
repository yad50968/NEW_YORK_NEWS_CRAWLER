import os
import xlrd
import time

from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver


def convert_time(input):
    dt = datetime.fromordinal(
        datetime(1900, 1, 1).toordinal() + int(input) - 2)
    return str(dt).split(' ')[0].replace('-', '')


if __name__ == '__main__':

    output_folder = './data/'
    data_file_name = 'example.xlsx'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    topic_list = []
    time_start_list = []
    time_end_list = []

    book = xlrd.open_workbook(data_file_name)
    sheet = book.sheet_by_index(0)
    for row in range(sheet.nrows):
        topic = sheet.cell_value(row, 0)
        start_time = convert_time(sheet.cell_value(row, 1))
        end_time = convert_time(sheet.cell_value(row, 2))
        topic_list.append(topic)
        time_start_list.append(start_time)
        time_end_list.append(end_time)

    driver = webdriver.Firefox()
    for index, t in enumerate(topic_list):
        output_data_folder = output_folder + str(index) + '/'
        if not os.path.exists(output_data_folder):
            os.makedirs(output_data_folder)

        search_url = 'https://www.nytimes.com/search/' + t + '/oldest/' + \
            time_start_list[index] + '/' + time_end_list[index]
        
        driver.get(search_url)

        while True:
            try:
                load_more_button_class = driver.find_element_by_class_name(
                    'Search-showMore--Plid0')
                load_more_button = load_more_button_class.find_element_by_tag_name(
                    'button')
                load_more_button.click()
                time.sleep(2)
            except Exception as e:
                break

        result_list = []
        headline_list = []

        search_html = driver.page_source
        search_soup = BeautifulSoup(search_html, 'lxml')
        search_result = search_soup.find_all(
            'div', {'class': 'Item-wrapper--2ba8L'})
        for result in search_result:
            a = result.find('a').get('href')
            try:
                if result_list[-1] == a:
                    pass
                else:
                    result_list.append(a)
                    headline = result.find(
                        'h4', {'class': 'Item-headline--3WqlT'})
                    headline_list.append(headline.text)
            except:
                result_list.append(a)
                headline = result.find('h4', {'class': 'Item-headline--3WqlT'})
                headline_list.append(headline.text)

        for result_index, r in enumerate(result_list):
            if 'http://' in r:
                news_url = r
            else:
                news_url = 'https://www.nytimes.com' + r
            driver.get(news_url)
            news_html = driver.page_source
            news_soup = BeautifulSoup(news_html, 'lxml')
            try:
                time = news_soup.find('time').attrs['datetime'].split('T')[0]
            except:
                time = ''
            file = open(output_data_folder + str(result_index) + '.txt', 'w+')
            file.write(headline_list[result_index] + '\n')
            file.write(time + '\n')
            content = news_soup.find_all('p', {'class': 'story-body-text'})
            for c in content:
                file.write(c.text + '\n')
            file.close()
    driver.quit()
