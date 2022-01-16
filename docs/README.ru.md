# Beard - Attack/Defense CTF scoreboard parser

<p align="center">
<a href=""><img src="https://img.shields.io/badge/supports-Docker-blue" /></a>
<a href=""><img src="https://img.shields.io/badge/license-MIT-red" /></a>
<a href = "https://t.me/redcadets_chat"><img src="https://img.shields.io/badge/chat-telegram-blue?logo=telegram" /></a>

<p align="center">
    Язык: <a href="https://github.com/Red-Cadets/beard">English</a> | <b>Русский</b>
</p>

<b>Beard - инструмент для удобного отслеживания прогресса вашей команды во время A/D CTF соревнований.</b> 

<img src="https://i.ibb.co/FDvzZYJ/image.png">

# ✨ Возможности

- Парсинг поддерживаемых видов турнирных таблиц (hackerdom/forcad)
- График очков всех команд с автоматическим масштабированием для вашей команды
- Примитивное предсказание графика очков
- График потерь флагов для каждого сервиса
- График получения флагов для каждого сервиса (аналогично эффективности эксплойтов)
- Оповещения в телеграм о потере флагов, статусе сервисов, изменении места команды (используйте [курьера](https://github.com/Red-Cadets/courier))

## 🛠 Поддерживаемые турнирные таблицы

| **A/D framework**  | Ссылка | Статус | Описание
| ------------------ | ---- | ------ | -----------
| ForcAD | https://github.com/pomo-mondreganto/ForcAD | ✅ | 
| HackerDom checksystem | https://github.com/HackerDom/checksystem | ✅ | парсинг старой версии на /board

## 🙋 Содержание
* 📖 [Инструкция по быстрой установке](https://github.com/Red-Cadets/beard/blob/master/docs/README.ru.md#-инструкция-по-быстрой-установке)
    * 🐋 [Docker](https://github.com/Red-Cadets/beard/blob/master/docs/README.ru.md#whale-docker)
* 🖼️ [Галерея скриншотов](https://github.com/Red-Cadets/beard/blob/master/docs/README.ru.md#-галерея)
* 🎪 [Сообщество](https://github.com/Red-Cadets/beard/blob/master/docs/README.ru.md#-сообщество)
* 📝 [Планы на будущее](https://github.com/Red-Cadets/beard/blob/master/docs/README.ru.md#-планы-на-будущее)


# 📖 Инструкция по быстрой установке]

## :whale: Docker 

Скачайте репозиторий
```bash
git clone https://github.com/Red-Cadets/beard.git
```
Перейдите в директорию:
```bash
cd beard
```
Измените .env с вашими настройками:
- `HOST` - IP адрес или домен, на котором будет развёрнуто приложение. Данный параметр необходим для настройки CORS. Пример: `http://8.8.8.8` или `http://example.com`
- `SCOREBOARD` - Адрес скорборда. Пример: `http://6.0.0.1`
- `TEAM` - Название команды либо IP команды, информацию о которой необходимо отображать. Пример: `Red Cadets` или `10.10.1.15`
- `TYPE` - Тип скорборда. Пример: `forcad` или `hackerdom`
- `BOT_URL` - Адрес бота (вебхук) для уведомления о событиях. Формат сообщения: ```{"message": "Здесь уведомление", "type": "markdown", "id": "parser"}```. Для простой интеграции бота используйте [курьера](https://github.com/Red-Cadets/courier). Формат сообщения:
```json
{
    "message": "Сообщение уведомления",
    "type": "markdown",
    "id": "parser",
    "to": "id телеграм чата"
}
```
- `ROUND_TIME` - Время раунда в секундах. Например: `120`
- `EXTEND_ROUND` - Количество раундов, на которое необходимо предсказать график очков всех команд. Предсказание происходит на основе очков крайних 5-ти раундов. Например: `10`
- `MONGO_USER` - Пользователь БД. Например: `parser`
- `MONGO_PASS` - Пароль пользователя БД. Например: `parser`

Запустите docker-compose:
```bash
docker-compose up -d
```
и перейдите по ссылке
```bash
http://127.0.0.1:65005/
```

## 🖼️ Галерея

||
|:-------------------------:|
|![Главная страница](https://i.ibb.co/SQrxpVD/Scores.png)|
|График очков всех команд на турнирной таблице|
|![Главная страница](https://i.ibb.co/Sc7vBzs/Echarts-lost.png)
|График потери флагов|
|![Главная страница](https://i.ibb.co/JCQD2g6/Echarts-got.png)|
|График получения флагов|
|![Главная страница](https://i.ibb.co/VCMzK05/image.png)|
|Оповещения в телеграм|



# 🎪 Сообщество

Вы можете оставить информацию о багах или улучшениях в виде ишьюсов.
Мы также открыты к вашим пулл-реквестам и любым видам взаимодействия!

Мы взаимодействуем через Telegram. [Нажмите здесь](https://t.me/redcadets_chat), чтобы вступить в наше сообщество!

## 📝 Планы на будущее

> Открыты к новым идеям!

# ❤️ Благодарности

Парсер турнирной таблицы Hackerdom основан на https://github.com/Vindori/hackerdom-board-parser
