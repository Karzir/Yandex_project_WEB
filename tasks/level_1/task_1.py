import bs4
import time
from selenium import webdriver


#Получите результат 200 или больше на сайте с прикольным котиком. Нажмите "Старт", чтобы начать. Время ограничено!
def main():
    driver = webdriver.Chrome()

    try:
        driver.get('https://popcat.click/')
        time.sleep(5)
        response = driver.execute_script('return document.documentElement.outerHTML')
        html = bs4.BeautifulSoup(response, 'lxml')
        item1 = html.find('div', 'cat-img p')
        item2 = html.find('div', 'cat-img op')
        if not (item1 is None):
            item1 = str(item1).split('>')
            if len(item1) < 3:
                print('Совет: попытайтесь кликнуть на котика в центре')
            else:
                if int(item1[-3][:-5]) >= 200:
                    print('Задание выполнено)')
                else:
                    print('Не получилось( Попробуйте ещё раз!')
        else:
            item2 = str(item2).split('>')
            if len(item2) < 3:
                print('Совет: попытайтесь кликнуть на котика в центре')
            else:
                if int(item2[-3][:-5]) >= 200:
                    print('Задание выполнено)')
                else:
                    print('Не получилось( Попробуйте ещё раз!')
    except Exception as ex:
        print('Кажется вы сделали что-то не так! Внимательно прочитайте инструкцию внизу сайта и попробуйте снова.')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()

