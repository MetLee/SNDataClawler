import copy
import json
import os

def merge(list1,list2,index):
    mergeResult = copy.deepcopy(list1)
    for item2 in list2:
        exist = False
        for item1 in list1:
            if item2[index] == item1[index]:
                exist = True
                break
        if not exist:
            mergeResult.append(copy.deepcopy(item2))
    return mergeResult

def analyser(data,filters=None): #filter应该为一个list
    if filters:
        result = {}
        for filter in filters: #初始化
            result[filter] = {'amount': 0, 'detail': []}

        for article in data: #计数
            subjects = article['subject']
            if subjects:
                for subject in subjects:
                    if subject in result:
                        result[subject]['amount'] += 1
                        result[subject]['detail'].append(article)

        union = {'amount': 0, 'detail': []}
        for filter in filters: #取并集
            union['detail'] = merge(union['detail'], result[filter]['detail'],'articleURL')
        union['amount'] = len(union['detail'])
        result['~union'] = union

        return result

    else: #只计数
        result = {}
        for article in data:
            subjects = article['subject']
            if subjects:
                for subject in subjects:
                    if subject in result:
                        result[subject]['amount'] += 1
                    else:
                        result[subject] = {'amount': 1}
        return result

def main():
    with open('datas.txt','r') as f:
        datas = json.load(f)

    if not os.path.exists('filters.txt'):
        result_Science = analyser(data=datas['Science'])
        with open('result_Science.txt','w') as f:
            f.write(json.dumps(result_Science,indent=4))

        result_Nature = analyser(data=datas['Nature'])
        with open('result_Nature.txt','w') as f:
            f.write(json.dumps(result_Nature,indent=4))

        result = {'Science': result_Science, 'Nature': result_Nature}
        with open('result.txt','w') as f:
            f.write(json.dumps(result,indent=4))
    else:
        with open('filters.txt','r') as f:
            filters = json.load(f)
        result_filter_Science = analyser(data=datas['Science'],filters=filters)
        result_filter_Nature = analyser(data=datas['Nature'],filters=filters)
        result_filter = {'Science': result_filter_Science, 'Nature': result_filter_Nature}
        with open('result_filter.txt','w') as f:
            f.write(json.dumps(result_filter,indent=4))

if __name__ == '__main__':
	main()   