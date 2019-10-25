import json
import requests as r
import re

def getSubject_Science(URL):  #throw(Exception) (C++ type)
    _ = r.get(URL).text
    try:
        subjects = re.findall(r'oas_tag.query = \'subject=(.*?)\';',_)[0]
        subjectList = subjects.split('&subject=')
    except IndexError as e:
        subjectList = None
        print(e)
    except Exception as e:
        raise(e)
    return subjectList

def getSubject_Nature(URL):  #throw(Exception) (C++ type)
    _ = r.get(URL).text
    try:
        subjects = re.findall(r'<meta name="WT.z_subject_term" content="(.*?)"/>',_)[0] #这里必须用/关闭meta标签
        subjectList = subjects.split(';')
    except IndexError as e:
        subjectList = None
        print(e)
    except Exception as e:
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
                article['subject'] = result
                counter += 1
                print(counter)
    except Exception as e:
        print(e)
    finally:
        with open('datas.txt','w') as f:
            f.write(json.dumps(datas,indent=4))

if __name__ == '__main__':
	#Nature()
    Science()