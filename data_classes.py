import json

from pprint import pprint as pp
from post_classes import Post


class DataPost:

    def __int__(self, POST_PATH):
        self.POST_PATH = POST_PATH

    def load_post(self):
        '''возвращает список всех кандидатов'''
        with open(self.POST_PATH, "r", encoding="utf-8") as file:
            file = json.load(file)
            list_post = []
            for post in file:
                pic = post[pic]
                content = post[content]
                posts = Post(pic, content)
                list_post.append(posts)
            return file


data = DataPost()
pp(data.load_post())
