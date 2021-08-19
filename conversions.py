from math import degrees, sqrt, atan, cos, radians, sin

def cart_to_polar(x, y):
    r = sqrt(x**2+y**2)
    angle = degrees(atan(y/x))
    return r, angle

def polar_to_cart(r, angle):
    x = r * cos(radians(angle))
    y = r * sin(radians(angle))
    return x, y

def transformed_rect_sides(side, angle):
    angle = sqrt( (angle)**2 )
    if (90 < angle < 180) or (270 < angle < 360):
        angle -= 90
    r = sqrt( (side/2)**2 + (side/2)**2 )
    width = 2*sqrt((r*sin(radians(45+angle)))**2)
    height = 2*sqrt((r*cos(radians(45-angle)))**2)
    return width, height 