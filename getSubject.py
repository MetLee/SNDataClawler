import json
import requests as r
import re

def getSubject_Science(URL):  #throw(Exception) (C++ type)
    _ = r.get(URL).content
    try:
        subject = re.findall(r'subject=([a-zA-Z\s]*?);',str(_))[0]
    except Exception as e:
        subject = None
        raise(e)
    return subject

def getSubject_Nature(URL):  #throw(Exception) (C++ type)
    _ = r.get(URL).content
    try:
        subjects = re.findall(r'<meta name="WT.z_subject_term" content="(.*?)">',str(_))[0]
        subjectList = subjects.split(';')
    except Exception as e:
        subjectList = None
        raise(e)
    return subjectList

def Science():
    with open('datas.txt','r') as f:
        datas = json.load(f)

    counter = 0
    try:
        for article in datas['Science']:
            if  'subject' not in article or article['subject'] == None:
                result = getSubject_Science(article['articleURL'])
                if result:
                    article['subject'] = result
                else:
                    article['subject'] = result
                counter += 1
                print(counter)
    except Exception as e:
        print(e)
    finally:
        with open('datas.txt','w') as f:
            f.write(json.dumps(datas,indent=4))

def Nature():
    with open('datas.txt','r') as f:
        datas = json.load(f)

    counter = 0
    try:
        for article in datas['Nature']:
            if  'subject' not in article or article['subject'] == None:
                result = getSubject_Nature(article['articleURL'])
                if result:
                    article['subject'] = result
                else:
                    article['subject'] = result
                counter += 1
                print(counter)
    except Exception as e:
        print(e)
    finally:
        with open('datas.txt','w') as f:
            f.write(json.dumps(datas,indent=4))

if __name__ == '__main__':
	Nature()