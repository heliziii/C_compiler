class MemoryManager(object):
    def __init__(self, main_memory, temp_memory):
        self.main_memory = main_memory
        self.temp_memory = temp_memory

    def get_variable(self, count):
        address = self.main_memory
        self.main_memory += 4 * count
        return address

    def get_temp(self, count):
        address = self.temp_memory
        self.temp_memory += 4 * count
        return address