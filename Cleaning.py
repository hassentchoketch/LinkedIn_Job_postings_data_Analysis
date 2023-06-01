import pandas as pd 
from helper import Cleaner
import openpyxl
def main():

    # Reading the CSV file into a pandas DataFrame
    df = pd.read_csv("data\\job_offers.csv")

    print('--------------- Cleaning data is just starting .... ---------------')
    cleaner =Cleaner(df)
    
    print('------ Spliting jobtype_experience  and company_size_industry Columns  -------')
    # Spliting jobtype_experience  and company_size_industry Columns
    cleaner.column_spliter('jobtype_experience','job_type','experience')
    cleaner.column_spliter('company_size_industry','company_size','industry')
    print(' -------------------------- Done -------------------------------------')
    
    print('-------------- cleaning company_location Column  ---------------------')
    # Keeping just the state name in location column
    cleaner.location_cleaner('company_location',location='state')
    print(' -------------------------- Done -------------------------------------')
    
    print('------------------- Cleaning applicants column  ----------------------')
    # Cleaning applicants column
    cleaner.noise_remover('applicants',noise=['applicants','applicant'])
    cleaner.fill_na('applicants',0)
    cleaner.data_type_convertor('applicants',int)
    print(' -------------------------- Done ------------------------------------')
    
    print('------------------- Removing missing data  --------------------------')
    # Remove rows with null values
    df.dropna(inplace=True)
    df.reset_index(inplace=True, drop=True)
    print(' -------------------------- Done -------------------------------------')
    
    print('---------------- Cleaning company_size column -----------------------')
    ## Cleaning company_size column
    cleaner.noise_remover('company_size',noise=[' employees',','])
    cleaner.company_size_cleaner('company_size')
    cleaner.data_type_convertor('company_size',int)
     # Define the categories and their corresponding ranges
    categories = {
        'small': (0, 100),
        'medium': (101, 1000),
        'large': (1001, float('inf'))
    }
    # Create a new column 'employee_class' based on the number of employees
    bins = [value[0] for value in categories.values()] + [float('inf')]
    df['company_size'] = pd.cut(df['company_size'], bins=bins,
                                labels=list(categories.keys()))
    print(' -------------------------- Done ------------------------------------')

    print('----------- Saving cleaned data into csv file   ----------------------')
    # Save the DataFrame 'df' to a CSV and xlsx file named 'cleaned_data.csv'
    df.to_csv('data\\cleaned_data.csv', index=False)
    df.to_excel('data\\cleaned_data.xlsx', index=False)

    print(' -------------------------- Done -------------------------------------')

if __name__ == '__main__':
    main()

