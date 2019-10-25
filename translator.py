import json
import requests as r


def translate(string,fr='en',to='zh'): #throw(Exception) (C++ type)
    api = 'http://translate.google.cn/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q='
    _ = r.get(api+string).text
    try:
        result = json.loads(_)[0][0][0]
    except Exception as e:
        result = None
        raise(e)
    return result


def main():
    with open('datas.txt','r') as f:
        datas = json.load(f)

    counter = 0
    try:
        for journal,journalData in datas.items():
            for article in journalData:
                if not article['articleTitle_zh']:
                    result = translate(article['articleTitle_en'])
                    if result:
                        article['articleTitle_zh'] = result
                    else:
                        article['articleTitle_zh'] = None
                    counter += 1
                    print(counter)
    except Exception as e:
        print(e)
    finally:
        with open('datas.txt','w') as f:
            f.write(json.dumps(datas,indent=4))

if __name__ == '__main__':
	main()    