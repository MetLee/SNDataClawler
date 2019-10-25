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

def main():
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

if __name__ == '__main__':
	main()