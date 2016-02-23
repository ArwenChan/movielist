from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


def getdata(year):
    movies = []
    for i in range(25):
        url = "http://movie.douban.com/tag/" + year + "?start=" + str(i * 20) + "&type=S"
        text = urlopen(url).read()
        soup = BeautifulSoup(text, 'html.parser')
        items = soup.find_all('div', 'pl2')
        flag = False
        for item in items:
            movie = {}
            info = str(item.p.string).split(' / ')
            if '纪录片' in info:
                continue
            if '真人秀' in info:
                continue
            if '脱口秀' in info:
                continue
            if '戏曲' in info:
                continue
            # 时间小于60分钟的过滤
            timekey = 0
            for key, eachinfo in enumerate(info):
                if '分钟' in eachinfo:
                    timekey = key
                    break
            minutes = 100
            # 没有分钟的默认100分钟
            if timekey:
                try:
                    minutes = int(info[timekey][:-2])
                except:
                    pass
            if minutes <= 60:
                continue

            # 分数少于8.2的过滤掉
            try:
                rating = float(item.div.find('span', 'rating_nums').string)
            except:
                continue
            if rating <= 8.2:
                flag = True
                break

            # 评分人数少于100的过滤掉
            try:
                rates_nums = int(item.div.find('span', 'pl').string[1:-1][:-3])
            except:
                continue
            if rates_nums < 100:
                continue

            #  只取第一个‘小名’，名字含有第＊季的归电视剧，过滤
            movie_name = [re.split('[\n/]+', x)[0].strip() for x in item.a.stripped_strings]
            istv = re.compile("\u7b2c[\u4e00-\u56db\u0030-\u0039\u0000-\u0009]+[\u5b63\u96c6\u8bdd]")
            if istv.search(movie_name[0]):
                continue
            try:
                if istv.search(movie_name[1]):
                    continue
            except:
                pass

            movie['name'] = movie_name
            movie['info'] = info
            movie['rating'] = rating
            movie['rates_nums'] = rates_nums
            movies.append(movie)
        if flag:
            break
#    for movie in movies:
#        print(movie)
#        print()
#    print(len(movies))
    return movies

# if __name__ == '__main__':
#    store.store(getdata('2005'), '2005')
