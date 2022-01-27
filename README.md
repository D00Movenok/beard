# Beard - Attack/Defense CTF scoreboard parser

<p align="center">
<a href=""><img src="https://img.shields.io/badge/supports-Docker-blue" /></a>
<a href=""><img src="https://img.shields.io/badge/license-MIT-red" /></a>

<p align="center">
    Language: <b>English</b> | <a href="https://github.com/D00Movenok/beard/blob/master/docs/README.ru.md">Русский</a>
</p>

<b>Beard - a comfortable way to track progress of your team during A/D competitions</b>
</p>


<img src="https://i.ibb.co/FDvzZYJ/image.png">

# ✨ Features

- Parsing of supported scoreboards (hackerdom/forcad)
- Score graph of all teams with automatic scaling for your team
- Primitive prediction of the score graph
- Flag loss graph for each service
- Graph of receiving flags for each service (similar to the effectiveness of exploits)
- Telegram alerts about flag loss, service status, place changing (use [achtung](https://github.com/D00Movenok/achtung))

## 🛠 Supported scoreboards

| **A/D framework**  | Link | Status | Description
| ------------------ | ---- | ------ | -----------
| ForcAD | https://github.com/pomo-mondreganto/ForcAD | ✅ | 
| HackerDom checksystem | https://github.com/HackerDom/checksystem | ✅ | parsing old-style view at /board

## 🙋 Table of Contents
* 📖 [Fast Installation Guide](https://github.com/D00Movenok/beard#-fast-installation-guide)
    * 🐋 [Docker Usage](https://github.com/D00Movenok/beard#whale-docker)
* 🖼️ [Gallery](https://github.com/D00Movenok/beard#-gallery)


# 📖 Fast Installation Guide

## :whale: Docker 

Clone repository
```bash
git clone https://github.com/D00Movenok/beard.git
```
Go to folder:
```bash
cd beard
```
Change .env with your settings:
- `SCOREBOARD` - Scoreboard location. Example: `http://6.0.0.1/board`
- `TEAM` - Team name or team IP to display information about. Example: `FaKappa` or `10.10.1.15`
- `TYPE` - Scoreboard type. Example: `forcad` or `hackerdom`
- `BOT_URL` and `BOT_TOKEN` - Telegram bot api address (webhook) for notification. For easy bot integration, use [achtung](https://github.com/D00Movenok/achtung).
- `ROUND_TIME` - Round time in seconds. For example: `120`
- `EXTEND_ROUND` - The number of rounds to predict future graph. The prediction is based on the points of the last 5 rounds. For example: `10`
- `MONGO_USER` - DB username. Например: `parser`
- `MONGO_PASS` - DB password. Например: `parser`
Run docker-compose:
```bash
docker-compose up -d
```
and go to URL
```bash
http://127.0.0.1:65005/
```

## 🖼️ Gallery

||
|:-------------------------:|
|![Главная страница](https://i.ibb.co/SQrxpVD/Scores.png)|
|Graph of scores of all teams on the scoreboard|
|![Главная страница](https://i.ibb.co/Sc7vBzs/Echarts-lost.png)
|Flag loss graph|
|![Главная страница](https://i.ibb.co/JCQD2g6/Echarts-got.png)|
|Graph of receiving flags|
|![Главная страница](https://i.ibb.co/VCMzK05/image.png)|
|Telegram alerts|
