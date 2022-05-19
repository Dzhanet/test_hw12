from flask import Flask, request, render_template, send_from_directory
from config import POST_PATH
from data_classes import DataPost

UPLOAD_FOLDER = "uploads/images"

data_post = DataPost(POST_PATH)

app = Flask(__name__)


@app.route("/")
def page_index():
    return render_template("index.html")


@app.route("/list/")
@app.route("/list/<word>")
def page_tag(s=None):
    if s is None:
        s = request.args.get('s')
    posts = data_post.get_by_word(s)
    return render_template("post_list.html", posts=posts, s=s)


@app.route("/post", methods=["GET", "POST"])
def page_post_form():
    return render_template("post_form.html")


@app.route("/post", methods=["POST"])
def page_post_upload():
    pass


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


if __name__ == "__main__":
    app.run(debug=True)
