## THIS FILE WAS CREATED BY MODIFYING AN ORIGINAL NOTEBOOK CREATED BY:
# Albe Eteme, Hussein Issa, Jane Kim, and Shailja Mathur
#
## MODIFICATIONS MADE BY:
# Andrew Anastasiades | @andrew-ana

# import dependencies
import pandas as pd
from sqlalchemy import create_engine
import psycopg2 as lily

# Required Files
alldata = "Resources/alldata(clean).csv"
datascientist = "Resources/datascientist(clean).csv"

# Create DataFrames
alldata_df = pd.read_csv(alldata)
datascientist_df = pd.read_csv(datascientist)

#connect to database
def execute_sql_statement(sqltext):
    conn=lily.connect( host="localhost", database="data_science_careers", user="postgres", password="pythondata")
#cursor is an object to put watever you want
    cursor=conn.cursor()
#xecute() method
    cursor.execute(sqltext)
    conn.commit()
#Closing the connection
    conn.close()

#from config import sqldb_connect
#engine = create_engine(sqldb_connect)


#Dropping all tables gathered 
execute_sql_statement("DROP TABLE IF EXISTS alldata,datascientist,company,location,industry,position CASCADE;")

#database tables
#Creating table as per requirement 
sql ='''CREATE TABLE company( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id))''' 
execute_sql_statement(sql)
print("Table created successfully........") 
#Closing the connection conn.close()

#Creating table as per requirement 
sql ='''CREATE TABLE position( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id))''' 
execute_sql_statement(sql)
print("Table created successfully........")

#Creating table as per requirement 
sql ='''CREATE TABLE location( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id) )''' 
execute_sql_statement(sql)
print("Table created successfully........")

#Creating for all data csv
#Creating table as per requirement 
sql ='''CREATE TABLE alldata( id INT GENERATED ALWAYS AS IDENTITY,
positionid INT, 
companyid INT, 
locationid INT, 
PRIMARY KEY(id),
CONSTRAINT fk_Pos_id FOREIGN KEY(positionid) REFERENCES position(id),
CONSTRAINT fk_Comp_id FOREIGN KEY(companyid) REFERENCES company(id),
CONSTRAINT fk_Loc_id FOREIGN KEY(locationid) REFERENCES location(id))'''
execute_sql_statement(sql)
print("Table created successfully........")

#Tables for Data scientist csv
#Creating table as per requirement 
sql ='''CREATE TABLE industry( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id) )''' 
execute_sql_statement(sql)
print("Table created successfully........")

#Creating table as per requirement 
sql ='''CREATE TABLE datascientist(id INT GENERATED ALWAYS AS IDENTITY, 
positionid INT, 
companyid INT, 
locationid INT,  
industryid INT, 
rating decimal, 
salary_estimate VARCHAR(255), 
PRIMARY KEY(id), 
CONSTRAINT fk_pos_1 FOREIGN KEY(positionid) REFERENCES Position(ID) ON DELETE CASCADE, 
CONSTRAINT fk_comp_1 FOREIGN KEY(companyid) REFERENCES Company(ID) ON DELETE CASCADE, 
CONSTRAINT fk_loc_1 FOREIGN KEY(locationid) REFERENCES Location(ID) ON DELETE CASCADE, 
CONSTRAINT fk_indus FOREIGN KEY(industryid) REFERENCES Industry(ID) ON DELETE CASCADE)''' 
execute_sql_statement(sql)
print("Table created successfully........")


#Insert Data
#Create Engine and connection to Database
engine = create_engine('postgresql://postgres:pythondata@localhost:5432/data_science_careers')


alldata_df.to_sql("all_data_df",engine,if_exists="replace")




datascientist_df.to_sql("datascientist_df",engine,if_exists="replace")


#Normalizing data
df_position=pd.DataFrame((pd.concat([alldata_df.Position,datascientist_df.Position],axis=0)).unique())
df_position.columns=["name"]
df_position.to_sql("position",engine,if_exists="append",index=False)



df_Location=pd.DataFrame((pd.concat([alldata_df.Location,datascientist_df.Location],axis=0)).unique())
df_Location.columns=["name"]
df_Location.to_sql("location",engine,if_exists="append",index=False)

df_Industry=pd.DataFrame(datascientist_df.Industry.unique())
df_Industry.columns=["name"]
df_Industry.to_sql("industry",engine,if_exists="append",index=False)


#We combined all data and data scientist together to get the unique value
df_Company=pd.DataFrame((pd.concat([alldata_df.Company,datascientist_df.Company],axis=0)).unique())
df_Company.columns=["name"]
df_Company.to_sql("company",engine,if_exists="append",index=False)


#Create a function to create a sql for PositionID,companyID and LocationID
def insert_for_alldata(pos_name,loc_name,comp_name):
    sql='''insert into alldata(positionid, companyid, locationid) select p.id,c.id,l.id from position p,location l, company c where p.name=\''''+pos_name+'''\' and l.name=\''''+loc_name+'''\' and c.name=\''''+comp_name+'\''
    execute_sql_statement(sql)
    return "success"



for index, row in alldata_df.iterrows():
    insert_for_alldata(row['Position'], 
                       row['Location'],
                       row['Company'])



#Create a function to creat a sql for PositionID,companyID and LocationID
def insert_for_datascientist(pos_name,loc_name,comp_name,ind_name,rating,salary_estimate):
    sql='''insert into datascientist(positionid, companyid, locationid, industryid,rating,salary_estimate) select p.id,c.id,l.id,ind.id, '''+str(rating)+ ', \''+salary_estimate+'''\' from position p,location l, company c, industry ind where p.name=\''''+pos_name+'''\' and l.name=\''''+loc_name+'''\' and c.name=\''''+comp_name+'''\' and ind.name=\''''+ind_name+'\''
    execute_sql_statement(sql)
    return "success"



for index, row in datascientist_df.iterrows():
    insert_for_datascientist(row['Position'],row['Location'],row['Company'],
                            row['Industry'],row['Rating'],row['Salary Estimate'])





