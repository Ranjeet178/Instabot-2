#!/usr/bin/env python
# coding: utf-8

# In[29]:


#importing all the necessary packages
from selenium import webdriver                                    #importing webdriver
from selenium.webdriver.support.ui import WebDriverWait           #To use implcit and explicit wait
from selenium.webdriver.support import expected_conditions as EC  #use in explicitly wait
from selenium.webdriver.common.by import By                       #to select the attribute by Class,link_text
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup                                              #work with attribute 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException  #to handle StaleElementReferenceException
from selenium.webdriver.common.keys import Keys #For navigating the pop up window
from selenium.common.exceptions import NoSuchElementException #to handle NoSuchElementException
from collections import Counter #for extracting the top n number of counts in dictionary
import matplotlib.pyplot as plt                                            #for plotting the graph
import pandas as pd
import csv


# In[30]:


# Log in to the instagram
driver=webdriver.Chrome(executable_path='C:/Users/singh/chromedriver') #path of 
driver.get('https://www.instagram.com/') #navigating to the instagram log in page
wait = WebDriverWait(driver, 10)
name= wait.until(EC.presence_of_element_located((By.NAME,'username'))) #locating the box to insert name of the user
name.send_keys('ra.njeet9098') # passing username
pas=driver.find_element_by_name('password') # locating the box to insert the password of the user
pas.send_keys('Ranjeet1996@') #passinf password
login=driver.find_element_by_class_name('L3NKy') #serch for login button
login.click() #clicking on the login button


# 1. Now your friend has followed a lot of different food bloggers, he needs to analyse the habits of these bloggers.
#  
#   A. From the list of instagram handles you obtained when you searched ‘food’ in previous project. Open the first 10 handles and find the top 5 which have the highest number of followers

# In[68]:


search=driver.find_element_by_xpath('//input[contains(@class,"XTCLo")]') #loacting the search box
search.send_keys("food")                                                #sending values for searching
time.sleep(3)
val=driver.find_elements_by_xpath('//div[@class = "fuqBx"]/a["href"]')  #fetching food list Handles 
food=[] #creating an empty list for appending the list of food handlers
for i in val[0:10]: #selecting first 10
    if 'explore' in i.get_attribute('href'):        #if explore present in link then it is hastags
        continue
    else:
        s = i.get_attribute('href').split('/')      #https://www.instagram.com/foodtalkindia
        #print(s[3])                                     # after split s= ['https:','','www.instagram.com','stockholmfood']
        if 'foodie_since97' not in s[3]:#as 'foodie_since97' private account we can't access the followers
            food.append(s[3])                          #appending s[3] in food_list       
a=driver.find_element_by_xpath('//input[contains(@class,"XTCLo")]')  #seaeching  input box 
a.clear() #clearing the input  box
b=driver.find_element_by_class_name('coreSpriteSearchClear').click() #selecting clear box by class name and clicking it
#new_food=food[:10]  
followers=[] #creating an empty dictionary for storing the nuber of followers.
for i in food:#opening each and ever profile of first 10 followers and then navigating back to the home-page
    search=driver.find_element_by_xpath('//input[contains(@class,"XTCLo")]') #loacting the search box
    #a.clear()
    search.send_keys(i) #sending the values for serching in search bar
    b = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'yCE8d')))     #selecting the follower-page
    b.click() #clicking it to open  the profile
    time.sleep(3)
    l=driver.find_element_by_xpath('//a[contains(@class, "-nal3")]/span').get_attribute('title') #ectracting the number of followers
    s=l.replace(',','')
    followers.append(int(s))
    
    driver.back() #navigating back to the home-page

res = {food[i]: int(followers[i]) for i in range(len(food))} #creating a dictionry with user name as keys and number of followers values
od=dict(Counter(res).most_common(5)) #extracting top 5 followers profiles
od    


# B. Now Find the number of posts these handles have done in the previous 3 days.

# In[69]:


