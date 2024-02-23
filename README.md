# Paste_Scraper

## SCHEMA
### Dictionary: 
Contains a unique ID for each word and the word itself.
### Words: 
Links words to URLs (though the actual URL is not stored in this table) and counts their usage.
### ScrapedContent: 
Stores the content scraped from web pages, including the content itself, the date and time it was scraped, the URL from where it was scraped, and references to two words from the Dictionary table.
### AnalysisResults: 
Holds the results of analyzing the scraped content, including three keywords extracted from the content, an optional alert field, and the date and time of the analysis. It references the ScrapedContent table via ContentID.

# Things to do:

-Re-do Db creation, containing also all the Dictionary;

-Query and extract;

-randomly take two words and put in the query;

-Write on the db what is found;

-Statistics;

-Chatgpt stuff.
