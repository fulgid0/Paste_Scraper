#!/usr/bin/python

import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('Paste_Scraper.db')
print("Opened database successfully")

# Create Dictionary table
conn.execute('''CREATE TABLE Dictionary (
        WordID INTEGER PRIMARY KEY AUTOINCREMENT,
        Word TEXT NOT NULL
);''')

# Create Words table
conn.execute('''CREATE TABLE Words (
        LootID INTEGER PRIMARY KEY AUTOINCREMENT,
        Word_urlID INTEGER NOT NULL,
        FOREIGN KEY (Word_urlID) REFERENCES Dictionary(WordID),
        UsageCount INTEGER DEFAULT 0
);''')

# Create ScrapedContent table
conn.execute('''CREATE TABLE ScrapedContent (
        ContentID INTEGER PRIMARY KEY AUTOINCREMENT,
        Word1ID INTEGER NOT NULL,
        Word2ID INTEGER NOT NULL,
        ScrapedText TEXT NOT NULL,
        ScrapedDateTime TEXT NOT NULL,
        URL TEXT NOT NULL,
        FOREIGN KEY (Word1ID) REFERENCES Dictionary(WordID),
        FOREIGN KEY (Word2ID) REFERENCES Dictionary(WordID)
);''')

# Create AnalysisResults table
conn.execute('''CREATE TABLE AnalysisResults (
        AnalysisID INTEGER PRIMARY KEY AUTOINCREMENT,
        ContentID INTEGER NOT NULL,
        Keyword1 TEXT NOT NULL,
        Keyword2 TEXT NOT NULL,
        Keyword3 TEXT NOT NULL,
        Alert TEXT DEFAULT NULL,
        AnalysisDateTime TEXT NOT NULL,
        FOREIGN KEY (ContentID) REFERENCES ScrapedContent(ContentID)
);''')

print("Tables created successfully")

# Close the connection to the database
conn.close()
