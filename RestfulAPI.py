from flask_cors import CORS
from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import apikeys
from datetime import datetime

# Connect to PostgreSQL 
conn = psycopg2.connect(
    dbname="Yuridex", 
    user=apikeys.user, 
    password=apikeys.password, 
    host="localHost", 
    port="5432"
)

cur = conn.cursor(cursor_factory=RealDictCursor)

searchResult = ""

# keyword search -> just title 
# filter by tag 
# filter by tag + keyword search join table 
# sort by ascending order descending titles? year published etc, like ratio etc. 


app = Flask(__name__)
CORS(app)

@app.route('/series', methods=["GET"]) #endpoint
def get_series():
    results = cur.execute("SELECT * FROM SERIES")
    return cur.fetchall(), 200

@app.route('/search', methods=["GET"]) #endpoint
def get_series_with_keyword_and_tag():
    titleArg = request.args.get("q", type=str)
    tagArg = request.args.get("tag", type=str)
    sortArg = request.args.get("sort", type=str)
    sortByArg = request.args.get("sortby", type=str) #ascending/descending 

    tagList = [""]
    results = [] 
    if titleArg is None: 
        titleArg = ""
    if tagArg is not None: 
        tagList = tagArg.split(",")
        tagList = [x.capitalize() for x in tagList]
        results = cur.execute("select * from series, tagseriesassign, tag where series.seriesid = tagseriesassign.seriesid and tag.tagid = tagseriesassign.tagid and series.seriesname ILIKE %s AND tag.tagname IN %s", ("%" + titleArg + "%", tuple(tagList)))
    else: 
        print(str(results) +"kljadsklfjaksldfjkaldjfklsajdfklsjkldfjasdklfjakljf")
        results = cur.execute("SELECT * FROM series WHERE seriesname ILIKE %s", ("%" + titleArg + "%",))
        print(str(results) +"kljadsklfjaksldfjkaldjfklsajdfklsjkldfjasdklfjakljf")
    
    results = cur.fetchall()
    if sortArg is not None: #sorting function 
        if sortArg == "title": #title sorting 
            if sortByArg is None or sortByArg == "ascending":  
                results.sort(key=lambda x: x["seriesname"].lower())
            else: #title descending 
                results.sort(reverse=True, key=lambda x: x["seriesname"].lower())
        elif sortArg == "likeratio": #sorting by like ratio 
            if sortByArg is None or sortByArg == "ascending": #sort ascending 
                results.sort(key=lambda x: x["rating"])
            else: #like ratio decending 
                results.sort(reverse=True, key=lambda x: x["rating"])     
    return results, 200

@app.route('/signup', methods=["POST"]) #endpoint
def create_user(): # creating a user + adding account to database 
    #accountId, accountname, email, creationdate, password, profilepic, birthday
    #unique values - accountname + email 

    # getting valid information 
    jsonRequest = request.get_json() # returns a dictionary 

    # putting insert statement together
    accountId = cur.execute("SELECT * FROM account")
    accountID = len(cur.fetchall()) + 1
    accountName = request.get_json().get('accountname', '')
    email = jsonRequest.get('email', '')
    currDate = str(datetime.today())
    currDate = currDate[0:10]
    password = jsonRequest.get('password', '')
    profilepic = ""
    birthday = jsonRequest.get('birthday', '')

    together = "(" + str(accountID) + ", '" + str(accountName) + "', '" + str(email) + "', '" + currDate + "', '" + password + "', '" + profilepic + "', '" + str(birthday) + "')"

    # executing insert statement
    cur.execute("INSERT INTO account (accountId, accountname, email, creationdate, password, profilepic, birthday) VALUES" + together)

    # commit changes to database 
    conn.commit()
    return {"status":"success"}, 200

if __name__ == '__main__': 
    app.run(debug = True)
