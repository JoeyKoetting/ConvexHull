#!/usr/bin/python3
# why the shebang here, when it's imported?  Can't really be used stand alone, right?  And fermat.py didn't have one...
# this is 4-5 seconds slower on 1000000 points than Ryan's desktop...  Why?

from shape import *
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import time


class ConvexHullSolverThread(QThread):

	def __init__( self, unsorted_points, demo):
		self.points = unsorted_points					
		self.pause = demo
		QThread.__init__(self)

	def __del__(self):
		self.wait()

	show_hull = pyqtSignal(list,tuple)
	display_text = pyqtSignal(str)

# some additional thread signals you can implement and use for debugging, if you like
	show_tangent = pyqtSignal(list,tuple)
	erase_hull = pyqtSignal(list)
	erase_tangent = pyqtSignal(list)

	#################################
	# split_list
	# Split the list into lower and upper lists and return the new lists
	#
	# Time Complexity: O(n)
	# Space Complexity: O(n)
	#################################
	def split_list(self, a_list):
		half = len(a_list) // 2
		return a_list[:half], a_list[half:]

	#################################
	# divide_and_conquer
	# Splits the list into 2 recursively until their are 6 or less elements in
	# each list. Divide the list, and create shape objects with the elements.
	# Append the shape together, then recursively append each other shape
	# on each return call.
	#
	# Time Complexity: O(log n)
	# Space Complexity:
	#################################
	def divide_and_conquer(self, points):
		if len(points) > 6:
			# Recursively divide array in half
			A, B = self.split_list(points)
			shape_A = self.divide_and_conquer(A)
			shape_B = self.divide_and_conquer(B)
		else:
			# Create shape objects and append items
			firstArray = []
			secondArray = []
			if len(points) > 3:
				for i in range(len(points)):
					if i < 3:
						firstArray.append(points[i])
					else:
						secondArray.append(points[i])

				shape_1 = Shape(self, firstArray)
				shape_2 = Shape(self, secondArray)

				shape_1.append_array(shape_2)

			else:
				for i in range(len(points)):
					firstArray.append(points[i])
				shape_1 = Shape(self, firstArray)
			return shape_1

		# Recursively return bigger and bigger shapes
		shape_A.append_array(shape_B)
		return shape_A

	def run( self):
		assert( type(self.points) == list and type(self.points[0]) == QPointF )

		n = len(self.points)
		print( 'Computing Hull for set of {} points'.format(n) )

		t1 = time.time()

		# SORT THE POINTS BY INCREASING X-VALUE
		self.points.sort(key = lambda p: p.x())

		t2 = time.time()
		print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

		t3 = time.time()

		# COMPUTE THE CONVEX HULL USING DIVIDE AND CONQUER
		circle = self.divide_and_conquer(self.points)

		t4 = time.time()

		# DISPLAY HULL
		circle.show_shape()
			
		# send a signal to the GUI thread with the time used to compute the hull
		self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
		print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
