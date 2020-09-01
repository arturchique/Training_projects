import os
import tempfile
import uuid


class File:
    def __init__(self, path):
        if os.path.exists(path):
            self.path = path
        else:
            f = open(path, "tw")
            f.close()
            self.path = path
        self.current_pos = 0

    def __str__(self):
        return self.path

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.path, "r") as f:
            f.seek(self.current_pos)
            result = f.readline()
            self.current_pos = f.tell()
            if result == "":
                self.current_pos = 0
                raise StopIteration
            return result

    def __add__(self, obj):
        new_path = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))
        with open(new_path, 'w') as new_file:
            new_file.write(f"{self.read()}{obj.read()}")
        return File(new_path)

    def read(self):
        with open(self.path, "r") as file:
            return file.read()

    def write(self, value):
        with open(self.path, "w") as file:
            file.write(value)


