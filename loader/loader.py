from flask import Blueprint, render_template

loader = Blueprint('loader', __name__)


@loader.route("/post/", methods=["GET", "POST"])
def page_post_form():
    return render_template("post_form.html")

