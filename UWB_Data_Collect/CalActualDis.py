import math
# timediff is a float
# car is a list about where it is. Ex. [x,y,z]
# anchors is a list about where they are. Ex. [[anchor1X,anchor1Y,anchor1Z],[anchor2....],.....]
# speed is a float about m/s
# dir is a list about eight direction. Ex. [1/0,1/0,1/0]
# return the list which include distances between each anchor and car. Ex. [Anchor1WithCar,Anchor2WithCar,......]

def calDis(timediff,car,anchors,speed,dir):
    move = speed * timediff
    for i,curDir in enumerate(dir):
        if curDir == 1:
            car[i] += move # calculate new car location
    output = []
    for anchor in anchors:
        try :
            output.append(calRange(car,anchor))
        except IndexError as InE:
            print(InE)
    return output

# both of parameter are list about location[X,Y,Z].
# return the Distance between car and anchor
def calRange(car,anchor):
    if len(car) != len(anchor):
        raise IndexError("Wrong Length of parameter")
    sum = 0
    for i,dimen in car:
        sum += pow(abs(dimen - anchor[i]),2)
    return math.sqrt(sum)

        


