import math
import sys
import matplotlib.pyplot as plt
import numpy as np
import random
from itertools import permutations
from shapely.geometry import LineString
print("""
****************************************************************************************
Travelling salesman problem : 

Author: Ing. Robert Polak
Contact Info: robopol@robopol.sk
website: https://www.robopol.sk
Purpose:
    An algorithm that solves the travelling salesman problem. Optimize nearest neighbor.  
 
Copyright notice: This code is Open Source, type: console program
To end the program, press 0 and the enter.
****************************************************************************************
""")
# enter numbers of random points in the console.
def get_input():
    while True:
        try:
            print("Enter the number of points:")
            input_string=sys.stdin.readline()
            num_points=int(input_string)
            
        except Exception:
            print("Please insert integer values")
            continue
        break
    return num_points

# function for random points
def get_random_points(num_points):
    points=[]
    for i in range(num_points):
        x=random.randint(1,1000)
        y=random.randint(1,1000)
        points.append((x,y))
    return points

# function check double points in the list
def check_double_points(points):    
    unique_list = []
    for item in points:
        if item not in unique_list:
            unique_list.append(item)
    # append first point to the end of the list
    unique_list.append(unique_list[0])
    return unique_list    

# function for distance between two points
def get_distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

# function intersection
def check_intersection(points):
    lines = []
    # Create line segments from points
    for i in range(len(points) - 1):
        lines.append(LineString([points[i], points[i+1]]))    
    # Check intersection for each segment
    for i in range(len(lines) - 1):
        for j in range(i+1, len(lines)):
            if lines[i].crosses(lines[j]):                    
                return points,lines[i],lines[j]            
    return points,0,0

# function Exchange of intersecting lines
def exchange_intersecting_lines(points,lines1,lines2):   
    points_temp=points[:]
    # get index of intersecting lines
    index1=points.index(lines1.coords[0])
    index2=points.index(lines1.coords[1])
    index3=points.index(lines2.coords[0])
    index4=points.index(lines2.coords[1])    
    # change points    
    points[index2], points[index3]=points[index3], points[index2]        
    # exchange of intersecting lines
    k=2
    if index4==0: index4=len(points)
    for i in range(index2+1,index4):
        points[i]=points_temp[index4-k]        
        k+=1    
    # get distance
    distance=get_distance(points[0],points[-1])
    for i in range(len(points)-1):        
        distance+=get_distance(points[i],points[i+1])            
    return points, distance    

# function for the nearest neighbor point with optimal path
def get_optimal_nearest_neighbor(points):
    # function for distance between two points
    def get_distance(point1, point2):        
        return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)
    # function for nearest neighbor     
    def get_nearest_neighbor(current, points):
        distances = [get_distance(current, point) for point in points]
        return points[np.argmin(distances)]
    best_path = []
    best_distance = float("inf")
    if len(points) < 200:
        for i, start_point in enumerate(points):
            current_path = [start_point]
            remaining_points = points[:i] + points[i+1:]
            while remaining_points:
                current = current_path[-1]
                nearest = get_nearest_neighbor(current, remaining_points)
                current_path.append(nearest)
                remaining_points.remove(nearest)
            current_path.append(start_point)
            current_distance = sum(get_distance(current_path[i], current_path[i+1]) for i in range(len(current_path)-1))
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = current_path
    else:
        for _ in range(200):
            start_point = random.choice(points)
            current_path = [start_point]
            remaining_points = [point for point in points if point != start_point]
            while remaining_points:
                current = current_path[-1]
                nearest = get_nearest_neighbor(current, remaining_points)
                current_path.append(nearest)
                remaining_points.remove(nearest)
            current_path.append(start_point)
            current_distance = sum(get_distance(current_path[i], current_path[i+1]) for i in range(len(current_path)-1))
            if current_distance < best_distance:
                best_distance = current_distance
                best_path = current_path
    return best_path, best_distance    

