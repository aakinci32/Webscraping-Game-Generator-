from bs4 import BeautifulSoup
import requests
from cmu_112_graphics import *

#----------------------------------------
def appStarted(app):
    resetApp(app)

def resetApp(app):
    app.teams = app.loadImage("all-32-nfl-teams-logos.webp")
    app.selectedRow = None
    app.selectedCol = None
    app.selectedCity = None
    app.selectedName = None
    app.selectedWeekRow = None
    app.selectedWeekCol = None
    app.selectedWeek = None
    app.selectedYearRow = None
    app.selectedYearCol = None
    app.games = None
    app.players = None
    
    app.pickATeamAndWeek = True
    app.pickAYear = False
    app.resultsMode = False
    app.hasGame = None



#---------------------------------------

def mousePressed(app, event):
    if app.pickATeamAndWeek == True:
        #checks if click is inside grid of teams
        if (event.x > 0.2 * app.width) and (event.y < 0.5 * app.height):
            app.selectedRow = (event.y) // 100
            app.selectedCol = (event.x - 200) // 100
            assignRowColToTeam(app, event)
        #checks if inside first row in grid of weeks
        if ((event.x) > 0.2*app.width and (event.x<0.8*app.width) and 
            event.y > 0.53 * app.height and event.y < 0.6 * app.height):
            app.selectedWeekCol = (event.x - 227) // 94
            app.selectedWeekRow = 0
        elif ( (event.x > 0.2*app.width) and (event.x<0.8*app.width) and 
            event.y>0.6*app.height and event.y<0.66*app.height):
            app.selectedWeekCol = (event.x - 227) // 94
            app.selectedWeekRow = 1
        elif ( (event.x > 0.2*app.width) and (event.x<0.8*app.width) and 
            event.y>0.66*app.height and event.y<0.72*app.height):
            app.selectedWeekCol = (event.x - 235) // 95
            app.selectedWeekRow = 2
        elif ( (event.x > 0.1*app.width) and (event.x<0.9*app.width) and 
            event.y>0.73*app.height and event.y<0.79*app.height):
            app.selectedWeekRow = 3
            app.selectedWeekCol = (event.x - 130) // 200
        assignRowColToWeek(app, event)
        isYearButtonPressed(app, event)
    if app.pickAYear == True:
        isBackButtonPressed(app, event)
        #assigns click to a row and column
        app.selectedYearRow = (event.y - 170) // 37
        app.selectedYearCol = (event.x - 120) // 80
        #fixes bug from transition between modes
        if app.selectedYearRow >= 10: 
            app.selectedYearRow, app.selectedYearCol = None, None
        #checks if inside grid of years
        if (event.x > 0.12*app.width and event.y>0.2*app.height and 
        event.x<0.88*app.width and event.y < 0.66 * app.height):   
            assignRowColToYear(app, event)
        isYearToSubmitButtonPressed(app, event)
    if app.resultsMode == True:
        buildURL(app, event)
        if doesTeamHaveGame(app, event) == False: 
            app.hasGame = False
        else:
            app.hasGame = True
            buildPlayerStatsURL(app, event)
        #checks if Home button is pressed
        if (event.x < 0.9 * app.width and event.x > 0.7 * app.width and 
            event.y > 0.05 * app.height and event.y < 0.15 * app.height):
            resetApp(app)

#builds the URL used to webscrape the players on the teams play9ing
def buildPlayerStatsURL(app, event):

    URL = 'https://www.cbssports.com/nfl/gametracker/boxscore/NFL_'
    opponent = getOpponentCity(app, event)
    #gets the home team 
    homeTeam = None
    awayTeam = None

    for team in app.games:
        if team == app.selectedCity + ' ' + app.selectedName:
            homeTeam = app.games[team][1]
            awayTeam = app.selectedCity + ' ' + app.selectedName
            break

        elif app.selectedCity + ' ' + app.selectedName == (app.games[team])[1]:
            homeTeam = app.selectedCity + ' ' + app.selectedName
            awayTeam = team
            break
    [homeAbbrev, awayAbbrev] = getAbbrevFromCity(homeTeam, awayTeam)
    numericDate = getNumericDateFromGame(app, event)
    URL += numericDate + '_' + f'{awayAbbrev}@{homeAbbrev}/'
    app.players = webScrapePlayers(URL)

