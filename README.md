# Project 2
 
![alt text](https://github.com/iyesogie/Data-Science-Jobs/blob/main/images/Data%20Science%20Jobs.png?raw=true![image](https://user-images.githubusercontent.com/79468835/128101220-b16c8c60-d2e1-4448-becb-842e8f4e612f.png)
)

### Part 1 - Database Installation
In order to set up the database on your local machine, you will need:  
1. A SQL database management application, such as DBeaver or PGAdmin. The default configuration assumes you are connected on localhost:5432, but you may change the port in the db_config.py file.
2. A new database. The default database is named 'data_science_careers', but can also be configured.
3. Your SQL server username and password. (Defaults to 'postgres' and 'postgres').

Once you have met the requirements, you will need to navigate to the root of the repository and run the setup_db.py file.  
Congratulations! Database installation is complete.

### Part 2 - Running the flask application  
Running the application is fairly straightforward. In your terminal, navigate to the root of the repository.  

If you wish to run in development mode, enter the following:
```bash
export FLASK_APP=data_app
export FLASK_ENV=development
flask run
```

If you simply want to view the application as is:
```bash
export FLASK_APP=data_app
flask run
```

Once you have run the commands, your terminal will tell you which port the application is hosted on and you can view application by navigating to:  
localhost:5000/home  
(where 5000 is the port supplied by your terminal)

If you are on a network you trust you can host the application to other devices on that network with 

```bash
export FLASK_APP=data_app
flask run --host 0.0.0.0
```

Simply determine the IP address of the device hosting and the port on which the application is running, then visit that url in a browser on your remote device. Example: http://192.123.4.56:5000/home

