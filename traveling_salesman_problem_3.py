import math
import sys
import matplotlib.pyplot as plt
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
    An algorithm that solves the travelling salesman problem. Simulated annealing method 
    and optimize nearest neighbor.  
 
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
            print("Enter the number of iterations:")
            input_string=sys.stdin.readline()            
            num_of_iterations=int(input_string)
        except Exception:
            print("Please insert integer values")
            continue
        break
    return num_points,num_of_iterations

# function for random points
def get_random_points(num_points):
    points=[]
    for i in range(num_points):
        x=random.randint(1,1000)
        y=random.randint(1,1000)
        points.append((x,y))
    return points

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
    # define variables
    best_path=[]; new_path=[];points_temp=[];best_distance=0; new_distance=0; nearest_neighbor=0  
    
    if len(points)<200:        
        for i in range(len(points)):
            # get first point for new path
            new_path.append(points[i])
            # remove first point from points
            points_temp=points[:]
            points_temp.remove(points[i])
            # get nearest neighbor
            nearest_neighbor=points_temp[0]
            for i in range(len(points_temp)):
                if get_distance(new_path[-1],points_temp[i])<get_distance(new_path[-1],nearest_neighbor):
                    nearest_neighbor=points_temp[i]
            # append nearest neighbor to the new path
            new_path.append(nearest_neighbor)
            # remove nearest neighbor from points_temp
            points_temp.remove(nearest_neighbor)
            # while loop
            while len(points_temp)>0:
                # get nearest neighbor
                nearest_neighbor=points_temp[0]
                for i in range(len(points_temp)):
                    if get_distance(new_path[-1],points_temp[i])<get_distance(new_path[-1],nearest_neighbor):
                        nearest_neighbor=points_temp[i]
                # append nearest neighbor to the best path
                new_path.append(nearest_neighbor)
                # remove nearest neighbor from points_temp
                points_temp.remove(nearest_neighbor)
            # append first point to the end of the list
            new_path.append(new_path[0])
            # get new distance
            new_distance=get_distance(new_path[0],new_path[-1])
            for i in range(len(new_path)-1):        
                new_distance+=get_distance(new_path[i],new_path[i+1])
            # if new distance is better than best distance
            if new_distance<best_distance or best_distance==0:
                best_distance=new_distance
                best_path=new_path[:]
            # clear new path
            new_path.clear()                               
    else:       
        for i in range(200):
            # get first randompoint for new path
            rand=random.randint(0,len(points)-1)
            new_path.append(points[rand])
            # remove first point from points
            points_temp=points[:]
            points_temp.remove(points[rand])
            # get nearest neighbor
            nearest_neighbor=points_temp[0]
            for i in range(len(points_temp)):
                if get_distance(new_path[-1],points_temp[i])<get_distance(new_path[-1],nearest_neighbor):
                    nearest_neighbor=points_temp[i]
            # append nearest neighbor to the new path
            new_path.append(nearest_neighbor)
            # remove nearest neighbor from points_temp
            points_temp.remove(nearest_neighbor)
            # while loop
            while len(points_temp)>0:
                # get nearest neighbor
                nearest_neighbor=points_temp[0]
                for i in range(len(points_temp)):
                    if get_distance(new_path[-1],points_temp[i])<get_distance(new_path[-1],nearest_neighbor):
                        nearest_neighbor=points_temp[i]
                # append nearest neighbor to the best path
                new_path.append(nearest_neighbor)
                # remove nearest neighbor from points_temp
                points_temp.remove(nearest_neighbor)
            # append first point to the end of the list
            new_path.append(new_path[0])
            # get new distance
            new_distance=get_distance(new_path[0],new_path[-1])
            for i in range(len(new_path)-1):        
                new_distance+=get_distance(new_path[i],new_path[i+1])
            # if new distance is better than best distance
            if new_distance<best_distance or best_distance==0:
                best_distance=new_distance
                best_path=new_path[:]            
            # clear new path
            new_path.clear()                  
    return best_path,best_distance      

# function for simulated annealing
def get_simulated_annealing(points):
    # define constants
    T=1000
    T_min=0.0001
    alpha=0.9
    # define variables
    best_path=points
    best_distance=get_distance(points[0],points[-1])
    for i in range(len(points)-1):
        best_distance+=get_distance(points[i],points[i+1])
    # while loop
    while T>T_min:
        # get new path
        new_path=best_path[:]
        # get random index
        i=random.randint(0,len(points)-1)
        j=random.randint(0,len(points)-1)
        # swap points
        new_path[i],new_path[j]=new_path[j],new_path[i]
        # get new distance
        new_distance=get_distance(new_path[0],new_path[-1])
        for i in range(len(new_path)-1):
            new_distance+=get_distance(new_path[i],new_path[i+1])
        # get delta
        delta=new_distance-best_distance
        # if delta<0
        if delta<0:
            best_path=new_path[:]
            best_distance=new_distance
        # if delta>0
        else:
            # get random number
            rand=random.random()
            # if rand<math.exp(-delta/T)
            if rand<math.exp(-delta/T):
                best_path=new_path[:]
                best_distance=new_distance
        # decrease temperature
        T=T*alpha
    # append first point to the end of the list
    best_path.append(best_path[0])
    return best_path, best_distance