no_of_post={}
for handle in od:
    search = driver.find_element_by_xpath('//div[contains(@class,"LWmhU")]/input')   #input box 
    search.send_keys(handle)                                                         #send hadles to search box
    b = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'z556c')))          #first profile
    first_search = driver.find_element_by_class_name('z556c')          
    first_search.click()
    a= wait.until(EC.presence_of_element_located((By.XPATH,'//input[contains(@class,"XTCLo")]')))  #clearing input box
    a.clear()
    count = 0
    i=0
    for i in range(12):
        driver.execute_script('window.scrollBy(0,document.body.scrollHeight);')                #scrolling 7 time to done side
        time.sleep(1)
    data=driver.find_elements_by_xpath('//div[contains(@class,"_9AhH0")]')                     #fetching the post
    for j in range(12):  
        driver.execute_script('window.scrollBy(0,-document.body.scrollHeight);')               #scrolling upside to move top
        time.sleep(1)
    #driver.execute_script('window.scrollBy(0,500);')                                           #scrolling downside ot mave till post
    final=data
    for i in range(len(final)):
        post=driver.find_elements_by_xpath('//div[contains(@class,"_9AhH0")]')               #finding post 
        driver.execute_script('window.scrollBy(0,80);')                                      #scrolling by 80 downside
        wait = WebDriverWait(driver, 15)                                                     #wait time
        post[i].click()                                                                      #click on each post
        test= wait.until(EC.presence_of_element_located((By.XPATH,'//time[contains(@class,"FH9sR")]'))) #test button
        val=test.text                            #fetch text
        time.sleep(2)
        if val[-1]=='d': #d for days,h for hours and m for mins
            new_val=int(val[0:-1])
            if new_val<4: #4 represents 4 day and so i have used this condition to extart info for only three notes
                count=count+1
            else:
                new=driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1] #extractint the close button 
                new.click()#clicking the close button to close the post
                break
        else:
            if val[-1]=='h': #d for days,h for hours and m for mins
                count=count+1
            elif val[-1]=='m': #d for days,h for hours and m for mins
                count=count+1
            else:
                new=driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1] #extractint the close button 
                new.click() #clicking the close button to close the post
                break
                
        close_btn = driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1]      #post close button
        close_btn.click()                                           #click on close button
        time.sleep(2)
    no_of_post[handle]=count                                       #count adding in dictionary
handles=[] #empty list for handlers name
number_posts=[] #emtpy list to count number of posts
for i in no_of_post:
    handles.append(i)                                            
    number_posts.append(no_of_post[i])
for i in range(len(handles)):
    print(handles[i],'',number_posts[i])#printing name with the number of post for the last 3 days
    


# C. Depict this information using a suitable graph.

# In[70]:


plt.bar(handles,number_posts,width=0.6)
plt.xticks(rotation=70)
plt.title('insta handles VS Number of posts')
plt.xlabel('Instagram Handlers name')
plt.ylabel('Number of posts posted in last 3 days')

plt.show()


# 2. Your friend also needs a list of hashtags that he should use in his posts.
# 
#   A. Open the 5 handles you obtained in the last question, and scrape the content of the first 10 posts of each handle.

# In[72]:


top_5_post_content={}
for t in od:
    post_content={}
    data=driver.find_element_by_xpath('//input[contains(@class,"XTCLo")]') #input box 
    data.send_keys(t)  #send hadlers name to search box
    driver.implicitly_wait(10)
    data=driver.find_element_by_xpath('//span[contains(@class,"Ap253")]') #first profile
    data.click() #clicking it to open the profile page
    driver.implicitly_wait(10)
    for i in range(1):
        driver.execute_script('window.scrollBy(0,document.body.scrollHeight);')                      #down scrolling
        time.sleep(1)
    data=driver.find_elements_by_xpath('//div[contains(@class,"_9AhH0")]')                           #fetching the data 
    for j in range(1):
        driver.execute_script('window.scrollBy(0,-document.body.scrollHeight);')                     #up scrolling
        time.sleep(1)
             
    driver.execute_script('window.scrollBy(0,500);')
    driver.execute_script('window.scrollBy(0,500);')
    for p in range(10):
        data=driver.find_elements_by_xpath('//div[contains(@class,"_9AhH0")]')#fetch the post
        driver.execute_script('window.scrollBy(0,80);') # scroll by 80
        driver.implicitly_wait(10) 
        data[p].click() #clicking on each post to extract the contents
        driver.implicitly_wait(10)
        con='post'+str(p+1)
        data=driver.find_element_by_xpath('//div[contains(@class,"C4VMK")]/span')#clicking on each post
        value=data.text#text data
        post_content[con]=value
        new=driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1] #extractint the close button
        new.click()#clicking the close botton
    top_5_post_content[t]=post_content
for i in top_5_post_content:
    print(i)
    print('####################')
    print(top_5_post_content[i])
    print('***************************************')


# B. Prepare a list of all words used in all the scraped posts and calculate the frequency of each word.

# In[73]:


total_words_freq={} #dictionary to store words as key and values a count
for i in top_5_post_content:
    val=top_5_post_content[i]
    for j in range(10):
        post_number='post'+str(j+1)
        new_val=val[post_number]
        final_val=new_val.split()  #spliting each and every post
        for k in final_val:
            if k[0]=='#':  #only fetching hastages
                ans=k[1:]
                if ans in total_words_freq:
                    total_words_freq[ans]+=1
                else:
                    total_words_freq[ans]=1
print(total_words_freq)


# C. Create a csv file with two columns : the word and its frequency

# In[74]:


freq_of_words=[] #creating an empty list
for i in total_words_freq:
    freq_of_words.append([i,total_words_freq[i]]) 
df=pd.DataFrame(freq_of_words,columns=['words','Frequency'])
df.to_csv('freq_of_words.csv',index=False) #creating the csv file.
print(df)


# D. Now, find the hashtags that were most popular among these bloggers

# In[75]:


top_5_most_popular_hastags=dict(Counter(total_words_freq).most_common(5)) #extracting top 5 hastags which are most popular among these bloggers
top_5_most_popular_hastags


# E. Plot a Pie Chart of the top 5 hashtags obtained and the number of times they were used by these bloggers in the scraped posts.

