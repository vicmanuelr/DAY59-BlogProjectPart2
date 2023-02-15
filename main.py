from flask import Flask, render_template, url_for, request
from datetime import datetime
import smtplib
import requests
import os

app = Flask(__name__)
year = datetime.now().year


def call_posts_api():
    blog_url = "https://api.npoint.io/8cb7d88de0d7d2c9ca8f"
    response = requests.get(url=blog_url)
    all_posts = response.json()
    return all_posts


def send_email(message, phone_number, name):
    MY_EMAIL = os.environ.get("EMAIL")
    MY_PASSWORD = os.environ.get("PASSWORD")
    with smtplib.SMTP("smtp.gmail.com", port=587) as msg:
        msg.starttls()
        msg.login(user=MY_EMAIL, password=MY_PASSWORD)
        msg.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=f"Subject:From blog!\n\n{message}\n",
        )


@app.route('/')
def home():
    all_posts = call_posts_api()
    return render_template("index.html", year=year, posts=all_posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(message=data["message"], name=data["name"], phone_number=data["phone"])
        return render_template("contact.html", data_entered=True)
    return render_template("contact.html", data_entered=False)


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
