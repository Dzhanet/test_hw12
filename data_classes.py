import json

from post_classes import Post


class DataPost:
    """ Класс обработки постов"""

    def __init__(self, POST_PATH):
        self.POST_PATH = POST_PATH

    @classmethod
    def loading_error_json(cls, POST_PATH):
        if not POST_PATH:
            return "Файл .json отсутствует или не хочет превращаться в список"

    def load_post(self):
        '''возвращает список всех постов'''
        with open(self.POST_PATH, encoding="utf-8") as file:
            file = json.load(file)
            list_post = []
            for post in file:
                pic = post["pic"]
                content = post["content"]
                posts = Post(pic, content)
                list_post.append(posts)
            return list_post

    def get_by_word(self, content):
        """ Возвращает посты по вхождению в строку"""
        get_words = self.load_post()
        search_word = []
        for words in get_words:
            if content.lower() in words.content.lower():
                search_word.append(words)
        return search_word

    @classmethod
    def loading_error_pic(cls, pic):
        if not pic:
            raise FileNotFoundError("Ошибка загрузки из-за отсутствия ФАЙЛА ")

    def loading_error_content(cls, content):
        if not content:
            raise TypeError("Ошибка загрузки из-за отсутствия ТЕКСТА ")

    def invalid_file_type(cls, filename, ALLOWED_EXTENSIONS):
        extension = filename.split(".")[-1]
        if extension not in ALLOWED_EXTENSIONS:
            raise TypeError(
                f"Загруженный файл - {extension} (Доступные расширение 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif')")

    def write_to_json(self, picture, contents):
        """ Добавляет/записывает пост в файл JSON"""
        with open(self.POST_PATH, "r", encoding="utf-8") as file:
            all_posts = json.load(file)
        new_post = {"pic": picture,
                    "content": contents
                    }
        all_posts.append(new_post)
        with open(self.POST_PATH, 'w+', encoding="utf-8") as file:
            json.dump(all_posts, file, ensure_ascii=False, indent=2)
        return new_post
