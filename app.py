from json import JSONDecodeError

from flask import Flask, request, render_template, send_from_directory
from config import POST_PATH
from data_classes import DataPost
from main.main import main

from loader.loader import loader

# Конфигурация
UPLOAD_FOLDER = "./uploads/images/"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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
        return "Строка поиска пустая"
    elif data_post.loading_error_json(POST_PATH):
        return JSONDecodeError, 500
    elif not posts:
        return "Нет таких постов"
    return render_template("post_list.html", posts=posts, word=word)


@app.route("/post/new", methods=["GET", "POST"])
def page_post_upload():
    picture_file = request.files.get("picture")
    if data_post.loading_error_pic(picture_file):
        return "Ошибка загрузки из-за отсутствия ФАЙЛА ", 501
    elif data_post.invalid_file_type(picture_file, ALLOWED_EXTENSIONS):
        return "Загруженный файл - не картинка (расширение не jpeg и не png)"
    filename = picture_file.filename
    picture_file.save(f"{UPLOAD_FOLDER}/{filename}")
    contents = request.values.get('content')
    if data_post.loading_error_content(contents):
        return "Ошибка загрузки из-за отсутствия ТЕКСТА ", 502
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
