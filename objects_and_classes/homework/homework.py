"""
Вам небхідно написати 3 класи. Колекціонери Гаражі та Автомобілі.
Звязкок наступний один колекціонер може мати багато гаражів.
В одному гаражі може знаходитися багато автомобілів.

Автомобіль має наступні характеристики:
    price - значення типу float. Всі ціни за дефолтом в одній валюті.
    type - одне з перечисленних значеннь з CARS_TYPES в docs.
    producer - одне з перечисленних значеннь в CARS_PRODUCER.
    number - значення типу UUID. Присвоюється автоматично при створенні автомобілю.
    mileage - значення типу float. Пробіг автомобіля в кілометрах.


    Автомобілі можна перівнювати між собою за ціною.
    При виводі(logs, print) автомобілю повинні зазначатися всі його атрибути.

    Автомобіль має метод заміни номеру.
    номер повинен відповідати UUID

Гараж має наступні характеристики:

    town - одне з перечислениз значеннь в TOWNS
    cars - список з усіх автомобілів які знаходяться в гаражі
    places - значення типу int. Максимально допустима кількість автомобілів в гаражі
    owner - значення типу UUID. За дефолтом None.


    Повинен мати реалізованими наступні методи

    add(car) -> Добавляє машину в гараж, якщо є вільні місця
    remove(cat) -> Забирає машину з гаражу.
    hit_hat() -> Вертає сумарну вартість всіх машин в гаражі


Колекціонер має наступні характеристики
    name - значення типу str. Його ім'я
    garages - список з усіх гаражів які належать цьому Колекціонеру. Кількість гаражів за замовчуванням - 0
    register_id - UUID; Унікальна айдішка Колекціонера.

    Повинні бути реалізовані наступні методи:
    hit_hat() - повертає ціну всіх його автомобілів.
    garages_count() - вертає кількість гаріжів.
    сars_count() - вертає кількість машиню
    add_car() - додає машину у вибраний гараж. Якщо гараж не вказаний, то додає в гараж, де найбільше вільних місць.
    Якщо вільних місць немає повинне вивести повідомлення про це.

    Колекціонерів можна порівнювати за ціною всіх їх автомобілів.
"""

import uuid
from typing import List
from constants import CARS_TYPES, CARS_PRODUCER, TOWNS




class Car:
    def __init__(self, car_type, producer, price: float, mileage: float):
        self.price = price
        self.number = uuid.uuid4()
        self.mileage = mileage
        self.owner = None
        if car_type in CARS_TYPES:
            self.car_type = car_type
        else:
            raise ValueError('Received unexpected data "{}"'.format(car_type))
        if producer in CARS_PRODUCER:
            self.producer = producer
        else:
            raise ValueError('Received unexpected data "{}"'.format(producer))

    def __eq__(self, other):
        return self.price == other.price

    def __ne__(self, other):
        return self.price != other.price

    def __lt__(self, other):
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price

    def __str__(self):
        return f"{self.producer} - {self.type}, Price:{self.price}, Mileage:{self.mileage}, Number:{self.number}"

    def changing_number(self):
        self.number = uuid.uuid4()


class Garage:

    cars = List[Car]

    def __init__(self, town, places: int, cars=None, owner=None):
        self.cars = cars if cars is not None else []
        self.places = places
        self.available_places = self.places - len(self.cars)
        self.owner = owner
        if town in TOWNS:
            self.town = town
        else:
            print("Did you get lost? Only town from TOWNS is allowed!")

    def __str__(self):
        return f"This garage is located in {self.town}. It has {self.places} places. " \
            f"There is(are) {len(self.cars)} car(s). Owner name is {self.owner}."

    def add_car(self, car: Car):
        if car in self.cars:
            print('This car is already here')
        elif car.owner:
            print('This car is already in another garage')
        elif self.available_places > 0:
            self.cars.append(car)
            car.owner = self.owner
        else:
            print("The garage is full!")
        self.available_places -= 1

    def remove(self, car: Car):
        self.cars.remove(car)
        car.owner = None
        self.available_places += 1

    def hit_hat(self):
        return sum(car.price for car in self.cars)



class Cesar:

    garages = List[Garage]
    garage: Garage

    def __init__(self, name: str, garages=None):
        self.name = name
        self.register_id = uuid.uuid4()
        self.garages = garages if garages is not None else []
        if garages:
            for garage in garages:
                garage.owner = self.register_id

    def __str__(self):
        return f'Cesar name is {self.name}. He has {self.garages}. His id is {self.register_id}.'

    def __eq__(self, other):
        return self.hit_hat() == other.hit_hat()

    def __ne__(self, other):
        return self.hit_hat() != other.hit_hat()

    def __gt__(self, other):
        return self.hit_hat() > other.hit_hat()

    def __lt__(self, other):
        return self.hit_hat() < other.hit_hat()

    def add_garage(self, garage: Garage):
        if garage.owner:
            print(f'The {self.name} has bought this garage already.')
        else:
            garage.owner = self.register_id
            self.garages.append(garage)
            for car in garage.cars:
                car.owner = self.register_id

    def hit_hat(self):
        return sum(garage.hit_hat() for garage in self.garages)

    def garages_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum([len(garage.cars) for garage in self.garages])

    def most_empty_garage(self):
        return max(self.garages, key=lambda garage: garage.available_places, default = None)

    def add_car(self, car: Car, garage=None):
        if garage is None:
            self.most_empty_garage().add_car(car)
        elif garage not in self.garages:
            print('This is not your garage!')
        elif car in garage.cars:
            print('This car is already yours!')
        elif garage.available_places == 0:
            print('The garage is full! Choose another one.')
        else:
            garage.add_car(car)
            car.owner = self.register_id

