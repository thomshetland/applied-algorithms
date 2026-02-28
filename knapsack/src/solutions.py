class Solution:
    def __init__(self, objects, object_list):
        self.objects = objects
        self.object_list = object_list
        self.value = 0
        self.weight = 0

    def update_value(self, new_value):
        self.value = new_value
        return self.value
    
    def update_weight(self, new_weight):
        self.weight = new_weight
        return self.weight