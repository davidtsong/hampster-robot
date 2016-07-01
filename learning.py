import threading
import time
from Queue import *
# a = 2 + 2
# c = [1,2,3,4,5]
# if(a > 3):
# 	print "A is greater than 3"
# else:
# 	print "A is not greater than 3"
# for i in range(10):
# 	print i
# for i in c:
# 	print "The number is " + str(i)
# userInput = raw_input("What would you like to enter?")

# #Print out in letters
# for i in range(len(userInput)):
# 	print userInput[i]

# #Add two numbers
# firstNum = raw_input("What is the first number to add?")
# secondNum = raw_input("What is the second number to add?")
# def add(x,y):
# 	return int(x) + int(y)
# print add(firstNum,secondNum)

# #These two do the same
# sequence = range(100)
# sum1 = 0
# sum2 = 0;
# for i in range(len(sequence)):
# 	sum1 = add(sum1, sequence[i])
# for num in sequence:
# 	sum1 = add(sum1, num)

# class Mountain:
# 	thing = ""
# 	def __init__(self, character):
# 		self.thing = character; 

# 	def printline(self, length):
# 		line = ""

# 		for i in range(length):
# 			line += self.thing
# 		print(line)

# 	def printMountain(self, length):
# 		for i in range(length):
# 			self.printline(i)
# 	def __str__(self):
# 		for i in range(length):
# 			self.printline(i)

# i = Mountain("c")
# lengthofMountain = raw_input("Length of mountin = ?")
# # i.printMountain(int(lengthofMountain)) #Does the same as below due to __str__
# print "Bow down to the mountain \n {}".format(str(i))#String formatting


#Review with James

q = Queue()

class Car:
    def __init__(self):
        self.color = ''
        self.numWheels = 4
        self.model = ''

    def setColor(self,color):
        self.color = color

    def getColor(self):
        return self.color

def thread1():
	done = True
	i = 0
	while done:
		q.put(i)
		i+=1
		print "put i"
		time.sleep(.1)
		if i >= 10:
			done = False

def thread2():
	while True:
		if not q.empty():
			print q.get()	
def main():
    tesla = Car()
    tesla.setColor("red")
    print (tesla.getColor())

    thread = threading.Thread(target = thread1)
    thread.daemon = True
    thread.start()

    threadread = threading.Thread(target=thread2)
    threadread.daemon = True
    threadread.start()

    thread.join()
    threadread.join()
    print "Thread is done"
main()









