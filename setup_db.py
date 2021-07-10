#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import dependencies
import pandas as pd
from sqlalchemy import create_engine
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2 as lily
import string


# In[2]:


# Files to Load 
alldata_path = "Resources/alldata.csv"
datascientist_path = "Resources/dataScientist.csv"


# In[3]:


# create the dataframe 
alldata_df = pd.read_csv(alldata_path)
alldata_df


# In[4]:


# import the dataset
datascientist_df = pd.read_csv(datascientist_path)
datascientist_df


# In[5]:


# delete extra columns in dataScientist csv
datascientist_df .drop(['Unnamed: 0' , 'Job Description', 'Headquarters', 'Size', 'Founded', 'Type of ownership', 'Revenue', 'Sector','Competitors', 'Easy Apply'], axis=1, inplace=True)
datascientist_df


# In[6]:


# delete extra columns in alldata csv
alldata_df .drop(['description', 'reviews'], axis=1, inplace=True)
alldata_df


# In[7]:


# drop all rows with missing information in alldata
alldata_df = alldata_df.dropna(how='any')


# In[8]:


# verify dropped rows in alldata
alldata_df.count()


# In[9]:


# drop all rows with missing information in DataScientist csv
datascientist_df = datascientist_df.dropna(how='any')


# In[10]:


# verify dropped rows in datascientist csv
datascientist_df.count()


# In[11]:


# rename the column names in alldata csv
alldata_df.columns=["Position", "Company", "Location"]
alldata_df


# In[12]:


# rename the column names in datascientist csv
datascientist_df.columns=["Index" , "Position", "Salary Estimate" , "Rating" , "Company", "Location" , "Industry"]
datascientist_df


# In[13]:


# clean the alldata.csv based on following Position

alldata_new_df = alldata_df.loc[(alldata_df["Position"].str.contains("Scientist")) | 
                                (alldata_df["Position"].str.contains("Analyst")) |
                                (alldata_df["Position"].str.contains("Engineer")) |
                                (alldata_df["Position"].str.contains("Research Scientist")) |
                                (alldata_df["Position"].str.contains("System Engineer")) |
                                (alldata_df["Position"].str.contains("Web Developer")) |
                                (alldata_df["Position"].str.contains("Amazon AI- Applied Scientist"))]

alldata_new_df


# In[14]:


# clean the datascientist.csv based on following Position

datascientist_new_df = datascientist_df.loc[(datascientist_df["Position"].str.contains("Scientist")) | 
                                            (datascientist_df["Position"].str.contains("Analyst")) |
                                            (datascientist_df["Position"].str.contains("Engineer")) |
                                            (datascientist_df["Position"].str.contains("Research Scientist")) |
                                            (datascientist_df["Position"].str.contains("System Engineer")) |
                                            (datascientist_df["Position"].str.contains("Web Developer")) |
                                            (datascientist_df["Position"].str.contains("Amazon AI- Applied Scientist"))] 
datascientist_new_df


# In[15]:


# output clean dataframe to csv for alldata.csv

alldata = "Resources/alldata(clean).csv"
alldata_new_df.to_csv(alldata,index=False)


# In[16]:


# output clean dataframe to csv for datascientist.csv

datascientist = "Resources/datascientist(clean).csv"
datascientist_new_df.to_csv(datascientist,index=False)


# In[17]:


# merge after invidual csv clean for multiple coloumns
ds_alldata=alldata_new_df.merge(datascientist_df,on=["Position","Location"])


# In[18]:


#Removing punctuations before we call DB functions
alldata_df["Position"]=alldata_df["Position"].apply(lambda z: z.translate(str.maketrans('', '', string.punctuation)))
alldata_df["Company"]=alldata_df["Company"].apply(lambda z: z.translate(str.maketrans('', '', string.punctuation)))
alldata_df["Location"]=alldata_df["Location"].apply(lambda z: z.translate(str.maketrans('', '', string.punctuation)))

datascientist_df["Position"]=datascientist_df["Position"].apply(lambda z: z.translate(str.maketrans('', '', string.punctuation)))
datascientist_df["Company"]=datascientist_df["Company"].apply(lambda z: z.translate(str.maketrans('', '', string.punctuation)))
datascientist_df["Location"]=datascientist_df["Location"].apply(lambda z: z.translate(str.maketrans('', '', string.punctuation)))
datascientist_df["Industry"]=datascientist_df["Industry"].apply(lambda z: z.translate(str.maketrans('', '', string.punctuation)))