# optimize permutations best path
def get_optimize_path(best_path, best_distance):    
    # define variables
    new_path=[]; new_distance=0; temp_distance=0
    # while loop
    if len(points)<=250:
        # exchange of elements in the field        
        for i in range(0,len(best_path)-7,1):
            # get permutations
            index_1=i+1; index_2=i+2; index_3=i+3; index_4=i+4; index_5=i+5; index_6=i+6; index_7=i+7            
            if index_7>len(best_path)-1: index_7=index_7-len(best_path)+1
            combin=list(permutations((index_1,index_2,index_3,index_4,index_5,index_6),6))
            # get temp distance
            temp_distance=get_distance(best_path[i],best_path[index_1])+get_distance(best_path[index_1],best_path[index_2])+get_distance(best_path[index_2],best_path[index_3])+get_distance(best_path[index_3],best_path[index_4])+get_distance(best_path[index_4],best_path[index_5])+get_distance(best_path[index_5],best_path[index_6])+get_distance(best_path[index_6],best_path[index_7])
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
                new_distance=get_distance(new_path[i],new_path[index_1])+get_distance(new_path[index_1],new_path[index_2])+get_distance(new_path[index_2],new_path[index_3])+get_distance(new_path[index_3],new_path[index_4])+get_distance(new_path[index_4],new_path[index_5])+get_distance(new_path[index_5],new_path[index_6])+get_distance(new_path[index_6],new_path[index_7])
                # if new distance is better than temp distance
                if new_distance<temp_distance:
                    temp_distance=new_distance
                    best_path=new_path[:]                    
    else:  
        # exchange of elements in the field        
        for i in range(0,len(best_path)-5,1):        
            # get permutations
            index_1=i+1; index_2=i+2; index_3=i+3; index_4=i+4; index_5=i+5            
            if index_5>len(best_path)-1: index_5=index_5-len(best_path)+1
            combin=list(permutations((index_1, index_2, index_3,index_4),4))
            # get temp distance        
            temp_distance=get_distance(best_path[i],best_path[index_1])+get_distance(best_path[index_1],best_path[index_2])+get_distance(best_path[index_2],best_path[index_3])+get_distance(best_path[index_3],best_path[index_4])+get_distance(best_path[index_4],best_path[index_5])                    
            for j in range(0,len(combin)-1):
                # get new path
                new_path=best_path[:]
                new_path[index_1]=best_path[combin[j][0]]
                new_path[index_2]=best_path[combin[j][1]]
                new_path[index_3]=best_path[combin[j][2]]
                new_path[index_4]=best_path[combin[j][3]]
                # get new distance
                new_distance=get_distance(new_path[i],new_path[index_1])+get_distance(new_path[index_1],new_path[index_2])+get_distance(new_path[index_2],new_path[index_3])+get_distance(new_path[index_3],new_path[index_4])+get_distance(new_path[index_4],new_path[index_5])            
                # if new distance is better than temp distance
                if new_distance<temp_distance:
                    best_path=new_path[:]
                    temp_distance=new_distance    
    # get best distance
    best_distance=0
    # cykle for best distance
    for i in range(len(best_path)-1):        
        best_distance+=get_distance(best_path[i],best_path[i+1])                                         
    return best_path, best_distance

# Infinite while loop console. Main program
while True:
    # input numbers of points
    num=get_input()
    # end of program
    if num[0]==0:
        break
    # call function for random points
    points=get_random_points(num[0])
    print("Random points:")
    print(points)
    # call function for simulated annealing
    best_path,best_distance=get_simulated_annealing(points)
    for i in range(num[1]):
        # call function for simulated annealing
        new_path,new_distance=get_simulated_annealing(best_path)
        if new_distance<best_distance:
            best_path,best_distance=new_path,new_distance                
    print("Best path -simulated annealing:")
    print(best_path)
    print(f'Best distance -simulated annealing: {best_distance}')    
    # plot best path simulating the salesman
    plt.title("Plot of best path : simulated annealing")
    plt.grid(True)
    plt.plot([x for (x,y) in best_path],[y for (x,y) in best_path],'ko-')
    plt.show()
                
    # call function for optimal nearest neighbor
    optimal_path=get_optimal_nearest_neighbor(points)    
    # call function for permutation
    new_path_permutation=get_optimize_path(optimal_path[0],optimal_path[1])    
    # reverse new_path_permutation to list
    temp_path_permutation=new_path_permutation[0][::-1]    
    # call function for permutation
    temp_path_permutation=get_optimize_path(temp_path_permutation,new_path_permutation[1])
    if new_path_permutation[1]<temp_path_permutation[1]:
        best_path_permutation=new_path_permutation
    else:
        best_path_permutation=temp_path_permutation    
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
        else:            
            break              
    # call function for permutation
    new_path_permutation=get_optimize_path(field_points[0],field_points[1])
    # reverse new_path_permutation to list
    temp_path_permutation=new_path_permutation[0][::-1]    
    # call function for permutation
    temp_path_permutation=get_optimize_path(temp_path_permutation,new_path_permutation[1])
    if new_path_permutation[1]<temp_path_permutation[1]:
        best_path_permutation=new_path_permutation
    else:
        best_path_permutation=temp_path_permutation    
    print("Best path -optimize optimal NN:")
    print(field_points[0])
    print(f'Best distance -optimize optimal NN: {best_path_permutation[1]}')
    # plot best path intercection function
    plt.title("Plot of best path : optimize optimal NN")
    plt.grid(True)
    plt.plot([x for (x,y) in best_path_permutation[0]],[y for (x,y) in best_path_permutation[0]],'ko-')
    plt.show()   