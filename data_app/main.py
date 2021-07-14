## THIS FILE CONTAINS ALL THE MAIN ROUTES
#  We can change the routes and the functionality here

from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import *

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    locs = Location.query.order_by(Location.name).all()
    for location in locs:
        print(location.name)
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')