from collections import deque, namedtuple
#from PIL import Image 
from PIL import Image 
from resizeimage import resizeimage
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import sqlite3
import os
import cgi
from PIL import Image,ImageTk
#import cv2

  
# Read image 
img = Image.open("C:\\Users\\HP\\Pictures\\lucif.png") 
  
# Output Images 
img.show() 
  
# prints format of image 
print(img.format) 
  
# prints mode of image 
print(img.mode) 

#import cv2
 
#img = cv2.imread("C:\\Users\\HP\\Pictures\\lucif.png", cv2.IMREAD_UNCHANGED)
 
#print('Original Dimensions : ',img.shape)
 
#width = 350
#height = 450
#dim = (width, height)
 
# resize image""
"""resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
 
print('Resized Dimensions : ',resized.shape)
 
cv2.imshow("Resized image", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()"""
# we'll use infinity as a default distance to nodes.

root = tk.Tk()
root.geometry('500x500')
root.title("Simple Navigator")
#root.configure(background="black")

class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)



        self.image = Image.open("C:\\Users\\HP\\Pictures\\lpu.png")
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)
    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)
        
e = Example(root)
e.pack(fill=BOTH, expand=YES)

label_0 = Label(root, text="Simple Navigator for LPU",width=20,font=("bold",20))
label_0.place(x=90,y=53)

label_1 = Label(root, text="Your Location",width=20,font=("bold",10))
label_1.place(x=70,y=130)

entry_1=(Entry(root,validate="key"))
#entry_1['validatecommand'] = (entry_1.register(omg),'%P')
#c=root.register(omg)
#entry_1.configure(validate="key",validatecommand=(c,'%P'))

entry_1.place(x=240,y=130)

label_2 = Label(root, text="Destination Block",width=20,font=("bold",10))
label_2.place(x=68,y=180)

entry_2=((Entry(root)))
entry_2.place(x=240,y=180)

a= str(entry_1)
b= str(entry_2)
Button(root,text='Submit',width=20,bg='orange',fg='black').place(x=180,y=420)
#Button(root,text='save',command=database,width=20,bg='pink',fg='black').place(x=300,y=420)


mainloop()


inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

#img = Image.open("C:\\Users\\HP\\Pictures\\echoo.png")


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path


graph = Graph([
    ("1", "2", 3),  ("2", "3", 3),  ("3", "5", 2), ("3", "4", 3),
    ("5", "6", 4), ("6", "7", 4), ("6", "8", 5),  ("8", "9", 8),
    ("9", "10", 5),("9", "11", 6),("9", "12", 4),("10", "11", 3),("11", "12", 3),("12", "13", 8),("13", "14", 7),
    ("14", "15", 8),("14", "30", 14),("15", "16", 7),("16", "17", 6),("16", "18", 6),
    ("17", "18", 10),("9", "10", 3),("18", "19", 8),("18", "20", 15),
    ("19", "20", 7),("20", "21", 7),("20", "22", 6),("21", "22", 3),("22", "24", 8),
    ("22", "23", 9),("24", "23", 2),("24", "25", 8),("23", "25", 6),("25", "26", 1),
    ("26", "27", 1),("26", "38", 8),("27", "28", 1),("28", "29", 1),("29", "30", 1),
    ("30", "31", 1),("31", "32", 1),("32", "33", 3),("32", "35", 6),("33", "34", 1),("33", "38", 3),
    ("34", "35", 2),("35", "36", 1),("36", "37", 1),("37", "38", 1),("38", "39", 14),
    ("39", "40", 4),("40", "41", 9),("41", "42", 7),("42", "43", 10),("43", "45", 12),
    ("40", "45", 18),("45", "46", 4),("46", "47", 7),("45", "47", 9),("47", "51", 25),
    ("45", "51", 18),("51", "52", 6),("52", "53", 6),("53", "54", 3),("54", "55", 3)])


print(graph.dijkstra("16", "30"))