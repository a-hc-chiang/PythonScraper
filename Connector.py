import psycopg2
import csv
import re
import random
import apikeys


# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="Yuridex", 
    user=apikeys.user, 
    password=apikeys.password, 
    host="localHost", 
    port="5432"
)
cur = conn.cursor()

#cur.execute("DELETE FROM series;") #delete contents of table 
# cur.execute("DELETE FROM TagSeriesAssign;")


# Open CSV file 
with open('./test.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header row
    series_id = 1 #seriesid counter 
    tag_id = 1
    tagsSet = set()

    #populating tags table 
    # for row in reader: 
    #     arr = row[2].split(",")
    #     toAdd = ""
    #     for s in arr: 
    #         s = re.sub(r'\W+', '', s)
    #         if s not in tagsSet and s != '' and s != 'NA':
    #             tagsSet.add(s)

    #adding tags entries 
    # for tag in tagsSet: 
    #     r = lambda: random.randint(0,255) #calling randint 3 times 
    #     color = "{:x}{:x}{:x}"
    #     cur.execute(
    #         """
    #         INSERT INTO tag (
    #             tagid, tagname, tagcolor
    #         )
    #         VALUES (%s, %s, %s)
    #         """,
    #         (
    #             str(tag_id),                         # tagID: int
    #             tag,                          # tagname: string
    #             color.format(r(), r(), r())     # tagcolor: hex val in string format 
    #         )
    #     )
    #     tag_id += 1

    #populating series table
    # for row in reader:
    #     # row is a row in your csv
        
    #     '''
    #     row idx: 
    #     0 = title 
    #     1 = authors
    #     2 = genres
    #     3 = cv img 
    #     4 = series type 
    #     5 = series status
    #     6 = publish date
    #     7 = summary 
    #     '''

    #     cur.execute(
    #         """
    #         INSERT INTO series (
    #             seriesid, seriesname, seriestype, accesslink, creationdate,
    #             seriesstatus, summary, rating, cover
    #         )
    #         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    #         """,
    #         (
    #             series_id,           # seriesid: integer or serial
    #             row[0],       # seriesname: string
    #             row[4],       # seriestype: string
    #             'N/A',        # accesslink: hardcoded val
    #             row[6],       # creationdate: string or date (verify this index is intentional)
    #             row[5],       # seriesstatus: string
    #             row[7],       # summary: string
    #             'N/A',       # rating: string or float
    #             row[3]          # cover: If not available, use None
    #         )
    #     )


    #     series_id += 1

with open('./test.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    #populating TagSeriesAssign table 
    for row in reader: 

        cur.execute("SELECT seriesid FROM series WHERE seriesname = %s AND creationdate = %s", [row[0], row[6]])
        seriesId = cur.fetchall()[0][0] #seriesID to add into 
        genreSet = set()
        arr = row[2].split(",")
        for s in arr: 
            s = re.sub(r'\W+', '', s)
            if s not in genreSet and s != '' and s != 'NA':
                genreSet.add(s)
        
        for tag in genreSet: 
            #getting tag id 
            print(tag)
            # print(row)
            cur.execute("SELECT TagID FROM tag WHERE tagname = %s", [tag])
            tagId = cur.fetchall()[0][0]
            print(tagId, seriesId)
            cur.execute(
                "SELECT COUNT(*) FROM TagSeriesAssign WHERE tagid = %s AND seriesid = %s",
                (tagId, seriesId)
            )
            exists = cur.fetchone()[0]

            if exists == 0:
                cur.execute(
                    """INSERT INTO TagSeriesAssign (tagid, seriesid) VALUES (%s, %s)""",
                    (tagId, seriesId)
                )
            else:
                print(f"Entry with tagid={tagId} and seriesid={seriesId} already exists.")


# Commit changes and close the connection
conn.commit()
cur.close()
conn.close()