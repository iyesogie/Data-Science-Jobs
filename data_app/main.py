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
    return render_template('home.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/company')
def company():
    ds_list = list(Datascientist.query.all())
    ds = [{
        "rating" : row.rating,
        "salary_estimate" : row.salary_estimate,
        "companyid" : row.companyid,
        "industryid": row.industryid
    } for row in ds_list]

    print(ds)
    comps_list = list(Company.query.all())
    comps = [{
        "id" : row.id,
        "name" : row.name
    } for row in comps_list]
    
    data = {
        'datascientists' : ds,
        'companies' : comps
    }
    return render_template('company.html', data=data)

