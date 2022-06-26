from bs4 import BeautifulSoup
import requests
from cmu_112_graphics import *

#----------------------------------------
def appStarted(app):
    app.teams = app.loadImage("all-32-nfl-teams-logos.webp")
    app.selectedRow = None
    app.selectedCol = None
    app.selectedCity = None
    app.selectedName = None


#---------------------------------------

def mousePressed(app, event):
    #checks if click is inside grid of teams
    if (event.x > 0.2 * app.width) and (event.y < 0.5 * app.height):
        app.selectedRow = (event.y) // 100
        app.selectedCol = (event.x - 200) // 100
        assignRowColToTeam(app, event)
    #checks if inside grid of weeks
    if ((event.x) > 0.2*app.width and (event.x<0.8*app.width) and 
        event.y > 0.5 * app.height and event.y < 0.72 * app.height):
        pass
    print('(x, y) ', (event.x, event.y))
    

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




#---------------------------------------
def redrawAll(app, canvas):
    drawTeamLogos(app, canvas)
    drawWeekChoices(app, canvas)
    drawYearChoices(app, canvas)
    drawSubmitButton(app, canvas)



def drawWeekChoices(app, canvas):
    canvas.create_text(app.width/10, 16*app.height/30, text = 'Pick a Week',
                    font = 'Impact 30')
    canvas.create_text(app.width/2, 17*app.height/30, 
                    text = '1         2         3         4         5         6  ', 
                    font  = 'Arial 30')        
    canvas.create_text(app.width/2, 19*app.height/30, 
                    text = ' 7         8         9         10        11       12', 
                    font = 'Arial 30')
    canvas.create_text(0.47*app.width, 21*app.height/30, 
                    text = '13        14         15        16         17', 
                    font = 'Arial 30')
    canvas.create_text(0.5*app.width, 23*app.height/30, 
                    text = 'Playoffs Rd. 1    Playoffs Rd. 2    Conference Finals  Super Bowl', font = 'Arial 27')
                    

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
    canvas.create_rectangle(0.8*app.width, 0.9*app.height, 0.99*app.width, 
                            0.97*app.height, fill = 'green', outline = 'black')
    canvas.create_text(0.9*app.width, 0.935*app.height, text = 'Submit', 
                        font = 'impact 30', fill = 'white')

#draws the year choices 
def drawYearChoices(app, canvas):
    canvas.create_text(app.width/10, 0.84*app.height, text = 'Pick A Year:', 
                        font = 'impact 30')



#--------------------------------------


runApp(width = 1000, height = 750)
