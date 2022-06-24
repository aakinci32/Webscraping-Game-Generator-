from bs4 import BeautifulSoup
import requests

source = requests.get('https://www.pro-football-reference.com/years/2018/week_19.htm').text

soup = BeautifulSoup(source, 'lxml')

games = soup.find_all('table', class_= "teams")


def createGameDictionary():
    d = {}
    for gameNumber in range(len(games)):
        components = (games[gameNumber].find_all('td'))

        result = []
    
        # remove html tags from string
        for i in range(len(components)):
            #checks if it is wasteful info
            if i == 3 or i == 6 or i == 7:
                continue
            item = str(components[i])
            index1 = item.find('>')
            index2 = str(item[index1+1:]).find('</')
            content =(str(components[i]))[index1 + 1: index2 + index1 + 1]
            result.append(content)

        #gets rid of extra info next to teams
        def filterTeamInfo(result):
            for i in [1, 3]:
                item1 = str(result[i])
                index1 = item1.find('>')
                result[i] = item1[index1+1:]
            return result


        result = filterTeamInfo(result)

        #turn the result into the dictionary
        d[result[1]] = [result[0], result[3], result[2], result[4]]
        d[result[3]] = [result[0], result[1], result[4], result[2]]
    return d


d = createGameDictionary()
print(d)