# In[21]:


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


# In[22]:


#Dropping all tables gathered 
execute_sql_statement("DROP TABLE IF EXISTS alldata,datascientist,company,location,industry,position CASCADE;")


# In[23]:


#database tables
#Creating table as per requirement 
sql ='''CREATE TABLE company( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id))''' 
execute_sql_statement(sql)
print("Table created successfully........") 
#Closing the connection conn.close()


# In[24]:


#Creating table as per requirement 
sql ='''CREATE TABLE position( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id))''' 
execute_sql_statement(sql)
print("Table created successfully........")


# In[25]:


#Creating table as per requirement 
sql ='''CREATE TABLE location( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id) )''' 
execute_sql_statement(sql)
print("Table created successfully........")


# In[26]:


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


# In[27]:


#Tables for Data scientist csv
#Creating table as per requirement 
sql ='''CREATE TABLE industry( id INT GENERATED ALWAYS AS IDENTITY, name VARCHAR(255) NOT NULL, PRIMARY KEY(id) )''' 
execute_sql_statement(sql)
print("Table created successfully........")


# In[28]:


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


# In[34]:


#Insert Data
#Create Engine and connection to Database
engine = create_engine('postgresql://postgres:pythondata@localhost:5432/data_science_careers')


# In[35]:


alldata_df.to_sql("all_data_df",engine,if_exists="replace")


# In[36]:


datascientist_df.to_sql("datascientist_df",engine,if_exists="replace")


# In[37]:


#Normalizing data
df_position=pd.DataFrame((pd.concat([alldata_df.Position,datascientist_df.Position],axis=0)).unique())
df_position.columns=["name"]
df_position.to_sql("position",engine,if_exists="append",index=False)


# In[38]:


df_Location=pd.DataFrame((pd.concat([alldata_df.Location,datascientist_df.Location],axis=0)).unique())
df_Location.columns=["name"]
df_Location.to_sql("location",engine,if_exists="append",index=False)


# In[39]:


df_Industry=pd.DataFrame(datascientist_df.Industry.unique())
df_Industry.columns=["name"]
df_Industry.to_sql("industry",engine,if_exists="append",index=False)


# In[40]:


#We combined all data and data scientist together to get the unique value
df_Company=pd.DataFrame((pd.concat([alldata_df.Company,datascientist_df.Company],axis=0)).unique())
df_Company.columns=["name"]
df_Company.to_sql("company",engine,if_exists="append",index=False)


# In[41]:


#Create a function to create a sql for PositionID,companyID and LocationID
def insert_for_alldata(pos_name,loc_name,comp_name):
    sql='''insert into alldata(positionid, companyid, locationid) select p.id,c.id,l.id from position p,location l, company c where p.name=\''''+pos_name+'''\' and l.name=\''''+loc_name+'''\' and c.name=\''''+comp_name+'\''
    execute_sql_statement(sql)
    return "success"


# In[42]:


for index, row in alldata_df.iterrows():
    insert_for_alldata(row['Position'], 
                       row['Location'],
                       row['Company'])


# In[43]:


#Create a function to creat a sql for PositionID,companyID and LocationID
def insert_for_datascientist(pos_name,loc_name,comp_name,ind_name,rating,salary_estimate):
    sql='''insert into datascientist(positionid, companyid, locationid, industryid,rating,salary_estimate) select p.id,c.id,l.id,ind.id, '''+str(rating)+ ', \''+salary_estimate+'''\' from position p,location l, company c, industry ind where p.name=\''''+pos_name+'''\' and l.name=\''''+loc_name+'''\' and c.name=\''''+comp_name+'''\' and ind.name=\''''+ind_name+'\''
    execute_sql_statement(sql)
    return "success"


# In[ ]:


for index, row in datascientist_df.iterrows():
    insert_for_datascientist(row['Position'],row['Location'],row['Company'],
                            row['Industry'],row['Rating'],row['Salary Estimate'])


# In[ ]:




