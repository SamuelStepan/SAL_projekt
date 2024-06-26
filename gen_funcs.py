import random as rn
import numpy as np
import math

def draw_line(n:int, img:np.array, point_x:tuple, point_y:tuple):
    """Function that draws line into given img between point_x and point_y"""
    curr_x, curr_y = point_x    ##current coordinates of drawing point
    steps = 2 * n
    if(point_y[0] - point_x[0] == 0):   ##vertical line
        h = (point_y[1] - point_x[1])/steps    ## distance of one step
        ##drawing the line from point_x to point_y
        for i in range(steps-1):
            curr_y += h
            img[math.floor(curr_x)][math.floor(curr_y)] = 255
    else:
        k = (point_y[1] - point_x[1])/(point_y[0] - point_x[0]) ##slope of line
        h = (point_y[0] - point_x[0])/steps    ## distance of one step
        ##drawing the line from point_x to point_y
        for i in range(steps-1):
            curr_x += h
            curr_y += k * h
            img[math.floor(curr_x)][math.floor(curr_y)] = 255

def gen_line(n:int):
    """Function that returns image of size n x n with random line of random length"""
    img = np.array([[0 for i in range(n)] for j in range(n)],dtype=int)
    point_x = (rn.randint(0, n-1), rn.randint(0, n-1))  ##beggining of the line
    point_y:tuple
    ##generates different random point
    while(True):
        point_y = (rn.randint(0, n-1), rn.randint(0, n-1))  ##end of line
        if(point_y != point_x):
            break
    
    draw_line(n, img, point_x, point_y)
    return img

def gen_circle(n:int):
    """Function that returns image of size n x n with random circle(random center point and random radius)"""
    img = np.array([[0 for i in range(n)] for j in range(n)],dtype=int)
    ##random center of circle that is atleast n/10 pixels distant from the border of image
    center = (rn.randint(math.floor(n/10), math.floor((9*n)/10)), rn.randint(math.floor(n/10), math.floor((9*n)/10)))  
    max_radius = min(center[0], center[1], (n - 1) - center[0], (n - 1) - center[1])
    radius = rn.randint(math.floor((5*n)/100), max_radius)  ##radius shall me atleast 5% of n up to max_radius so full circle can be drawn
    angle_step = 1/(math.pi * n)    ##there will be no need to draw more that pi * n pixels
    angle = 0
    while(angle < 2 * math.pi):
        img[math.floor(center[0] + radius * math.cos(angle))][math.floor(center[1] + radius * math.sin(angle))] = 255
        angle += angle_step

    return img

def gen_square(n:int):
    """Function that returns image of size n x n with random square(random size and rotation)"""
    img = np.array([[0 for i in range(n)] for j in range(n)],dtype=int)
    ##random center of square that is atleast n/10 pixels distant from the border of image
    center = (rn.randint(math.floor(n/10), math.floor((9*n)/10)), rn.randint(math.floor(n/10), math.floor((9*n)/10)))  
    max_diag_dist = min(center[0], center[1], (n - 1) - center[0], (n - 1) - center[1]) ##maximal diagonal distance between center of square and the border of image
    angle = rn.uniform(0, math.pi / 2)
    diag_dist = rn.randint(math.floor((8*n)/100), max_diag_dist)    ##diagonal distance from center of square shall me atleast 5% of n up to max_diag_dist so full square can be drawn
    vertices = []
    ##generation vertices of square
    curr_angle = 0
    for i in range(4):
        vertices.append((math.floor(center[0] + diag_dist * math.cos(angle + curr_angle)),math.floor(center[1] + diag_dist * math.sin(angle + curr_angle))))
        curr_angle += math.pi/2
    ##drawing all 4 lines of square    
    for ind_1, ind_2 in [(0,1),(1,2), (2,3), (0,3)]:
        draw_line(n, img, vertices[ind_1], vertices[ind_2])
    
    return img

def gen_eqi_triangle(n:int):
    """Function that returns image of size n x n with random equilateral triangle(random position and random size)"""
    img = np.array([[0 for i in range(n)] for j in range(n)],dtype=int)
    center = (rn.randint(math.floor(n/10), math.floor((9*n)/10)), rn.randint(math.floor(n/10), math.floor((9*n)/10)))  
    angle = rn.uniform(0, math.pi / 3)
    max_dist = min(center[0], center[1], (n - 1) - center[0], (n - 1) - center[1]) ##maximal distance between center of gravity of triangle and the border of image
    dist = rn.uniform(math.floor(7*n/100), max_dist)
    vertices = []
    ##generation of vertices of equilateral triangle with center of gravity at point center and with given angle with respect to x axis
    for i in range(3):
        vertices.append((math.floor(center[0] + dist * math.cos(angle)),math.floor(center[1] + dist * math.sin(angle))))
        angle += 2*math.pi/3
    ##drawing triangle as 3 lines
    for ind_1, ind_2 in [(0,1),(1,2), (0,2)]:
        draw_line(n, img, vertices[ind_1], vertices[ind_2])
    
    return img

def gen_triangle(n:int):
    """Function that returns image of size n x n with random triangle(3 random points)"""
    img = np.array([[0 for i in range(n)] for j in range(n)],dtype=int)
    point_A = (rn.randint(0, n-1), rn.randint(0, n-1))  ##beggining of the line
    point_B:tuple
    ##generates different random point
    while(True):
        point_B = (rn.randint(0, n-1), rn.randint(0, n-1))  ##end of line
        if(point_B != point_A):
            break
    point_C:tuple
    vec_A_B = (point_A[0] - point_B[0], point_A[1] - point_B[1])
    ##generates 3rd point that is not on line AB
    while(True):
        point_C = (rn.randint(0, n-1), rn.randint(0, n-1))  ##end of line
        vec_A_C = (point_A[0] - point_C[0], point_A[1] - point_C[1])
        if(vec_A_B[0]*vec_A_C[1]!=vec_A_B[1]*vec_A_C[0]):
            break
    vertices = [point_A, point_B, point_C]
    ##drawing triangle as 3 lines
    for ind_1, ind_2 in [(0,1),(1,2), (0,2)]:
        draw_line(n, img, vertices[ind_1], vertices[ind_2])

    return img

def gen_data(l_shapes:list[str], n:int, num_imgs:int):
    """Function that returns tuple of 2 lists, one with randomly generated images of given shapes of size n x n, each shape will be num_imgs times.
    strings representing shapes are:line,circle,square,eq_tri,tri"""
    funcs = {"line":gen_line, "circle":gen_circle, "square":gen_square, "eq_tri":gen_eqi_triangle, "tri":gen_triangle}
    data = []
    #creates num_imgs pairs of 
    for i, s in enumerate(l_shapes):
        data += list(zip([funcs[s](n) for x in range(num_imgs)], [i for x in range(num_imgs)]))
    rn.shuffle(data)
    imgs, labels = zip(*data)
    return (np.array(imgs), np.array(labels))
    

