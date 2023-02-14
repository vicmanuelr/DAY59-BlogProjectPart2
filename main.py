from flask import Flask, render_template, url_for, request
from datetime import datetime
import requests

app = Flask(__name__)
year = datetime.now().year


def call_posts_api():
    blog_url = "https://api.npoint.io/8cb7d88de0d7d2c9ca8f"
    response = requests.get(url=blog_url)
    all_posts = response.json()
    return all_posts


@app.route('/')
def home():
    all_posts = call_posts_api()
    return render_template("index.html", year=year, posts=all_posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")
    elif request.method == "POST":
        data = request.form
        print(data["name"], data["email"], data["phone"])
        return "<h1>Successfully sent your request</h1>"


@app.route("/blog/<num>")
def get_blog(num):
    all_posts = call_posts_api()
    post_selected = {}
    for post in all_posts:
        if int(post["id"]) == int(num):
            post_selected = post
    return render_template("post.html", year=year, post=post_selected)


if __name__ == "__main__":
    app.run(debug=True)
