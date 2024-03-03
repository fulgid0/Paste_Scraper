# Paste_Scraper

## SCHEMA
### Dictionary: 
Contains all words collected by default repository, or (if provided via CLI) specific dictionary file. It tracks also success occurences for statics reasons (via 'UsageCount' field).
### ScrapedContent: 
Stores the content scraped from web pages, including the content itself, the date and time it was scraped, the URL from where it was scraped, and references to two words from the Dictionary table (via foreign key).
### AnalysisResults: 
This is the table populated after chatgpt interraction.
Holds the results of analyzed the scraped content, including three keywords extracted from the content, an optional alert field (a list of sensible info found) and the date and time of the analysis. It references the ScrapedContent table via ContentID (foreign key).

## Details on schema fields
### Dictionary Table
* WordID: INTEGER PRIMARY KEY AUTOINCREMENT
* Word: TEXT NOT NULL
* UsageCount: INTEGER DEFAULT 0

### ScrapedContent Table
* ContentID: INTEGER PRIMARY KEY AUTOINCREMENT
* Word1ID: INTEGER NOT NULL (Foreign Key references Dictionary(WordID))
* Word2ID: INTEGER NOT NULL (Foreign Key references Dictionary(WordID))
* ScrapedText: TEXT NOT NULL
* ScrapedDateTime: TEXT NOT NULL
* URL: TEXT NOT NULL

### AnalysisResults Table
* AnalysisID: INTEGER PRIMARY KEY AUTOINCREMENT
* ContentID: INTEGER NOT NULL (Foreign Key references ScrapedContent(ContentID))
* Keyword1: TEXT NOT NULL
* Keyword2: TEXT NOT NULL
* Keyword3: TEXT NOT NULL
* Alert: TEXT DEFAULT NULL
* AnalysisDateTime: TEXT NOT NULL

# Things to do on the main script:
- [x] Re-do Db creation, containing also all the Dictionary;
- [x] Query and extract;
- [x] randomly take two words and put in the query;
- [x] Track back on the db what is found;
- [x] Statistics;
- [ ] Comment the code, and that's all 🎉

# Things to do on the ChatGPT script:
- [ ] API KEY via file or cli;
- [ ] Extraction of targets links from the DB;
- [ ] Query preparation;
- [ ] Write back on db;
- [ ] Signaling feature?
- [ ] Comment the code, and that's all 🎉
