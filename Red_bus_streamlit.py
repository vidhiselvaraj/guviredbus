import streamlit as st
import mysql.connector
import pandas as pd
import datetime as dt
from datetime import datetime

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"

)
cursor = con.cursor()

query="use MDE92"
cursor.execute(query)

#Bus route dropdown
st.header("Red Bus scraping project")

col1= st.columns([0.4,0.3,0.3])
col2= st.columns([0.4,0.3,0.3])

query="select distinct route_name from test_red_bus5"
cursor.execute(query)
Route_list =[]
for data in cursor:
    y = data[0]
    Route_list.append(y)
    print(Route_list)

route_option=col1[0].selectbox('Bus routes',Route_list)
print(route_option)
#
#Bus type dropdown

Seat_type_list=['All','Sleeper','Semi-sleeper','Seater']
seat_option = col1[1].selectbox('Select the seat type',Seat_type_list)

#A/C type dropdown

Bus_type_list=['All','A/C','Non A/C']
ac_option = col1[2].selectbox('Select the A/C type',Bus_type_list)

#rating dropdown

Rating_list=['Any rating','Less than 3','3 to 4','Greater than 4']
rating_option = col2[0].selectbox('Select the rating range',Rating_list)

#Bus fare dropdown

Price_list=['All price range','Less than 500','500 to 800','800 to 1000','More than 1000']
fare_option = col2[1].selectbox('Select the Bus fare range',Price_list)

#Timing dropdown

Time_list =['Any time','Before 12:00','12:00 to 17:00','17:00 to 20:00','After 20:00']
time_option = col2[2].selectbox('Select the Bus time range',Time_list)

####Selectinf data from table based on the selection made
#
query="select busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available " \
      "from test_red_bus5 where route_name = '%s'" %route_option

cursor.execute(query)

df = pd.DataFrame(cursor.fetchall(),columns=['Bus Name','Bus Type','Departure Time','Travel Duration','Arrival Time','Rating','Price','Seats available'])

#==================filtering data based on dropdown selection

#seat option  'Sleeper','Semi-sleeper','Seater'
if seat_option == 'Sleeper':
    # df= df[(df["Bus Type"].str.lower().str.contains("sleeper")) and (~df["Bus Type"].str.lower.str.contains("Semi"))]
    df= df[(df["Bus Type"].str.contains("sleeper",case = False)) & (df["Bus Type"].str.contains("semi",case=False)==False)]
elif seat_option == 'Semi-sleeper':
    df = df[(df["Bus Type"].str.contains("semi",case=False)) ]
elif seat_option == 'Seater':
    df= df[(df["Bus Type"].str.contains("seater",case = False))]

#Bus type AC/ non AC

if ac_option == 'A/C':
    # df= df[(df["Bus Type"].str.lower().str.contains("sleeper")) and (~df["Bus Type"].str.lower.str.contains("Semi"))]
    df= df[(df["Bus Type"].str.contains("A/C",case = False)) & (df["Bus Type"].str.contains("non",case=False)==False)]
elif ac_option == 'Non A/C':
    df = df[(df["Bus Type"].str.contains("non",case=False)) ]

#rating option  'Any rating','Less than 3','3 to 4','Greater than 4'
if rating_option == 'Less than 3':
    df= df[(df["Rating"] < 3)]
elif rating_option == '3 to 4':
    df = df[(df["Rating"] >= 3) & (df["Rating"] < 4) ]
elif rating_option == 'Greater than 4':
    df= df[(df["Rating"] >=4)]

#pricing option  'All price range','Less than 500','500 to 800','800 to 1000','More than 1000'
if fare_option == 'Less than 500':
    df= df[(df["Price"] < 500)]
elif fare_option == '500 to 800':
    df = df[(df["Price"] >= 500) & (df["Price"] < 800) ]
elif fare_option == '800 to 1000':
    df= df[(df["Price"] >= 800) & (df["Price"] < 1000) ]
elif fare_option == 'More than 1000':
    df= df[(df["Price"] >=1000)]


#Timing option  ''Any time','Before 12:00','12:00 to 17:00','17:00 to 20:00','After 20:00''
if time_option == 'Before 12:00':
    time_str = '12:00:00'
    time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
    df= df[(df["Departure Time"].dt.time < time_obj)]
elif time_option == '12:00 to 17:00':
    time_str1 = '12:00:00'
    time_str2 = '17:00:00'
    time_obj1 = datetime.strptime(time_str1, '%H:%M:%S').time()
    time_obj2 = datetime.strptime(time_str2, '%H:%M:%S').time()
    df= df[(df["Departure Time"].dt.time >= time_obj1) & (df["Departure Time"].dt.time < time_obj2)]
elif time_option == '17:00 to 20:00':
    time_str1 = '17:00:00'
    time_str2 = '20:00:00'
    time_obj1 = datetime.strptime(time_str1, '%H:%M:%S').time()
    time_obj2 = datetime.strptime(time_str2, '%H:%M:%S').time()
    df= df[(df["Departure Time"].dt.time >= time_obj1) & (df["Departure Time"].dt.time < time_obj2)]
elif time_option == 'After 20:00':
    time_str = '20:00:00'
    time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
    df= df[(df["Departure Time"].dt.time >= time_obj)]


st.dataframe(df)