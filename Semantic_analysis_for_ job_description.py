from helper import semantic_analyzer 


def main():
    
    # Read jobs description text file 
    with open('data\\job_descriptions.txt','r',encoding='utf-8') as file:
        text = file.read()
 
    print('----  Semantic Analysis of job description is just starting ...   ---')
    analyzer = semantic_analyzer()

    print('------------------------ Text preprocessing ------------------------- ')
    analyzer.text_cleaner(text)
    print(' -------------------------- Done -------------------------------------')
    
    print('------------------------ Skills  preprocessing ---------------------- ')
    data_science_soft_skills = [
                            "project management", 'Project Coordination',
                            "Communication Skills","communication",'Negotiation Skills','Presentation Skills','Public Speaking','Collaboration Skills', 
                            "problem-solving",'Critical Thinking','Analytical Thinking','Creative Thinking','Decision Making',
                            "Data Storytelling","Storytelling",'Data Communication','Data Interpretation','Data Presentation',
                            "analytical skills","analytical",'Data Analysis','Diagnostic Skills',
                            "collaboration",'Teamwork','Cooperation','Group Work','Networking','Working Together','Collective Effort','team','Team Player',
                            "Curiosity","Product Understanding","Experience", "solutions"
                            ] 
    data_science_technical_skills = [
                                "Programming Python","Programming","Python","Programming R", "R", "Programming skills","Python R",
                                "Statistical Modeling","Statistical Analysis",'Statistical',"Probability", 'Statistics',"mathematical modeling",'mathematical','mathematics',
                                "Machine Learning","ML","Deep Learning","DL","Artificial Intelligence","AI",
                                "big data","Data Visualization","Data Cleaning","Data Ethics", "data governance","data lineage","Data privacy","Data security","security","data engineering","data visualization",
                                "Database Management", "scalable data",'Data cleaning','Data preprocessing','Data warehousing',
                                "cloud computing","AWS", "Azure","GCP","cloud","cloud platforms",
                                "Knowledge NLP","NLP", "computer vision","image processing","Knowledge optimization","optimization",
                                "technologies"," Hadoop","Spark","software development","web development","computing","frameworks","Apache Hadoop","Apache Spark",
                                "SQL","NoSQL", "Tableau",  "Power BI", 
                                "scikit-learn","Keras", "TensorFlow",  "PyTorch", "Matplotlib", 'pandas', "Seaborn","Plotly",
                                "control systems","Git","practices","design patterns"
                                ]

    analyzer.skills_cleaner(data_science_soft_skills)
    analyzer.skills_cleaner(data_science_technical_skills)
    print(' -------------------------- Done -------------------------------------')
    
    print('------------------------ Text Analysis ------------------------------ ')
    analyzer.analyzer(data_science_soft_skills,'Soft Skills')
    analyzer.analyzer(data_science_technical_skills,'Technical Skills')
    print(' -------------------------- Done -------------------------------------')
    
if __name__ == '__main__':
    main()








































# # 1- Language Identification and translate 
# # Write a pattern to match sentence endings: sentence_endings
# sentence_endings = r'[.!?]'
# # Split my_string on sentence endings and print the result
# sentences = re.split(sentence_endings, text) 
# english_sentences = []
# # german_sentences = []

# # print(type(sentences))
# for sentence in sentences[:]:
#     # print(sentence)
#     try:
#      lang = detect(sentence)
#     except:pass
#     if lang == 'en':
#         english_sentences.append(sentence)
#     elif lang == 'de':
#         try: 
#             translated_sentence = translator.translate(sentence, dest='en')
#             english_sentences.append(translated_sentence)
#         except:
#             pass
        
 
# # Remove ponctuation from the txte
# english_text = remove_punctuation(' '.join(english_sentences))

# # Filte the text (remove stop words)
# filtred_english_text = text_filter(english_text)



# data_science_soft_skills = [
#                           "project management", 'Project Coordination',
#                           "Communication Skills","communication",'Negotiation Skills','Presentation Skills','Public Speaking','Collaboration Skills', 
#                           "problem-solving",'Critical Thinking','Analytical Thinking','Creative Thinking','Decision Making',
#                           "Data Storytelling","Storytelling",'Data Communication','Data Interpretation','Data Presentation',
#                           "analytical skills","analytical",'Data Analysis','Diagnostic Skills',
#                           "collaboration",'Teamwork','Cooperation','Group Work','Networking','Working Together','Collective Effort','team','Team Player',
#                           "Curiosity","Product Understanding","Experience", "solutions"] 
 
