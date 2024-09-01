'''VIDEO LINK: https://drive.google.com/file/d/1Ps5PptkEjUlUwlayed6bHClxEvaYn0_m/view?usp=drive_link'''

from cmu_graphics import *
import random

class ListElement:
    def __init__(self, val, listLength):
        listSpacing = 210/listLength
        whiteSpace = listSpacing*(listLength-1)
        totalLength = 540
        self.height = val * (190/listLength) #changes height based on number of elems in the list
        self.width = (totalLength - whiteSpace)/(listLength) 
        self.selected = False
        self.isCurrMaxVal = False
        self.sorted = False
        self.isTemp = False
        
    def __repr__(self):
        s1 = f'value: {self.height} isSelected: {self.selected} '
        s2 = f'isCurrMaxVal: {self.isCurrMaxVal} isSorted:{self.sorted}'
        return s1 + s2
        
class Button:
    def __init__(self, left, top, width, height, name):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.name = name
        self.selected = False
        
    def __repr__(self):
        return f'{self.name} button'
    
    def pressed(self, mouseX, mouseY):
        return ((self.left <= mouseX <= self.left+self.width) and 
                (self.top <= mouseY <= self.top+self.height))
                
def onAppStart(app):
    app.width = 800
    app.height = 600
    app.listLen = 16
    app.currListLen = ''
    app.elemBottom = 300
    app.stepSpacing = 20
    buttonNames = ['New Sort', 'Run', 'Pause', 'Step', 'Fast Mode', 'New Size']
    buttonTops = [100 + i*67 for i in range(6) ]
    app.buttons = [Button(696, top, 80, 50, name) for top, name in zip(buttonTops, buttonNames)]
    restart(app)

def restart(app):
    getNewList(app)
    app.timer = 0
    app.totalComparisons = 0
    app.copies = 0
    app.run = False
    app.pause = False
    app.gameStart = True
    app.drawChangeSize = False
    app.sortedStartIndex = len(app.mainList) #start of the part of the list thats sorted
    app.currIndex = 0
    app.currMaxIndex = -1
    app.tempElem = None
    
def getNewList(app):
    valList = [i for i in range(1,app.listLen+1)]
    app.listSpacing = 210/len(valList)
    random.shuffle(valList)
    app.mainList = [ListElement(val, app.listLen) for val in valList]
    
def redrawAll(app):
    drawBackground(app)
    drawButtons(app)
    drawList(app)
    if app.drawChangeSize: drawChangeSize(app)
    
def drawBackground(app):
    drawRect(80, 100, 560, 400, fill='snow', border='darkOliveGreen')
    drawLabel('Visual Selection Sort', 154, 80, size = 16)
    drawLabel(f'Comparisons: {app.totalComparisons}', 728, 560)
    drawLabel(f'Copies: {app.copies}', 751, 580)
    drawLabel('Temp', 360, 484, bold=True)

def drawButtons(app):
    for button in app.buttons:
        if (button.name == 'Pause'):
            color = 'grey' if app.pause else 'lightGray'
        elif (button.name == 'Run'):
            color = 'grey' if app.run else 'lightGray'
        else:
            color = 'grey' if button.selected else 'lightGray'
        drawRect(button.left, button.top, 
                button.width, button.height, fill=color)
        drawLabel(button.name, button.left+button.width/2, 
                    button.top+button.height/2)
                    
def drawList(app):
    for i in range(len(app.mainList)):
        elem = app.mainList[i]
        elemLeft = 89 + i*(elem.width + app.listSpacing)
        elemTop = app.elemBottom - elem.height
        if elem.isTemp: 
            drawTemp(app, app.mainList[i])
            drawSelectionBorder(app, elem, elemLeft)
            continue
        if elem.selected:
            drawSelectionBorder(app, elem, elemLeft)
        if elem.isCurrMaxVal:
            drawCurrMaxLabel(app, elem, elemLeft)
            drawSelectionBorder(app, elem, elemLeft)
        color = 'black' if elem.sorted else 'lightSteelBlue'
        drawRect(elemLeft, elemTop, elem.width, elem.height, fill = color, 
                border = 'black', borderWidth = 1)
                
def drawTemp(app, elem):
    elemBottom = 470
    elemCenter = 361
    elemLeft = elemCenter - elem.width/2
    drawRect(elemLeft, elemBottom-(elem.height*0.8), elem.width, elem.height*0.8,
            fill = 'lightSteelBlue', border = 'black', borderWidth = 1)
                
def drawSelectionBorder(app, elem, elemLeft):
    borderOffSet = 4
    drawRect(elemLeft-borderOffSet, 106, elem.width+(2*borderOffSet), 
                (app.elemBottom-106)+borderOffSet, fill = None, border='green')

def drawCurrMaxLabel(app, elem, elemLeft):
    maxLabelOffSet = 10
    drawLabel('MAX', elemLeft + elem.width/2, app.elemBottom + maxLabelOffSet)
    
