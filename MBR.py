import csv
from collections import defaultdict
import math
from pylab import *

class Point(object):
    '''Creates a point on a coordinate plane with values x and y.'''
    def __init__(self, x = float('-inf'), y = float('-inf')):
        '''Defines x and y variables'''
        self.x = x
        self.y = y

    def move(self, dx, dy):
        '''Determines where x and y move'''
        self.x = self.x + dx
        self.y = self.y + dy

    def printPoint(self):
        return "Point(%s,%s)"%(self.x, self.y)


    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx**2 + dy**2)


class Segment(object):
    def __init__(self, p1, p2):
        self.p1 = Point(p1.x,p1.y)
        self.p2 = Point(p2.x,p2.y)

    def length(self):
        dist_x = abs(self.p2.x - self.p1.x)
        dist_y = abs(self.p2.y - self.p1.y)
        dist_x_squared = dist_x ** 2
        dist_y_squared = dist_y ** 2
        line_length = math.sqrt(dist_x_squared + dist_y_squared)
        return line_length

    def printSegment(self):
        x1,y1 = self.p1.x, self.p1.y
        x2,y2 = self.p2.x, self.p2.y
        line = "Segment((%f,%f);(%f,%f))"%(x1,y1,x2,y2)
        return line
    def slope(self):
        dist_y = self.p2.y - self.p1.y
        dist_x = self.p2.x - self.p1.x
        line_slope = dist_y/dist_x
        return line_slope
    ##    Checks whether point on segment or not
    ##  Substitute the point coordinates to Line equation
    def isPointOnSegment(self, point):
        epsilon = 0.001
        a = self.p2.y - self.p1.y
        b = self.p1.x - self.p2.x
        c = self.p2.x*self.p1.y - self.p1.x*self.p2.y
        index = a*point.x + b*point.y + c
        if (abs(index) < epsilon and point.x >= min(self.p1.x, self.p2.x) and point.x  <= max(self.p1.x, self.p2.x)):
            return True
        else:
            return False
## ## End of Segment class

##    A : the end-point of the segment with the smallest y coordinate
##        (A must be "below" B)
##    B : the end-point of the segment with the greatest y coordinate
##        (B must be "above" A)

##      Given a point and a polygon, check if the point is inside or outside the polygon using the ray-casting algorithm.
##      Source: http://rosettacode.org/wiki/Ray-casting_algorithm


def ray_intersects_segment(point, side, boundaryCase):

    A = Point()
    B = Point()
    e = 0.000001
    m_red = 0
    m_blue = 0

##  Checks for special case - whether point on segment or not
    if side.isPointOnSegment(point):
        boundaryCase.append(True)
        return False


    if side.p1.y < side.p2.y:
        A = side.p1
        B = side.p2
    else:
        A = side.p2
        B = side.p1
    if point.y == A.y or point.y == B.y:
        point.y = point.y + e
    if point.y < A.y or point.y > B.y:
        return False
    elif point.x > max(A.x,B.x):

        return False
    else:
        if point.x < min(A.x,B.x):

            return True
        else:
            if A.x != B.x:
                m_red = (B.y - A.y)/(B.x - A.x)
            else:
                m_red = float('inf')
            if A.x != point.x:
                m_blue = (point.y - A.y)/(point.x - A.x)
            else:
                m_blue = float('inf')
            if m_blue >= m_red:
                return True
            else:
                return False


##Get the input Point Cordinate file and Polygon coordinate file
polyFilePath = input("Enter the polygon file path:\n")
#Format : C:\Users\User1\Desktop\testPoly.csv
pointFilePath = input("Enter the point file path:\n")
#Format : C:\Users\User\Desktop\testPoints.csv'

##Read the Polygon File
polygonFile = csv.reader(open(polyFilePath,"rt"))

##Initialize points with MinX, MinY, MaxX, MaxY
pointWithMinX = Point(float('inf'),float('inf'))
pointWithMinY = Point(float('inf'),float('inf'))
pointWithMaxX = Point(float('-inf'), float('-inf'))
pointWithMaxY = Point(float('-inf'), float('-inf'))

##Create a Polygon List to hold the points
polygonList = []
xList = []
yList = []
for Polycoords in polygonFile:
##    Get the MinX, MinY & MaxX, MaxY from polygon coords
    polyCoord = Point(float(Polycoords[0]),float(Polycoords[1]))
    polygonList.append(polyCoord)
    xList.append(polyCoord.x)
    yList.append(polyCoord.y)
    if polyCoord.x < pointWithMinX.x :
        pointWithMinX.x = polyCoord.x
        pointWithMinX.y = polyCoord.y

    if polyCoord.y < pointWithMinY.y:
        pointWithMinY.x = polyCoord.x
        pointWithMinY.y = polyCoord.y

    if polyCoord.x > pointWithMaxX.x :
        pointWithMaxX.x = polyCoord.x
        pointWithMaxX.y = polyCoord.y

    if polyCoord.y > pointWithMaxY.y:
        pointWithMaxY.x = polyCoord.x
        pointWithMaxY.y = polyCoord.y

xList.append(xList[0])
yList.append(yList[0])
##Creates a collection object and stores the columns as collections
columns = defaultdict(list)
with open(pointFilePath) as f:
    reader = csv.DictReader(f)
    for row in reader:
        for (k,v) in row.items():
            columns[k].append(v)

## Loop For each point in the Point Coordinate File

for  i in range(0,len(columns['x'])):
    MBRClassification = 'Outside'
    Inside = False
    boundaryCase = []
    border = False
    ActualClassification = ""
    pointCoord = Point(float(columns['x'][i]),float(columns['y'][i]))
    count = 0

##    If point lies within bounding rectange
    if pointCoord.x >= pointWithMinX.x and pointCoord.x <= pointWithMaxX.x and pointCoord.y >= pointWithMinY.y and pointCoord.y <= pointWithMaxY.y:
        MBRClassification = 'Inside'

##        Loop for each polygon coordinate
        for j in range(0, len(polygonList)-1):
            firstPoint = polygonList[j]

##            If last point
            if( j == len(polygonList) - 2):
                secondPoint = polygonList[0]
            else:
                secondPoint = polygonList[j+1]
            #Create a segment with each set of points in the polygon
            side = Segment(firstPoint, secondPoint)

            if ray_intersects_segment(pointCoord,side, boundaryCase):
                count = count + 1


        if True in boundaryCase:
            border = True
        else:
##            If count is odd, point within polygon, nelse outside polygo
            if (count%2 == 1):
                Inside = True
            else:
                Inside = False
##    Point outside bounding rectange
    else:
        Inside = False

    if(border):
        ActualClassification = "Border"
    elif(Inside):
        ActualClassification = "Inside"
    else:
        ActualClassification = "Outside"

    print('\n' + pointCoord.printPoint()+ '\t\'Actual Class\': ' + columns['Classification'][i] + ':\t\'MBR Class\': ' + MBRClassification + '\t\'Found:\'' + ActualClassification)
####Plot the Points
plot(columns['x'], columns['y'],'r^', markersize=12)
####Plot the polygon
plot(xList, yList, 'bo-', label='polygon', linewidth=2)



for X, Y, Z in zip(columns['x'], columns['y'], columns['Classification']):
    # Annotate the points 5 _points_ above and to the left of the vertex
    annotate('{0},({1},{2})'.format(Z,X,Y), xy=(X,Y), xytext=(-5, 5), ha='right',
                textcoords='offset points')
    
xlabel('x')
ylabel('y')
title('Points in Polygon algorithm')
##grid(True)
savefig("Results.png")
show()
