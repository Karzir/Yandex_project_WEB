import requests
import bs4


# Давайте предстаим что вы выйграли миллион рублей в лотерею. Интересно сколько у вас теперь долларов по последнему курсу?
# Введите целую часть суммы в строку и нажмите кнопку "проверить". Актуальный курс можно посмотреть здесь.
def main():
    try:
        response = requests.get('https://www.cbr.ru/')
        html = bs4.BeautifulSoup(response.text, 'lxml')
        box = html.find_all('div', 'col-md-2 col-xs-9 _right mono-num')
        item = str(box[-3]).split(',')
        item1 = item[0]
        if item1[-3] == '>':
            item1 = int(item1[-2:])
        else:
            item1 = int(item1[-3:])
        item2 = int(str(item[1])[:4]) / 10000
        return int(1000000 // (item1 + item2))
    except Exception as ex:
        print('Введите, пожалуйста, только целую часть суммы в долларах арабскими цифрами')


if __name__ == '__main__':
    main()
