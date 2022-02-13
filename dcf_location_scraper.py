import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv
import json
from pprint import pprint as pp
import re



#function scrapes website for DCF site name and postode
def dcf_scraper(input):
    dcf_dict = {}
    site_list = []
    postcode_list = []
    
    #url formatted to accept different letters in alphabet (directory is a-z) for scraping
    url = f"http://dcflist.valpak.co.uk/?search={input}"
    
    #test connection is valid
    try:
        res = requests.get(url)
        print("URL is valid")
    
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("URL is not valid", exception)
        return 0
    
    #scrape the site name and site postcode into separate lists
    else:
        soup = BeautifulSoup(res.content, 'lxml')
        tables = soup.find_all('table')
        

        for i in range(len(tables)):
            df = pd.read_html(str(tables))[i]
            site_name = (df["Site Name"]).tolist()
            site_list.append(site_name)
    
            post_code = (df["Postcode"]).tolist()
            postcode_list.append(post_code)
    
            i+= 1
        
        #if no data is scraped into list, the function returns False   
        if len(site_list) == 0 or len(postcode_list) == 0:
            print("No results")
            return 0
        
        #if data has been scraped into a list, the lists are flattened due to nested site addresses on the website
        else:
            
            return dcf_scraper_clean(site_list, postcode_list)


def dcf_scraper_clean(sites, postcodes):
    
    flat_site_list = [x for l in sites for x in l]
            
    uc_flat_postcode_list = [y for l in postcodes for y in l]
        
    c_flat_postcode_list = []

    #the input is validated - any special characters are removed and appended to a new list
    for post_code in uc_flat_postcode_list:
        c_post_code = re.sub(r"[^a-zA-Z0-9]","",post_code)
        c_flat_postcode_list.append(c_post_code)

    #the clean data is put into a dictionary
    dcf_dict = {flat_site_list[i]: c_flat_postcode_list[i] for i in range(len(flat_site_list))}

    #if it is not a full postcode (6 characters), then the site is removed from the dictionary because the api
    #requires a full postcode in order to retrieve location coordinates
    remove_list = [k for k in dcf_dict if (len(dcf_dict[k]) < 6)]

    for k in remove_list: 
        del dcf_dict[k]

    #number of valid data entries scraped 
    print(f"DCF sites scraped: {len(dcf_dict)}")
        
    #the dcf site dictionary (site name: site postcode) is input into the api request function
    return postcode_api_request(dcf_dict)


#function makes an api request and retrieves the latitude and longitude using the postcode from the dcf dictionary values.
def postcode_api_request(dictionary):
    site_geodict = {}
    site_info = {}
    list = []
    
    try:
    
        for site, postcode in dictionary.items():
            endpoint = f"http://api.getthedata.com/postcode/{postcode}"
            response = requests.get(endpoint)
            status = response.status_code
        
            #if the response is valid, then data is loaded
            if status == 200:
                data = json.loads(response.text)
            
                #if the query has a match for the postcode, then it is iterated over to retrieve coordinates
                if data['status'] == 'match':
                    c_data = data['data']
                    latitude, longitude = c_data['latitude'], c_data['longitude']
                    #a new list for all sites for which location coordinates have been retrieved
                    list.append([site, postcode, latitude, longitude])
                
                else:
                    #if a site does not have location coordinates avaiable, the site name is changed to 'Error'
                    dictionary[site] = "Error"
        
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Request is not valid", exception)
        pass
        
      
    else:
        #if a site request does not have a response, then the dictionary site name is changed to 'Error
        dictionary[site] = "Error"
        
    
    #if no location coordinates can be retrieved from postcode, function returns 0
    #any valid data is input to csv writing function
    if len(list) > 0:
        return dcf_data_csv(list)
    else:
        return len(list)
    

#list of sites [sitename, postcode, latitude, longitude] per row is written to a csv

def dcf_data_csv(dataset):
    
    fields =['place_name', 'postcode', 'latitude', 'longitude']
    
    #write the list to file
    with open("dcf_sites.csv", "a") as f:
        writer = csv.writer(f)
        # writer.writerow(fields)
        writer.writerows(dataset)

    print(f"DCF location coordinates retrieved: {len(dataset)}")
    
    return len(dataset)



if __name__ == '__main__':
    
    list1 = ['7']
    list2 = ['7', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'Y']

    for letter in list1:
        dcf_scraper(letter)