# In[76]:


hastags=[]
counts=[]
for i in top_5_most_popular_hastags:
    hastags.append(i)
    counts.append(top_5_most_popular_hastags[i])
plt.pie(counts,labels=hastags,autopct="%.2f%%")
plt.axis('equal')
plt.show()


# 3. You need to also calculate average followers : likes ratio for the obtained handles.
# Followers : Likes ratio is calculated as follows:
#         

# A. Find out the likes of the top 10 posts of the 5 handles obtained earlier.

# In[101]:


top_5_post_like={}                                                          #empty dictionary for top five post
for t in od:                                                        
    post_likes={}
    count=0
    data=driver.find_element_by_xpath('//input[contains(@class,"XTCLo")]')  #input box
    data.send_keys(t)                                                       #send handle
    driver.implicitly_wait(10)
    data=driver.find_element_by_xpath('//span[contains(@class,"Ap253")]')   #first search
    data.click()
    driver.implicitly_wait(10)
    for i in range(12):
        driver.execute_script('window.scrollBy(0,2000);')                  #scroll by 2000
        time.sleep(1)
    data=driver.find_elements_by_xpath('//div[contains(@class,"_9AhH0")]') #fetch the elements
    for j in range(12): 
        driver.execute_script('window.scrollBy(0,-2000);')                 #scroll by 2000
        time.sleep(1)
    driver.execute_script('window.scrollBy(0,500);')                       #make in proper place f post
    driver.execute_script('window.scrollBy(0,500);')
    final=data
    driver.implicitly_wait(10)
    for p in range(len(final)):
        if count>9:
            break  
        try:
            data=driver.find_elements_by_xpath('//div[contains(@class,"_9AhH0")]')  #fetch post
            driver.execute_script('window.scrollBy(0,80);')
            final=len(data)
            driver.implicitly_wait(10)
           
            data[p].click()
            driver.implicitly_wait(10)
            data=driver.find_element_by_xpath('//button[contains(@class,"sqdOP ")]//span')  #find likes on post
            val=data.text
            if val=='':
                new=driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1] #extractint the close button
                new.click()
                continue
            if val[0]=='V':
                new=driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1] #extracting the close button
                new.click()
                continue
            val=val.replace(',','')
            ans=val
            count=count+1
            number='post'+str(count)
            post_likes[number]=ans
            new=driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1] #extracting the close button
            new.click()
            
        except NoSuchElementException:
            new=driver.find_elements_by_xpath('//button[contains(@class,"wpO6b")]/div')[-1] #extracting the close button
            new.click()
    
    top_5_post_like[t]=post_likes
print(top_5_post_like)


# B. Calculate the average likes for a handle.

# In[107]:


average_handles={} #empty dic to store average value as key and handlers name as value
for i in top_5_post_like:
    c=0
    tsum=0
    d=top_5_post_like[i]#extracting each and every post likes
    #print(d)
    d = [d[w].replace('Hide replies', '0') for w in d]#replacing the hidden likes counts with 0
    for j in d:
        c=c+1
        tsum+=int(j)#converting the values from string to int and summing up them.
        average=tsum/c #calculating the average
    average_handles[i]=average
for key in average_handles.keys():
    print(key,end="    ")
    print("{0:.2f}".format(average_handles[key]))


# In[ ]:





# C. Divide the average likes obtained from the number of followers of the handle to get the average followers:like ratio of each handle.

# In[109]:


top_5_average_like=[] #creating empty list to append the average value
dic={}#creating empty dictionary to have handler name as key and number of followers as values
top_5_followers=[]
average_followers_likes=[]
top_5=[]
for i in average_handles:
    top_5_average_like.append(average_handles[i])#appending the  average value 
for i in od: 
    data=driver.find_element_by_xpath('//input[contains(@class,"XTCLo")]') #input box
    data.send_keys(i) #send handle
    driver.implicitly_wait(10)
    data=driver.find_element_by_xpath('//span[contains(@class,"Ap253")]')
    data.click() #clicking to visit the profile
    driver.implicitly_wait(10)
    data=BeautifulSoup(driver.page_source,'html.parser') #reading and parsing data using beautifulsoap
    new_data=data.a.span
    #time.sleep(2)
    final_data=new_data['title'] #extracting the number of followers
    final_data=int(final_data.replace(',',''))
    final_data
    dic[i]=final_data
    top_5.append(i)#appending the handlers name
for i in dic:
    top_5_followers.append(dic[i])
for i in range(len(top_5_followers)):
    val=top_5_average_like[i]/top_5_followers[i]#clacuting the average
    average_followers_likes.append(val)
for i in range(len(top_5_followers)):   
    print(top_5[i],average_followers_likes[i])


# D.Create a bar graph to depict the above obtained information.

# In[110]:


import matplotlib.pyplot as plt
plt.bar(top_5,average_followers_likes)
plt.xticks(rotation=90)
plt.xlabel('Handles')
plt.ylabel('Like vs Followers ratio')
plt.title('Handle vs Like Followers Ratio')
plt.show()


# In[ ]:




