import math


def applyAngleRestriction(angle):
    if(radian2degree(angle) >= 170):
        return degree2radian(170)
    if(radian2degree(angle) <= 10):
        return degree2radian(10)
    return angle

def radian2degree(radian):
    return radian * 180 / math.pi

def degree2radian(degree):
    return degree * math.pi / 180

def calculateAngle(start_x, start_y, end_x, end_y):
    if(end_x == start_x):
        return math.pi / 2
    if(end_y >= start_y):
        if(end_x < start_x):
            return applyAngleRestriction(math.pi)
        else:
            return applyAngleRestriction(0)
      
    angle = math.atan((end_y - start_y) / (end_x - start_x))
    if(angle <= 0):
        return applyAngleRestriction(abs(angle))

    return applyAngleRestriction(math.pi - angle)