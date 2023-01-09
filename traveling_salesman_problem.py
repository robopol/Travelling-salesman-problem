import math
import sys
import matplotlib.pyplot as plt
import random
print("""
****************************************************************************************
Travelling salesman problem : 

Author: Ing. Robert Polak
Contact Info: robopol@robopol.sk
website: https://www.robopol.sk
Purpose:
    An algorithm that solves the travelling salesman problem. Simulated annealing method.  
 
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

# function for distance between two points
def get_distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)

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
    return best_path

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
    # call function for simulated annealing  
    best_path=get_simulated_annealing(points)
    # append first point to the end of the list
    best_path.append(best_path[0])
    print("Best path -simulated annealing:")
    print(best_path)
    # plot best path simulating the salesman
    plt.title("Plot of best path : simulated annealing")
    plt.grid(True)
    plt.plot([x for (x,y) in best_path],[y for (x,y) in best_path],'ko-')
    plt.show()  
