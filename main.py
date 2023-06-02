# import scrips 
import subprocess
# import Scraping,Cleaning,Exploratory_data_analysis, Sementic_analysis_for_ job_description

def main(): 
    #- Scrapping Data 
    subprocess.run(['python','Scraping.py'])

    # Cleaning Data 
    subprocess.run(['python','Cleaning.py'])

    # Exploratory Data Analysis 
    subprocess.run(['python','Exploratory_data_analysis.py'])
    
    # Sementic Analysis of job description 
    subprocess.run(['python','Semantic_analysis_for_ job_description.py'])
if __name__ == '__main__':
    main()

