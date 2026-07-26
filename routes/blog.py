from flask import Blueprint, render_template

blog = Blueprint("blog", __name__)


@blog.route("/career-hub")
def career_hub():

    return render_template("coming_soon.html")