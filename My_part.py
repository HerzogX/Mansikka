import openpyxl
import random
import sqlite3
import pandas as pd

#day = input("Enter which day of the year you are interested  \n ") #try the date to be on the Preddate column
#amount = float(input("Enter how many kgs do you want \n ")) #try the amount to be in the Prenumber column


def cropamount(day, amount):
    cnx = sqlite3.connect('StrawberryERP.db')
    df = pd.read_sql_query("SELECT * FROM CropPredictions", cnx)
    new_data = df[df['Preddate'] == int(day)]
    max_value = float(new_data['Prednumber'].max())
    neweast_data = new_data[new_data['Prednumber'] == max_value]
    if max_value >= amount:
        after_substract = max_value - amount
        number_of_row = int(neweast_data['Row'])
        id = int(neweast_data['PredictionID'])
        neweast_data = neweast_data.copy()
        df.iloc[int(id)-1, 2] =  after_substract
        df.to_sql(name='CropPredictions', con=cnx, if_exists='replace', index=False)
        cnx.close()
        return number_of_row
        #return max_value - amount
    else: 
        cnx.close()
        return "Sorry, we don't have that amount of crop"

def OrderRecorder(day, amount, row):
    DBConn = sqlite3.connect('StrawberryERP.db')
    DBcursor = DBConn.cursor()
    with DBConn:
        DBcursor.execute("INSERT INTO ordertable (ReservationDate, Amount, RowID) VALUES (?, ?, ?)", (day, amount, row))
    DBConn.close()

def reservationReview():
    DBConn = sqlite3.connect('StrawberryERP.db')
    DBcursor = DBConn.cursor()
    with DBConn:
        DBcursor.execute("SELECT ReservationDate, Amount, RowID, OrderID FROM ordertable ORDER BY OrderID DESC LIMIT 1")
    fetchresult = DBcursor.fetchone()
    return fetchresult
    
#Result = cropamount(day, amount)
#print(Result)