# data_science_technical_skills = [
#     "Programming Python","Programming","Python","Programming R", "R", "Programming skills","Python R",
#     "Statistical Modeling","Statistical Analysis",'Statistical',"Probability", 'Statistics',"mathematical modeling",'mathematical','mathematics',
#     "Machine Learning","ML","Deep Learning","DL","Artificial Intelligence","AI",
#     "big data","Data Visualization","Data Cleaning","Data Ethics", "data governance","data lineage","Data privacy","Data security","security","data engineering","data visualization",
#     "Database Management", "scalable data",'Data cleaning','Data preprocessing','Data warehousing',
#     "cloud computing","AWS", "Azure","GCP","cloud","cloud platforms",
#     "Knowledge NLP","NLP", "computer vision","image processing","Knowledge optimization","optimization",
#     "technologies"," Hadoop","Spark","software development","web development","computing","frameworks","Apache Hadoop","Apache Spark",
#     "SQL","NoSQL", "Tableau",  "Power BI", 
#    "scikit-learn","Keras", "TensorFlow",  "PyTorch", "Matplotlib", 'pandas', "Seaborn","Plotly",
#     "control systems","Git","practices","design patterns"]

# # Converte skills into lowercase 
# data_science_soft_skills=[skill.lower() for skill in data_science_soft_skills]
# data_science_technical_skills=[skill.lower() for skill in data_science_technical_skills]


# soft_skills = word_tokenize(remove_punctuation(' '.join(data_science_soft_skills).replace("’","")))
# technical_skills = word_tokenize(remove_punctuation(' '.join(data_science_technical_skills).replace("’","")))

# # Remove stop words
# stop_words = set(stopwords.words('english'))
# filtered_soft_skills = [word for word in soft_skills if word.lower() not in stop_words]
# filtered_technical_skills = [word for word in technical_skills if word.lower() not in stop_words]
# soft_skills = remove_punctuation(' '.join(filtered_soft_skills)).lower()
# tech_skills = remove_punctuation(' '.join(filtered_technical_skills)).lower()

# soft_skills_freq_dic= skills_frequancy_dictionary(1, filtred_english_text,data_science_soft_skills )
# technical_skills_freq_dic= skills_frequancy_dictionary(1 , filtred_english_text,data_science_technical_skills )

# soft_keys = list(soft_skills_freq_dic.keys())
# soft_frequance = list(soft_skills_freq_dic.values())
# dict_soft_skills={i:soft_frequance[i] for i in  range(len(soft_keys))}

# tech_keys = list(technical_skills_freq_dic.keys())
# tech_frequance = list(technical_skills_freq_dic.values())
# dict_soft_skills={i:tech_frequance[i] for i in  range(len(tech_keys))}

# soft_text_data_tokens = [soft_keys]
# tech_text_data_tokens = [tech_keys]

# soft_dictionary = gensim.corpora.Dictionary(soft_text_data_tokens)
# tech_dictionary = gensim.corpora.Dictionary(tech_text_data_tokens)

# soft_corpus = [[(i , soft_frequance[i]) for i in range(len(soft_keys))]]
# tech_corpus = [[(i , tech_frequance[i]) for i in range(len(tech_keys))]]

# soft_corpus
# tech_corpus
# # # Build the LDA model
# soft_lda_model = gensim.models.LdaModel(corpus=soft_corpus, 
#                                    id2word=soft_dictionary, 
#                                    num_topics=4)
# tech_lda_model = gensim.models.LdaModel(corpus=tech_corpus, 
#                                    id2word=tech_dictionary, 
#                                    num_topics=4)
# # Print the topics and their words
# for topic, words in soft_lda_model.print_topics():
#     print ('-----------------------------------------------------------')
#     print(topic, words)
    
# for topic, words in tech_lda_model.print_topics():
#     print ('-----------------------------------------------------------')
#     print(topic, words)


# # Create the LDA model
# soft_lda_model = gensim.models.ldamodel.LdaModel(corpus=soft_corpus, id2word=soft_dictionary, num_topics=4)
# tech_lda_model = gensim.models.ldamodel.LdaModel(corpus=tech_corpus, id2word=tech_dictionary, num_topics=4)
# # Create the visualization data
# soft_tvis_data = pyLDAvis.gensim_models.prepare(soft_lda_model, soft_corpus, soft_dictionary)
# tech_tvis_data = pyLDAvis.gensim_models.prepare(tech_lda_model, tech_corpus, tech_dictionary)
# # Visualize the data
# # pyLDAvis.display(vis_data)

# # Save the visualization as an HTML file
# pyLDAvis.save_html(soft_tvis_data, 'soft_visualization.html')
# pyLDAvis.save_html(tech_tvis_data, 'tech_visualization.html')
# # Open the HTML file in a web browser

# webbrowser.open('soft_visualization.html')
# webbrowser.open('tech_visualization.html')

# # Create a word cloud for each topic
# for i in range(1):
#     topic_words = dict(soft_lda_model.show_topic(i, topn=50))
#     wordcloud = WordCloud(width=8000, 
#                           height=8000, 
#                           background_color="white").generate_from_frequencies(topic_words)
#     plt.imshow(wordcloud)
#     plt.axis("off")
#     plt.show()
    
# for i in range(1):
#     topic_words = dict(tech_lda_model.show_topic(i, topn=50))
#     wordcloud = WordCloud(width=8000, 
#                           height=8000, 
#                           background_color="white").generate_from_frequencies(topic_words)
#     plt.imshow(wordcloud)
#     plt.axis("off")
#     plt.show()