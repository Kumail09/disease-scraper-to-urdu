from symtable import symtable
from bs4 import BeautifulSoup as bs
import requests
import mysql.connector
from translate import Translator
#translator instance - Language: Auto Detect to Urdu 
translator= Translator(to_lang="ur-PK", email="")


# MySql Data base Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="diseases"
)
mycursor = mydb.cursor()



def createTable():
    mycursor.execute("""CREATE TABLE IF NOT EXISTS `diseases` (
            id INT AUTO_INCREMENT PRIMARY KEY,
            `title` VARCHAR(512),
            `symptoms` VARCHAR(1024),
            `causes` VARCHAR(1024),
            `riskFactors` VARCHAR(1024),
            `prevention` VARCHAR(1024),
            `url` VARCHAR(256)
            );""")



"""
Function To Scrape Data from given url. 
Use https://www.mayoclinic.org/ for best Results

:params: string <str>
:returns: translated string <str> 
"""

def translateString(string):
    return translator.translate(string)


"""
Function To Scrape Data from given url. 
Use https://www.mayoclinic.org/ for best Results
:params: url
:returns: None

"""
def scrapeData(url):
    response = requests.get(url)
    if response:
        content = response.content
        soup = bs(content, 'html.parser')  
        try:
            title = soup.find('title').text
        except:
            title = ''
        try:
            symptoms = soup.find("h2", string="Symptoms").nextSibling.text
        except Exception as E:
            symptoms = ''
        try:
            causes = soup.find("h2", string="Causes").nextSibling.text
        except Exception as E:
            causes = ''
        try:
            risk_factors = soup.find("h2", string="Risk factors").nextSibling.text
        except Exception as E:
            risk_factors = ''
        try:
            prevention = soup.find("h2", string="Prevention").nextSibling.text
        except Exception as E:
            prevention = ''

        sql = """INSERT INTO diseases (title, symptoms, causes, riskFactors, prevention, url) 
        VALUES (%s, %s, %s, %s, %s, %s)"""
        
        val = (translateString(title), translateString(symptoms), 
                translateString(causes), 
                translateString(risk_factors), 
                translateString(prevention),
                url)
        mycursor.execute(sql, val)
        print("Scraped: ", url)



"""
Main Function containing the driver code
:params: None
:returns: None
"""
def main():
    #List of Urls 
    urls = ["https://www.mayoclinic.org/diseases-conditions/back-pain/symptoms-causes/syc-20369906", 
    "https://www.mayoclinic.org/diseases-conditions/galactorrhea/symptoms-causes/syc-20350431"
    ]

    #Create Table and Cols in DB
    createTable()

    #Parse Urls
    for url in urls:
        scrapeData(url)    

    #No changes will be made to database until mydb.commit() is called
    mydb.commit()


main()