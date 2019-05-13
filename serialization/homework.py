"""
Для попереднього домашнього завдання.
Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) файлу відповідно

Для класів Колекціонер Машина і Гараж написати методи, які зберігають стан обєкту в файли формату
yaml, json, pickle відповідно.

Для класів Колекціонер Машина і Гараж написати методи, які конвертують обєкт в строку формату
yaml, json, pickle відповідно.

Для класу Колекціонер Машина і Гараж написати методи, які створюють інстанс обєкту
з (yaml, json, pickle) строки відповідно


Advanced
Добавити опрацьовку формату ini

"""
import sys
from typing import List
from objects_and_classes.homework.constants import CARS_TYPES, CARS_PRODUCER, TOWNS
from uuid import uuid4
import json
import pickle
from ruamel.yaml import YAML, yaml_object
from ruamel.yaml.compat import StringIO


class NewYaml(YAML):  # This class would not appear here without Pavlo Zubariev's help !
    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()

yaml = NewYaml()


@yaml_object(yaml)
class Car:

    yaml = NewYaml()

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

    @staticmethod
    def json_default(obj):  # encoder
        data = {"producer": obj.producer,
                "car_type": obj.car_type,
                "price": obj.price,
                "mileage": obj.mileage,
                "number": obj.number,
                "owner": obj.owner}
        return data

    @classmethod
    def json_hook(cls, data):  # decoder
        producer = data['producer']
        car_type = data['car_type']
        price = data['price']
        mileage = data['mileage']
        car = Car(producer=producer,
                  car_type=car_type,
                  price=price,
                  mileage=mileage)
        car.number = data.get('number')
        car.owner = data.get('owner')
        return car

    def json_serialize_to_string(self):
        return json.dumps(self, default=Car.json_default, indent=4)

    def json_serialize_to_file(self, json_file):
        with open(json_file, 'w') as file:
            json.dump(self, file, default=Car.json_default, indent=4)

    @staticmethod
    def json_deserialize_from_string(obj):
        return json.loads(obj, object_hook=Car.json_hook)

    @staticmethod
    def json_deserialize_from_file(json_file):
        with open(json_file, 'r') as file:
            return json.load(file, object_hook=Car.json_hook)

    def pickle_serialize_to_string(self):
        return pickle.dumps(self)

    def pickle_serialize_to_file(self, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def pickle_deserialize_from_string(obj):
        return pickle.loads(obj)

    @staticmethod
    def pickle_deserialize_from_file(pickle_file):
        with open(pickle_file, 'rb') as file:
            return pickle.load(file)

    def yaml_serialise_to_string(self):
        return yaml.dump(self)

    def yaml_serialize_to_file(self, file_name):
        with open(file_name, 'w') as file:
            yaml.dump(self, file)

    @staticmethod
    def yaml_deserialize_from_string(obj):
        return yaml.load(obj)

    @staticmethod
    def yaml_deserialize_from_file(yaml_file):
        with open(yaml_file, 'r') as file:
            return yaml.load(file)


@yaml_object(yaml)
class Garage:
    yaml = NewYaml()
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

    @staticmethod
    def json_default(obj):  # encoder
        cars = json.dumps(obj.cars, default=Car.json_default)
        data = {'town': obj.town,
                'places': obj.places,
                'cars': cars,
                'owner': obj.owner,
                'free_places': obj.free_places}
        return data

    @classmethod
    def json_hook(cls, data):  # decoder
        town = data['town']
        places = data['places']
        cars = json.loads(data['cars'], object_hook=Car.json_hook)
        garage = Garage(town=town,
                        places=places,
                        cars=cars)
        garage.free_places = data.get('free_places')
        garage.owner = data.get('owner')
        return garage

    def json_serialize_to_string(self):
        return json.dumps(self, default=Garage.json_default, indent=4)

    def json_serialize_to_file(self, json_file):
        with open(json_file, 'w') as file:
            json.dump(self, file, default=Garage.json_default, indent=4)

    @staticmethod
    def json_deserialize_from_string(obj):
        return json.loads(obj, object_hook=Garage.json_hook)

    @staticmethod
    def json_deserialize_from_file(json_file):
        with open(json_file, 'r') as file:
            return json.load(file, object_hook=Garage.json_hook)

    def pickle_serialize_to_string(self):
        return pickle.dumps(self)

    def pickle_serialize_to_file(self, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def pickle_deserialize_from_string(obj):
        return pickle.loads(obj)

    @staticmethod
    def pickle_deserialize_from_file(pickle_file):
        with open(pickle_file, 'rb') as file:
            return pickle.load(file)

    def yaml_serialise_to_string(self):
        return yaml.dump(self)

    def yaml_serialize_to_file(self, file_name):
        with open(file_name, 'w') as file:
            yaml.dump(self, file)

    @staticmethod
    def yaml_deserialize_from_string(obj):
        return yaml.load(obj)

    @staticmethod
    def yaml_deserialize_from_file(yaml_file):
        with open(yaml_file, 'r') as file:
            return yaml.load(file)


@yaml_object(yaml)
class Cesar:
    yaml = NewYaml()
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

    @staticmethod
    def json_default(obj):  # encoder
        garages = json.dumps(obj.garages, default=Garage.json_default)
        data = {'name': obj.name,
                'garages': garages,
                'register_id': obj.register_id}
        return data

    @classmethod
    def json_hook(cls, data):  # decoder
        name = data['name']
        garages = json.loads(data['garages'], object_hook=Garage.json_hook)
        cesar = Cesar(name=name,
                      garages=garages)
        cesar.register_id = data.get('register_id')
        return cesar

    def json_serialize_to_string(self):
        return json.dumps(self, default=Cesar.json_default, indent=4)

    def json_serialize_to_file(self, json_file):
        with open(json_file, 'w') as file:
            json.dump(self, file, default=Cesar.json_default, indent=4)

    @staticmethod
    def json_deserialize_from_string(obj):
        return json.loads(obj, object_hook=Cesar.json_hook)

    @staticmethod
    def json_deserialize_from_file(json_file):
        with open(json_file, 'r') as file:
            return json.load(file, object_hook=Cesar.json_hook)

    def pickle_serialize_to_string(self):
        return pickle.dumps(self)

    def pickle_serialize_to_file(self, file_name):
        with open(file_name, "wb") as file:
            pickle.dump(self, file)

    @staticmethod
    def pickle_deserialize_from_string(obj):
        return pickle.loads(obj)

    @staticmethod
    def pickle_deserialize_from_file(pickle_file):
        with open(pickle_file, 'rb') as file:
            return pickle.load(file)

    def yaml_serialise_to_string(self):
        return yaml.dump(self)

    def yaml_serialize_to_file(self, file_name):
        with open(file_name, 'w') as file:
            yaml.dump(self, file)

    @staticmethod
    def yaml_deserialize_from_string(obj):
        return yaml.load(obj)

    @staticmethod
    def yaml_deserialize_from_file(yaml_file):
        with open(yaml_file, 'r') as file:
            return yaml.load(file)