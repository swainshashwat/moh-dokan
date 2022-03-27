from flask import render_template, session, request, redirect, url_for

from shop import app, db

@app.route('/')
def home():
    return "HOME"