import os
import csv


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return str(os.path.splitext(self.photo_file_name)[1])

    def __str__(self):
        return self.brand

    def __repr__(self):
        return self.brand


class Car(CarBase):
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super(Car, self).__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = int(passenger_seats_count)
        self.car_type = 'car'


class Truck(CarBase):
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        self.car_type = 'truck'
        whl = body_whl.split('x')
        try:
            if len(whl) == 3:
                self.body_width = float(whl[1]) or 0.0
                self.body_height = float(whl[2]) or 0.0
                self.body_length = float(whl[0]) or 0.0
            else:
                self.body_width = 0.0
                self.body_height = 0.0
                self.body_length = 0.0

        except:
            self.body_width = 0.0
            self.body_height = 0.0
            self.body_length = 0.0

    def get_body_volume(self):
        return self.body_height * self.body_length * self.body_width


class SpecMachine(CarBase):
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra
        self.car_type = 'spec_machine'


FORMATS_LIST = (".jpeg", ".jpg", ".png", ".gif")


def is_file_valid(file):
    return os.path.splitext(file)[1] in FORMATS_LIST


def get_car_list(file):
    car_list = []
    try:
        with open(file) as csv_fd:
            reader = csv.reader(csv_fd, delimiter=';')
            next(reader)
            for row in reader:
                if len(row) == 0:
                    car = None
                elif row[0] == 'car' and row[1] and row[2] and row[3] and row[5] and is_file_valid(row[3]):
                    car = Car(brand=row[1], passenger_seats_count=row[2], photo_file_name=row[3], carrying=row[5])
                elif row[0] == 'truck' and row[1] and row[3] and row[5] and is_file_valid(row[3]):
                    car = Truck(brand=row[1], photo_file_name=row[3], carrying=row[5], body_whl=row[4])
                elif row[0] == 'spec_machine' and row[1] and row[6] and row[3] and row[5] and is_file_valid(row[3]):
                    car = SpecMachine(brand=row[1], photo_file_name=row[3], carrying=row[5], extra=row[6])
                else:
                    car = None
                if car is not None:
                    car_list.append(car)
    except:
        pass
    return car_list

print(len(get_car_list("cars.csv")))
