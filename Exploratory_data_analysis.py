# import libraries 
import os
import pandas as pd 

from helper import count_plot

def main():
        
    # Create diractory for graphs
    dir = os.path.join(os.getcwd(),'graphs')
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Reading the CSV file into a pandas DataFrame
    df = pd.read_csv('data\\cleaned_data.csv',index_col=0)
    print(df.head())
    print('------------------- Exploratory Data Analysis is just starting .... --------------------------')
    print('------------------DataFrame Infos:--------------------------------')
    print(df.info())

    print('-------------------- Q 1 - Which companies have the most job openings? ----------------------')
    count_plot(df,'company_name','Top 10 Companies by Job Openings')
    print('------------------------------ Done ------------------------------------------')

    print('-------------------- Q 2 - What are the top 10 state where the jobs are being offered? ----------------------')
    count_plot(df,'company_location','Top 10 Stats by Job Openings')
    print('------------------------------ Done ------------------------------------------')

    print('-------------------- Q 3 - Which seniority levels are in demand? ----------------------')
    count_plot(df,'experience','Distribution of Job Openings by Seniority Level', orient = 'v')
    print('------------------------------ Done ------------------------------------------')

    print('-------------------- Q 4 - Which industries have the highest number of job openings? ----------------------')
    count_plot(df,'industry','Top 10 Industries by job Openings')
    print('------------------------------ Done ------------------------------------------')

    print('-------------------- Q 5 -  What is the distribution of employment types (full-time, part-time, contract, etc.)? ----------------------')
    count_plot(df,'job_type','Employment type Distribution of job Openings',orient='v')
    print('------------------------------ Done ------------------------------------------')

    print('-------------------- Q 6 -  What is the distribution of workplace type (Remote, On-site )? ----------------------')
    count_plot(df,'workplace_type','Employment type Distribution of job Openings',orient= 'v')
    print('------------------------------ Done ------------------------------------------')

    print('-------------------- Q 7 -  What is the distribution of company size of job Openings  (small, medium, large )? ----------------------')
    count_plot(df,'company_size','Company size Distribution of job Openings',orient='v')
    print('------------------------------ Done ------------------------------------------')
    
if __name__ == '__main__':
    main()