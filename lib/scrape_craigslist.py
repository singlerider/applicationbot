#! /usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup # For HTML parsing
from lib.helpers import *
import urllib2 # Website connections
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots
import random


def text_cleaner(website):
    '''
    This function just cleans up the raw html so that I can look at it.
    Inputs: a URL to investigate
    Outputs: Cleaned text only
    '''
    try:
        site = urllib2.urlopen(website).read() # Connect to the job posting
    except:
        return   # Need this in case the website isn't there anymore or some other weird connection problem
    soup_obj = BeautifulSoup(site).findAll(id='postingbody') # Get the html from the site
    #print soup_obj
    text = soup_obj[0].get_text()
    #print text
    lines = (line.strip() for line in text.splitlines()) # break into lines
    chunks = (phrase.strip() for line in lines for phrase in line.split("  ")) # break multi-headlines into a line each
    def chunk_space(chunk):
        chunk_out = chunk + ' ' # Need to fix spacing issue
        return chunk_out
    text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
    # Now clean out all of the unicode junk (this line works great!!!)
    try:
        text = text.decode('unicode_escape').encode('ascii', 'ignore') # Need this as some websites aren't formatted
    except:                                                            # in a way that this works, can occasionally throw
        return                                                         # an exception
    text = re.sub("[^a-zA-Z.+3]"," ", text)  # Now get rid of any terms that aren't words (include 3 for d3.js)
                                                # Also include + for C++
    text = text.lower().split()  # Go to lower case and split them apart
    stop_words = set(stopwords.words("english")) # Filter out any stop words
    text = [w for w in text if not w in stop_words]
    text = list(set(text)) # Last, just get the set of these. Ignore counts (we are just looking at whether a term existed
                            # or not on the website)
    return text


