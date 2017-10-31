import planning_map as m
import library



def getPositionValue(t):
    row=t[0]
    col=t[1]

    if row>3:
        row-=1
    if col>4:
        col-=1
    return(m.world_map[row][col])

def getNeigh(t):
    top = (t[0]-1,t[1])
    left= (t[0],t[1]-1)
    right= (t[0],t[1]+1)
    bottom= (t[0]+1,t[1])
    return top,left,right,bottom
    
def main():
    orientation = "forward"
    currentPosition = m.start

    while(currentPosition != m.goal):
        positionValue = getPositionValue(currentPosition)
        top,left,right,bottom = getNeigh(currentPosition)
        
        topValue = getPositionValue(top)
        leftValue = getPositionValue(left)
        rightValue = getPositionValue(right)
        bottomValue = getPositionValue(bottom)
        #neighList = [topValue,leftValue,rightValue,bottomValue]

        seek = positionValue - 1

        if seek == topValue:
            if orientation =="forward":
                library.moveForward(45,500)

            elif orientation=="right":
                library.turnLeft(90,100)
                library.moveForward(45,500)
                orientation = "forward"

            elif orientation=="left":
                library.turnRight(90,100)
                library.moveForward(45,500)
                orientation = "forward"

            elif orientation=="down":
                library.moveForward(45,-500)

            currentPosition = top
            print(currentPosition)

        elif seek == leftValue:
            if orientation =="left":
                library.moveForward(45,500)

            elif orientation=="right":
                library.moveForward(45,-500)

            elif orientation=="forward":
                library.turnLeft(90,100)
                library.moveForward(45,500)
                orientation = "left"

            elif orientation=="down":
                library.turnRight(90,100)
                library.moveForward(45,500)
                orientation = "left"
            currentPosition = left
            print(currentPosition)

        elif seek == rightValue:
            if orientation =="right":
                library.moveForward(45,500)

            elif orientation=="left":
                library.moveForward(45,-500)

            elif orientation=="forward":
                library.turnRight(90,100)
                library.moveForward(45,500)
                orientation = "right"

            elif orientation=="down":
                library.turnLeft(90,100)
                library.moveForward(45,500)
                orientation = "right"
            currentPosition = right
            print(currentPosition)

        elif seek == bottomValue:
            if orientation =="down":
                library.moveForward(45,500)

            elif orientation=="right":
                library.turnRight(90,100)
                library.moveForward(45,500)
                orientation = "down"

            elif orientation=="left":
                library.turnLeft(90,100)
                library.moveForward(45,500)
                orientation = "down"

            elif orientation=="forward":
                library.moveForward(45,-500)
    
            currentPosition = bottom
            print(currentPosition)


    print("We reached our goal")
                

        
        

        
        

    
        #print(top,left,right,bottom)


main()

    
    
    
