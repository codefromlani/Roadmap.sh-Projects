from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from datetime import datetime, timezone
import secrets
from functools import wraps


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

ARTICLES_DIR = "articles"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password"

if not os.path.exists(ARTICLES_DIR):
    os.makedirs(ARTICLES_DIR)

def get_articles():
    articles = []
    if os.path.exists(ARTICLES_DIR):
        for filename in os.listdir(ARTICLES_DIR):
            if filename.endswith(".json"):
                with open(os.path.join(ARTICLES_DIR, filename), "r") as f:
                    article = json.load(f)
                    article["id"] = filename[:-5] # Remove .json extension
                    articles.append(article)

    return sorted(articles, key=lambda x: x["date"], reverse=True)

def get_article(article_id):
    filepath = os.path.join(ARTICLES_DIR, f"{article_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            article = json.load(f)
            article["id"] = article_id
            return article
    return None

def save_article(article):
    if "id" not in article or not article["id"]:
        article["id"] = secrets.token_hex(8)

    filepath = os.path.join(ARTICLES_DIR, f"{article['id']}.json")
    save_data = {k: v for k, v in article.items() if k != "id"}

    with open(filepath, "w") as f:
        json.dump(save_data, f)

    return article["id"]

def delete_article(article_id):
    filepath = os.path.join(ARTICLES_DIR, f"{article_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def home():
    articles = get_articles()
    return render_template("guest/home.html", articles=articles)

@app.route("/article/<article_id>")
def view_article(article_id):
    article = get_article(article_id)
    if article:
        return render_template("guest/article.html", article=article)
    return "Article not found", 404

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Please try again.")

    return render_template("admin/login.html")

@app.route("/admin/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("home"))

@app.route("/admin/dashboard")
@login_required
def dashboard():
    articles = get_articles()
    return render_template("admin/dashboard.html", articles=articles)

@app.route("/admin/add", methods=["GET", "POST"])
@login_required
def add_article():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        article = {
            "title": title,
            "content": content,
            "date": date
        }

        article_id = save_article(article)
        flash("Article added successfully!")
        return redirect(url_for("dashboard"))
    
    return render_template("admin/add_article.html")

@app.route("/admin/edit/<article_id>", methods=["GET", "POST"])
@login_required
def edit_article(article_id):
    article = get_article(article_id)

    if not article:
        flash("Article not found!")
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        article["title"] = request.form.get("title")
        article["content"] = request.form.get("content")

        save_article(article)
        flash("Article updated successfully!")
        return redirect(url_for("dashboard"))
    
    return render_template("admin/edit_article.html", article=article)

@app.route("/admin/delete/<article_id>")
@login_required
def delete_article(article_id):
    if delete_article(article_id):
        flash("Article deleted successfully!")

    else:
        flash("Failed to delete article!")

    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)