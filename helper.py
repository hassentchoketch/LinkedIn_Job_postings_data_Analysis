# Import libraries

import re
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException


from nltk.corpus import stopwords
import string
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

from googletrans import Translator
from langdetect import detect


import gensim
import pyLDAvis
import pyLDAvis.gensim_models

from wordcloud import WordCloud
import webbrowser

# Importing the warnings module for handling warning messages
import warnings

# Ignoring warning messages to prevent interruptions during code execution
warnings.filterwarnings("ignore")



class linkedinScrapper():
    def __init__(self,driver):
        self.driver = driver
        
    def login(self):
        # User Credentials
        # Reading txt file where we have our user credentials
        with open('user_credentials.txt', 'r',encoding="utf-8") as file:
            user_credentials = file.readlines()
            user_credentials = [line.rstrip() for line in user_credentials]

        user_name = user_credentials[0] # First line
        password = user_credentials[1] # Second line
        self.driver.find_element('xpath','//*[@id="username"]').send_keys(user_name)
        self.driver.find_element('xpath','//*[@id="password"]').send_keys(password)
        time.sleep(1)

        # Login button
        self.driver.find_element('xpath','//*[@id="organic-div"]/form/div[3]/button').click()
        self.driver.implicitly_wait(30)
        
    def listing_jobs_scrapper(self,link,pages_num):
        
        self.driver.get(link)
        time.sleep(3)
        links = []
        print(f'{25*(pages_num-1)} Links are being collected now.')
        try:
         for page in range(2,pages_num+3):
            time.sleep(2)
            jobs_block = self.driver.find_element(By.CLASS_NAME,'jobs-search-results-list')
            jobs_list= jobs_block.find_elements(By.CSS_SELECTOR, '.jobs-search-results__list-item')
            
            for job in jobs_list:
                all_links = job.find_elements(By.TAG_NAME,'a')
                for a in all_links:
                   if str(a.get_attribute('href')).startswith("https://www.linkedin.com/jobs/view") and a.get_attribute('href') not in links: 
                       links.append(a.get_attribute('href'))
                else:
                    pass
                # scroll down for each job element
                self.driver.execute_script("arguments[0].scrollIntoView();", job) 
                
            print(f'Collecting the links in the page: {page-1}')
            # go to next page:
            self.driver.find_element('xpath',f"//button[@aria-label='Page {page}']").click()
            time.sleep(3)
        except:
            pass    
        print('Found ' + str(len(links)) + ' links for job offers')  
        
        # Save links into txt file
        with open('data\\jobs_links.txt','w',encoding="utf-8") as f:
            for link in links:
                f.write(link)
                f.write('\n')
                
        return  links
    
    def job_pages_scrapper(self,links): 
        # Create empty lists to store information
        self.job_titles    = []
        self.company_names = []
        self.company_locations = []
        self.workplace_type    = []
        self.post_dates = []
        self.applicants = []
        self.jobtype_experience    = []
        self.company_size_industry = []
        # self.industry = []
        # self.followers = []
        # self.experience = []
        self.job_desc = []
        
        i = 0
        self.j = 1

        # Visit each link one by one to scrape the information
        print('Visiting the links and collecting information just started.')
        
        for i in range(len(links)):
            
            self._get_into_the_page(links[i])
           
            self._scrap_genaral_infos()
            
            self._scrap_job_sescription()

        # Creating the dataframe 
        df = pd.DataFrame(list(zip(self.job_titles,self.company_names,self.company_locations,
                                   self.workplace_type,self.post_dates,self.applicants,
                                   self.jobtype_experience,self.company_size_industry,                                   
                                    # self.experience,
                                    # self.followers
                                    # self.industry,
                              )),
                    columns =['job_title', 'company_name','company_location',
                              'workplace_type','post_date','applicants',
                              'jobtype_experience','company_size_industry',
                        #    'experience',
                        #    'followers',
                        #    'industry'
                             ]
                         )    
        
        # Storing the data to csv file
        df.to_csv('data\\job_offers.csv', index=False)

        # Output job descriptions to txt file
        with open('data\\job_descriptions.txt','w',encoding="utf-8") as f:
            for line in self.job_desc:
                f.write(line)
                f.write('\n')
                
    def _get_into_the_page(self,page_link):
            try:
                self.driver.get(page_link)
                i=i+1
                time.sleep(2)
                # Click See more.
                self.driver.find_element(By.CLASS_NAME,"artdeco-card__actions").click()
                # time.sleep(2)
            except:
                pass        
                
    def _scrap_genaral_infos(self):
            # Find the general information of the job offers
            contents = self.driver.find_elements(By.CLASS_NAME,'p5')
            for content in contents:
                try:
                    self.job_titles.append(content.find_element(By.TAG_NAME,"h1").text)
                except Exception:
                    self.job_titles.append(np.nan)   
                try :    
                    self.company_names.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__company-name").text)
                except Exception:
                    self.company_names.append(np.nan)
                try:
                    self.company_locations.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__bullet").text)
                except Exception:
                    self.company_locations.append(np.nan)
                try:
                    self.workplace_type.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__workplace-type").text)
                except Exception:
                    self.workplace_type.append(np.nan)
                try:
                    self.post_dates.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__posted-date").text)
                except Exception:
                    self.post_dates.append(np.nan)
                try:
                    self.applicants.append(content.find_element(By.CLASS_NAME,"jobs-unified-top-card__applicant-count").text)
                except Exception:
                    self.applicants.append(np.nan)
                try:
                    self.jobtype_experience.append(content.find_elements(By.CLASS_NAME,"jobs-unified-top-card__job-insight")[0].text)
                except Exception:
                    self.jobtype_experience.append(np.nan)
                try:
                    self.company_size_industry.append(content.find_elements(By.CLASS_NAME,"jobs-unified-top-card__job-insight")[1].text)
                except Exception:
                    self.company_size_industry.append(np.nan)
                    
                print(f'Scraping the Job Offer {self.j} DONE.')
                self.j += 1  
                time.sleep(2)
            
    def _scrap_job_sescription(self):
            # Scraping the job description
            job_description = self.driver.find_elements(By.CLASS_NAME,'jobs-description__content')
            for description in job_description:
                job_text = description.find_element(By.CLASS_NAME,"jobs-box__html-content").text
                self.job_desc.append(job_text)
                print(f'Scraping the Job Offer {self.j}')
                time.sleep(2)
        
