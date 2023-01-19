import math
import sys
import matplotlib.pyplot as plt
import random
from itertools import permutations
print("""
****************************************************************************************
Travelling salesman problem : 

Author: Ing. Robert Polak
Contact Info: robopol@robopol.sk
website: https://www.robopol.sk
Purpose:
    An algorithm that solves the travelling salesman problem. Simulated annealing method and other.  
 
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
    
# function for the nearest neighbor point
def get_nearest_neighbor(points):
    # define variables
    best_path=[];points_temp=[]; nearest_neighbor=0    
    # define points_temp
    points_temp=points[:]
    # get first point
    best_path.append(points_temp[0])
    # remove first point from points_temp
    points_temp.remove(points[0])
    # get nearest neighbor
    nearest_neighbor=points_temp[0]
    for i in range(len(points_temp)):
        if get_distance(best_path[-1],points_temp[i])<get_distance(best_path[-1],nearest_neighbor):
            nearest_neighbor=points_temp[i]
    # append nearest neighbor to the best path
    best_path.append(nearest_neighbor)
    # remove nearest neighbor from points_temp
    points_temp.remove(nearest_neighbor)
    # while loop
    while len(points_temp)>0:
        # get nearest neighbor
        nearest_neighbor=points_temp[0]
        for i in range(len(points_temp)):
            if get_distance(best_path[-1],points_temp[i])<get_distance(best_path[-1],nearest_neighbor):
                nearest_neighbor=points_temp[i]
               
        # append nearest neighbor to the best path
        best_path.append(nearest_neighbor)
        # remove nearest neighbor from points
        points_temp.remove(nearest_neighbor)
    # get new distance
    best_distance=get_distance(best_path[0],best_path[-1])
    for i in range(len(best_path)-1):
        best_distance+=get_distance(best_path[i],best_path[i+1])            
    # append first point to the end of the list
    best_path.append(best_path[0])      
    return best_path, best_distance

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
    new_path=best_path; original_path=best_path; new_distance=best_distance
    # exchange of elements in the field        
    for i in range(0,len(best_path)-1+int(0.2*len(best_path)),1):        
        # get permutations
        index_1=i+1; index_2=i+2; index_3=i+3; index_4=i+4; index_5=i+5
        if index_1>len(best_path)-1: index_1=index_1-len(best_path)+1
        if index_2>len(best_path)-1: index_2=index_2-len(best_path)+1
        if index_3>len(best_path)-1: index_3=index_3-len(best_path)+1
        if index_4>len(best_path)-1: index_4=index_4-len(best_path)+1
        if index_5>len(best_path)-1: index_5=index_5-len(best_path)+1                           
        combin=list(permutations((index_1, index_2, index_3, index_4, index_5),5))                    
        for j in range(0,len(combin)-1):
            # get new path
            new_path=original_path[:]
            new_path[index_1]=original_path[combin[j][0]]
            new_path[index_2]=original_path[combin[j][1]]
            new_path[index_3]=original_path[combin[j][2]]
            new_path[index_4]=original_path[combin[j][3]]
            new_path[index_5]=original_path[combin[j][4]]
            # get new distance
            new_distance=get_distance(new_path[0],new_path[-1])
            for k in range(len(new_path)-1):
                new_distance+=get_distance(new_path[k],new_path[k+1])
            # if new distance is better than best distance
            if new_distance<best_distance:
                best_path=new_path[:]
                best_distance=new_distance
                                 
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
    print("Best path -simulated annealing:")
    print(best_path)
    print(f'Best distance -simulated annealing: {best_distance}')    
    # plot best path simulating the salesman
    plt.title("Plot of best path : simulated annealing")
    plt.grid(True)
    plt.plot([x for (x,y) in best_path],[y for (x,y) in best_path],'ko-')
    plt.show()
    # call function for nearest neighbor
    best_path_narest_neighbor=get_nearest_neighbor(points)    
    print("Best path -nearest neighbor:")
    print(best_path_narest_neighbor[0])    
    print(f'Best distance -nearest neighbor: {best_path_narest_neighbor[1]}')
    # plot best path nearest neighbor
    plt.title("Plot of best path : nearest neighbor")
    plt.grid(True)
    plt.plot([x for (x,y) in best_path_narest_neighbor[0]],[y for (x,y) in best_path_narest_neighbor[0]],'ko-')
    plt.show()    
    # call function for optimal nearest neighbor
    optimal_path=get_optimal_nearest_neighbor(points)
    print("Best path - optimal nearest neighbor:")
    print(optimal_path[0])
    print(f'Best distance -optimal nearest neighbor: {optimal_path[1]}')        
    # plot best path for optimal nearest neighbor
    plt.title("Plot of best path : optimal nearest neighbor")
    plt.grid(True)
    plt.plot([x for (x,y) in optimal_path[0]],[y for (x,y) in optimal_path[0]],'ko-')
    plt.show()
    
    # call function for permutation
    best_path_criss_cross=get_optimize_path(optimal_path[0],optimal_path[1])
    print("Best path -optimize optimal nearest neighbor:")
    print(best_path_criss_cross)
    # plot best path for criss-cross algorithm
    plt.title("Plot of best path : Optimize optimal nearest neighbor")
    plt.grid(True)
    plt.plot([x for (x,y) in best_path_criss_cross[0]],[y for (x,y) in best_path_criss_cross[0]],'ko-')
    plt.show()   
