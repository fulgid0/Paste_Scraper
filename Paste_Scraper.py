#!/usr/bin/python

import os,sys
import sqlite3, time, re
import subprocess
import random
import requests
import time
import multiprocessing
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
MAX_SUB_PROCESSES = 15
COUNTER_DOUBLE_F = 0
TIMEOUT = 60

def escaping(var_str):
 escaped = var_str.translate(str.maketrans({"-":  r"\-",
                                          "]":  r"\]",
                                          "\\": r"\\",
                                          "^":  r"\^",
                                          "$":  r"\$",
                                          "*":  r"\*",
                                          "'":  r"''",
                                          "@":  r"\@",
                                          "\x00":  r"",
                                          ".":  r"\."}))
 return escaped
 

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

def check_and_fetch_content(random_words, COUNTER_DOUBLE_F):
    base_url = "https://paste.c-net.org/"
    user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
    message_neg="There's no such file here :("
    # Generate URLs for both word orders
    urls = [f"{base_url}{random_words[0]}{random_words[1]}", f"{base_url}{random_words[1]}{random_words[0]}"]
    flag=0
    flag1=0
    double_fail=0
    for url in urls:
     flag= flag+1
     headers = {'User-Agent': random.choice(user_agents)}
     # Perform a HEAD request to check if the page exists
     retry_strategy = Retry(total=3,    backoff_factor=1)
     adapter = HTTPAdapter(max_retries=retry_strategy)
     http = requests.Session()
     http.mount("https://", adapter)
     try:
      #response = http.get(url,headers=headers)
      #response = os.system("wget -q "+url)
      #response_string = response.text
      stringa= "curl "+url
      print(stringa)
      #response_string = os.open(stringa).read()#subprocess.check_output(stringa, shell=True)
      #proc = subprocess.Popen([stringa], stdout=subprocess.PIPE)
      #(response_string, err) = proc.communicate()
      p = subprocess.Popen(["curl", url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      response_string = str(p.stdout.read()).split('"')[1]
      #print(response_string)
     except:
      response_string = message_neg
      double_fail=double_fail+1
      #os.system("service tor reload"); print("\n")
      print("entering in sleeping after failure")
      time.sleep(2)
      print("Awakening")
      flag1=1
         #head_response = requests.head(url)
        # If the page exists (HTTP status code 200)
     if message_neg not in response_string and flag1==0:
            # Perform a GET request to fetch the page's content
            #get_response = requests.get(url)
            # Return the content if the page was successfully fetched
            #if get_response.status_code == 200:
               #content=escaping(str(response.text))
               content=escaping(response_string)
               print(content)
               if len(content) >200:
                content="10TOO_LONG!01"
               if flag == 1:
                insert_scraped_content_and_words(random_words[0], random_words[1], content, url.split('//')[1].strip())
               else:
                insert_scraped_content_and_words(random_words[1], random_words[0], content, url.split('//')[1].strip())
               return content
    if double_fail > 1:
               print("double FAIL")
               COUNTER_DOUBLE_F = COUNTER_DOUBLE_F +1
    # Return None if neither URL points to a valid page
    return None

    # Function to insert or find a word in the Dictionary and return its WordID
def get_or_insert_word_id(word,cursor):
 cursor.execute("SELECT WordID, UsageCount FROM Dictionary WHERE Word = ?", (word,))
 result = cursor.fetchall()
 return result[0]
  

def insert_scraped_content_and_words(word1, word2, content, url):
   conn = sqlite3.connect("Paste_Scraper.db")
   cursor = conn.cursor()
   query= "SELECT COUNT(URL) FROM ScrapedContent WHERE URL = '"+url+"';"
   cursor.execute(query)
   flag= cursor.fetchone() 
   if flag[0] ==0:
    try:
        # Get or insert words and retrieve their IDs
        
        word1_Array = get_or_insert_word_id(word1,cursor)
        word2_Array = get_or_insert_word_id(word2,cursor)

        # Insert into ScrapedContent table
        query="INSERT INTO ScrapedContent (Word1ID, Word2ID, ScrapedText, ScrapedDateTime, URL) VALUES ("+str(word1_Array[0])+", "+str(word2_Array[0])+", '"+content+"', datetime('now'), '"+url+"')" 
        print("printo: "+query)
        cursor.execute(query)
        queryw1="UPDATE Dictionary SET UsageCount  = "+str(word1_Array[1]+1)+" WHERE WordID= "+str(word1_Array[0])+";"
        queryw2="UPDATE Dictionary SET UsageCount  = "+str(word2_Array[1]+1)+" WHERE WordID= "+str(word2_Array[0])+";"
        cursor.execute(queryw1)
        cursor.execute(queryw2)        
        conn.commit()
        print("Database updated successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
   else:
     print("Url already present in the DB: consider to extend the dictionary")

def MultiProc():
 random_words = get_two_random_words()
 print(random_words)
 # Example usage with two sample words
 content = check_and_fetch_content(random_words,COUNTER_DOUBLE_F)
 if content:
  print("Content fetched successfully.")
  print(content)
 else:
  print("No valid page found for the given word combinations.")
 str(os.system("date +%k:%M.%S")).strip()


if len(sys.argv) > 1:
 Paste_dictionary(sys.argv[1])
else:
 Paste_dictionary()
# Example usage random words
while True:
    results = []
    COUNTER_DOUBLE_F = 0
    running_processes = []
    index = 0
    procs = []
    start = time.time()
    for index in range(1, MAX_SUB_PROCESSES+1):
      p = multiprocessing.Process(target=MultiProc)
      procs.append(p)
      p.start()
    while time.time() - start <= TIMEOUT:
      time.sleep(0.5) #just to don't stress the CPU too much
      if not any(p.is_alive() for p in procs):
       # All the processes are done, break now.
       break
     # else:
       # We only enter this if we didn't 'break' above.
    print("timed out, killing all processes")
      # print(time.time() -  start)
    for p in procs:
     p.terminate()
     p.join()
    print(str(MAX_SUB_PROCESSES)+" Processes closed")
    print(str(COUNTER_DOUBLE_F)+" Double fails!")
