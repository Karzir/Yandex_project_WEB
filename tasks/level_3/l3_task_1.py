import bs4
import time
from selenium import webdriver


# Получите 1 уровень в тетрисе, играя в режиме Solo. Нажмите "Старт", чтобы начать. Время ограничено!
# (Регистрироваться и входить не надо, засчитывается только последняя попытка)
# Инструкция: Вы не должны закрывать открывшееся окно самостоятельно! Дождитесь пока оно закроется само. В противном случае задание не будет засчитано!!!
def main():
    driver = webdriver.Chrome()

    try:
        driver.get('https://online-tetris.ru/')
        time.sleep(200)
        response = driver.execute_script('return document.documentElement.outerHTML')
        html = bs4.BeautifulSoup(response, 'lxml')
        item = html.find('span', 'local-level')
        if int(str(item)[-8]) >= 1:
            return True
        else:
            return False
    except Exception as ex:
        return False
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
