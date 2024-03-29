# Paste_Scraper

The aim is scrap for file stored on one of pastebin-like services, and save the finding on the DB. 
Shortly also chatGPT funtionality will be implemented in order to automatically describe the finding and alert on any sensible information found (like emails, credentials, api kyes...)

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

# Installation

To install and use the Paste_Scraper, you'll first need to clone the repository to your local machine. Ensure you have Git installed before you begin..

Follow these steps to clone and start using Paste_Scraper:

1. **Clone the repository**

Open your terminal or command prompt and execute the following command:

>git clone https://github.com/fulgid0/Paste_Scraper.git

This command downloads a copy of the Paste_Scraper project to your local machine.

2. **Navigate to the project directory**

Change into the Paste_Scraper project directory with:

>cd Paste_Scraper


# Things to do on the main script:
- [x] Re-do Db creation, containing also all the Dictionary;
- [x] Query and extract;
- [x] randomly take two words and put in the query;
- [x] Track back on the db what is found;
- [x] Statistics;
- [x] Multi HTTP agent support;
- [x] Bad character management escape;
- [x] Better error handeler in case of connection holds (desynchronization);
- [x] Documentation - Requirements (under testing) & github clone;
- [x] MultiProcessing;
- [x] Escaping in case of process stuck (60s timeout)
- [ ] Comment the code, and that's all 🎉
- [ ] (extras) on-board Proxing capabilities;
- [ ] (extras) Add some prompt during the waiting, just to remark that is alive and doing stuff❔

# Things to do on the ChatGPT script:
- [ ] API KEY via file or cli;
- [ ] Extraction of targets links from the DB;
- [ ] Query preparation;
- [ ] Write back on db;
- [ ] Signaling feature?
- [ ] Comment the code, and that's all 🎉
