from rake_nltk import Rake
from bs4 import BeautifulSoup
from mtranslate import translate
import sys
import pandas as pd
import requests
import mysql.connector
import nltk 
from summarizer import Summarizer
import textrazor
import re
from nltk import sent_tokenize
import tweepy
from datetime import date
from newspaper import Article
from googlesearch import search
import urllib.parse
from selenium import webdriver
import spacy
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
nltk.download('punkt')

Technology = ["technology (general)","aerospace","science (general)","engineering","technology","it/computer sciences","computing and information technology","energy and resource","manufacturing and engineering","renewable energy","internet"]
Economics = ["international (foreign) trade","business (general)","economy (general)"]
Medical = ["gastronomy", "government health care","disease","illness","medicine","epidemic and plague","animal diseases","retrovirus","virus diseases","viruses","virus","virus disease","diseases and conditions","health","communicable disease"]
Security = ["security","networking"]
Transportation = ["travel","travelling","tourism and leisure","tourism","superbike","traffic","traffic (general)","motorcycle"]

dict1 = {}

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome(options=options)

nlp = spacy.load('en_core_web_lg')

Category=''
today = date.today()  
Day = today.strftime("%d")
Month = today.strftime("%B")[:3]

def SearchGoogle(urllinks):
	for query in urllinks:
		LINKS = []
		for url in search(query, tld='ae',stop=10):

			LINKS.append(url)
			# article = Article(url)
			# article.download()
			# article.parse()
			# print(article.text)
		if query not in dict1:
			dict1[query]=LINKS
		else:
			dict1[query].extend(LINKS)

def SearchURL(topics):
	SearchGoogle(topics)

	return dict1
def text_razor(t):
    textrazor.api_key="03036ae3ea86b59e99be7f5bbf9f12aa63ebb2615cd98bf75578207e"
    client=textrazor.TextRazor(extractors=["entities","topics"])
    client.set_cleanup_mode("raw")
    client.set_classifiers(["textrazor_newscodes"])
    response=client.analyze(t)
    #print(response.entities)
    entities=list(response.entities())
    #print(entities)
    entities.sort(key=lambda x: x.relevance_score, reverse=True)

    seen=set()
    for entity in entities:
        if entity.id not in seen:
            #print(entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types)
            seen.add(entity.id)
    li=[]
    for category in response.categories():
        try:
            d = category.label
            p = len(d)
        #e=re.findall(">[a-zA-Z0-9]",d)
        #print(e)
            e = d.rindex('>')
            #new=
            li.append(d[e+1:p])
        except:
            continue

    v = set(li)
    v=list(v)
    try:
        if(v[0]):
            if(v[0] in Technology):
                category_1 = "Technology"
            elif(v[0] in Transportation):
                category_1 = "Transportation"
            elif(v[0] in Economics):
                category_1 = "Economics"
            elif(v[0] in Medical):
                category_1 = "Medical"
            elif(v[0] in Security):
                category_1 = "Security"
            else:
                category_1 = "Uncategorised"
    except:
        category_1 = "Uncategorised"
    return(category_1)


