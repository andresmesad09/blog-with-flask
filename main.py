from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = Flask(__name__)
API_POSTS = "https://api.npoint.io/e70d4a8773af546507e7"
SENDER = os.environ.get("SENDER")
PWD = os.environ.get("PWD")

print(SENDER)
print(PWD)


def send_email(name, email, phone, message):
    print("sending message")
    body = f"""
    Name: {name}
    phone: {phone}
    {message}
    """
    with smtplib.SMTP("smtp.gmail.com") as connection:
        # to encrypt
        connection.starttls()
        connection.login(user=SENDER, password=PWD)
        connection.sendmail(
            from_addr=SENDER,
            to_addrs=SENDER,
            msg=f"Subject:{email}\n\n{body}")
    print("Message was sent")


def get_posts():
    try:
        response = requests.get(API_POSTS)
        response.raise_for_status()
        posts = response.json()
        return posts
    except Exception as e:
        print(e)
        raise e


POSTS = get_posts()


@app.route("/")
def index():
    posts = POSTS
    return render_template("index.html", posts=posts)
    # return render_template("test.html")


@app.route("/form-entry")
def receive_data(message_header):
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    message = request.form.get('message')
    send_email(name, email, phone, message)
    return render_template("contact.html", message_header=message_header)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html", message_header="Contact Me")
    else:
        return receive_data(message_header="Successfully sent message")


@app.route("/posts/<int:post_id>")
def render_post(post_id):
    post = None
    for p in POSTS:
        if p['id'] == post_id:
            post = p
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
