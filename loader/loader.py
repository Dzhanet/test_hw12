from flask import Blueprint, render_template


loader = Blueprint('loader', __name__, template_folder="templates")


@loader.route("/", methods=["GET", "POST"])
def page_post_form():
    """Возвращает форму добавления поста"""
    return render_template("/loader/post_form.html")
