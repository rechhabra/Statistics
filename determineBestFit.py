import matplotlib.pyplot as plt #To graph 
import numpy as np #float ranges
from scipy import optimize #best fit assistance

##Methods##
def formatPrinting(listToFormat):
  #Organizing methods made code easier to debug
  return [str("("+str(i['x'])+","+str(i['y'])+")") for i in listToFormat]

def linearFunction(x,m,b):
  return m*x+b

def quadraticFunction(x,a,b,c):
  return a*x**2 + b*x + c

def sinFunction(x,a,b,c,d):
  return a*np.sin(b*x+c)+d

def logisticFunction(x,a,b,c):
  if c<-5: return 0 # overflow error with huge exponent
  return a/(1+b*np.exp(-1*(c*x)))

def getQuadraticPoints(xValues,a,b,c):
  #returns an x and y list to plot. I want to plot many for the graph because it will display more like a graph instead of connecting lines
  minX = min(xValues)
  maxX = max(xValues)
  xrange = np.arange(minX,maxX,0.1) ##Note: struggle to make it work for float without realizing arange works in numpy library
  return [xrange,[quadraticFunction(x,a,b,c) for x in xrange]]

def getSinPoints(xValues,a,b,c,d):
  minX = min(xValues)
  maxX = max(xValues)
  xrange = np.arange(minX,maxX, 0.1)
  return [xrange, [sinFunction(x,a,b,c,d) for x in xrange]]

def getLinearPoints(xValues,m,b):
  minX = min(xValues)
  maxX = max(xValues)
  xrange = np.arange(minX,maxX, 0.5)
  return [xrange, [linearFunction(x,m,b) for x in xrange]]

def getLogisticPoints(xValues,a,b,c):
  minX = min(xValues)
  maxX = max(xValues)
  xrange = np.arange(minX,maxX, 0.1)
  return [xrange, [logisticFunction(x,a,b,c) for x in xrange]]

def solveForSin(xValues,yValues):
  a,b,c,d = 1,1,1,1
  params, param_covar = optimize.curve_fit(sinFunction, xValues, yValues, maxfev=10000)
  a,b,c,d = params
  return [a,b,c,d]

def solveForQuadratic(xValues,yValues):
  a,b,c = 1,1,1
  params, param_covar = optimize.curve_fit(quadraticFunction, xValues, yValues, maxfev=10000)
  a,b,c = params
  return [a,b,c]

def solveForLinear(xValues,yValues):
  m,b = 1,1
  params, param_covar = optimize.curve_fit(linearFunction, xValues, yValues, maxfev=10000)
  m,b = params
  return [m,b]

def solveForLogistic(xValues,yValues):
  a,b,c = 1,1,1
  params, param_covar = optimize.curve_fit(logisticFunction, xValues, yValues, maxfev=1000000)
  #Logistic maxfev is high due to the time complexity of finding the best fit
  a,b,c = params
  return [a,b,c]

def graphData(listOfData,fitType,constants):
  ##listOfData is a list containing dictionaries, fitType is a string
  xValues = [i['x'] for i in listOfData]
  yValues = [i['y'] for i in listOfData]
  plt.scatter(xValues, yValues, label= "", color= "blue", marker= "o", s=30)
  ##functToGraph = np.square(xValues)
  Xs,Ys = 0,0 ###defining the variables
  if fitType=="linear":
    m,b = constants
    Xs,Ys = getLinearPoints(xValues,m,b)
    m,b = round(m,5),round(b,5)
    equationToString = "y = "+str(m)+"x + "+str(b)
  elif fitType == "quadratic":
    a,b,c = constants
    Xs,Ys = getQuadraticPoints(xValues,a,b,c)
    a,b,c = round(a,5),round(b,5),round(c,5)
    equationToString = "y = "+str(a)+"x^2 + "+str(b)+"x + "+str(c)
  elif fitType == "logistic":
    a,b,c = constants
    Xs,Ys = getLogisticPoints(xValues,a,b,c)
    a,b,c = round(a,5),round(b,5),round(c,5)
    equationToString = "y = "+str(a)+"/[1 + "+str(b)+"e^(-"+str(c)+"x)]"
  elif fitType == "sin":
    a,b,c,d = constants
    Xs,Ys = getSinPoints(xValues,a,b,c,d)
    a,b,c,d = round(a,5),round(b,5),round(c,5), round(d,5)##Note: to make the printing seem nicer
    equationToString = "y = "+str(a)+"sin("+str(b)+"x + "+str(c)+") + "+str(d)
  plt.plot(Xs,Ys)
  plt.title("The given data points using a "+fitType.upper()+" regression fit\n"+equationToString)
  plt.show()
  plt.savefig('graph.png')
