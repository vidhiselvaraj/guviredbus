
import mysql.connector
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678"

)
cursor = con.cursor()

query="use MDE92"
cursor.execute(query)

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

