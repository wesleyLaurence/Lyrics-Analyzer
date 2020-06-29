import mysql.connector
from datetime import datetime
import pandas as pd

class SQL_kit(object):
    
    def __init__(self, userID=None, password=None, database=None):
        
        self.userID = userID
        self.password = password
        self.database = database
        
    def insert_row(self, sql, val):   
        """ update_db  

        Required Parameters
        sql: a string of the SQL code you want executed.
        
        val: a tuple of all values being loaded into SQL table
     
        """   
      
        try: 
            #
            mydb=mysql.connector.connect(
            host="localhost",
            port=3306,
            user=self.userID,
            passwd=self.password,
            database=self.database
            )

            mycursor = mydb.cursor()
            mycursor.execute(sql, val)
            mydb.commit()
            mycursor.close()
            mydb.close()

        except Error as e:
            mycursor.close()
            mydb.close()
            print(e)
            
            
    # get data from cleanlyrics SQL table
    def get_data(self):   

        try: 
            #
            mydb=mysql.connector.connect(
            host="localhost",
            port=3306,
            user=self.userID,
            passwd=self.password,
            database=self.database
            )

            # get data
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM cleanlyrics;")
            myresult = mycursor.fetchall()
            mycursor.close()

            # get column names
            mycursor = mydb.cursor()
            mycursor.execute("SHOW columns FROM cleanlyrics;")
            column_names = list(pd.DataFrame(mycursor.fetchall())[0])
            mycursor.close()
            mydb.close()

        except Error as e:
            mycursor.close()
            mydb.close()
            print(e)

        df = pd.DataFrame(myresult,columns=column_names)
        df.set_index('SongID',inplace=True)

        return df
    # MusiCode class updates
    
    def cleanlyrics_table(self, song_name, artist_name, clean):         
            sql = "INSERT INTO cleanlyrics (Song, Artist, Clean) VALUES (%s, %s, %s)" 
            val = (song_name, artist_name, clean)     
            self.insert_row(sql,val)
