# Paste_Scraper

## SCHEMA
### Dictionary: 
Contains all words collected by default repository, or (if provided via CLI) specific dictionary file.
### Words: 
Words resulted in a valid link, also counting the occurance. The idea is to use this value for statistics, making further scrapping smarter [TO DEVELOP]. The world is not directly stored in this table, but we use the foreign key of Dictionary table.
### ScrapedContent: 
Stores the content scraped from web pages, including the content itself, the date and time it was scraped, the URL from where it was scraped, and references to two words from the Dictionary table (via foreign key).
### AnalysisResults: 
This is the table populated after chatgpt interraction.
Holds the results of analyzing the scraped content, including three keywords extracted from the content, an optional alert field (a list of sensible info found) and the date and time of the analysis. It references the ScrapedContent table via ContentID (foreign key).

## Details on schema fields
### Dictionary Table
WordID: INTEGER PRIMARY KEY AUTOINCREMENT
Word: TEXT NOT NULL

### Words Table
LootID: INTEGER PRIMARY KEY AUTOINCREMENT
Word_urlID: INTEGER NOT NULL (Foreign Key references Dictionary(WordID))
UsageCount: INTEGER DEFAULT 0

### ScrapedContent Table
ContentID: INTEGER PRIMARY KEY AUTOINCREMENT
Word1ID: INTEGER NOT NULL (Foreign Key references Dictionary(WordID))
Word2ID: INTEGER NOT NULL (Foreign Key references Dictionary(WordID))
ScrapedText: TEXT NOT NULL
ScrapedDateTime: TEXT NOT NULL
URL: TEXT NOT NULL

### AnalysisResults Table
AnalysisID: INTEGER PRIMARY KEY AUTOINCREMENT
ContentID: INTEGER NOT NULL (Foreign Key references ScrapedContent(ContentID))
Keyword1: TEXT NOT NULL
Keyword2: TEXT NOT NULL
Keyword3: TEXT NOT NULL
Alert: TEXT DEFAULT NULL
AnalysisDateTime: TEXT NOT NULL

# Things to do:

-Re-do Db creation, containing also all the Dictionary;

-Query and extract;

-randomly take two words and put in the query;

-Write on the db what is found;

-Statistics;

-Chatgpt stuff.
