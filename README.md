DCF_SCRAPER

Built a webscraper using pandas and Beautiful Soup to collect site name and postcodes for UK Designated Collection Facilities (for e-waste). Scraper filters unusuable data before geocoding postcodes using a public access API. Site name, long/lat coordinates are saved to csv.
The app.py file requires FLASK to run. The map visualises all the sites collected in the csv using Folium
The DCF_Sites CSV is prepopulated with data collected from the Designated Collection Facilities (DCF) directory webpages.
