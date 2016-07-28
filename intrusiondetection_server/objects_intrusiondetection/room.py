from objects_common.jsonObject import JsonObject
from objects_common.enumType import EnumType

class Room(JsonObject):

    def __init__(self, json_struct=None):
        self.status=Status(2)
        self.doorsensorID=""
        self.motionsensorID=""
        super(Room, self).__init__(json_struct)

class Status(EnumType):
    possible_values = ['occupied', 'unoccupied']
    range_end = 2

    def __init__(self, initial_value):
        super(Status, self).__init__(initial_value)
