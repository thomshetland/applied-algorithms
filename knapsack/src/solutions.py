class Solution:
    def __init__(self, objects, object_list):
        self.objects = objects # hold dict of all objects with their weight
        self.object_list = object_list # list of objects, sorted by weight or value
        self.total_value = 0
        self.total_weight = 0

    def update_value(self, new_total_value):
        self.total_value = new_total_value
        return self.total_value
    
    def update_weight(self, new_total_weight):
        self.total_weight = new_total_weight
        return self.total_weight
    
    def sort_weight(self):
        sorted_objects = []
        for i in range(len(object)):
            max_key = max(self.objects, key=lambda k: self.objects[k][0])
            print(f"MAXKEY: {max_key}")
            sorted_objects.append(max_key)
            object.pop(max_key)
        return sorted_objects
    
    def sort_value(self):
        sorted_objects = []
        for i in range(len(object)):
            max_key = max(self.objects, key=lambda k: self.objects[k][1])
            sorted_objects.append(max_key)
            object.pop(max_key)
        return sorted_objects