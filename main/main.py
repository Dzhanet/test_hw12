from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder="templates")


@main.route("/")
def page_index():
    """возвращает форму поиска по постам"""

    print('Hello')
    return render_template("/main/index.html")