class Cleaner():
    def __init__(self,df):
        self.df = df
    
    def column_spliter(self,column_name,new_column_1,new_column_2,spliter= '·'):
        # Splitting the column and assigning the split values to new 2 columns
        self.df[[new_column_1, new_column_2]] = self.df[column_name].str.split(spliter, expand=True)
        # Dropping the 'Level_and_involvement' column from the DataFrame
        self.df.drop(column_name, axis=1, inplace=True)  
        
    def noise_remover(self,column_name,noise):
        # Remove noise from the column values
        for _ in noise:
            self.df[column_name]= self.df[column_name].str.replace(_,'')
        
    def fill_na(self,column_name,fill_with):   
        # Replace missing values 
       self.df[column_name] = self.df[column_name].fillna(fill_with)   
    
    def data_type_convertor(self,column_name,new_type):
        # Convert the column to integer data type
        self.df[column_name] = self.df[column_name].fillna(0).astype(new_type)   
    
    def company_size_cleaner(self,column_name):
        
        self.df[column_name] = self.df[column_name].str.replace('(\d+)-(\d+)', r'\2', regex=True)
        self.df[column_name] = self.df[column_name].str.replace('\+', '', regex=True)
    
    
    def location_cleaner(self,column_name,location ='state'):
        if location == 'state':
           self.df[column_name] = self.df[column_name].str.split(',' ,expand=True)[1]
        elif location == 'city':
           self.df[column_name] = self.df[column_name].str.split(',' ,expand=True)[0]
             
def count_plot(data, column_name, plot_title,nlargest = 10, orient = 'h'):
    # Compute the value counts of the specified column and get the top 10 categories
    category_counts = data[column_name].value_counts().nlargest(nlargest)

    # Set the size and resolution of the figure
    plt.figure(figsize=(8, 4), dpi=80)

    # Create a horizontal bar plot using seaborn
    if orient == 'v':
       chart = sns.barplot(x=category_counts.index, y=category_counts.values  , palette='dark',orient=orient)
    else:
       chart = sns.barplot(x=category_counts.values, y=category_counts.index  , palette='dark',orient=orient)

    # Set the title and axis labels with custom styles
    plt.title(plot_title, fontsize=12, fontweight='bold')
    plt.xlabel("Number of Job Openings", fontsize=10, fontweight='bold')
    # plt.ylabel(column_name, fontsize=12, fontweight='bold')

    # Set the tick label size for better readability
    plt.xticks(fontsize=10, fontweight='bold')
    plt.yticks(fontsize=10, fontweight='bold')
    
    # Add data labels to the bars with custom styling
    # for i, v in enumerate(category_counts.values):
    #     chart.text(v + 10, i, f"{v}", va='center', fontsize=10, fontweight='bold', color='white')

    # Customize the plot appearance
    sns.despine()
    chart.grid(axis='x', linestyle='--', linewidth=0.5, color='lightgray')
    chart.set_axisbelow(True)

    # Adjust the padding between plot elements
    plt.tight_layout()

    # Display the plot
    # plt.show()   
    
    # Save fig 
    plt.savefig(f'graphs\\{plot_title}.png', dpi=300) 
        
