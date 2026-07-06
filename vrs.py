from abc import ABC, abstractmethod


class VehicleNotAvailableError(Exception):
    pass


class NotRentedByCustomerError(Exception):
    pass


class Vehicle(ABC):
    def __init__(self, item_no, no_plate):
        self.item_no = item_no
        self.no_plate = no_plate
        self.__is_borrowed = False

    def available(self):
        return not self.__is_borrowed

    def borrow(self):
        if self.__is_borrowed:
            raise VehicleNotAvailableError(f"Vehicle {self.item_no} is already borrowed.")
        self.__is_borrowed = True
        print(f"Vehicle {self.item_no} has been borrowed successfully.")

    def return_vehicle(self):
        if self.__is_borrowed:
            self.__is_borrowed = False
            print(f"Vehicle {self.item_no} has been returned successfully.")
        else:
            print(f"Vehicle {self.item_no} was not borrowed.")

    @abstractmethod
    def cost(self, days):
        pass

    def __str__(self):
        return f"[{self.item_no}] {self.no_plate}"


class Car(Vehicle):
    def cost(self, days):
        return days * 100


class Bike(Vehicle):
    def cost(self, days):
        return days * 80


class Customer:
    def __init__(self, name, ID):
        self.name = name
        self.ID = ID
        self.rented = []

    def rent(self, vehicle):
        self.rented.append(vehicle)
        print(f"{vehicle.item_no} has been rented by {self.name}.")

    def rented_vehicle(self):
        if not self.rented:
            print(f"{self.name} hasn't rented any vehicle.")
        else:
            for v in self.rented:
                print(v)

    def return_vehicle(self, vehicle):
        if vehicle in self.rented:
            self.rented.remove(vehicle)
            print("The vehicle has been returned.")
        else:
            raise NotRentedByCustomerError(f"{self.name} hasn't rented vehicle {vehicle.item_no}.")


class RentalSystem:
    def __init__(self):
        self.vehicles = []

    def add(self, v):
        self.vehicles.append(v)

    def show(self):
        for v in self.vehicles:
            print(v)

    def rent_vehicle(self, customer, vehicle, days):
        try:
            if not vehicle.available():
                raise VehicleNotAvailableError(f"Vehicle {vehicle.item_no} is currently unavailable.")
            vehicle.borrow()
            customer.rent(vehicle)
            cost = vehicle.cost(days)
            print(f"The cost is {cost}")
        except VehicleNotAvailableError as e:
            print(f"Rental failed: {e}")

    def return_vehicle(self, customer, vehicle):
        try:
            customer.return_vehicle(vehicle)
            vehicle.return_vehicle()
        except NotRentedByCustomerError as e:
            print(f"Return failed: {e}")


system = RentalSystem()
cust1 = Customer("Ram", "1")
c1 = Car(101, "BA-1-PA-1234")
b1 = Bike(102, "BA-2-CHA-5678")

system.add(c1)
system.add(b1)
system.show()

system.rent_vehicle(cust1, c1, 3)
cust1.rented_vehicle()

system.rent_vehicle(cust1, c1, 3)
system.return_vehicle(cust1, c1)
cust1.rented_vehicle()