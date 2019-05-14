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
from typing import List
from objects_and_classes.homework.constants import CARS_TYPES, CARS_PRODUCER, TOWNS
from uuid import uuid4
import json
import pickle
from ruamel.yaml import YAML, yaml_object
from ruamel.yaml.compat import StringIO


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Car):
            return dict(Car=dict(price=obj.price, car_type=obj.car_type, producer=obj.producer, mileage=obj.mileage,
                                 number=obj.number))
        if isinstance(obj, Garage):
            return dict(Garage=dict(town=obj.town, places=obj.places, owner=obj.owner, cars_in_garage=obj.cars_in_garage,
                                    free_places=obj.free_places))
        if isinstance(obj, Cesar):
            return dict(Cesar=dict(name=obj.name, garages=obj.garages, register_id=obj.register_id))
        return json.JSONEncoder.default(self, obj)


def json_hook(obj):
    if "Car" in obj:
        price = obj["Car"]["price"]
        car_type = obj["Car"]["car_type"]
        producer = obj["Car"]["producer"]
        mileage = obj["Car"]["mileage"]
        new_obj = Car(price=price, car_type=car_type, producer=producer, mileage=mileage)
        new_obj.number = obj["Car"].get("number", uuid4().hex)
        return new_obj

    if "Garage" in obj:
        town = obj["Garage"]["town"]
        places = obj["Garage"]["places"]
        cars_in_garage = obj["Garage"]["cars_in_garage"]
        new_obj = Garage(town=town, places=places, cars=cars_in_garage)
        return new_obj

    if "Cesar" in obj:
        name = obj["Cesar"]["name"]
        garages = obj["Cesar"]["garages"]
        new_obj = Cesar(name=name, garages=garages)
        new_obj.register_id = obj["Cesar"].get("register_id", uuid4().hex)
        return new_obj

    return obj


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

    @staticmethod
    def from_yaml_str(obj):
        yaml = YAML()
        return yaml.load(obj)

    @staticmethod
    def from_yaml_file(yaml_file):
        yaml = YAML()
        with open(yaml_file, 'r') as file:
            return yaml.load(file)

    def to_yaml_str(self):
        yaml = YAML()
        yaml.register_class(Car)
        return yaml.dump(self, stream=StringIO())

    def to_yaml_file(self, file_name):
        yaml = YAML()
        with open(file_name, 'w') as file:
            yaml.dump(self, file)

    @staticmethod
    def from_json_file(json_file):
        with open(json_file, 'r') as f:
            return json.load(f, object_hook=json_hook)

    @staticmethod
    def from_json_str(json_str):
        return json.loads(json_str, object_hook=json_hook)

    def to_json_file(self, json_file):
        with open(json_file, 'w') as f:
            json.dump(self, f, cls=JsonEncoder, indent=4)

    def to_json_str(self):
        return json.dumps(self, cls=JsonEncoder, indent=4)

    @staticmethod
    def from_pickle_str(pickle_str):
        return pickle.loads(pickle_str)

    @staticmethod
    def from_pickle_file(pickle_file):
        with open(pickle_file, 'rb') as file:
            return pickle.load(file)

    def to_pickle_str(self):
        return pickle.dumps(self)

    def to_pickle_file(self, pickle_file):
        with open(pickle_file, 'wb') as file:
            pickle.dump(self, file)


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

    @staticmethod
    def from_yaml_str(obj):
        yaml = YAML()
        return yaml.load(obj)

    @staticmethod
    def from_yaml_file(yaml_file):
        yaml = YAML()
        with open(yaml_file, 'r') as file:
            return yaml.load(file)

    def to_yaml_str(self):
        yaml = YAML()
        yaml.register_class(Car)
        return yaml.dump(self, stream=StringIO())

    def to_yaml_file(self, file_name):
        yaml = YAML()
        with open(file_name, 'w') as file:
            yaml.dump(self, file)

    @staticmethod
    def from_json_file(json_file):
        with open(json_file, 'r') as f:
            return json.load(f, object_hook=json_hook)

    @staticmethod
    def from_json_str(json_str):
        return json.loads(json_str, object_hook=json_hook)

    def to_json_file(self, json_file):
        with open(json_file, 'w') as f:
            json.dump(self, f, cls=JsonEncoder, indent=4)

    def to_json_str(self):
        return json.dumps(self, cls=JsonEncoder, indent=4)

    @staticmethod
    def from_pickle_str(pickle_str):
        return pickle.loads(pickle_str)

    @staticmethod
    def from_pickle_file(pickle_file):
        with open(pickle_file, 'rb') as file:
            return pickle.load(file)

    def to_pickle_str(self):
        return pickle.dumps(self)

    def to_pickle_file(self, pickle_file):
        with open(pickle_file, 'wb') as file:
            pickle.dump(self, file)


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
    def from_yaml_str(obj):
        yaml = YAML()
        return yaml.load(obj)

    @staticmethod
    def from_yaml_file(yaml_file):
        yaml = YAML()
        with open(yaml_file, 'r') as file:
            return yaml.load(file)

    def to_yaml_str(self):
        yaml = YAML()
        yaml.register_class(Car)
        return yaml.dump(self, stream=StringIO())

    def to_yaml_file(self, file_name):
        yaml = YAML()
        with open(file_name, 'w') as file:
            yaml.dump(self, file)

    @staticmethod
    def from_json_file(json_file):
        with open(json_file, 'r') as f:
            return json.load(f, object_hook=json_hook)

    @staticmethod
    def from_json_str(json_str):
        return json.loads(json_str, object_hook=json_hook)

    def to_json_file(self, json_file):
        with open(json_file, 'w') as f:
            json.dump(self, f, cls=JsonEncoder, indent=4)

    def to_json_str(self):
        return json.dumps(self, cls=JsonEncoder, indent=4)

    @staticmethod
    def from_pickle_str(pickle_str):
        return pickle.loads(pickle_str)

    @staticmethod
    def from_pickle_file(pickle_file):
        with open(pickle_file, 'rb') as file:
            return pickle.load(file)

    def to_pickle_str(self):
        return pickle.dumps(self)

    def to_pickle_file(self, pickle_file):
        with open(pickle_file, 'wb') as file:
            pickle.dump(self, file)
