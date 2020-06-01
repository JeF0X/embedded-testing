import time
import threading
from pushbullet import Pushbullet

portArduino = serial.Serial("/dev/ttyACM0", baudrate=9600, timeout=1)
portNucleo = serial.Serial("/dev/ttyACM1", baudrate=9600, timeout=1)
api_key = "XXXXXXXXXXXXXXXXXXXXXXXXX" #PushBullet API-key
pushB = Pushbullet(api_key)
bulletIsKilled = False

#Write html page to server for Temperature
def tempToHtml(nFloat):
    htmlFile = open("/var/www/html/index.html", "w")
    htmlFile.write("<!Doctype html>")
    htmlFile.write("<head><meta http-equiv=\"refresh\" content=\"3\"> </head>")
    htmlFile.write("<html>")
    htmlFile.write("<body><h1>")
    htmlFile.write(str(nFloat))
    htmlFile.write("</h1></body>")
    htmlFile.write("</html>")
    htmlFile.close()

#Get latest message from in PushBullet thread to check for any commands by user
def pushToBullet():
    global bulletIsKilled
    pushes = pushB.get_pushes() #Get messages from pushbullet
    latest = pushes[0]
    lastMessage = latest.get("body") #Message body for latest message
    if lastMessage == "STOP":
        time.sleep(1800)		#sleep thread for 30 minutes
    elif lastMessage == "KILL":
        bulletIsKilled = True
        return
    else:
        bulletIsStopped = False;
        pushB.push_note("HALYTYS!", "Vesivuoto!") #Send message to Pushbullet
    time.sleep(60)

#Nucleo thread
def readNucleo():
    while True:
        rcvN = portNucleo.readline().strip() #read serial
        #try to convert reading to float
		try:
            nFloat = round(float(rcvN), 1)
            tempToHtml(nFloat)
            portNucleo.reset_input_buffer()
        except ValueError:      #If the reading cannot be converted to float do nothing
            pass

#Arduino thread
def readArduino():
    global bulletIsKilled
    while bulletIsKilled == False: #If user has given KILL message, run the thread to end
        rcvA = portArduino.readline().strip() #read serial
		#try to convert reading to float
        try:
            aFloat = float(rcvA)
            pushToBullet()
            portArduino.reset_input_buffer()
        except ValueError:		#If the reading cannot be converted to float do nothing
            pass

def main():
     #Start threads
     threading.Thread(target=readNucleo).start()
     threading.Thread(target=readArduino).start()

if __name__ == '__main__':main()
