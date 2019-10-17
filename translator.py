import json
import requests as r


def main():
    api = 'http://translate.google.cn/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q='

    with open('datas.txt','r') as f:
        datas = json.load(f)

    counter = 0
    try:
        for journal,journalData in datas.items():
            for article in journalData:
                if not article['articleTitle_zh']:
                    _ = r.get(api+article['articleTitle_en']).content
                    result = json.loads(_)[0][0][0]
                    if result:
                        article['articleTitle_zh'] = result
                        counter += 1
                        print(counter)
    except Exception as e:
        print(e)
    finally:
        with open('datas.txt','w') as f:
            f.write(json.dumps(datas,indent=4))

if __name__ == '__main__':
	main()    