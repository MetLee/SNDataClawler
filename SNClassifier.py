
import json
import re
import requests as r
from bs4 import BeautifulSoup as bs

def translate(string,fr='en',to='zh'):
    api = 'http://translate.google.cn/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q='

    _ = r.get(api+string).content
    try:
        result = json.loads(_)[0][0][0]
    except Exception as e:
        print(e)
        result = None
    return result

def getIssueURLList_Science(fr=2015,to=2019):
    issueURLs = []

    if fr > to:
        return []
    else:
        for year in range(fr, to+1):
            archiveURL = 'https://science.sciencemag.org/content/by/year/' + str(year)
            _ = r.get(archiveURL).content
            soup = bs(_, features='lxml')
            issues = soup.find(class_='archive-issue-list') #定位

            if issues:
                issueList = issues.contents[1]
                for issue in issueList.children: #遍历issue
                    issueURL = 'https://science.sciencemag.org' + issue.a.attrs['href'] #需要补全
                    issueURLs.append(issueURL)
            else:
                continue
        return issueURLs   

def getArticleDataListByIssueURL_Science(URL):
    datas = []
    _ = r.get(URL).content
    soup = bs(_, features='lxml')
    articles = soup.find(class_='issue-toc-section-research-articles') #定位 research article 板块

    if articles:
        articleList = articles.contents[1]
        for article in articleList.children: #遍历每篇文章
            target = article.find(class_='highwire-cite-linked-title')

            if target:
                articleTitle_en = target.get_text() #使用 .string 会无法识别<sup></sup>
                articleTitle_zh = translate(articleTitle_en)
                articleURL = 'https://science.sciencemag.org' + target.attrs['href'] #需要补全
                data = {
                    'articleTitle_en': articleTitle_en,
                    'articleTitle_zh': articleTitle_zh,
                    'articleURL': articleURL}
                datas.append(data)
            else:
                continue
        return datas
    else:
        return []

def getVolumeURLList_Nature(fr=2015,to=2019):
    volumeURLs = []

    if fr > to:
        return []
    else:
        archiveURL = 'https://www.nature.com/nature/volumes'
        _ = r.get(archiveURL).content
        soup = bs(_, features='lxml')

        for year in range(fr, to+1):
            yearTag = soup.find(lambda tag:tag.string == str(year)) #定位标题年份
            volumeList = yearTag.next_sibling
            while volumeList.string == '\n':
                volumeList = volumeList.next_sibling #跳过空白行

            volumeList = volumeList.find_all('a')
            for volume in volumeList:
                volumeURL = 'https://www.nature.com' + volume.attrs['href'] #需要补全
                volumeURLs.append(volumeURL)

        return volumeURLs

def getIssueURLListByVolumeURL_Nature(volumeURL):
    issueURLs = []
    _ = r.get(volumeURL).content
    soup = bs(_, features='lxml')
    issues = soup.find(id='issue-list')

    for issue in issues.children:
        if issue.string == '\n':
            continue #跳过空白行
        else:
            issueURL = 'https://www.nature.com' + issue.a.attrs['href'] #需要补全
            issueURLs.append(issueURL)

    return issueURLs

def getIssueURLList_Nature(fr=2015,to=2019):
    issueURLs = []

    if fr > to:
        return []
    else:
        volumeURLs = getVolumeURLList_Nature(fr,to)
        for volumeURL in volumeURLs:
            issueURLs_volume = getIssueURLListByVolumeURL_Nature(volumeURL)
            issueURLs += issueURL_volume
        return issueURLs

def getArticleDataListByIssueURL_Nature(URL):
    datas = []
    _ = r.get(URL).content
    soup = bs(_, features='lxml')

    research =  soup.find(attrs={'aria-labelledby':'Research'})

    if research:
        articleTag = research.find(lambda tag:tag.string == 'Articles')
        letterTag = research.find(lambda tag:tag.string == 'Letters') #定位
        article = articleTag.next_sibling

        while not article == letterTag:
            if article.string == '\n':
                pass #跳过空白行
            else:
                articleTitle_en = re.findall(r'\s*(.*)',article.a.get_text())[0] #处理掉句首的空白字符
                articleTitle_zh = translate(articleTitle_en)
                articleURL = 'https://www.nature.com' + article.a.attrs['href'] #需要补全
                data = {
                    'articleTitle_en': articleTitle_en,
                    'articleTitle_zh': articleTitle_zh,
                    'articleURL': articleURL}
                datas.append(data)
            article = article.next_sibling
        return datas
    else:
        return []

def main():
    datas = {'Science':[],'Nature':[]}

    #Science
    issueURLs_Science = getIssueURLList_Science()
    for issueURL_Science in issueURLs_Science:
        data = getArticleDataListByIssueURL_Science(issueURL_Science)
        datas['Science'] += data

    #Nature
    issueURLs_Nature = getIssueURLList_Nature()
    for issueURL_Nature in issueURLs_Nature:
        data = getArticleDataListByIssueURL_Nature(issueURL_Nature)
        datas['Nature'] += data

    #output
    with open('datas.txt','w') as f:
        f.write(json.dumps(datas,indent=4))

if __name__ == '__main__':
	main()          