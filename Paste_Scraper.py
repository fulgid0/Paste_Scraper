#!/usr/bin/python

import os,sys
import sqlite3, time, re
import subprocess
import random
import requests 



'''


def Scansione(conn):
 cursor = conn.execute("SELECT Subdomain, Number FROM Anagrafica")
 cursor.fetchone()
 for row in cursor:
  if "receive-smss.com" in row:
   Scan_Receive_sms(conn,row[1].split("+")[1])
  if "smstome.com" in row:
   Scan_Smstome_sms(conn,row[1]) #### CONTROLLARE PERCHE SOLO UN GIRO
 
def DB_Ana(conn, Subdomain, Number, Alive, Nation):
 cursor = conn.execute("SELECT * FROM Anagrafica WHERE Number= '" + Number + "' AND Nation= '" +Nation+"'")
 row = cursor.fetchone()
 if row is None:
  query1= "INSERT INTO Anagrafica (Subdomain, Number, Alive, Nation) VALUES ('"+Subdomain+"', '"+Number+"',  '"+Alive+"', '"+Nation+"')"
  cursor = conn.execute(query1)
  conn.commit()
  print ("New finding: " + Number + " [" + Nation + "] - Records created successfully");

def Ana_Receive_smss():
 print ("ANAGRAFICA Receive-smss.com");
 conn = sqlite3.connect('SMS_DB.db')
 sup_file= 'receive-smss'
 os.system("wget -O " + sup_file + " " + 'https://receive-smss.com/')
 subdomain = "receive-smss.com"
 flag = 0
 with open(sup_file) as file:
  for line in file:
   if '<div class="number-boxes-itemm-number" style="color:black">' in line:
    number = line.split('<div class="number-boxes-itemm-number" style="color:black">')[1].split('</div>')[0]
    flag = flag+1
   if '<div class="number-boxes-item-country number-boxess-item-country">' in line:
    nation = line.split('<div class="number-boxes-item-country number-boxess-item-country">')[1].split('</div>')[0]  
    flag = flag+1
   if flag > 1:
    alive = "none"
    DB_Ana(conn, subdomain, number, alive, nation)
    flag = 0
    number = "NULL"
    nation = "NULL"
 os.system("rm "+sup_file)
 Scansione(conn)
 conn.close()

def Ana_SMStome():
 print ("ANAGRAFICA smstome.com");
 conn = sqlite3.connect('SMS_DB.db')
 sup_file= 'SMStome'
 os.system("wget -O " + sup_file + " " + 'https://smstome.com/')
 subdomain = "smstome.com"
 flag = 0
 flag2 = 0
 with open(sup_file) as file:
  for line in file:
   if '                            <a href="' in line and '/country/' in line:
    sup_2 = line.split('                            <a href="')[1].split('" class="button button-clear">')[0]
    nation = sup_2.split('/country/')[1].split('/')[0]
    flag = flag+1
   if flag > 1:
    flag = 0
    sup_file2 = "SMStome_"+nation
    os.system("wget -O " + sup_file2 + " " + 'https://smstome.com'+sup_2+"?page="+str(randint(1, 30)))
    with open(sup_file2) as file:
     for line2 in file:
      if 'button button-outline button-small numbutton' in line2:
       number_link = line2.split('<a href="https://smstome.com')[1].split('" class=')[0]
       flag2 = flag2+1
      if flag2 > 1:
       alive = "none"
       DB_Ana(conn, subdomain, number_link, alive, nation)
       flag2 = 0    
    os.system("rm "+sup_file2)
 Scansione(conn)
 os.system("rm "+sup_file)
 conn.close()
 
while True: 
 Ana_Receive_smss()
 Ana_SMStome()
 print("---- Execution Hold ---- at time: ")
 str(os.system("date +%k:%M.%S")).strip()
 time.sleep(180) 
 
''' 
def Dictionary_pop(conn,word):
 flag=0
 query1= "INSERT INTO Dictionary (Word) VALUES ('"+word+"')"
 if "'" not in word:
  cursor = conn.execute("SELECT * FROM Dictionary WHERE Word= '" + word + "'")
  row = cursor.fetchone()
  if row is None:
   try:
    cursor = conn.execute(query1)
   except:
    flag=1
 return flag