def remove_punctuation(text):
    # Create a table of punctuation characters and their corresponding None values
    table = text.maketrans('', '', string.punctuation)
    # Use this table to remove all punctuation from the text
    text = text.translate(table)
    return text

def text_filter(text):
    # Initialize the list of stop words
    stop_words = set(stopwords.words('english'))

    # Initialize the stemmer
    stemmer = SnowballStemmer("english")

    # Initialize an empty list to store the filtered text
    filtered_text = []

    # Iterate over each review in your text data
    topic=text
    # Tokenize the review into words
    words = word_tokenize(remove_punctuation(topic.replace("’","")))

    # Remove stop words
    filtered_words = [word.lower() for word in words if word.lower() not in stop_words]

    # Join the filtered words back into a single string
    filtered_review = " ".join(filtered_words)

    # Append the filtered review to the list
    filtered_text.append(filtered_review)
    return filtered_text

def normalising(self, dictionary_skills,skills_list ):
        for key in list(dictionary_skills.keys()) :
            for skill in skills_list:
                if key in skill or skill in key :
                    try :
                        dictionary_skills[skill] = dictionary_skills.pop(key)
                    except : pass
        return dictionary_skills
    
def skills_frequancy_dictionary(num_topic , filtered_text ,skills_list):
    dictionary_skills={}
    words_list = filtered_text[num_topic -1 ].split(' ')
    for i in range(len(words_list)-1) :
        topic = ' '.join([words_list[i], words_list[i+1]] )
        if topic in skills_list :
            if topic in list(dictionary_skills.keys()):
                dictionary_skills[topic]+=1
            else :
                dictionary_skills[topic]=1

        if words_list[i] in skills_list:
            if words_list[i] in list(dictionary_skills.keys()):
                dictionary_skills[words_list[i]]+=1
            else :
                dictionary_skills[words_list[i]]=1 
    return normalising( normalising( dictionary_skills,skills_list ) ,skills_list)

