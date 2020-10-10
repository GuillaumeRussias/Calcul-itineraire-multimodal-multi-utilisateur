""" The goal of this file is to have all the information on a graph, to plot it. """

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eig


class Graph:
    """ All the information of a graph are contained here. """
    def __init__(self,pairs_of_vertices):
        """ Entry : a list of connected pairs of vertices. """
        self._pairs_of_vertices = pairs_of_vertices

    @property
    def pairs_of_vertices(self):
        """ Returns the list of connected pairs of vertices. """
        return self._pairs_of_vertices

    def number_of_edges(self):
        """ Returns the number of edges. """
        return len(self._pairs_of_vertices)

    def list_of_vertices(self):
        """ Returns the list of vertices. """
        vertices = []
        for i in self._pairs_of_vertices:
            [a,b] = i
            if a not in vertices:
                vertices.append(a)
            if b not in vertices:
                vertices.append(b)
        return vertices

    def number_of_vertices(self):
        """ Returns the number if vertices. """
        return len(self.list_of_vertices())

    def laplace_matrix(self):
        """ Returns the laplace matrix. """
        n = self.number_of_vertices()
        laplace_matrix = np.zeros((n, n))
        for i in range(n):
            laplace_matrix[i][i]=1
            for j in range(n):
                l = self.list_of_vertices()
                if [l[i],l[j]] in self._pairs_of_vertices or [l[j],l[i]] in self._pairs_of_vertices:
                    laplace_matrix[i][j]=1
        return laplace_matrix

    def list_of_coord(self):
        """ Defines the coordinates in a 2D space of each vertice using eigenvectors. """
        m = self.laplace_matrix()
        eigenvalues, eigenvectors = eig(m)
        eigenvalues = np.real(eigenvalues)
        eigen = [[eigenvectors[k], eigenvalues[k]] for k in range(len(m))]
        eigen.sort(key = lambda e : e[1], reverse=True)
        #Reverse : we take the eigenvectors associated with the two largest eigenvalues
        v1, v2 = eigen[0][0], eigen[1][0]
        return [[v1[k], v2[k]] for k in range(len(m))]

    def plot(self):
        """ Plots the graph. """
        list_of_coord = self.list_of_coord()
        x_axis = []
        y_axis = []
        for (x,y) in list_of_coord:
            x_axis.append(x)
            y_axis.append(y)
        plt.scatter(x_axis,y_axis)
        list_of_vertices = self.list_of_vertices()
        for e in self.pairs_of_vertices:
            # print(list_of_coord)
            # print(list_of_vertices)
            # print(e)
            # print(list_of_vertices.index(e[0]))
            # print(list_of_coord[list_of_vertices.index(e[0])])
            l1 = list_of_coord[list_of_vertices.index(e[0])]
            l2 = list_of_coord[list_of_vertices.index(e[1])]
            plt.plot([l1[0], l2[0]], [l1[1], l2[1]], lw=2)
        plt.axis('off')
        plt.show()







