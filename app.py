from flask import Flask, request, render_template, send_from_directory
from config import POST_PATH
from data_classes import DataPost
from main.main import main

from loader.loader import loader

# Конфигурация
UPLOAD_FOLDER = "./uploads/images/"
data_post = DataPost(POST_PATH)

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(loader, url_prefix="/post/")


@app.route("/list/")
def page_tag():
    """ Поиск по совпадениям в словах"""
    word = request.args.get('word')
    posts = data_post.get_by_word(word)
    if word:
        return render_template("post_list.html", posts=posts, word=word)
    return render_template("post_list.html")


@app.route("/post/new", methods=["GET", "POST"])
def page_post_upload():
    picture_file = request.files.get("picture")
    filename = picture_file.filename
    picture_file.save(f"{UPLOAD_FOLDER}/{filename}")
    contents = request.values.get('content')
    content = data_post.write_to_json(UPLOAD_FOLDER + filename, contents)
    return render_template("post_uploaded.html",
                           filename=filename,
                           content=contents)


@app.route("/uploads/<path:path>", methods=["GET", "POST"])
def static_dir(path):
    return send_from_directory(UPLOAD_FOLDER, path)


@app.errorhandler(404)
def pageNotFound(error):
    """ Возвращает обратно если ошибка 404"""
    return render_template('page404.html', title="Страница не найдена", error=error)


if __name__ == "__main__":
    app.run(debug=True)
