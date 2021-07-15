from . import db

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Datascientist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    positionid = db.Column(db.Integer)
    companyid = db.Column(db.Integer)
    locationid = db.Column(db.Integer)
    industryid = db.Column(db.Integer)
    rating = db.Column(db.Float)
    salary_estimate = db.Column(db.String(255), unique=False, nullable=False)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

# Company and Datascientists
class Datascientist_df(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    Index = db.Column(db.Integer, primary_key=True)
    Position = db.Column(db.String)
    Company = db.Column(db.String)
    Rating = db.Column(db.Float)
    Location = db.Column(db.String)
    Industry = db.Column(db.String)
    salary_estimate = db.Column("Salary Estimate",db.String(255), unique=False, nullable=False)