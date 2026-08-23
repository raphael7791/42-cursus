from enum import Enum

class CityType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    VIP = "vip"

class City:
    def __init__(self, name, capacity, city_type):
        self.name = name
        self.capacity = capacity
        self.city_type = city_type


if __name__ == "__main__":

    tokyo = City("Tokyo", 3, CityType.NORMAL)

    print(isinstance(tokyo, City))                    # True
    print(isinstance("Tokyo", City))                  # False
    print(isinstance(tokyo.name, str))                # True
    print(isinstance(tokyo.capacity, int))            # True
    print(isinstance(tokyo.city_type, CityType))      # True
    print(isinstance(tokyo.city_type, str))           # False
    print(isinstance(tokyo.city_type.value, str))     # True
    print(isinstance(CityType.VIP, CityType))         # Je ne sais pas