### Examples and Function Reference for Queue ###

# Constructor
q = Queue.Queue()



# Example storing simple event
simple_event = Event("simple",[""])
q.put(simple_event)

# Example storing event with data
my_event = Event("event_name",[""])
q.put(my_event)



# Retrieving queue items
q.empty() # Returns true if the queue is empty
r_event = q.get()
r_event.type # Returns a string with the event name
r_event.data[0] # Returns variables
r_event.data[1] # Returns variables



# Example
if not q.empty():

	r_event = q.get()

	if (r_event.type = "name_1"):
		# stuff 1
	elif (r_event.type = "name_2"):
		# stuff 2
