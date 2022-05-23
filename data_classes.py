import json

from config import POST_PATH
from post_classes import Post


class DataPost:
    """ Класс обработки постов"""

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

    def write_to_json(self, picture, contents):
        """ Добавляет/записывает пост в файл JSON"""
        with open(self.POST_PATH, "r", encoding="utf-8") as posts:
            all_posts = json.load(posts)
        with open(self.POST_PATH, 'w+', encoding="utf-8") as post:
            add_post = all_posts[0]
            new_post = {"pic": picture,
                        "content": contents
                        }
            add_post.update(new_post)
            json.dump(all_posts, post, ensure_ascii=False, indent=2)
            return new_post

# dp= DataPost(POST_PATH)
# print(dp.write_to_json('1', '2'))
