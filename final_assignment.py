#path finder USING dijkstra's Algorithm
#import tkinter GUI tool kit
from tkinter import messagebox, Tk
import pygame
import sys


#create windows, width=500 hright 500
window_width= 600
window_height = 600
window = pygame.display.set_mode((window_width, window_height))


#create Grid
columns =25 
rows =25

box_width =window_width // columns
box_height = window_height //rows

grid =[]
#make a queue =[]
queue = []
#path =[]
path=[]


class Box:
    def __init__(self,i, j):
        self.x =i
        self.y =j

        self.start =False #set to true
        self.wall = False #set to true
        self.target = False 
        self.queued =False
        self.visited = False
        self.neighbours = []
        self.prior = None
        
        
    def draw(self, win, color):
        pygame.draw.rect(win,color,(self.x*box_width, self.y*box_height, box_width - 2, box_height - 2))

    def set_neighbours(self):
        if self.x > 0: 
            self.neighbours.append(grid[self.x -1][self.y])
        if self.x < columns -1:
            self.neighbours.append(grid[self.x +1][self.y])
        if self.y>0: 
            self.neighbours.append(grid[self.x][self.y -1])
        if self.y < rows -1:
            self.neighbours.append(grid[self.x][self.y +1])

#GRID 
for i in range(columns):
    myarr =[]
    for j in range(rows):
        myarr.append(Box(i,j))
    grid.append(myarr)

#set Neighbours
for i in range (columns):
    for j in range(rows):
        grid[i][j].set_neighbours()

box_start = grid[0][0]
box_start.start = True
box_start.visited=True
queue.append(box_start)

#main method
def main():
    search_start =False
    set_target_box = False
    searching = True
    target_box = None #stire the box that we want to reach
    while True:
        for event in pygame.event.get():
            #colse the window ,
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #control Mouse
            elif event.type ==pygame.MOUSEMOTION:
                x= pygame.mouse.get_pos()[0]
                y= pygame.mouse.get_pos()[1]
                #draw wall
                if event.buttons[0]:
                    i = x // box_width
                    j = y // box_height
                    grid[i][j].wall = True
                #set target
                if event.buttons[2] and not set_target_box:
                    i=x //box_width
                    j=y //box_height
                    target_box = grid [i] [j]
                    target_box.target = True
                    set_target_box =True
            #start algo
            if event.type == pygame.KEYDOWN and set_target_box:
                search_start =True


        if search_start:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0) #sets the current box variable to the first elemnt of queue
                current_box.visited = True # in each loop a box is removed formm the queue and current_box is set to true.
                if current_box == target_box: #check taken box out of the queuee is a target box or not
                    searching = False

                    #path fidingin main algo
                    while current_box.prior != box_start:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            queue.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution!")
                    searching = False

        window.fill((0, 0, 0))

        for i in range (columns):
            for j in range(rows):
                box =grid[i][j]
                box.draw(window, (20,20,20))
                if box.queued:
                    box.draw(window, (200,0,0))
                if box.visited:
                    box.draw(window, (0,200,0))
                if box in path: #
                    box.draw(window, (0,0,200))                   
                if box.start:
                    box.draw(window,(0,200,200))
                if box.wall:
                    box.draw(window,(90,90,90))
                if box.target:
                    box.draw(window,(200,200,0))
                

        pygame. display.flip()

main()