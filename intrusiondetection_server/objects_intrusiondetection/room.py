from objects_common.jsonObject import JsonObject

class Room(JsonObject):

    def __init__(self, json_struct=None):
        self.doorsensorID=""
        self.motionsensorID=""
        super(Room, self).__init__(json_struct)