###########






#In case the file doesn't exist
currentData = ""
try:
  currentData = open("currentDataPoints.txt","r")
  currentData.close()
except:
  currentData = open("currentDataPoints.txt","w+")
  currentData.write("0 1\n1 2\n2 3\n3 4\n4 5\n")
  #Making random data points in case they don't have the 'currentDataPoints.txt' file
  currentData.close()
currentData = open("currentDataPoints.txt","r")
#Import current data points before prompting user to add more
dataPoints = [dict(zip(['x','y'], map(float, line.split()))) for line in currentData]
currentData.close()

  
#Now prompting user to add more if neccesary, printing out the list
print("Hello. At the moment you have the following data set entered:\n")
formattedList = formatPrinting(dataPoints)
[print(i) for i in formattedList]

#Now question if he wants to (1) restart or (2) continue with the current data
print('\nWould you like to:\n1) Clear the list and enter your own data\n2) Continue with the data above\n')
numEntered = int(input())
while numEntered>2 or numEntered<1:
  print("\nYou have entered an invalid option. Enter the integer 1,2, or 3:\n")
  numEntered = int(input())

##Entering a new list
if numEntered==1:
  currentData = [] #emptying list
  print("Enter the data points in the following format:\nX Y,where X is your x value and Y is your y value\nEnter 0 when you are done.\n")
  ##Keeping in mind the number of ways the code and crash
  xAndY = ""
  while xAndY!="0":
    x,y = "usedForChecking","usedForChecking"
    while x==y=="usedForChecking":
      xAndY = input()
      if xAndY == "0": break
      try:
        x,y = map(float, xAndY.split())
        currentData.append({'x': x, 'y': y})
      except:
        print("\nYou have entered an invalid format. An example of entering (4.9,3) would be \"4.9 3\"\n")
    if xAndY=="0": break

  print("Data:\n")
  [print(i) for i in formatPrinting(currentData)]
  savedData = open("currentDataPoints.txt","w")
  ##Updating file with new data points
  for i in currentData:
    savedData.write(str(i['x'])+" "+str(i['y'])+"\n")
  savedData.close()


#Now we proceed with the data in the list
print("Now calculating the best method of fit...")

##Let 1 = Linear, 2 = Quadratic, 3 = Logistic, 4 = Sin fit
##Here we will determine which fit is the best. This will be done by checking the smallest Sum of Squared Residuals

#Let's do linear first:
#Calculate best fit:
xValues = [i['x'] for i in dataPoints]
yValues = [i['y'] for i in dataPoints]

m,b = solveForLinear(xValues,yValues)
linearConstants = [m,b]
optionOneSSR = sum([(i['y']-linearFunction(i['x'],m,b))**2 for i in dataPoints])

a,b,c = solveForQuadratic(xValues,yValues)
optionTwoSSR = sum([(i['y']-quadraticFunction(i['x'],a,b,c))**2 for i in dataPoints])
quadraticConstants = [a,b,c]

a,b,c = solveForLogistic(xValues,yValues)
optionThreeSSR = sum([(i['y']-logisticFunction(i['x'],a,b,c))**2 for i in dataPoints])
logisticConstants = [a,b,c]

a,b,c,d, = solveForSin(xValues, yValues)
optionFourSSR = sum([(i['y']-sinFunction(i['x'],a,b,c,d))**2 for i in dataPoints])
sinConstants = [a,b,c,d]

groupOfSSRs = [optionOneSSR, optionTwoSSR, optionThreeSSR, optionFourSSR]
print("The best fit is...", end = "  ")
smallestSSR = min(groupOfSSRs)
if optionOneSSR == smallestSSR:
  graphData(dataPoints, "linear",linearConstants)
  print("Linear!")
elif optionTwoSSR == smallestSSR:
  graphData(dataPoints, "quadratic",quadraticConstants)
  print("Quadratic!")
elif optionThreeSSR == smallestSSR:
  graphData(dataPoints, "logistic",logisticConstants)
  print("Logistic!")
elif optionFourSSR == smallestSSR:
  graphData(dataPoints, "sin",sinConstants)
  print("Sin!")
print("View the graph on \"graph.png\"")
