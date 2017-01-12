class UserModel:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    def getUser(self):
        return self.id, self.name, self.image
