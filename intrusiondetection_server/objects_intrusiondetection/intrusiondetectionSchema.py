from objects_common.jsonObject import JsonObject
from room import Room
from objects_common.enumType import EnumType

class IntrusiondetectionSchema(JsonObject):

    def __init__(self, json_struct=None):
        self.systemLocation=""
        self.sensors=Room() #import
        self.systemID=""
        self.systemStatus=Systemstatus(4)
        super(IntrusiondetectionSchema, self).__init__(json_struct)

class Systemstatus(EnumType):
    possible_values = ['up', 'down', 'armed', 'disarmed']
    range_end = 4

    def __init__(self, initial_value):
        super(Systemstatus, self).__init__(initial_value)