#webscrapes for all the players
def webScrapePlayers(URL):
    source = requests.get(URL).text
    soup = BeautifulSoup(source, 'lxml')
    players = soup.find_all('div', class_= "player-name-num-pos")

    result = []
    for i in range(len(players)):
        fullString = str(players[i])
        fullString = fullString[82:]
        subString = fullString.split(' ')
        try: name = subString[0] + ' ' + subString[1]
        except: continue
        name = name[:-2]
        index1 = fullString.index('>')
        index2 = (fullString[index1+1:]).find('<')
        
        subString = (fullString[index1:index2 + index1 +1])[1:]
        subString = subString.split(' ')
        number, position = subString[0], subString[1]
        if ( (name,number, position) not in result and position != 'K' and
        position != 'P'):
            result.append( (name, number, position) )
    print(result)
    return result

    


#turns any date to numbers, YEARMMDD
#ex.) September 12, 2021  -> 20210912
def getNumericDateFromGame(app, event):
    fullName = app.selectedCity + ' ' + app.selectedName
    result = ''
    for team in app.games:
        if team == fullName:
            date = app.games[fullName][0]
    splitString = date.split(' ')
    wordsToNumber = {'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12', 
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04' }
    result += splitString[2]
    result += wordsToNumber[splitString[0]]
    result+=(splitString[1])[:-1] 
    return result
    
    
    




#gets the acronyms for the city names
def getAbbrevFromCity(homeTeam, awayTeam):
    result = []
    cityAcronyms= {'Arizona' : 'ARI', 'Atlanta': 'ATL', 
        'Baltimore': 'BAL', 'Buffalo': 'BUF', 'Carolina': 'CAR', 
        'Chicago': 'CHI', 'Cincinnati': 'CIN' , 'Cleveland': 'CLE', 
        'Dallas': 'DAL', 'Denver': 'DEN', 'Detroit': 'DET', 'Green Bay': 'GB' ,
        'St. Louis': 'STL', 'San Diego': 'SD', 'Oakland': 'OAK', 'Houston': 'HOU', 
        'Indianapolis': 'IND', 'Jacksonville': 'JAC', 'Kansas City': 'KC', 
        'Las Vegas': 'LV', 'Los Angeles Chargers': 'LAC', 
        'Los Angeles Rams': 'LAR', 'Miami': 'MIA', 'Minnesota': 'MIN', 
        'New England': 'NE','New Orleans': 'NO', 'New York Giants': 'NYG', 
        'New York Jets': 'NYJ', 'Philadelphia': 'PHI', 'Pittsburgh': 'PIT',
        'San Francisco': 'SF', 'Seattle': 'SEA', 'Tampa Bay': 'TB', 
        'Tennessee': 'TEN', 'Washington': 'WAS' }
    for team in [homeTeam, awayTeam]:
        if team == 'Washington Football Team' or team == 'Washington Redskins':
            acronym = 'WAS'
        else:
            teamList = team.split(' ')
            teamList.pop()
            cityName = ''
            for word in teamList:
                cityName += word + ' '
            cityName = cityName[:-1]
            if cityName == 'New York' or cityName == 'Los Angeles':
                acronym = cityAcronyms[team]
            else:
                acronym = cityAcronyms[cityName]
        result.append(acronym)
    return result


#gets the city of the opponent of the selected team
def getOpponentCity(app, event):
    for team in app.games:
        if team == app.selectedCity + ' ' + app.selectedName:
            return (app.games[app.selectedCity + ' ' + app.selectedName])[1]


#buils the URL used to webscrape the score and data
def buildURL(app, event):
    URL = 'https://www.pro-football-reference.com/years/'
    URL += f'{app.selectedYear}/week_{app.selectedWeek}.htm'
    source = requests.get(URL).text
    soup = BeautifulSoup(source, 'lxml')
    games = soup.find_all('table', class_= "teams")
    app.games = createGameDictionary(games)

#returns a dictionary of the games during a given week and year
def createGameDictionary(games):
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

#checks if the selected team has a game that week
def doesTeamHaveGame(app, event):
    for fullName in app.games:
        if fullName == app.selectedCity + " " + app.selectedName:
            return True
    if app.selectedName == 'Rams':
        app.selectedCity = 'St. Louis'
        return True
    elif app.selectedName == 'Chargers':
        app.selectedCity = 'San Diego'
        return True
    elif app.selectedName == 'Raiders':
        app.selectedCity = 'Oakland'
        return True
    elif app.selectedCity == 'Washington':
        if app.selectedYear == 2021 or app.selectedYear == 2020:
            app.selectedName = 'Football Team'
            return True
        else:
            app.selectedName = 'Redskins'
            return True
    elif app.selectedName == 'Cardinals':
        app.selectedCity = 'Phoenix'
    elif app.selectedName == 'Colts':
        app.selectedCity = 'Baltimore'
    return False
    


def isYearToSubmitButtonPressed(app, event):
    if (event.x > 0.7 * app.width and event.x < 0.9 * app.width and 
    event.y > 0.8 * app.height and event.y < 0.98 * app.height):
        app.pickAYear = False
        app.resultsMode = True


#takes in a row and column to a year
def assignRowColToYear(app, event):
    d = { (0,0): 2022, (0,1): 2021, (0,2): 2020, (0,3): 2019, (0,4): 2018, 
        (0,5): 2017, (0,6): 2016, (0,7): 2015, (0,8): 2014, (0,9): 2013, 
        (1,0): 2012, (1,1): 2011, (1, 2): 2010, (1,3): 2009, (1,4): 2008, 
        (1, 5): 2007, (1, 6): 2006, (1, 7): 2005, (1, 8): 2004, (1,9): 2003, 
        (2, 0): 2002, (2, 1): 2001, (2,2): 2000, (2, 3): 1999, (2, 4): 1998, 
        (2, 5): 1997, (2, 6): 1996, (2, 7): 1995, (2, 8): 1994, (2, 9): 1993, 
        (3, 0): 1992, (3, 1): 1991, (3,2): 1990, (3, 3): 1989, (3, 4): 1988, 
        (3, 5): 1987, (3, 6): 1986, (3, 7): 1985, (3, 8): 1984, (3,9): 1983, 
        (4, 0): 1982, (4, 1): 1981, (4, 2): 1980, (4, 3): 1979, (4, 4): 1978,
        (4, 5): 1977, (4, 6): 1976, (4, 7): 1975, (4, 8): 1974, (4, 9): 1973,
        (5, 0): 1972, (5, 1): 1971, (5, 2): 1970, (5, 3): 1969, (5, 4): 1968, 
        (5, 5): 1967, (5, 6): 1966, (5, 7): 1965, (5, 8): 1964, (5, 9): 1963, 
        (6, 0): 1962, (6, 1): 1961, (6, 2): 1960, (6, 3): 1959, (6, 4): 1958, 
        (6, 5): 1957, (6, 6): 1956, (6, 7): 1955, (6, 8): 1954, (6, 9): 1953,
        (7, 0): 1952, (7, 1): 1951, (7, 2): 1950, (7,3): 1949, (7, 4): 1948,
        (7, 5): 1947, (7, 6): 1946, (7, 7): 1945, (7, 8): 1944, (7, 9): 1943, 
        (8, 0): 1942, (8, 1): 1941, (8, 2): 1940, (8, 3): 1939, (8, 4): 1938, 
        (8, 5): 1937, (8, 6): 1936, (8, 7): 1935, (8, 8): 1934, (8, 9): 1933 }
    if app.selectedYearRow != None:
        app.selectedYear = d[(app.selectedYearRow, app.selectedYearCol)]

#checks if the back button is pressed on the Pick A Year Page
def isBackButtonPressed(app, event):
    if (event.x > 0.05 * app.width and event.x < 0.15 * app.width 
    and event.y > 0.05 * app.height and event.y < 0.15*app.height):
        app.pickATeamAndWeek = True
        app.pickAYear = False



#checks if the year button is pressed 
def isYearButtonPressed(app, event):
    if (event.x > 0.3*app.width and event.x < 0.7 * app.width and 
        event.y > 0.83 * app.height and event.y < 0.97 * app.height):
        app.pickATeamAndWeek = False
        app.pickAYear = True
    
#takes in the row and column and then assigns the corresponding team
def assignRowColToTeam(app, event):
    rowColDict = { (0, 0): ['Arizona', 'Cardinals'],
                    (0, 1): ['Atlanta', 'Falcons'],
                    (0, 2): ['Baltimore', 'Ravens'],
                    (0, 3): ['Buffalo', 'Bills'], 
                    (0, 4): ['Carolina', 'Panthers'],
                    (0, 5): ['Chicago', 'Bears'], 
                    (0, 6): ['Cincinnati', 'Bengals'], 
                    (0, 7): ['Cleveland', 'Browns'],
                    (1, 0): ['Dallas', 'Cowboys'], 
                    (1, 1): ['Denver', 'Broncos'],
                    (1, 2): ['Detroit', 'Lions'], 
                    (1, 3): ['Green Bay', 'Packers'], 
                    (1, 4): ['Houston', 'Texans'], 
                    (1, 5): ['Indianapolis', 'Colts'],
                    (1, 6): ['Jacksonville', 'Jaquars'], 
                    (1, 7): ['Kansas City', 'Chiefs'],
                    (2, 0): ['Las Vegas', 'Raiders'],
                    (2, 1): ['Los Angeles', 'Chargers'],
                    (2, 2): ['Los Angeles', 'Rams'],
                    (2, 3): ['Miami', 'Dolphins'],
                    (2, 4): ['Minnesota', 'Vikings'],
                    (2, 5): ['New England', 'Patriots'],
                    (2, 6): ['New Orleans', 'Saints'],
                    (2, 7): ['New York', 'Giants'],
                    (3, 0): ['New York', 'Jets'], 
                    (3, 1): ['Philadelphia', 'Eagles'], 
                    (3, 2): ['Pittsburgh', 'Steelers'],
                    (3, 3): ['San Francisco', '49ers'],
                    (3, 4): ['Seattle', 'Seahawks'], 
                    (3, 5): ['Tampa Bay', 'Buccaneers'], 
                    (3, 6): ['Tennessee', 'Titans'],
                    (3, 7): ['Washington', 'Commanders'] }
    app.selectedCity = rowColDict[ (app.selectedRow, app.selectedCol) ][0]
    app.selectedName = rowColDict[ (app.selectedRow, app.selectedCol) ][1]

def assignRowColToWeek(app, event):
    if app.selectedWeekRow != None and app.selectedWeekRow <= 2: 
        app.selectedWeek = 6*app.selectedWeekRow + app.selectedWeekCol + 1
    else:
        #playoff weeks
        d = { (3, 0): 18, (3,1): 19, 
        (3,2): 20, (3, 3): 21, (None, None): None}
        app.selectedWeek = d[(app.selectedWeekRow, app.selectedWeekCol)]
        
#---------------------------------------
def redrawAll(app, canvas):
    if app.pickATeamAndWeek == True:
        drawTeamLogos(app, canvas)
        drawWeekChoices(app, canvas)
        drawSubmitButton(app, canvas)
    elif app.pickAYear == True:
        drawYearChoices(app, canvas)
        drawYearToSubmitButton(app, canvas)
    elif app.resultsMode == True:
        drawHomeButton(app, canvas)
        if app.hasGame == True: 
            drawGameResults(app, canvas)
            drawPlayers(app, canvas)
        elif app.hasGame == False:
            #draw "NO GAME" SCREEN
            drawNoGameResults(app, canvas)

def drawPlayers(app, canvas):
    counter = 0
    for stats in app.players:
        counter += 1
        canvas.create_text((0.20 * (counter//12)) * app.width + 0.1 * app.width, 
                            (0.05 * (counter % 12)) * app.height + 0.35 * app.height, 
                            text = stats)

        pass


#draws the Home BUtton on the result page
def drawHomeButton(app, canvas):
    canvas.create_rectangle(0.7*app.width, 0.05*app.height, 0.9*app.width, 
                            0.15*app.height, fill = 'red')
    canvas.create_text(0.8*app.width, 0.1*app.height, text = 'Home', 
                        font  = 'Arial 25')

#draws "No Game Founded"
def drawNoGameResults(app, canvas):
    canvas.create_text(app.width/2, app.height/2, 
text = f'''The {app.selectedCity} {app.selectedName}
didn't have a game this week.''', 
font = 'Impact 50')


#draws the results of the game that was founded
def drawGameResults(app, canvas):
    for team in app.games:
        fullSelectedTeamName = app.selectedCity + ' ' + app.selectedName
        if team == fullSelectedTeamName:
            #draws the date
            canvas.create_text(app.width/2, app.height/12, 
            text = (app.games[fullSelectedTeamName])[0], fill = 'black',
                    font = 'Arial 40')

            #draws the score 
            them = (app.games[fullSelectedTeamName])[1]
            ourScore = (app.games[fullSelectedTeamName])[2]
            theirScore=(app.games[fullSelectedTeamName])[3]
            canvas.create_text(app.width/2, 3*app.height/12, 
            text = f'{fullSelectedTeamName}: {ourScore}\n{them}: {theirScore}', 
            font = 'Impact 50')

def drawWeekChoices(app, canvas):
    canvas.create_text(app.width/10, 16*app.height/30, text = 'Pick a Week',
                    font = 'Impact 30')
    canvas.create_text(app.width/2, 17*app.height/30, 
                    text = '1         2         3         4         5         6', 
                    font  = 'Arial 30')        
    canvas.create_text(app.width/2, 19*app.height/30, 
                    text = ' 7         8         9         10       11      12', 
                    font = 'Arial 30')
    canvas.create_text(0.47*app.width, 21*app.height/30, 
                    text = '13        14         15        16         17', 
                    font = 'Arial 30')
    canvas.create_text(0.5*app.width, 23*app.height/30, 
        text = 'Playoffs Rd. 1    Playoffs Rd. 2    Conf. Finals  Super Bowl', 
        font = 'Arial 27')
    drawSelectedWeekSquare(app, canvas)

def drawYearToSubmitButton(app, canvas):
    canvas.create_rectangle(0.7 * app.width, 0.8 * app.height, 
                            0.9 * app.width, 0.98 * app.height, fill = 'green')
    canvas.create_text(0.8*app.width, 0.89 * app.height, 
                        text = 'Click Here to Submit', font = 'Impact 20',
                        fill = 'white')
    
#draws the selected week's square 
def drawSelectedWeekSquare(app, canvas):
    if app.selectedWeekRow == 0:
        canvas.create_rectangle(0.22*app.width + app.selectedWeekCol * 90, 
                                0.53*app.height , 
                                0.22*app.width + (app.selectedWeekCol + 1) * 90,
                                0.59*app.height )
    elif app.selectedWeekRow == 1:
        canvas.create_rectangle(0.22*app.width + app.selectedWeekCol * 90, 
                                0.60*app.height, 
                                0.22*app.width + (app.selectedWeekCol + 1) * 90,
                                0.65*app.height)
    elif app.selectedWeekRow == 2:
        canvas.create_rectangle(0.22*app.width + app.selectedWeekCol * 100, 
                                0.67*app.height, 
                                0.22*app.width + (app.selectedWeekCol + 1) * 100,
                                0.72*app.height)
    elif app.selectedWeekRow == 3:
        canvas.create_rectangle(0.135*app.width + 190 * app.selectedWeekCol, 
                                0.74*app.height, 
                                0.135*app.width +190 *(app.selectedWeekCol + 1),
                                0.79 * app.height)


                    

#draws the team selection screen
def drawTeamLogos(app, canvas):
    canvas.create_text(app.width/10, app.height/30, text = 'Pick a Team:',
        font = 'Impact 30')
    canvas.create_image(0.6*app.width, 0.25*app.height, 
                        image = ImageTk.PhotoImage(app.teams))
            
    #remove surrounding space
    canvas.create_rectangle(0.21*app.width, 0.50*app.height, app.width, 
                            0.58*app.height, outline = 'white', fill = 'white')
    if app.selectedRow != None:
        canvas.create_rectangle(200 + 100*app.selectedCol, 
                                100*app.selectedRow - 15, 
                                300 + 100*app.selectedCol, 
                                100*app.selectedRow + 85)
        #displays name
        canvas.create_text(app.width/10, 4*app.height/30, 
                        text = f'{app.selectedCity}\n{app.selectedName}',
                        font = 'Impact 30')
    
#submit button for the choices page                       
def drawSubmitButton(app, canvas):
    canvas.create_rectangle(0.3*app.width, 0.83*app.height, 0.7*app.width, 
                            0.97*app.height, fill = 'green', outline = 'black')
    canvas.create_text(0.5*app.width, 0.9*app.height, 
            text = 'Click To Pick A Year', font = 'impact 30', fill = 'white')

#draws the year choices
def drawYearChoices(app, canvas):
    drawPrevInformation(app, canvas)
    canvas.create_text(0.1*app.width, 0.2 * app.height, text = 'Pick A Year: ',
                        font = 'Impact 30', fill = 'black')
    #draws all the years
    canvas.create_text(0.5 * app.width, 0.25 * app.height, 
text = '2022   2021   2020   2019   2018   2017   2016   2015   2014   2013', 
font = 'Arial 25')
    canvas.create_text(0.5 * app.width, 0.30 * app.height, 
text = '2012   2011   2010   2009   2008   2007   2006   2005   2004   2003',
font = 'Arial 25')
    canvas.create_text(0.5*app.width, 0.35 * app.height, 
text = '2002   2001   2000   1999   1998   1997   1996   1995   1994   1993', 
font = 'Arial 25')
    canvas.create_text(0.5*app.width, 0.4 * app.height, 
text = '1992   1991   1990   1989   1988   1987   1986   1985   1984   1983', 
font = 'Arial 25')
    canvas.create_text(0.5*app.width, 0.45 * app.height, 
text = '1982   1981   1980   1979   1978   1977   1976   1975   1974   1973', 
font = 'Arial 25')
    canvas.create_text(0.5*app.width, 0.5 * app.height, 
text = '1972   1971   1970   1969   1968   1967   1966   1965   1964   1963', 
font = 'Arial 25')
    canvas.create_text(0.5*app.width, 0.55 * app.height, 
text = '1962   1961   1960   1959   1958   1957   1956   1955   1954   1953', 
font = 'Arial 25')
    canvas.create_text(0.5*app.width, 0.60 * app.height, 
text = '1952   1951   1950   1949   1948   1947   1946   1945   1944   1943', 
font = 'Arial 25')
    canvas.create_text(0.5*app.width, 0.65 * app.height, 
text = '1942   1941   1940   1939   1938   1937   1936   1935   1934   1933', 
font = 'Arial 25')

    #draws surrounding box around year 
    if app.selectedYearRow != None:
                            canvas.create_rectangle (
                            0.11*app.width+app.selectedYearCol*77, 
                            171 + app.selectedYearRow * 37, 
                    0.11*app.width + (app.selectedYearCol+1)*77, 
                            171 + (app.selectedYearRow + 1) * 37)
    #gets rid of the year 2022
    canvas.create_rectangle(184, 202, 90,  166, fill = 'white', 
                        outline = 'white')




#draws the already selected information 
def drawPrevInformation(app, canvas):
    canvas.create_text(0.7*app.width, 0.05*app.height, 
text = f'''
        Selected Team: {app.selectedCity} {app.selectedName}
        Selected Week: {app.selectedWeek}''', font = 'Impact 27')
    #home button 
    canvas.create_rectangle(0.05*app.width, 0.05*app.height, 0.15*app.width,
                             0.15*app.height, fill = 'red')
    canvas.create_text(0.1*app.width, 0.1*app.height, text = 'Back', 
                        font = 'arial 20', fill = 'white')
    

#--------------------------------------


runApp(width = 1000, height = 750)