def scrape_and_apply(data):
    '''
    TODO: UPDATE DESCRIPTION
    '''

    final_job = data["title"]
    final_job = final_job.replace(" ", "+") # searching for data scientist exact fit("data scientist" on Craigslist search)
    final_site_list = ["https://sfbay.craigslist.org/search/jjj", "?query=", final_job]
    final_site = ''.join(final_site_list) # Merge the html address together into one string
    base_url = 'https://sfbay.craigslist.org'
    try:
        html = urllib2.urlopen(final_site).read() # Open up the front page of our search first
    except Exception as error:
        print error # In case the city is invalid
        return
    soup = BeautifulSoup(html) # Get the html from the first page
    # Now find out how many jobs there were
    total_num_jobs = int(soup.find(class_= "totalcount").string.encode('utf-8'))
    # Now extract the total number of jobs found - The 'totalcount' object has this
    #print "num_jobs_area", num_jobs_area
    print "There were {} jobs found".format(total_num_jobs)
    # Display how many jobs were found
    num_pages = (total_num_jobs/100) + 1# This will be how we know the number of times we need to iterate over each new
                                      # search result page
    job_listings = [] # Store all our descriptions in this list
    job_descriptions = {}
    for i in xrange(1,num_pages + 1): # Loop through all of our search result pages
        print "Getting page {} out of {} pages".format(i, num_pages)
        start_num = (i*100) - 100 # Assign the multiplier of 100 to view the pages we want
        current_page = 'https://sfbay.craigslist.org/search/jjj?s={}&query={}'.format(start_num, final_job)
        print "i:", i, "current_page:", current_page, "range:", range(1,num_pages + 1)
        print "num_pages:", num_pages, "start_num:", start_num
        # Now that we can view the correct 100 job returns, start collecting the text samples from each
        try:
            html_page = urllib2.urlopen(current_page).read() # Get the page
            print current_page
        except:
            print "TIMEOUT FOR PAGE {}".format(i)
        page_obj = BeautifulSoup(html_page) # Locate all of the job links
        job_URLS = [base_url + link.get('href') for link in page_obj.findAll(class_='hdrlnk')]
        random.shuffle(job_URLS) # Make it appear like we are checking the jobs out of order
        descriptions = [desc for desc in soup.findAll(class_= "hdrlnk")]
        #print job_URLS
        print "Job URLs:", "{} on Page {}".format(len(job_URLS), i)
        for j in xrange(0,len(job_URLS)):
            description = descriptions[j].get_text()
            data["company"] = description
            if description in job_descriptions:
                continue # prevents scraping duplicate pages
            else:
                job_descriptions[description] = True # inserts job description as a key
            print description
            try:
                site = urllib2.urlopen(job_URLS[j]).read()
            except Exception as error:
                print error
                continue
            local_soup = BeautifulSoup(site)
            button_url = local_soup.find(class_ = "reply_button js-only")
            listing = text_cleaner(job_URLS[j])
            data["listing"] = listing
            if button_url is None:
                #button_url = "Reply Below"
                continue # Nothing to do without an available email yet
            else:
                page = job_URLS[j].split("/")[5].split(".")[0] # separates the url into what we need
                url = "https://sfbay.craigslist.org/reply/sfo/sof/{}".format(page)
                sleep(random.uniform(5.00, 10.00)) # Another request is being made here. Let's be nice about it
                email_soup = BeautifulSoup(urllib2.urlopen(url).read())
                email_address = email_soup.find(class_="anonemail")
                if email_address is not None:
                    email_address = email_address.get_text()
                    print email_address
                    # I will expand on the below variable's purpose later
                    message_text = build_message_text(data) # Generate a unique cover letter from information on the page
                    if "y" in data["initialize"][0]:
                        print "YES"
                        print send_email(data, email_address, description, message_text)
                    if "y" in data["initialize"][1] and "y" in data["initialize"][2]:
                        print "AND YES"
                        print bot.update_trello(data, message_text)
                    print "email_address:", email_address
                else:
                    print "No email address found"
            print "Page: {} | Listing {} complete".format(i, j + 1)
            job_listings.append(listing) #print final_description
            sleep(random.uniform(5.00, 10.00)) # So that we don't be jerks. If you have a very fast internet connection you could hit the server a lot!
    print 'Done with collecting the job postings!'
    print 'There were', len(job_listings), 'jobs successfully found.'
    print final_job
    doc_frequency = Counter() # This will create a full counter of our terms
    [doc_frequency.update(item) for item in job_listings] # List comp
    # Now we can just look at our final dict list inside doc_frequency
    # Obtain our key terms and store them in a dict. These are the key skills we are looking for
    lang_dict = Counter({
                    'R':doc_frequency['r'], 'Python':doc_frequency['python'],
                    'Java':doc_frequency['java'], 'C++':doc_frequency['c++'],
                    'Ruby':doc_frequency['ruby'], 'C': doc_frequency['c'],
                    'Perl':doc_frequency['perl'], 'Matlab':doc_frequency['matlab'],
                    'JavaScript':doc_frequency['javascript'], 'Scala': doc_frequency['scala'],
                    'PHP': doc_frequency['php'], 'HTML': doc_frequency['html'],
                    'CSS': doc_frequency['css'], 'Objective-C': doc_frequency['objective-c'],
                    'Go': doc_frequency['go']
                    })
    tool_dict = Counter({
                        'Excel':doc_frequency['excel'],  'Tableau':doc_frequency['tableau'],
                        'D3.js':doc_frequency['d3.js'], 'SAS':doc_frequency['sas'],
                        'SPSS':doc_frequency['spss'], 'D3':doc_frequency['d3'],
                        'Hadoop': doc_frequency['hadoop'], 'RabbitMQ': doc_frequency['rabbitmq']
                        })
    web_dict = Counter({
                'Backbone':doc_frequency['backbone'], 'Ember':doc_frequency['ember'],
                'React':doc_frequency['react'], 'Rails':doc_frequency['rails'],
                'Angular':doc_frequency['angular'], 'Node':doc_frequency['node']
                })
    database_dict = Counter({
                    'SQL':doc_frequency['sql'], 'NoSQL':doc_frequency['nosql'],
                    'HBase':doc_frequency['hbase'], 'Cassandra':doc_frequency['cassandra'],
                    'MongoDB':doc_frequency['mongodb'], 'MySQL': doc_frequency['mysql']
                    })
    overall_total_skills = lang_dict + tool_dict + web_dict + database_dict # Combine our Counter objects
    final_frame = pd.DataFrame(overall_total_skills.items(), columns = ['Term', 'NumPostings']) # Convert these terms to a
                                                                                                # dataframe
    # Change the values to reflect a percentage of the postings
    final_frame.NumPostings = (final_frame.NumPostings)*100/len(job_listings) # Gives percentage of job postings
                                                                                    #  having that term
    # Sort the data for plotting purposes
    final_frame.sort_values(by= 'NumPostings', ascending = False, inplace = True)
    return final_frame # End of the function

if __name__ == "__main__":
    data = {}
    scrape_and_apply(data)