try:
    textrazor.api_key="707f2386a16dedf30f636cc8a799f6afa45849469284175020bdc9d8"
    consumer_key = "Pywlk64OFS82OtOWIJuBKjPEW"
    consumer_secret = "Ql3Cb53gSsx6UWxdRfWyB0rnorlX8j9psdJ1T4bwo6ssPz6vrz"
    access_key = "332760146-dcUzpvnmz8i1XKHm8cTpfvG51mXJ8IaPNK5e3ytf"
    access_secret = "ZwwmWA8KgNJXjrlg9VZ5gfOd5EHLnistFi1OQNMODo1mB"
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    client=textrazor.TextRazor(extractors=["topics"])
    
    DICT={}
    t=''
    our_url=''
    short=''
    CATEGORIES=''
    rake_column=''
    TOPICS=''
    event_complete = ''
    whole_text=''
    impact=''
    Links=''
    Link=''
    http0 = sys.argv[1]
    for word in sys.argv[2:]:
        event_complete += word + ' '
    http0 = http0[http0.find("[")+1:http0.find("]")]
    http1 = http0.split(",")
    Link = ','.join(http1)
    mydb=mysql.connector.connect(host="localhost",user="sfadmin",passwd="7@3xyeR6x%uNAcy",database="nlp_engine")
    mycursor = mydb.cursor(buffered=True)
    def get_tweets(username):
        tweet_bundle=''
        tweets = api.user_timeline(screen_name=username,count=40,tweet_mode="extended")
        tweets_for_csv = [tweet for tweet in tweets]
        for j in tweets_for_csv:
            trans=translate(j.full_text)
            trans = re.sub(r'^https?:\/\/.*[\r\n]*', '', trans, flags=re.MULTILINE)
            if re.search(event_complete, trans, re.IGNORECASE):
            	var1=j.id_str
            	var2=j.user.screen_name
            	save_url='https://twitter.com/'+var2+'/status/'+var1
            	tweet_bundle=tweet_bundle+" "+trans
            	return tweet_bundle,save_url
            else:
            	continue
        return tweet_bundle
    mycursor.execute("SELECT Event, COUNT(*) FROM Events WHERE Event = %s GROUP BY Event",(event_complete,))
    row_count = mycursor.rowcount
    print(row_count)
    if row_count == 0:
	    if(http0):
	        for url in http1:
	            url = url.replace("\/","/")
	            x=re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',url)

	            if(x!=None):
	                t=x[0]

	            else:
	                t=x
	            if(t!=None):
	                y=re.findall("twitter.com*",t)
	                if(y):
	                    yfinal=t.rfind('/')
	                    yfinal=re.sub(t[0:yfinal+1],"",str(t))
	                    try:
	                        bomb,url=get_tweets(yfinal)
	                        bomb = bomb.replace("#", "");
	                        whole_text = whole_text+" "+bomb
	                        DICT[url]=bomb
	                    except:
	                        pass
	                    
	                else:
	                    # source=requests.get(t).text
	                    # soup = BeautifulSoup(source,'lxml')
	                    # mytext = ''
	                    # h=soup.find_all('p')
	                    # for m in h:
	                    #     mytext = mytext + m.text
	                    article = Article(t, language="en")
	                    article.download()
	                    article.parse()
	                    article.nlp()
	                    mytext =  translate(article.text)
	                    DICT[url] = mytext
	                    whole_text = whole_text+' '+mytext
	            else:
	                url1 = url+" " +event_complete
	                URLs_selected = SearchURL([url1])
	                dict1 = {}
	                for one in URLs_selected.items():
	                    Links = ','.join(one[1][:1])
	                    for i in one[1][:1]:
	                        try:
	                            article = Article(i, language="en")
	                            article.download()
	                            article.parse()
	                            article.nlp()
	                            whole_text = whole_text+ " " + translate(article.text)
	                        except:
	                            continue
	    else:
	        URLs_selected = SearchURL([event_complete])
	        for one in URLs_selected.items():
	            Links = ','.join(one[1][:10])
	            for i in one[1][:7]:
	                try:
	                    article = Article(i, language="en")
	                    article.download()
	                    article.parse()
	                    article.nlp()
	                    whole_text = whole_text+ " " + translate(article.text)
	                except:
	                    continue

	            # url="#"+url
	            # i=0
	            # for tweet in tweepy.Cursor(api.search,q=url,count=20,since="2019-11-11",tweet_mode="extended").items(20):
	            #     trans=translate(tweet.full_text)
	            #     trans = re.sub(r'^https?:\/\/.*[\r\n]*', '', trans, flags=re.MULTILINE)
	            #     var1=tweet.id_str
	            #     var2=tweet.user.screen_name
	            #     save_url='https://twitter.com/'+var2+'/status/'+var1
	            #     trans = trans.replace("#", "");
	            #     whole_text=whole_text+' '+trans
	            #     DICT[save_url]=trans
	            #     i+=1
	            #     if(i==20):
	            #         break
	                

	    model = Summarizer()
	    whole_text = whole_text[len(whole_text[0:whole_text.find(".")])+1 : len(whole_text)]
	    paragraph = model(whole_text)
	    impact1 = paragraph

	    for i in range(0,5):
	        if len(sent_tokenize(paragraph))>15:
	            paragraph = model(paragraph)
	        else:
	            break
	    if(len(sent_tokenize(paragraph))>5):
	        paragraph = "".join(sent_tokenize(paragraph)[:5])
	    Category = text_razor(impact1)
	    article_1 = sent_tokenize(whole_text)
	    entities_system_know = dict()
	    entities_in_article = dict()
	    relations = set()

	    for article in article_1:
	        doc = nlp(article)
	        for ent in doc.ents: 
	            if ent.label_ not in ['DATE', 'TIME', 'CARDINAL', 'ORDINAL', 'PERCENT', 'MONEY' , 'PRODUCT', 'NORP']:
	                entities_in_article[ent.text] = ent.label_

	        if(len(entities_system_know) > 0):
	            for entity in  entities_system_know.keys():
	                if entity in entities_in_article.keys():
	                    for ent_new in entities_in_article.keys():
	                        if not ent_new == entity:
	                            relations.add((entity, ent_new))
	            entities_system_know = {**entities_system_know, **entities_in_article}

	            entities_in_article = dict()

	        else:
	            entities_system_know = {**entities_system_know, **entities_in_article}
	            for comb in combinations(entities_system_know, 2):
	                relations.add(comb)
	            entities_in_article = dict()

	    G = nx.Graph()
	    G.add_edges_from(list(relations))

	    plt.figure(figsize=(100, 100))

	    nx.draw(G, with_labels=True, node_size=1000, node_color="skyblue", node_shape="o", alpha=0.5, linewidths=4, font_size=15, font_color="grey", font_weight="bold", width=2, edge_color="grey")

	    plt.savefig('knowledge_graphs/'+event_complete.strip()+'.png')

	    sql = 'INSERT INTO Events(Event,Analysis,Day,Month,Link,Links,Description,Category) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
	    val = (event_complete,paragraph,Day,Month,Link,Links,whole_text,Category)
	    mycursor.execute(sql,val)
	    # split_summary = sent_tokenize(impact1)
	    # for summary in split_summary:
	    #     summary = summary.replace(u'\xa0', u' ')
	    #     summary = summary.strip()
	    #     for url,p_value in DICT.items():
	    #         if summary in p_value:
	    #             our_url+=summary+'`'+url+'~'
	    # rake_column = our_url
	    # response = client.analyze(impact)
	    # for topics1 in response.topics():
	    #     if topics1.score>.7:
	    #         TOPICS = TOPICS+topics1.label+'@'+str(topics1.score)+','
	        # r=Rake()
	        # r.extract_keywords_from_text(mytext)
	        # l=r.get_ranked_phrases()
	        #print("calculating impacts . . . .")
	        # impact='~'.join(l[:10])
	    # for url in http1:
	    #     url = url.replace("\/","/")
	    #     analysis_name=event_complete
	    #     credibility=""
	    #     mycursor.execute("SELECT * FROM data_sources WHERE SOURCE_NAME ='"+url+"'")
	    #     result_set=mycursor.fetchall()
	    #     for value in result_set:
	    #         credibility=value[4]
	    #     sql='INSERT INTO analysis(ANALYSIS_NAME,SOURCE_NAME,IMPACT,CREDIBILITY,RAKE,TOPICS) VALUES (%s,%s,%s,%s,%s,%s)'
	    #     val=(analysis_name,url,impact,credibility,rake_column,TOPICS)
	    #     mycursor.execute(sql,val)
    else:
	    print('already exist')
    mydb.commit()
    print("DONE")

except Exception as e:
    print(e)
