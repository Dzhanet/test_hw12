import json

from pprint import pprint as pp
from config import POST_PATH
from post_classes import Post


class DataPost:

    def __init__(self, POST_PATH):
        self.POST_PATH = POST_PATH

    def load_post(self):
        '''возвращает список всех постов'''
        with open(self.POST_PATH, "r", encoding="utf-8") as file:
            file = json.load(file)
            list_post = []
            for post in file:
                pic = post["pic"]
                content = post["content"]
                posts = Post(pic, content)
                list_post.append(posts)
            return list_post

    def get_by_word(self, content):
        """ Вовзращает посты по вхождению в строку"""
        get_words = self.load_post()
        search_word = []
        for words in get_words:
            if content.lower() in words.content.lower():
                search_word.append(words)
        return search_word


# data = DataPost(POST_PATH)
# pp(data.get_by_word("#"))
