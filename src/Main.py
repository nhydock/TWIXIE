import threading

_internal_resolution = [320, 240]	#size that the engine should render in
_output_resolution = [800, 600]		#size that the engine will output for viewing and interacting

class Runner(threading.Thread):
	#Runner method for the update thread
	#this controls update calls to the system and graphic components of the program
	def run(self):
	
		#start/initializes the Thread and its engine components
		i = 0
		#engine = Engine()
		#graphics = ClientComponent(_internal_resolution, _output_resolution, ClientComponent.SDL)
	
		while True:
			i += 1
			print "brrrr"
			if i > 20:	
				break;	#kill the thread

#main execution method
def main():
	thread = Runner()
	thread.start()

	
if __name__ == '__main__':
	main()
