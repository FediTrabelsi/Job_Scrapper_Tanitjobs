#you need to install
#pip install request
#pip install BeautifulSoup4

import requests
from bs4 import BeautifulSoup


#type : my user agent in google and copy the result and put it in the text below instead
my_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'
headers= {"User-Agent":my_agent}

#key words for the requirements you want in the job offer
my_pref=["Spring","JAVA","boot"]

#copy any url from tanitjobs and replace it below, in my case i searched for engineer under jobs 
baseURL='https://www.tanitjobs.com/jobs/?listing_type%5Bequal%5D=Job&action=search&keywords%5Ball_words%5D=ingenieur&GooglePlace%5Blocation%5D%5Bvalue%5D=&GooglePlace%5Blocation%5D%5Bradius%5D=50'

#max range of search pages to scrapp (a cause de la pagination)
pages_to_parcour = list(range(1,100))

#This function decides based on a logic you implliment if the job matchs your criteries, for simplicity this example just checks if one of your prefrences is listed in the requirement list of the job
def matchRequirements(job_req):
    for jReq in job_req:
        if jReq.lower().find('stage')!=-1 or jReq.lower().find('stagiaire')!=-1:
            return False
    for mReq in my_pref:
        for jReq in job_req:
            if jReq.lower().find(mReq.lower())!=-1:
                return True
    return False
        
    

#returns the list of skills or requirements for this job (hard_skills, soft_skills ...)
def getRequirmentsFromJob(job):
    requirements = []
    if job.find("div",{"class" : "bootstrap-tagsinput"}) is None:
        return []
    job_req = job.find("div",{"class" : "bootstrap-tagsinput"}).findAll("a")
    for req in job_req :
            requirements.append(req.find('span').text)
    return requirements

#returns experience Education_Level (if bac+5 Enginneer = true else Engineer=false), needed_Experience and Salary
def getJobInformations(job):
    neededData={'Engineer' : False, 'Exp' :"", "salary" : ""}
    if job.find("div",{"class" : "infos_job_details"}) is None :
        return neededData
    infos = job.find("div",{"class" : "infos_job_details"}).findAll("div")[:-1]
    
    for info in infos:
        if info.find("dl").find("dt").text.find("Experience")!= -1:
            neededData['Exp']= info.find("dl").find("dd").text
        if info.find("dl").find("dt").text.find("Rémunération proposée")!= -1:
            neededData['salary']= info.find("dl").find("dd").text
        if info.find("dl").find("dt").text.find("Niveau d'étude")!= -1:
            if info.find("dl").find("dd").text.find("Ingénieur")!=-1 or info.find("dl").find("dd").text.find("+5")!=-1 :
                neededData['Engineer']=True
            
    return neededData



f = open("search_results.txt", "w")

for page in pages_to_parcour:
    #base url to start scraping
    URL = baseURL+'&page='+str(page)
    current_page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(current_page.content,'html.parser') 
    articles = soup.find("div",{"class" : "search-results col-xs-12 col-sm-9"}).findAll('article')
    #print(soup)
    for article in articles:
        job_url = article.find("div",{"class" : "media-heading listing-item__title"}).find("a",{"class":"link"})
        job_page = requests.get(job_url['href'], headers=headers)
        job = BeautifulSoup(job_page.content,'html.parser')
        req_list = getRequirmentsFromJob(job)
        job_info = getJobInformations(job)
        #if a job matches your requirements it will be added in a file called "search_results.txt" created in the same root directory of this scrapper.py
        if matchRequirements(req_list) :
            f.write("\nJob link : "+job_url['href']+"\n")
            f.write("Basic info : "+ str(job_info)+"\nRequirements : ")
            for item in req_list:
                f.write("%s " % item)
            f.write("\n-----------------------")
            print (job_info)
            print(req_list)
            print (True)
        else:
            print (False)

        print("---------")
f.close()