def drawChangeSize(app):
    s1 = 'Please enter numbers to input the new size;'
    s2 =  'then press enter to enact the change (maximum size of 32)'
    drawLabel(f'New Size: {app.currListLen}', 725, 503)
    drawLabel(s1 + s2, 505, 523)
        
                    
def onMousePress(app, mouseX, mouseY):
    button = buttonPressed(app, mouseX, mouseY)
    if (button != None):
        if (button == 'New Sort'):
            newSortHelper(app)
        elif (button == 'Run'):
            runHelper(app)
        elif (button == 'Pause'):
            pauseHelper(app)
        elif (button == 'Step'):
            stepHelper(app)
        elif (button == 'Fast Mode'):
            fastModeHelper(app)
        elif (button == 'New Size'):
            newSizeHelper(app)

def buttonSelectionHelper(app, name):
    for button in app.buttons:
        if (button.name == name):
            button.selected = not button.selected
    
def buttonPressed(app, mouseX, mouseY):
    for button in app.buttons:
        if button.pressed(mouseX, mouseY):
            return button.name
    return None
    
def newSortHelper(app):
    restart(app)
    
def runHelper(app):
    if app.run: return
    if app.gameStart: app.gameStart = False
    app.run = True
    app.pause = False
    
def pauseHelper(app):
    if app.pause: return
    app.run = False
    app.pause = True
    
def stepHelper(app):
    takeStep(app)
    
def fastModeHelper(app):
    buttonSelectionHelper(app, 'Fast Mode')
    app.stepSpacing = 20 if (app.stepSpacing == 10) else 10
    
def newSizeHelper(app):
    if app.drawChangeSize: return
    buttonSelectionHelper(app, 'New Size')
    app.drawChangeSize = True
    if (not app.pause):
        app.pause = True
        buttonSelectionHelper(app, 'Pause')
    
def onKeyPress(app, key):
    if (app.drawChangeSize):
        if (key == 'enter'):
            if (0 <= int(app.currListLen) <= 32):
                app.listLen = app.sortedStartIndex = int(app.currListLen)
                app.currListLen = ''
                app.drawChangeSize = False
                buttonSelectionHelper(app, 'New Size')
                getNewList(app)
                restart(app)
        if (key == 'backspace'):
            if (app.currListLen != ''):
                app.currListLen = app.currListLen[:-1]
        if (key.isdigit()) and (len(app.currListLen) < 2):
            app.currListLen += key
    
def takeStep(app):
    if (app.sortedStartIndex == 0): return
    if (app.sortedStartIndex == 1):
        app.mainList[0].sorted = True
        app.mainList[0].selected = False
        app.totalComparisons += 1
        app.sortedStartIndex -= 1
        return
    currElem = app.mainList[app.currIndex] 
    if (app.currIndex == app.sortedStartIndex-1):#done looping this round
        maxElem = app.mainList[app.currMaxIndex]
        if (app.tempElem != None): #mid switch
            swapVals(app)
            maxElem.sorted = True
            app.mainList[app.currMaxIndex].selected = False
            app.mainList[app.sortedStartIndex-1].selected = False
            maxElem.isCurrMaxVal = maxElem.isTemp = False
            app.sortedStartIndex -= 1
            startNewRun(app)
            return 
        else: 
            if (maxElem.height<currElem.height):
                maxElem.isCurrMaxVal = maxElem.selected = False
                maxElem = currElem
                maxElem.isCurrMaxVal = True
                app.currMaxIndex = app.currIndex
                app.totalComparisons += 1
                return
            app.tempElem = maxElem 
            maxElem.isTemp = True
            app.totalComparisons += 1
            return
    if (app.currIndex == 0):
        if (not app.currIndex == app.sortedStartIndex-1):
            nextElem = app.mainList[1]
            currElem.selected = nextElem.selected = True
            currElem.isCurrMaxVal = True
            app.currMaxIndex = 0
            app.currIndex += 1
            app.totalComparisons += 1
            return
    else:
        maxElem = app.mainList[app.currMaxIndex]
        if (currElem.height > maxElem.height):
            maxElem.isCurrMaxVal, currElem.isCurrMaxVal = False, True
            maxElem.selected = False
            app.currMaxIndex = app.currIndex
        else:
            currElem.selected = False
        app.currIndex += 1
        app.mainList[app.currIndex].selected = True
        app.totalComparisons += 1
        return
    
def swapVals(app):
    temp = app.mainList[app.currMaxIndex]
    app.mainList[app.currMaxIndex] = app.mainList[app.sortedStartIndex-1]
    app.mainList[app.sortedStartIndex-1] = temp

def startNewRun(app):
    app.currIndex = 0
    app.currMaxIndex = -1
    app.tempElem = None
    app.copies += 1
            
def onStep(app):
    if ((not app.pause) and (app.timer % app.stepSpacing == 0)
        and (not app.gameStart)):
        takeStep(app)
    app.timer += 1
        
def main():
    runApp()
    
main()