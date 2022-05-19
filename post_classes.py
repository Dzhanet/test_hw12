class Post:

    def __int__(self, pic, content):
        self.pic = pic
        self.content = content

    def __repr__(self):
        return f"{self.pic}, {self.content}"
