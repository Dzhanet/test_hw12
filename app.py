from flask import Flask, request, render_template, send_from_directory
from config import POST_PATH
from data_classes import DataPost
from main.main import main
from loader.loader import loader

# Конфигурация
UPLOAD_FOLDER = "uploads/images"
data_post = DataPost(POST_PATH)

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(loader)


@app.route("/list/")
@app.route("/list/<word>")
def page_tag(s=None):
    """Осуществляет поиск по тексту"""
    if s is None:
        s = request.args.get('s')
    posts = data_post.get_by_word(s)
    return render_template("post_list.html", posts=posts, s=s)


@app.route("/post/new/", methods=["POST"])
def page_post_upload():
    return render_template("post_uploaded.html")


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


if __name__ == "__main__":
    app.run(debug=True)
