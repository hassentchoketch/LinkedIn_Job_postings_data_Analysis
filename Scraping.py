# import libraries  
import os
import time 

from selenium import webdriver
from helper import linkedinScrapper

def main():
    
    # Create diractory for data
    dir = os.path.join(os.getcwd(),'data')
    if not os.path.exists(dir):
        os.makedirs(dir)
        
    print('-------- Scraping Linkedin job data is just starting .... ----------')
    # Driver path
    path = 'chromedriver.exe'
    driver = webdriver.Chrome(path)  

    # Maximize Window
    driver.maximize_window() 
    driver.switch_to.window(driver.current_window_handle)
    driver.implicitly_wait(5)

    print('---------------  Entering to the site and login ---------------------')
    # Enter to the site and login 
    driver.get('https://www.linkedin.com/login')
    time.sleep(2)
    scraper = linkedinScrapper(driver)
    scraper.login()
    print(' -------------------------- Done -------------------------------------')

    print('-----------  Searching for a jobs in specific country ----------------')
    # Search for job in specific country
    job_name = 'data Science' 
    location = 'Germany'
    job_keywords = job_name.replace(' ','%20')
    linke = f'https://www.linkedin.com/jobs/search/?currentJobId=3601247028&geoId=101282230&keywords={job_keywords}&location={location}&refresh=true'
    time.sleep(10)
    print(' -------------------------- Done -------------------------------------')

    print('------------  Geting the link of each job page  ----------------------')
    # Extract the link of each job page from job listing pages
    links = scraper.listing_jobs_scrapper(linke,10)
    print(' -------------------------- Done -------------------------------------')

    print('------------  Geting the job details from each job page --------------')
    # Extract the job details from each job page
    scraper.job_pages_scrapper(links)
    print(' -------------------------- Done -------------------------------------')
    
    
if __name__ == '__main__':
    main()  