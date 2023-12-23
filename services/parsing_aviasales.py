from datetime import datetime

import requests

from config_data.config import AVIASALES_TOKEN


class Parser:
    def __init__(self):
        self.token = AVIASALES_TOKEN
        self.url = 'https://api.travelpayouts.com/aviasales/v3/prices_for_dates'

    def get_tickets(self, departure, destination, date):
        resp = requests.get(
            self.url, params={
                'currency': 'rub',
                'origin': departure,
                'destination': destination,
                'departure_at': date,
                'token': self.token
            }
        )
        if resp.status_code == 200:
            return resp.json()
        return None

    def display_tickets_info(self, departure, destination, date):
        tickets_data = self.get_tickets(departure, destination, date)
        if tickets_data and tickets_data["success"]:
            currency = tickets_data["currency"]
            for ticket in tickets_data["data"]:
                departure_datetime = datetime.fromisoformat(ticket['departure_at'])
                departure_date = departure_datetime.strftime('%Y-%m-%d')
                departure_time = departure_datetime.strftime('%H:%M:%S')

                ticket_info = [
                    f"Номер рейса: {ticket['flight_number']}",
                    f"Авиакомпания: {ticket['airline']}",
                    f"Аэропорт отправления: {ticket['origin_airport']}",
                    f"Аэропорт назначения: {ticket['destination_airport']}",
                    f"Цена билета: {ticket['price']} {currency}",
                    f"Дата отправления: {departure_date}",
                    f"Время отправления: {departure_time}",
                    f"Длительность полёта: {ticket['duration']} мин."
                ]

                return ticket_info
        else:
            return "К сожалению, таких рейсов не существует"


parser = Parser()
