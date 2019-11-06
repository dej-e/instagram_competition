# Инструмент для конкурсов в Instagram

Скрипт ищет победителей конкурса в [Instagram](https://www.instagram.com/)


### Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

Для работы скрипта необходимо зарегистрироваться в Instagram.
 
Если у вас нет аккаута в Instagram, создайте его.

После клонирования проекта создайте в корень файл ```.env``` с таким содержимым:
```
INSTAGRAM_LOGIN=_ваш логин от Instagram_
INSTAGRAM_PASSWORD=_ваш пароль от Instagram_
INSTAGRAM_DIR=instagram
```


### Пример запуска

```python competition.py _ссылка на конкурс в Instagram_```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).