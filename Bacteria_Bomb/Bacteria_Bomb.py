'''
——————————Version 3.0————————————
Reading the "Read me!" document before running this model will help you better
understand this model.
@author: FUGANGZHOU

'''
import seaborn as sns
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import warnings
warnings.filterwarnings('ignore')

'''
Step 1: Pull in data file and find bombing point.

'''
# Pull in data file'
img_train = pd.read_csv('wind.txt',header=None)
# Find the bombing point.
'''
for a in range(300):
    for b in range(300):
        if img_train[a][b] != 0.0:
            print(img_train[a][b])
            print(a,b)
'''
img_train = np.array(img_train)# Convert to array.

'''
Step 2: Calculate where 5000 bacteria will end up and show them in scatter plot.
        Save the coordinates of each particle's position to a file as text.  
'''
def get_Result(wind=1,num=5000,height=75):
    # Initialize Bacterias.
    bacterias=[]
    for i in range(1,num+1):
        bacterias.append([i,50,150,75])# Use a list to represent each bacteria.
    
    # Move each bacteria.
    def move(bacteria):                
        bacteriaX=bacteria[1]# X coordinate
        bacteriaY=bacteria[2]# Y cooordinate
        bacteriaHeight=bacteria[3]# Height
        # Rise or fall in turbulence.
        if bacteriaHeight==0:
            pass
        elif bacteriaHeight>=75:
            # If a particle's height is not less than 75 meters
            Height_random=random.random()
            if Height_random<=0.2:
                # There is a 20% chance it will rise by a metre.
                bacteriaHeight+=1
            elif Height_random>0.3:
                # There is a 70% chance it will fall one metre.
                bacteriaHeight-=1
            else:
                #There is a 10% it will stay at the same level.
                pass
        elif bacteriaHeight<75 and bacteriaHeight>0:
            # Below 75 metres, the particle will drop by a meter a second.
            bacteriaHeight-=1
        
        # Affected by wind to move horizontally.
        Direction_random=random.random()
        if Direction_random<=0.05:
            # 5% chance to move west.
            bacteriaX=bacteriaX-1*wind
        elif Direction_random>0.05 and  Direction_random<=0.15:
            # 10% chance to move east.
            bacteriaY=bacteriaY+1*wind
        elif Direction_random>0.15 and  Direction_random<=0.25:
            # 10% chance to move south.
            bacteriaY=bacteriaY-1*wind
        else:
            # 75% chance to move east.
            bacteriaX=bacteriaX+1*wind
        # Return each particle's number, coordinates and height.
        return [bacteria[0],bacteriaX,bacteriaY,bacteriaHeight] 

    # Move particles untill all particles have landed on the ground.
    count=0
    while count<num:
        count=0
        for i in range(len(bacterias)):
            if bacterias[i][3]==0:# if Height = 0：
                count+=1
                continue
            else:
                bacterias[i]=move(bacterias[i])# Update each particle's coordinates and height.
    
    # Display each particle's position by scatter plots.
    x=[]
    y=[]
    x.append(50)# Append the coordinates of the building.
    y.append(150)
    img_train = pd.read_csv('wind.txt',header=None).values
    for i in bacterias:
        x.append(i[1])
        y.append(i[2])
        img_train[i[1],i[2]]=255
    
    # Draw the background.
    fig = plt.figure(figsize=(10, 10))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1=plt.subplot(111)
    # plot particles.
    plt.xlim(0, 300)
    plt.ylim(0, 300)
    c=['r','c','g','b','r','y','g','b','m']# A list represents different colours
    t=[]
    for i in range(len(y)):
    	t.append(random.choice(c))   
    ax1.scatter(x,y,c=t)# Give particles colour randomly to improve the discrimination between particles.
    fig.savefig('Scatter_plot.jpg')# Save scatter plot.
    np.savetxt('windoutput.txt',img_train.astype(int),fmt='%d')# Save scatter plot to a file as text.
    plt.show()
'''
Step 3: Initialize GUI Window and Scale bar widget.
    
'''
# Initialize GUI main window.
root = tk.Toplevel()
root.geometry('400x300')
root.wm_title("Bacteria Bomb")
print('A GUI window should appear, please adjust the scrollbar to run the model.')
wind=1
pointnum=5000

# Pass the wind scale bar value to control the wind speed.
def getwind(value):
    global wind
    wind=value
    num=pointnum
    height=75
    get_Result(int(wind),int(num),int(height))
    
# Pass the quantity scale bar value to control the number of particles.
def getpointnum(value):
    global pointnum
    pointnum=value
    wind1=wind
    num=int(pointnum)
    height=75
    get_Result(int(wind1),int(num),int(height))

# Initialize Scale bar widget
s1 = tk.Scale(root, label=('Wind Class'),from_=0, to=3, length=200, tickinterval=1,orient=tk.HORIZONTAL,  command=getwind)
s1.pack()
s2 = tk.Scale(root, label=('Number of Particles'), from_=1000, to=5000, length=200, tickinterval=1000, orient=tk.HORIZONTAL, command=getpointnum)
s2.pack()
# Quit and destroy the main window.
def exiting():
    print('End program!')
    root.quit()
    root.destroy()    
root.protocol('WM_DELETE_WINDOW', exiting)
root.mainloop()
'''
Step 4: Draw and save the Density map.

'''
img_train = np.loadtxt('windoutput.txt')# Pull in the data of particles' distribution.

X=[]
Y=[]
for x in range(img_train.shape[0]):
    for y in range(img_train.shape[1]):
        if  img_train[x,y]!=0:
            X.append(x)
            Y.append(y)
# Draw the Density map.
fig = plt.figure(figsize=(10, 10))
ax = sns.kdeplot(X,Y, shade = True, cmap = "PuBu")
ax.patch.set_facecolor('white')
ax.collections[0].set_alpha(0)
fig.savefig('Density_map.jpg')# Save Density map as jpg picture.
plt.xlim(0, 300)
plt.ylim(0, 300)
plt.show()  
print('The density map has been saved! Thank you for running this model! ')



