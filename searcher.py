from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from urllib.request import urlopen
import string


json_file = open('inventory.json', encoding='utf-8-sig')
data = json.loads(json_file.read())
driver = webdriver.Chrome()
driver.set_window_position(-10000, 0)
failed = False

for i in range(0, len(data)):
    failed = False
    #print(data[i]['Book Title'])

    driver.get("https://hub.lexile.com/find-a-book/search")
    #assert "Python" in driver.title
    #elem = driver.find_element_by_name("q")
    driver.implicitly_wait(1.5)
    search_bar = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/main/div/form/div/div[2]/div[1]/div/div/input')
    search_bar.send_keys(str(data[i]['Book Title']).replace("\n", ""))
    search_bar.send_keys(Keys.RETURN)

    #program first tries finding book on lexile.com:
    try:

        #finds reading level
        driver.implicitly_wait(2)
        reading_level_element = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/main/div/form/div/div[2]/div[1]/div[1]/div/div[2]/div/div[1]/div')
        reading_level = reading_level_element.text
        data[i]["Lexile Measure"] = reading_level
        print(data[i]['Book Title'] + "'s Lexile measure:", reading_level)

        #calculates the grade level based off lexile measure
        whitelist = set(string.digits)
        reading_level = ''.join(c for c in reading_level if c in whitelist)
        if int(reading_level) < 165:
            data[i]["Grade Level"] = "K"
        elif int(reading_level) < 425:
            data[i]["Grade Level"] = "1"
        elif int(reading_level) < 645:
            data[i]["Grade Level"] = "2"
        elif int(reading_level) < 850:
            data[i]["Grade Level"] = "3"
        elif int(reading_level) < 950:
            data[i]["Grade Level"] = "4"
        elif int(reading_level) < 1030:
            data[i]["Grade Level"] = "5"
        elif int(reading_level) < 1095:
            data[i]["Grade Level"] = "6"
        elif int(reading_level) < 1155:
            data[i]["Grade Level"] = "7"
        elif int(reading_level) < 1205:
            data[i]["Grade Level"] = "8"
        elif int(reading_level) < 1250:
            data[i]["Grade Level"] = "9"
        elif int(reading_level) < 1295:
            data[i]["Grade Level"] = "10"
        elif int(reading_level) < 1310:
            data[i]["Grade Level"] = "11"
        elif int(reading_level) >= 1310:
            data[i]["Grade Level"] = "12"

        print(data[i]['Book Title'] + "'s grade level:", data[i]["Grade Level"])

        #finds isbn
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/main/div/form/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div[1]').click()
        driver.implicitly_wait(3)
        isbn = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/main/div/div/div/div[1]/div[1]/div[1]/div[2]/div[3]/div/span').text
        data[i]["isbn"] = isbn.replace("ISBN: ", "")
        print(data[i]['Book Title'] + "'s isbn:", isbn)

    #if failed to find on website, use the google books api to get top isbn result. reading_level will be N/A
    except:
        failed = True

    try:
        if failed:
            # Retrieves ISBN from Google's Book API
            title = json.dumps(data[i]['Book Title']).replace(" ", "+")
            title = title.replace("\\n", "")
            whitelist = set(string.ascii_lowercase + string.ascii_uppercase + string.digits + " " + "," + "+" + "'")
            title = ''.join(c for c in title if c in whitelist)
            #print(title)
            query = str("https://www.googleapis.com/books/v1/volumes?q=intitle:" + title)
            #print(query)
            resp = urlopen(query)
            book_data = json.load(resp)
            #print(book_data)
            isbn = book_data["items"][0]["volumeInfo"]["industryIdentifiers"][0]["identifier"]  # Change the [0] to [1] if want ISBN_10 instead
            data[i]["Lexile Measure"] = "N/A"
            print(data[i]['Book Title'] + "'s Lexile measure: ", data[i]["Lexile Measure"])
            data[i]["Grade Level"] = "N/A"
            print(data[i]['Book Title'] + "'s grade level:", data[i]["Grade Level"])
            data[i]["isbn"] = isbn.replace("ISBN: ", "")
            print(data[i]['Book Title'] + "'s isbn:", isbn)

    except:
        data[i]["Lexile Measure"] = "N/A"
        data[i]["Grade Level"] = "N/A"
        data[i]["isbn"] = "N/A"
        print(data[i]['Book Title'] + "'s Lexile measure: ", data[i]["Lexile Measure"])
        print(data[i]['Book Title'] + "'s grade level:", data[i]["Grade Level"])
        print(data[i]['Book Title'] + "'s isbn:", "N/A")

    with open('new_inventory.json', 'w') as f:
        json.dump(data, f, indent=2)

driver.quit() # exits



