from json import JSONDecodeError
import logging
from flask import Flask, request, render_template, send_from_directory
from config import POST_PATH
from data_classes import DataPost
from main.main import main

from loader.loader import loader

# Конфигурация
UPLOAD_FOLDER = "./uploads/images/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# ЛОГИРОВАНИЕ
new_logger = logging.getLogger()

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("log.txt")

new_logger.addHandler(console_handler)
new_logger.addHandler(file_handler)



data_post = DataPost(POST_PATH)

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(loader, url_prefix="/post/")


@app.route("/list/")
def page_tag():
    """ Поиск по совпадениям в словах"""
    word = request.args.get('word')
    posts = data_post.get_by_word(word)
    if not word:
        return "Строка поиска пустая", 506
    elif data_post.loading_error_json(POST_PATH):
        return JSONDecodeError, 500
    elif not posts:
        return "Нет таких постов", 505
    return render_template("post_list.html", posts=posts, word=word)


@app.route("/post/new", methods=["GET", "POST"])
def page_post_upload():
    picture_file = request.files.get("picture")
    if data_post.loading_error_pic(picture_file):
        return FileNotFoundError, 501
    filename = picture_file.filename
    if data_post.invalid_file_type(filename, ALLOWED_EXTENSIONS):
        return TypeError, 503
    picture_file.save(f"{UPLOAD_FOLDER}/{filename}")
    contents = request.values.get('content')
    if data_post.loading_error_content(contents):
        return ValueError, 502
    content = data_post.write_to_json(f'/uploads/{filename}', contents)
    return render_template("post_uploaded.html",
                           filename=filename,
                           contents=contents)


@app.route("/uploads/<path:path>", methods=["GET", "POST"])
def static_dir(path):
    return send_from_directory(UPLOAD_FOLDER, path)


@app.errorhandler(404)
def pageNotFound(error):
    """ Возвращает обратно если ошибка 404"""
    return render_template('page404.html', title="Страница не найдена", error=error)


if __name__ == "__main__":
    app.run(debug=True)
