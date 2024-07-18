import time
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import pandas as pd
from datetime import datetime
#
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

#website to scrape
driver.get('https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile')

time.sleep(5)
wait = WebDriverWait(driver, 10)

def format_date(date1):     #date formatting

    date_input = date1
    date_obj = datetime.strptime(date_input, '%d %b')
    return (date_obj.strftime('%d-%m-2024'))

def format_time(time):   #time formatting
    time_input = time
    date_obj = datetime.strptime(time_input, '%H:%M')
    return (date_obj.strftime('%H:%M:00'))

def Get_Bus_details():

    ##expand hidden buses
    try:
        driver.find_element(By.XPATH, '//*[@id="result-section"]/div[2]/div/div[2]/div/div[4]/div[2]/i').click()
    except:
        pass

    time.sleep(5)
    try:
        driver.find_element(By.XPATH, '//*[@id="result-section"]/div[1]/div/div[2]/div/div[4]/div[2]/i').click()
    except:
        pass
    time.sleep(5)

    ####

    bus_name=[]
    time_start=[]
    time_end=[]
    time_duration=[]
    bus_type =[]
    bus_rating = []
    bus_fare = []
    seat_avail = []
    a = 0
    b = 0
    bus_start_date_elem = driver.find_element(By.CSS_SELECTOR,'input[id="searchDat"]')
    print(bus_start_date_elem.get_attribute("value"))
    bus_start_date_x = bus_start_date_elem.get_attribute("value")
    bus_start_date=format_date(bus_start_date_x)

    time.sleep(5)
    for i in range(3):
        driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight," + "document.body.scrollHeight,document.documentElement.clientHeight));");
        a +=1
        print("a",a)
        id = driver.find_elements(By.CSS_SELECTOR,'li[class="row-sec clearfix"]')
    for i in id:
        b+=1
        print("b",b)
        try:
            bus_name_elem= i.find_element(By.CSS_SELECTOR,'div[class="travels lh-24 f-bold d-color"]')
            bus_name.append(bus_name_elem.text)
        except:
            bus_name.append(np.nan)


        try:
            time_start_elem= i.find_element(By.CSS_SELECTOR,'div[class="dp-time f-19 d-color f-bold"]')
            z=format_time(time_start_elem.text)
            time_start.append(z)
            print("time start length")

        except:
            time_start.append(np.nan)


        try:
            time_end_elem =  i.find_element(By.CSS_SELECTOR,'div[class="bp-time f-19 d-color disp-Inline"]')
            z=format_time(time_end_elem.text)
            time_end.append(z)
        except:
            time_end.append(np.nan)


        try:
            time_duration_elem = i.find_element(By.CSS_SELECTOR,'div[class="dur l-color lh-24"]')
            time_duration.append(time_duration_elem.text)
        except:
            time_duration.append(np.nan)


        try:
            bus_type_elem = i.find_element(By.CSS_SELECTOR,'div[class="bus-type f-12 m-top-16 l-color evBus"]')
            bus_type.append(bus_type_elem.text)
        except:
            bus_type.append(np.nan)


        try:
            bus_rating_elem = i.find_element(By.CSS_SELECTOR,'div[class="rating-sec lh-24"]')
            bus_rating.append(bus_rating_elem.text)
        except:
            bus_rating.append(np.nan)


        try:
            bus_fare_elem = i.find_element(By.CSS_SELECTOR,'div[class="fare d-block"]')
            bus_fare.append(bus_fare_elem.text)
        except:
            bus_fare.append(np.nan)


        try:
            seat_avail_elem=i.find_element(By.CSS_SELECTOR,'div[class="seat-left m-top-30"]')
            seat_avail.append(seat_avail_elem.text)
        except:
            try:
                seat_avail_elem1 = i.find_element(By.CSS_SELECTOR,'div[class="seat-left m-top-16"]')
                seat_avail.append(seat_avail_elem1.text)
            except:
                seat_avail.append(np.nan)


    # dictionary of lists
    dict = {'Bus_name': bus_name, 'Bus_type': bus_type, 'Starting_time': time_start, 'Duration': time_duration, 'Reaching_time': time_end, 'Bus_rating': bus_rating, 'Bus_fare': bus_fare, 'Seat_avail':seat_avail}

    df = pd.DataFrame(dict)
    aday = dt.timedelta(days=1)
    df['Bus_route'] = current_bus_route
    df['Bus_route_link'] = current_bus_link
    df['Starting_date'] = bus_start_date
    # df['Reaching_date'] = bus_start_date

    df['Starting_date_time']= pd.to_datetime(df['Starting_date'] + ' ' + df['Starting_time'])
    df['Reaching_date_time']= pd.to_datetime(df['Starting_date'] + ' ' + df['Reaching_time'])
    for i in range(len(df["Starting_date_time"])):

        if (df["Starting_date_time"][i]) > (df["Reaching_date_time"][i]):
            df['Reaching_date_time'][i] = (df['Reaching_date_time'][i])+ aday


    print(df['Starting_date_time'])
    print(df['Reaching_date_time'])

    # saving the dataframe
    df.to_csv(r'C:\Users\vidhi\Desktop\ds\Bus_route_details_new.csv')
    return True


bus_routes={}
# i.text gives list of bus routes and get_attribute to get links
bus_routes_elem= driver.find_elements(By.CSS_SELECTOR,'a[class="route"]')
time.sleep(5)

#dictionary with route: href links
for i in bus_routes_elem:
    bus_routes[i.text]=i.get_attribute('href')

time.sleep(5)
#

for i in bus_routes:
    print(i)
    current_bus_route = i
    current_bus_link = bus_routes[i]
    x = 'a[title="'+i+'"]'
    print(x)
    time.sleep(5)
    element = driver.find_element(By.CSS_SELECTOR, x)
    driver.execute_script("arguments[0].click();", element)
    time.sleep(5)

    ###code to get bus details
    x=Get_Bus_details()

    #code to go back
    # driver.back()
    driver.execute_script("window.history.go(-1)")
    print("go back")

    # driver.navigate().back()
    # driver.navigate().to("http://www.example.com");
    driver.get('https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile')


    # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[class="D117_main D117_container"]')))
    time.sleep(5)
    # driver.find_elements(By.CSS_SELECTOR,'div[class="D121_header_wrapper"]')

