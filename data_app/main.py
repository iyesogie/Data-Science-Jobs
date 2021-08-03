# THIS FILE CONTAINS ALL THE MAIN ROUTES
#  We can change the routes and the functionality here

from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import *
import json
import os

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('main.home'))

@main.route('/home')
def home():
    data = dict()
    data["page_name"] = "Home"
    return render_template('home.html', data=data)

@main.route('/company')
def company():
    data = dict()
    data["page_name"] = "Job seach"
    ds_list = list(Datascientist_df.query.all())
    ds = [{
        "rating": str(row.Rating),
        "salary_estimate" : row.salary_estimate,
        "company": row.Company,
        "industry": row.Industry,
        'location':row.Location,
        'position':row.Position
    } for row in ds_list]
    comps_list = list(Company.query.all())
    comps = [{"id": row.id,
              "name": row.name
              } for row in comps_list]
    data['datascientists'] = ds
    data['companies'] = comps
    return render_template('company.html', data=data)


@main.route('/map')
def map():
    data=dict()
    data["page_name"] = "Salary And Rating"
    ds_list = list(Datascientist_df.query.all())
    locations = [{
        "company" : row.Company,
        "rating" : row.Rating,
        "location" : row.Location,
        "position" : row.Position,
        "salary":row.salary_estimate,
    } for row in ds_list]
    data["locations"] = locations
    file=os.path.join("data_app","static","data","cities.json",)
    with open(file) as file:
        codata=json.load(file)
    data["codata"] = codata
    return render_template('map.html',data=data)

@main.route('/position')
def position():
    data=dict()
    data["page_name"] = "Available Positions"
    ds_list = list(Datascientist_df.query.all())
    locations = [{
        "company" : row.Company,
        "rating" : row.Rating,
        "location" : row.Location,
        "position" : row.Position,
        "salary":row.salary_estimate,
    } for row in ds_list]
    data["locations"] = locations
    file=os.path.join("data_app","static","data","cities.json",)
    with open(file) as file:
        codata=json.load(file)
    data["codata"] = codata
    return render_template('position.html',data=data)

@main.route('/size')
def size():
    data=dict()
    data["page_name"] = "Industry Analysis"
    ds_list = list(Datascientist_df.query.all())
    companies = [{
        "company" : row.Company,
        "industry" : row.Industry,
    } for row in ds_list]
    data["companies"] = companies
    return render_template('size.html', data=data)
# company, rating, location, position
# additional json

@main.route('/RatingVsSalary')
def rating():
    data=dict()
    data["page_name"] = "Rating vs. Salary"
    return render_template('rating_and_salary.html', data=data)