class semantic_analyzer():
    def __init__(self,num_topic=1):
        self.num_topic= num_topic
        
    def text_cleaner(self,text) :
        # --------1- Language Identification and translate --------
        # Write a pattern to match sentence endings: sentence_endings
        sentence_endings = r'[.!?]'

        # Split my_string on sentence endings 
        sentences = re.split(sentence_endings, text) 
        
        # Detect language and translate non-english sentences
        english_sentences = []
        for sentence in sentences:
            try:
               lang = detect(sentence)
               if lang != 'en':
                    translated_sentence = Translator.translate(sentence, dest='en')
                    english_sentences.append(translated_sentence)
               else:
                    english_sentences.append(sentence)              
            except:
                pass
       
        # Remove ponctuation from the txte
        text = self._remove_punctuation(' '.join(sentences))

        # Filte the text (remove stop words)
        self.filtred_text = self._text_filter(text)
        
           
    def skills_cleaner(self,skills):
        # Converte skills into lowercase 
        skills=[skill.lower() for skill in skills]
        self.filtred_skills = self._text_filter(' '.join(skills))
        
        
    def analyzer(self,skills,skills_type):
        # Converte skills into lowercase 
        skills=[skill.lower() for skill in skills]
        
        skills_freq_dic= self._skills_frequancy_dictionary(self.num_topic, self.filtred_text,skills )
        
        
        # bar plot for skills frequances
        skills_freq_dic = dict(sorted(skills_freq_dic.items(), key=lambda item: item[1], reverse=True))
        self._barplot(list(skills_freq_dic.keys()),list(skills_freq_dic.values()),f'Top {skills_type} In-Demand')
        
        keys = list(skills_freq_dic.keys())
        frequance = list(skills_freq_dic.values())
        dict_skills={i:frequance[i] for i in  range(len(keys))}
        

        text_data_tokens = [keys]
        dictionary = gensim.corpora.Dictionary(text_data_tokens)
        corpus = [[(i , frequance[i]) for i in range(len(keys))]]
        lda_model = gensim.models.LdaModel(corpus=corpus, 
                                   id2word=dictionary, 
                                   num_topics=self.num_topic)
        # Print the topics and their words
        for topic, words in lda_model.print_topics():
            # print ('-----------------------------------------------------------')
            print(topic, words)
            
        # Create the LDA model
        lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=2 )#self.num_topic)
        # Create the visualization data
        soft_tvis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
        # Save the visualization as an HTML file and open it 
        pyLDAvis.save_html(soft_tvis_data, f'graphs\\{skills_type}_visualization.html')
        webbrowser.open(f'graphs\\{skills_type}_visualization.html')
        
        for i in range(1):
            topic_words = dict(lda_model.show_topic(i, topn=50))
            wordcloud = WordCloud(width=5000, 
                                height=5000, 
                                background_color="white").generate_from_frequencies(topic_words)
            # Set the size and resolution of the figure
            plt.figure(figsize=(8, 4), dpi=80)
            plt.imshow(wordcloud)
            plt.axis("off")
            # Set the title and axis labels with custom styles
            plt.title(f'{skills_type} wordcloud', fontsize=12, fontweight='bold')
            # Save fig 
            plt.savefig(f'graphs\\{skills_type} wordcloud.png', dpi=300) 
            # plt.show()


    def _remove_punctuation(self, text):
        # Create a table of punctuation characters and their corresponding None values
        table = text.maketrans('', '', string.punctuation)
        # Use this table to remove all punctuation from the text
        text = text.translate(table)
        return text
    
    def _text_filter(self,text):
    # Initialize the list of stop words
        stop_words = set(stopwords.words('english'))

        # Initialize the stemmer
        stemmer = SnowballStemmer("english")

        # Initialize an empty list to store the filtered text
        filtered_text = []

        # Iterate over each review in your text data
        topic=text
        # Tokenize the review into words
        words = word_tokenize(remove_punctuation(topic.replace("’","")))

        # Remove stop words
        filtered_words = [word.lower() for word in words if word.lower() not in stop_words]

        # Join the filtered words back into a single string
        filtered_review = " ".join(filtered_words)

        # Append the filtered review to the list
        filtered_text.append(filtered_review)
        return filtered_text
    
    def _skills_frequancy_dictionary(self,num_topic , filtered_text ,skills_list):
        dictionary_skills={}
        words_list = filtered_text[num_topic -1 ].split(' ')
        for i in range(len(words_list)-1) :
            topic = ' '.join([words_list[i], words_list[i+1]] )
            if topic in skills_list :
                if topic in list(dictionary_skills.keys()):
                    dictionary_skills[topic]+=1
                else :
                    dictionary_skills[topic]=1

            if words_list[i] in skills_list:
                if words_list[i] in list(dictionary_skills.keys()):
                    dictionary_skills[words_list[i]]+=1
                else :
                    dictionary_skills[words_list[i]]=1 
        return self._normalising(self._normalising( dictionary_skills,skills_list) ,skills_list)
    
    def _normalising(self, dictionary_skills,skills_list ):
        for key in list(dictionary_skills.keys()) :
            for skill in skills_list:
                if key in skill or skill in key :
                    try :
                        dictionary_skills[skill] = dictionary_skills.pop(key)
                    except : pass
        return dictionary_skills

    def _barplot(self,y, x, plot_title, orient='h'):
        plt.figure(figsize=(8, 4), dpi=80)
        chart = sns.barplot(y=y, x=x  , palette='dark',orient=orient)
        # Set the title and axis labels with custom styles
        plt.title(plot_title, fontsize=12, fontweight='bold')
        plt.xlabel("Frequances", fontsize=10, fontweight='bold')
        plt.ylabel("Skills", fontsize=10, fontweight='bold')
        # Set the tick label size for better readability
        plt.xticks(fontsize=10,fontweight='bold')
        plt.yticks(fontsize=10, fontweight='bold')
        # Customize the plot appearance
        sns.despine()
        chart.grid(axis='x', linestyle='--', linewidth=0.5, color='lightgray')
        chart.set_axisbelow(True)
        # Adjust the padding between plot elements
        plt.tight_layout()

        # Display the plot
        # plt.show()
        # Save fig 
        plt.savefig(f'graphs\\{plot_title}.png', dpi=300) 