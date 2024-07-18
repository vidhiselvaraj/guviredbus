#
import pandas as pd
import mysql.connector
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"

)
cursor = con.cursor()

query="use MDE92"
cursor.execute(query)

#Query to create table for storing bus data
query="""create table if not exists test_red_bus5(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                                route_name varchar(100),
                                route_link varchar(200),
                                busname varchar(100),
                                bustype varchar(200),
                                departing_time DATETIME,
                                duration varchar(50),
                                reaching_time DATETIME,
                                star_rating float,
                                price decimal(10,2),
                                seats_available INT)"""
cursor.execute(query)
con.commit()

df=pd.read_csv(r'C:\Users\vidhi\Desktop\ds\Bus_route_details_new.csv')
print(df.columns)
# df = df.drop(['Unnamed: 0'],axis=1)
df1 = pd.DataFrame()

df1['Bus_route']=df['Bus_route']
df1['Bus_route_link']=df['Bus_route_link']
df1['Bus_name']=df['Bus_name']
df1['Bus_type']=df['Bus_type']
df1['Starting_date_time']=pd.to_datetime(df['Starting_date_time'])
df1['Duration']=df['Duration']
df1['Reaching_date_time']=pd.to_datetime(df['Reaching_date_time'])
df1['Bus_rating']=df['Bus_rating'].astype(float)
df1['Bus_rating']=df['Bus_rating'].fillna(0)
# df1['Bus_fare']=df['Bus_fare']
for i in range(len(df['Bus_fare'])):
    fare = []

    for j in df['Bus_fare'][i]:
        if j.isnumeric():
            fare.append(j)
    df['Bus_fare'][i] = "".join(fare)
# print(df['Bus_fare'],df1['Bus_fare'])

df1['Bus_fare']=df['Bus_fare'].astype(float)

# df1['Seat_avail']=df['Seat_avail']
for i in range(len(df['Seat_avail'])):
    seat = []

    for j in df['Seat_avail'][i]:
        if j.isnumeric():
            seat.append(j)
    df['Seat_avail'][i] = "".join(seat)
# print(df['Seat_avail'],df1['Seat_avail'])
df1['Seat_avail']=df['Seat_avail'].astype(float)
print(df1.columns)
print(df1)
print("3333333333")
# df2 = pd.DataFrame()
# df2['Bus_rating']=df1['Bus_rating']
# df2['Bus_fare']=df1['Bus_fare']

# df2['Seat_avail']=df1['Seat_avail']
# query = "show tables"
# cursor.execute(query)
# for table in cursor:
#     print(table)
query = "desc test_red_bus5"
cursor.execute(query)
for table in cursor:
    print(table)
# print("3333333333")
# query = "insert into test_red_bus (route_name,route_link,busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
# for index in df1.index:
#     row = tuple(df1.loc[index].values)
#     print(row)
#     print("4444444")
#     cursor.execute(query,row)
# con.commit()
query = "insert into test_red_bus5 (route_name,route_link,busname,bustype,departing_time,duration,reaching_time,star_rating,price,seats_available) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
for index in df1.index:
    row = tuple(df1.loc[index].values)
    print(row)
    print("4444444")
    cursor.execute(query,row)
con.commit()
print("data from table")
query = "Select * from test_red_bus5"
cursor.execute(query)
for data in cursor:
    print(data)
# # query = "Select * from test_red_bus3 where id = 1"
# # cursor.execute(query)
# # for data in cursor:
# #     print(data)
