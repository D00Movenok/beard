import os
import requests
import coloredlogs
import logging

import board_parser

coloredlogs.install()

URL = os.getenv('BOT_URL', 'https://bot.example.com/key')
TOKEN = os.getenv('BOT_TOKEN')


class AD(object):
    def __init__(self, ip, driver, scoreboard, teamname):
        global info, delta, soup
        delta = []
        self.ip = ip
        self.teamname = teamname
        self.scoreboard = scoreboard

        if not driver:
            soup = board_parser.get_soup_by_address(self.scoreboard)
        else:
            soup = None

        self.patch = board_parser.init_patch(driver, soup)

        self.round = board_parser.get_current_round(driver, soup)
        info = board_parser.get_teams_info(driver, soup)

    def get_info_by_ip(self, ip):
        for team in info:
            if team['ip'] == ip:
                return team
        logging.critical("Нет команды с IP {ip}".format(ip=ip))

    def get_info_by_name(self, name):
        for team in info:
            if team['name'] == name:
                return team
        logging.critical("Нет команды с названием {}".format(name))

    def dump(self):
        return info

    def get_delta_by_ip(self, ip):
        for team in delta:
            if team['ip'] == ip:
                return team
        logging.critical("Нет команды с IP {ip}".format(ip=ip))

    def get_delta_by_name(self, name):
        for team in delta:
            if team['name'] == name:
                return team
        logging.critical("Нет команды с названием {name}".format(name=name))

    def refresh(self, driver):
        global info
        if driver:
            driver.get(self.scoreboard)
            current_round = board_parser.get_current_round(driver, None)
            if self.round != current_round:
                new_info = board_parser.get_teams_info(driver, None)
                self.round = current_round
                self.__recalculate_delta(new_info)
                info = new_info
                return True
            else:
                return False
        else:
            new_soup = board_parser.get_soup_by_address(self.scoreboard)
            new_info = board_parser.get_teams_info(driver, new_soup)
            current_round = board_parser.get_current_round(driver, new_soup)
            if self.round != current_round:
                self.round = current_round
                self.__recalculate_delta(new_info)
                info = new_info.copy()
                return True
            else:
                return False

    def __recalculate_delta(self, new_info):
        global delta
        delta = []
        for team_new in new_info:
            if self.ip:
                team_old = self.get_info_by_ip(team_new['ip'])
            else:
                team_old = self.get_info_by_name(team_new['name'])
            delta_services = {}
            for service_new, service_old in zip(team_new['services'], team_old['services']):
                name = service_new['name']
                team_got_new_flags = service_new['flags']['got'] - \
                    service_old['flags']['got']
                team_lost_new_flags = service_new['flags']['lost'] - \
                    service_old['flags']['lost']
                delta_services[name] = {
                    'status': service_new['status'],
                    'title':  service_new['title'],
                    'flags': {
                        'got': team_got_new_flags,
                        'lost': team_lost_new_flags
                    }}

            if team_new['ip'] == self.ip or team_new['name'] == self.teamname:
                # * Уведомление о положении команды в рейтинге
                if team_old['place'] > team_new['place']:
                    telegram_alert(
                        'PLACE', status='up', place_old=team_old['place'], place_new=team_new['place'])
                elif team_old['place'] < team_new['place']:
                    telegram_alert(
                        'PLACE', status='down', place_old=team_old['place'], place_new=team_new['place'])

                # * Уведомление о статусе сервисов
                for service_new, service_old in zip(team_new['services'], team_old['services']):
                    name = service_new['name']
                    title = service_new['title']

                    new_status = service_new['status']
                    old_status = service_old['status']

                    if soup:
                        new_status = board_parser.return_status(new_status)
                        old_status = board_parser.return_status(old_status)

                    # * Если сервис не взлетел или не изменил своего состояния
                    if new_status == old_status and new_status != 'UP':
                        telegram_alert(
                            'STATUS',
                            status='not change',
                            now=new_status,
                            service=name,
                            title=title
                        )

                    # * Если сервис взлетел или изменил состояние на UP
                    if old_status != 'UP' and new_status == 'UP':
                        telegram_alert(
                            'STATUS',
                            status='up',
                            now=new_status,
                            service=name
                        )

                    # * Если сервис не взлетел или изменил состояние не на UP
                    if old_status != new_status and new_status != 'UP':
                        telegram_alert(
                            'STATUS',
                            status='down',
                            now=new_status,
                            service=name,
                            title=title
                        )

                    # * Уведомление о первой крови
                    if int(delta_services[name]['flags']['lost']) != 0 and self.patch[name] == True:
                        self.patch[name] = False
                        telegram_alert('FB', service=name)

                    # * Уведомление о прекращении потери флагов
                    elif int(delta_services[name]['flags']['lost']) == 0 and self.patch[name] == False and new_status == 'UP':
                        self.patch[name] = True
                        telegram_alert('PATCH', service=name)

            delta.append({
                'round': self.round,
                'name': team_new['name'],
                'ip': team_new['ip'],
                'place': team_new['place'],
                'score': round(team_new['score'] - team_old['score'], 2),
                'services': delta_services
            })


def telegram_alert(alert_type, **args):
    if alert_type == 'PLACE':
        requests.post(URL, json={
            "message": "{} с <b>{}</b> на <b>{}</b> место".format('⬇ Наша команда спустилась' if args['status'] == 'down' else '⬆ Наша команда поднялась', args['place_old'], args['place_new']),
            "access_token": TOKEN
        })
    if alert_type == 'STATUS':
        if args['now'] == 'UP':
            simb = '<b>🟢 {} 🟢</b>\n'
        elif args['now'] == 'DOWN':
            simb = '<b>🔴 {} 🔴</b>\n'
        elif args['now'] == 'CORRUPT':
            simb = '<b>🔵 {} 🔵</b>\n'
        elif args['now'] == 'MUMBLE':
            simb = '<b>🟠 {} 🟠</b>\n'
        elif args['now'] == 'CHECK FAILED':
            simb = '<b>🟡 {} 🟡</b>\n'

        if args['status'] == 'down':
            otvet = "Сервису поплохело"
            if args['title']:
                otvet += "\n{}".format(args['title'])
        elif args['status'] == 'up':
            otvet = "Сервис снова жив"
        elif args['status'] == 'not change':
            otvet = "Сервису ВСЁ ЕЩЁ плохо"
            if args['title']:
                otvet += "\n </b>Check Error:</b> {}".format(args['title'])

        requests.post(URL, json={
            "message": "{} {}".format(simb.format(args['service']), otvet),
            "access_token": TOKEN
        })
    if alert_type == 'FB':
        requests.post(URL, json={
            "message": "🩸 Мы теряем флаги на сервисе <b>{}</b>".format(args['service']),
            "access_token": TOKEN
        })
    if alert_type == 'PATCH':
        requests.post(URL, json={
            "message": "💎 Мы запатчили сервис <b>{}</b>".format(args['service']),
            "access_token": TOKEN
        })
