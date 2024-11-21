import sqlite3
import pandas as pd
from datetime import datetime

# sqlite db
db_filename = 'imdb.db'


# connect
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Titles
# cols: tconst,titleType,primaryTitle,originalTitle,isAdult,startYear,endYear,runtimeMinutes,genres
csv_path = "./ImdbTitleBasics.csv"
df_titles = pd.read_csv(csv_path, low_memory=False)

#df_titles = df_titles.iloc[:100]
df_titles = df_titles.sample(5000).drop_duplicates().reset_index(drop=True)


# Crew
# cols: tconst,ordering,nconst,category,job,characters
csv_path = "./ImdbTitlePrincipals.csv"
df_crew = pd.read_csv(csv_path)

# Ratings
# cols: tconst,averageRating,numVotes
csv_path = "./ImdbTitleRatings.csv"
df_ratings = pd.read_csv(csv_path)

# People
# nconst,primaryName,birthYear,deathYear,primaryProfession,knownForTitles
csv_path = "./ImdbName.csv"
df_people = pd.read_csv(csv_path)
df_people["birthYear"]=df_people["birthYear"].replace("\\N", "1965")
df_people["deathYear"]=df_people["deathYear"].replace("\\N", "2025")
df_people["birthYear"]=df_people["birthYear"].astype(int)
df_people["deathYear"]=df_people["deathYear"].astype(int)

df_titles["startYear"]=df_titles["startYear"].replace("\\N", "1965")
df_titles["endYear"]=df_titles["endYear"].replace("\\N", "2025")
df_titles["startYear"]=df_titles["startYear"].astype(int)
df_titles["endYear"]=df_titles["endYear"].astype(int)

df_titles['title_id'] = df_titles.tconst.apply(lambda x: int(x[2:])) 
df_crew['title_id'] = df_crew.tconst.apply(lambda x: int(x[2:])) 
df_crew['person_id'] = df_crew.nconst.apply(lambda x: int(x[2:])) 

df_ratings['title_id'] = df_ratings.tconst.apply(lambda x: int(x[2:])) 
df_people['person_id'] = df_people.nconst.apply(lambda x: int(x[2:])) 


# shrink the dataframes
df_crew = df_crew.query("title_id in @df_titles.title_id")
df_ratings = df_ratings.query("title_id in @df_titles.title_id")
df_people = df_people.query("person_id in @df_crew.person_id")

# adjust the column names
columns = ["title_id","person_id","category", "job", "characters"]
df_crew = df_crew[columns]

columns = ["person_id","primaryName", "birthYear", "deathYear"]
df_people = df_people[columns]

columns = ["title_id","averageRating", "numVotes"]
df_ratings = df_ratings[columns]

columns = ["title_id","titleType","primaryTitle","originalTitle","isAdult","startYear","endYear","runtimeMinutes","genres"]
df_titles = df_titles[columns]

print(len(df_ratings))
print(len(df_titles))
print(len(df_crew))
print(len(df_people))


# Insert the rows into people
tuples_people = list(df_people.itertuples(index=False, name=None))
cursor.executemany('''
    INSERT INTO people (person_id, name, born, died)
    VALUES (?, ?, ?, ?)
''', tuples_people)


# Insert the rows into ratings
tuples_ratings = list(df_ratings.itertuples(index=False, name=None))
cursor.executemany('''
    INSERT INTO ratings (title_id, rating, votes)
    VALUES (?, ?, ?)
''', tuples_ratings)

# Insert the rows into crew
tuples_crew = list(df_crew.itertuples(index=False, name=None))
cursor.executemany('''
    INSERT INTO crew (title_id, person_id, category, job, character)
    VALUES (?, ?, ?, ?, ?)
''', tuples_crew)


# Insert the rows into titles
tuples_titles = list(df_titles.itertuples(index=False, name=None))
cursor.executemany('''
    INSERT INTO titles (title_id,type,primary_title,original_title,is_adult,premiered,ended,runtime,genres)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
''', tuples_titles)

conn.commit()
conn.close()


print(f"Database '{db_filename}' updated successfully with data from CSV file.")