# optimize permutations best path
def get_optimize_path(best_path):    
    # define variables
    new_path=[]; new_distance=0; temp_distance=0
    # while loop    
    # exchange of elements in the field        
    for i in range(0,len(best_path)-1,1):
        # get permutations
        index_1=i+1; index_2=i+2; index_3=i+3; index_4=i+4; index_5=i+5; index_6=i+6; index_7=i+7            
        if index_1>len(best_path)-1: index_1=index_1-len(best_path)+1
        if index_2>len(best_path)-1: index_2=index_2-len(best_path)+1
        if index_3>len(best_path)-1: index_3=index_3-len(best_path)+1
        if index_4>len(best_path)-1: index_4=index_4-len(best_path)+1
        if index_5>len(best_path)-1: index_5=index_5-len(best_path)+1
        if index_6>len(best_path)-1: index_6=index_6-len(best_path)+1
        if index_7>len(best_path)-1: index_7=index_7-len(best_path)+1
        combin=list(permutations((index_1,index_2,index_3,index_4,index_5,index_6),6))
        if i<=len(best_path)-7:
            # get temp distance
            indexes = [index_1, index_2, index_3, index_4, index_5, index_6, index_7]
            temp_distance =get_distance(best_path[i],best_path[index_1]) 
            for j in range(len(indexes) - 1):
                temp_distance += get_distance(best_path[indexes[j]], best_path[indexes[j+1]])            
            # get new path
            for j in range(0,len(combin)-1):
                # get new path
                new_path=best_path[:]
                new_path[index_1]=best_path[combin[j][0]]
                new_path[index_2]=best_path[combin[j][1]]
                new_path[index_3]=best_path[combin[j][2]]
                new_path[index_4]=best_path[combin[j][3]]
                new_path[index_5]=best_path[combin[j][4]]
                new_path[index_6]=best_path[combin[j][5]]
                # get new distance
                new_distance=get_distance(new_path[i],new_path[index_1])
                for k in range(len(indexes) - 1):
                    new_distance += get_distance(new_path[indexes[k]], new_path[indexes[k+1]])                
                # if new distance is better than temp distance
                if new_distance<temp_distance:
                    temp_distance=new_distance
                    best_path=new_path[:]
        else:
            # get temp distance
            temp_distance=get_distance(best_path[0],best_path[-1])
            for k in range(0,len(best_path)-1):
                temp_distance+=get_distance(best_path[k],best_path[k+1])
            for j in range(0,len(combin)-1):
                # get new path
                new_path=best_path[:]
                new_path[index_1]=best_path[combin[j][0]]
                new_path[index_2]=best_path[combin[j][1]]
                new_path[index_3]=best_path[combin[j][2]]
                new_path[index_4]=best_path[combin[j][3]]
                new_path[index_5]=best_path[combin[j][4]]
                new_path[index_6]=best_path[combin[j][5]]
                # cykle for new distance
                new_distance=get_distance(new_path[0],new_path[-1])
                for k in range(0,len(new_path)-1):
                    new_distance+=get_distance(new_path[k],new_path[k+1])
                # if new distance is better than temp distance
                if new_distance<temp_distance:
                    temp_distance=new_distance                        
                    best_path=new_path[:]                                                 
    return best_path,temp_distance

# Infinite while loop console. Main program
while True:
    # input numbers of points
    num=get_input()
    # end of program
    if num==0:
        break
    # call function for random points
    points=get_random_points(num)
    print("Random points:")
    print(points)                  
    # call function for optimal nearest neighbor
    optimal_path=get_optimal_nearest_neighbor(points)
    print("Best path - best nearest neighbor:")
    print(optimal_path[0])
    print(f'Best distance -best nearest neighbor: {optimal_path[1]}')        
    # plot best path for optimal nearest neighbor
    plt.title("Plot of best path : best nearest neighbor")
    plt.grid(True)
    plt.plot([x for (x,y) in optimal_path[0]],[y for (x,y) in optimal_path[0]],'ko-')
    plt.show()    
    # call function for permutation
    best_path_permutation=get_optimize_path(optimal_path[0])      
    # delete double points
    best_path_correction=check_double_points(best_path_permutation[0])
    best_path_permutation=[best_path_correction,best_path_permutation[1]]    
    # call intercection function    
    intersection=check_intersection(best_path_permutation[0])
    if intersection[1]!=0 and intersection[2]!=0:        
        field_points=exchange_intersecting_lines(intersection[0], intersection[1], intersection[2])
    else:
        field_points=best_path_permutation
    # cykle for intercection function
    while intersection[1]!=0 and intersection[2]!=0:
        intersection=check_intersection(field_points[0])
        if intersection[1]!=0 and intersection[2]!=0:
            field_points=exchange_intersecting_lines(intersection[0], intersection[1], intersection[2])
            # delete double points
            best_path_correction=check_double_points(field_points[0])
            field_points=[best_path_correction,field_points[1]]
        else:            
            break            
    # call function for permutation
    best_path_permutation=get_optimize_path(field_points[0])            
    # delete double points
    best_path_correction=check_double_points(field_points[0])
    field_points=[best_path_correction,field_points[1]]
    print("Best path -optimize best NN:")
    print(field_points[0])
    print(f'Best distance -optimize best NN: {best_path_permutation[1]}')
    # plot best path 
    plt.title("Plot of best path : optimize best NN")
    plt.grid(True)
    plt.plot([x for (x,y) in field_points[0]],[y for (x,y) in field_points[0]],'ko-')
    plt.show()
