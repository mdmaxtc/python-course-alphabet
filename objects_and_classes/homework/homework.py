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
from typing import List
from constants import CARS_TYPES, CARS_PRODUCER, TOWNS
from uuid import uuid4
import random


class Car:

    def __init__(self, producer, type, price, mileage):
        self.price = float(price)
        self.mileage = float(mileage)
        self.number = uuid4().hex
        if type in CARS_TYPES and producer in CARS_PRODUCER:
            self.type = type
            self.producer = producer
        else:
            print("Only position from CARS_TYPES and CARS_PRODUCER is allowed!")
            raise ValueError

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
    cars: List[Car]

    def __init__(self, town, places: int, cars=None, owner=None):
        self.cars = cars
        self.parking_places = parking_places
        self.owner = owner
        self.free_places = self.places - len(self.cars)
        if town in TOWNS:
            self.town = town
        else:
            print("Did you get lost? Only town from TOWNS is allowed!")

    def __str__(self):
        return f"{self.town}, {self.parking_places}, {self.cars}, {self.owner}"

    def add_car_to_garage(self, car: Car):
        if self.parking_places <= len(self.cars):
            print("The garage is full!")
        else:
            self.cars.append(car)

    def remove_car(self, car: Car):
        self.cars.remove(car)

    def hit_hat(self):
        return sum([car.price for car in self.cars])


class Cesar:
    garages = List[Garage]

    def __init__(self, name: str, garages=None):
        self.name = name
        self.garages = garages
        self.register_id = uuid4().hex

    def __str__(self):
        return f'{self.name}: {self.garages}'

    def __eq__(self, other):
        return self.hit_hat() == other.hit_hat()

    def __ne__(self, other):
        return self.hit_hat() != other.hit_hat()

    def __lt__(self, other):
        return self.hit_hat() < other.hit_hat()

    def __gt__(self, other):
        return self.hit_hat() > other.hit_hat()

    def add_garage(self, garage: Garage):
        if garage.owner == None:
            self.garages.append(garage)
            garage.owner = self.register_id
        else:
            print(f'The {self.name} has bought this garage already.')

    def most_empty(self):
        most_empty = self.garages[0]
        for i in range(1, len(self.garages)):
            if self.garages[i].free_places > most_empty.free_places:
                most_empty = self.garages[i]
        if most_empty.free_places == 0:
            return None
        return most_empty

    def add_car(self, car, garage):
        if garage in self.garages:
            garage.add(car)
        else:
            print(f'The {self.name} hasn`t bought this garage')

    def garages_count(self):
        return len(self.garages)

    def cars_count(self):
        return sum([len(garage.cars) for garage in self.garages])

    def hit_hat(self):
        return sum([garage.hit_hat() for garage in self.garages])


car1 = Car(random.choice(CARS_PRODUCER), random.choice(CARS_TYPES),
           random.randrange(100, 1000), random.randrange(100, 2000), )

print(car1)