def Paste_dictionary(filename=""):
 link ="https://raw.githubusercontent.com/sujithps/Dictionary/master/Oxford%20English%20Dictionary.txt"
 flag =0;
 sup_file="sup_file.txt"
 conn = sqlite3.connect('Paste_Scraper.db')
 if len(filename) < 1:
  os.system("wget -O sup_file.txt " + link)
 else:
  os.system("cp "+filename+" sup_file.txt")
 with open(sup_file) as file:
  for line in file:
   word=line.split(' ')[0].strip()
   if len(word) > 1:
    flag=Dictionary_pop(conn,word)
   if flag == 1:
    break
 os.system("rm "+sup_file);
 if flag ==0:
  print("dictionary acquisition complete")
  conn.commit() 
 else:
  print("issue in dictionary acquisition, trouble with the line: ["+word+"]")
  conn.rollback() 
 conn.close()

def get_two_random_words():
    # Connect to the SQLite database
    conn = sqlite3.connect('Paste_Scraper.db')
    cursor = conn.cursor()
    # SQL query to select two random words from the Dictionary table
    query = '''SELECT Word FROM Dictionary ORDER BY RANDOM() LIMIT 2;'''    
    try:
        cursor.execute(query)
        words = cursor.fetchall()  # Fetches the two random words
        if words:
            return [word[0] for word in words]  # Return the words as a list of strings
        else:
            return []  # Return an empty list if no words are found
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return []  # Return an empty list in case of an error
    finally:
        conn.close()  # Ensure the database connection is closed

def check_and_fetch_content(random_words):
    base_url = "https://paste.c-net.org/"
    
    # Generate URLs for both word orders
    urls = [f"{base_url}{random_words[0]}{random_words[1]}", f"{base_url}{random_words[1]}{random_words[0]}"]
    flag=0
    for url in urls:
        flag= flag+1
        # Perform a HEAD request to check if the page exists
        head_response = requests.head(url)
        print(url)
        
        # If the page exists (HTTP status code 200)
        if head_response.status_code == 200:
            # Perform a GET request to fetch the page's content
            get_response = requests.get(url)
            # Return the content if the page was successfully fetched
            if get_response.status_code == 200:
               content=get_response.text
               if len(content) >200:
                content="10TOO_LONG!01"
               if flag == 1:
                insert_scraped_content_and_words(random_words[0], random_words[1], content, url.split('//')[1].strip())
               else:
                insert_scraped_content_and_words(random_words[1], random_words[0], content, url.split('//')[1].strip())
               return content
    # Return None if neither URL points to a valid page
    return None

    # Function to insert or find a word in the Dictionary and return its WordID
def get_or_insert_word_id(word,cursor):
 cursor.execute("SELECT WordID FROM Dictionary WHERE Word = ?", (word,))
 result = cursor.fetchone()
 if result:
  return result[0]
'''        else:
            cursor.execute("INSERT INTO Dictionary (Word) VALUES (?)", (word,))
            return cursor.lastrowid
'''    

def insert_scraped_content_and_words(word1, word2, content, url):
    conn = sqlite3.connect("Paste_Scraper.db")
    cursor = conn.cursor()
    

    try:
        # Get or insert words and retrieve their IDs
        word1_id = str(get_or_insert_word_id(word1,cursor))
        word2_id = str(get_or_insert_word_id(word2,cursor))
        
        # Insert into ScrapedContent table
        query="INSERT INTO ScrapedContent (Word1ID, Word2ID, ScrapedText, ScrapedDateTime, URL) VALUES ("+word1_id+", "+word2_id+", '"+content+"', datetime('now'), '"+url+"')" 
        print("printo: "+query)
        cursor.execute(query)

        #################LA TABELLA WORD!!!!!!
        # Insert into Words table if not exists; this assumes you want to track each word's usage in URLs
        # This is a simple implementation and might need adjustment based on your actual requirements
#       for word_id in [word1_id, word2_id]:
#            query2= "INSERT OR REPLACE INTO Words (Word_urlID, UsageCount) VALUES ("+word_id+", 1) ON CONFLICT(Word_urlID) DO UPDATE SET UsageCount = UsageCount + 1"
#            print ("questo invece: "+query2)
#            cursor.execute(query2)
        conn.commit()
        print("Database updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# Assuming you have fetched content using the previous function
# content = check_and_fetch_content("ExampleWord1", "ExampleWord2")
# if content:
#     insert_scraped_content_and_words("ExampleWord1", "ExampleWord2", content)



if len(sys.argv) > 1:
 Paste_dictionary(sys.argv[1])
else:
 Paste_dictionary()
# Example usage random words
while True:
 random_words = get_two_random_words()
 print(random_words)
 # Example usage with two sample words
 content = check_and_fetch_content(random_words)
 if content:
  print("Content fetched successfully.")
  print(content)
 else:
  print("No valid page found for the given word combinations.")

