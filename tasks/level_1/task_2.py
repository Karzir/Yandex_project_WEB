import bs4
import time
from selenium import webdriver


#Найдите минимум три невидимые коровы по звуку. Нажмите "Старт", чтобы начать. Время ограничено!
def main():
    driver = webdriver.Chrome()

    try:
        driver.get('https://findtheinvisiblecow.com/')
        time.sleep(5)
        response = driver.execute_script('return document.documentElement.outerHTML')
        html = bs4.BeautifulSoup(response, 'lxml')
        item = html.find('div', 'sc-hMqMXs itfgTZ')
        if int(str(item)[-7]) >= 3:
            return True
        else:
            return False
    except Exception as ex:
        print('Кажется вы сделали что-то не так! Внимательно прочитайте инструкцию внизу сайта и попробуйте снова.')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
