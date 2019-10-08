
# MENG Final Year project - University of Birmingham, Department of Electrical and Electronic Engineering 
# Project Runtime:      10/2018 - TBC/2019
# Creator:              Jordan Andrew (Kelly) Small - 1561404
# Project Supervisor:   Robert Stone
# Title:                Medical Emergency Response Teams (MERT) - Desktop Application
# Summary:              Controls the Pulse simulator through bluetooth communication
# Languages:            Python (Backend) and Kivy (Frontend)

# This is a test for the test branch within github
# Test

# Libraries
import serial           # Bluetooth serial properties 
import time             # Delay properties throughout the application   
import kivy             # Import Kivy library
import xlrd             # Allow Excel files to be READ
import xlwt             # Allow Excek files to be WROTE

kivy.require ("1.9.1")			  				# Stating Kivy Version
from kivy.config import Config					# Import configuration file to be able to load kivy modules
from kivy.app import App						# Import App Class; the basis for the Kivy Application
from kivy.uix.widget import Widget				# Import widget library to present the widgets in the application window
from kivy.uix.image import Image                # Import Image to allow the use of custom images i.e. Heart image in main window
from kivy.lang import Builder                   # Import Builder to parse from kivy to python
from kivy.graphics import Color, Rectangle      # Allow rectangle to be used during Kivy
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition        # Import fade transition for the evaluation windows
from kivy.uix.floatlayout import FloatLayout    # Import Float layout attributions
from kivy.uix.label import Label                # Import Label assets
from kivy.uix.popup import Popup                # Import popup attributes for the evaluation windows
from kivy.animation import Animation            # Import animation for the evaluation window tranistion
from datetime import datetime                   # Import the date and time library for the excel document


# Desktop Window Size - This is a static application. For simplication, it'll be a fixed size...
Config.set('graphics', 'resizable', '0')    # 0 states the margin of realizability i.e.  none
Config.set('graphics', 'width', '700')      # Widnow Size (WIDTH)
Config.set('graphics', 'height', '500')     # Window Size (HEIGHT)
Config.set('graphics', 'resizable', False)  # Window is not resizable


# Globabl Variables - Accessed throughout the entiraty of the system...
connect = False			        # Global Bluetooth Variable is set to false 
start_ = False                  # During Perception Evaluation, this states whether the test has begun
user_started_Test = False       # JND Evaluation - During JND Evaluation, this states whether the test has begun
slider_value = "40"		        # The slider value is initialised to the starting value
statusString = "Disconnected"   # The statusString that states if the BLE is connected is initialised to false i.e. 'Disconnected'
evaluation_value = 60           # For the Perpection Evaluation Test, the first value is 60BPM. Thus, is initial value. 
incrementvalue = 60             # Incremental value (Showing the next value to be tested during the evaluation), is initialised to 60 aswell
deincrementvalue = 60           # - Also initialised to 60... All set during accordingly within the evaluation.
iterations = 0                  # During perception Evaluation this acts as the COUNTER
saveincrement = 0               # To prevent ERRORs during the Excel sheet WRITE, the is incremented by this value
i_JND = 0                       # JND Evaluation - Counter to keep track of the JND test
trial_no = 0                    # JND Evaluation - What trial number is this?
HR_to_test = 0                  # JND Evaluation - What HR/BPM is being sent during the JND evaluation
order_of_fastest = 0            # JND Evaluation - What is the order of the non-constant value?
correct_response = 1            # JND Evaluation - Variable stating the correct Answer


# MICROSOFT EXCEL, READ SHEET - Reading the spreadsheet file 
book = xlrd.open_workbook("JND_Trials.xlsx")    # Open the spreadsheet file
sheet = book.sheet_by_index(0)                  # Open the first and ONLY sheet in JND_Trials
            

# MICROSOFT EXCEL, WRITE SHEET - Writing to the spreadsheet file
wb = xlwt.Workbook()                    # Create a blank spreadsheet file
ws = wb.add_sheet("A Test Sheet")       # Create a sheet within the file


# Attempt to connect to the bluetooth module, If not THEN don't freeze and continue (ERROR Prevention)
try:                                                # Try open the bluetooth port
    port="/dev/tty.DSDTECHHC-05-DevB"               # Address of the bluetooth port in relation to THIS PC - CHANGE on a different system
    bluetooth=serial.Serial(port, 9600)             # Baud rate of 9600 as standard
    bluetooth.flushInput()                          # Flush the input, bytes available = 0. 
    bluetooth.write(b"CON")                        # Attempt to write to the BLE modules
    connect = True  # Connection is successful      # if the TRY function is successful the connection is TRUE
    statusString = "Connected"                      # Tell the user the connection is successful
   
except:                                             # FAILURE - If failed simply tell the user a connection wasn't possible              
    connect = False                                 
    statusString = "Disconnected"



    
    

# Class 1 of 4 - KIVY Widget, MAIN SCREEN Delegate: All Function WRT the homescreen are located here...   
class Widgets(Widget):                  # Main Screen

    def btn(self):                      # Evaulation screen button - E1 (PERCEPTION EVALUATION)
        show_popup()                    # Activates the popup function to present the screen


    def btn2(self):                     # Evaulation screen button - E2 (JND EVALUATION)
        show_popup2()                   # Activates the popup function to present the screen


    def update(self, *args):            # Slider delegate - Able to extract the current value from the slider
        global slider_value             # Access to slider value   

        slider_value = str(int(args[1]))                # Cast it to a string for the Label 
        self.lblid.text = str(slider_value) + " BPM"    # Present information of the status of the lable. i.e. 60BPM, 55 PBM
        print("BMP = ", slider_value)                   # print to console aswell 
        

    def on_off(self, *args):            # ON OFF Button - Turns the pulse generator on or off
        global bluetooth                # Access to the bluetooth Variable
        global statusString             # Access to the Status String
		
        if args[0].state == 'down':     # IF the state of the button is down, DO The following...
            try:                        # TRY This is we have bluetooth connection DO NOT Freeze the program - ERROR Control
                print("ON")             # Print a message to the console stating the user has pressed the ON Button
                self.btnid.text = str("ON")                 # Set the button text to say ON
                string_send = str(length_) + str(string_)   # Prepare the message - 
                string_ = "ONN" + str(slider_value)         # Command for the Arduino Code - This will recognise the Pulse should be ON
                length_ = len(string_)                      # Get the LENGTH of this string - This should be 3
                string_send = str(length_) + str(string_)   # Combine the strings - "Length (packet size)" + "Message (Payload)"
                bluetooth.write(b""+str.encode(str(string_send)))   # Write to the BLE
                statusString = "Connected"                          # State the Bluetooth is connected 
                self.main_status.text = str("BLE Pulse is ON")      # Update the main status
                self.lblid2.text = str(slider_value)                                # Update the second label - Showing the current pulse
                self.bluetooth_.text = str("Bluetooth (" + statusString +")" )      # State the Bluetooth is connected
            except:                       # IF you FAIL - Then go through this routine: State a connection can't be made, thus can't send data
                print("Couldn't Turn BLE Pulse ON")
                self.main_status.text = str("Couldn't Turn BLE Pulse OFF")
                statusString = "Disconnected"
                self.bluetooth_.text = str("Bluetooth (" + statusString +")" )
        else:                                   # If the button is OFF, then go through this routine
            try:                                # IF a connection is possible TRY The following - Send a message to pause the PUSLSE  
                print("OFF")                    # State to the console that the pulse is off 
                self.btnid.text = str("OFF")    # Set the button label to OFF
                bluetooth.flushInput()          # Clean the input of the Bluetooth
                string_ = "OFF"                 # Prepare the message - Will send the OFF command
                length_ = len(string_)                              # Get the length of the message
                string_send = str(length_) + str(string_)           # Combine the two - now ready to send the message
                bluetooth.write(b""+str.encode(str(string_send)))   # Write to the Bluetooth
                self.lblid2.text = str(0)                           # Set the label to 0, as there is no Pulse currently on the system
                statusString = "Disconnected"                                       # Set the status as disconnected
                self.bluetooth_.text = str("Bluetooth (" + statusString +")" )      # Set the status as disconnected
                self.main_status.text = str("Pulse is OFF")                         # Tell the user the pulse is OFF
            except:                             # IF the CONNECTION isn't possible - Then say the system is disconnected...
                print("Couldn't Turn BLE Pulse OFF")
                self.main_status.text = str("Couldn't Turn BLE Pulse OFF")
                statusString = "Disconnected"
                self.bluetooth_.text = str("Bluetooth (" + statusString +")" )


    def send_pulse_data(self):          # Send button - Sending the selected value to the bluetooth
        global slider_value             # Access to the slider value 
        global bluetooth                # Access to the bluetooth variable
        global statusString             # Access to the status string

        if slider_value == '':          # If the slider value is BLANK initialise it to 40
            slider_value = 40           # set to 40 BPM
        try:                                                                # TRY send data if a BLUETOOTH connection is enabled
            print("**** Data Sending to BLE ****")                          # Print to console as to what the system is doing
            self.main_status.text = str("Data Sending to BLE")              # Tell the user what's happening 
            print("Data Out: BPM Value =", slider_value)                    # print to console the value to be sent 
            
            # Go through the Packet Process as before: Packet (Size of packet | Message ) -> then update GUI
            bluetooth.flushInput()                                          
            string_ = "BPM" + str(slider_value)                             
            length_ = len(string_)
            string_send = str(length_) + str(string_)
            bluetooth.write(b""+str.encode(str(string_send)))
            time.sleep(0.1)		# This is needed otherwise the connection is closed to fast
            statusString = "Connected"
            self.bluetooth_.text = str("Bluetooth (" + statusString +")" )
            self.lblid2.text = str(slider_value +" BPM")
            self.main_status.text = str("")
            print(string_send)
        except:                                                             # If this fails, tell the user a connection cannot be established                
            print("Couldn't Send Data, check connection")
            self.main_status.text = str("Couldn't Send Data, check connection")
            statusString = "Disconnected"
            self.bluetooth_.text = str("Bluetooth (" + statusString +")" )
        

    def connectbtn_clk(self, *args):        # Connect Button - Attempting to establish a connection with the bluetooth module
        global bluetooth                    # Access to bluetooth variable
        global connect                      # Access to connect variable
        global port                         # Access to bluetooth 'port'variable
        global statusString                 # Access to status string variable

        self.main_status.text = str("Attempting to Connect to BLE.....")        # Set the status - to show the user is attempting to connect
        print("Attempting to Connect to BLE.....")                              # Print to the console

        try:                                                                    # TRY open a connection with the Bluetooth module
            port="/dev/tty.DSDTECHHC-05-DevB"                                   # Use this port
            bluetooth=serial.Serial(port, 9600, timeout=2)                      # Use the port as stated at 9600 baud, please stop after 2 seconds.
            print("Connection Established")                                     # Print to console to state it was successful 
            print("Cleaning BLE Input port")                                    # Print to console - tell me your status
            bluetooth.flushInput()                                              # This gives the bluetooth a kick and cleans the port ready for new data
            print("Device Ready....")                                           # Print to console - tell me you're ready

            # Send a packet of data - to get the Arduino ready
            string_ = "CON"                                                     # Send a CON message - Arduino will recieve and prepare the system
            length_ = len(string_)                                              # Get the length of the message
            string_send = str(length_) + str(string_)                           # Combine to create the packet
            bluetooth.write(b""+str.encode(str(string_send)))                   # Write to the bluetooth module
            input_data=bluetooth.readline()                                     # If anything is incoming, take it
            print(input_data.decode())                                          # Tell me what the bluetooth said back
            statusString = "Connected"                                          # Set the status as true 
            self.bluetooth_.text = str("Bluetooth (" + statusString +")" )      # Set the status as connected
            self.main_status.text = str("Connected")                            # Set the status as connected 
            time.sleep(0.1)	                                                    # Rest for a short period - prevent buffer overload
        except:                                                                 # IF all Fails - Tell the user a connection is not established
            print("Can't open")
            self.main_status.text = str("Can't open")
            statusString = "Disconnected"
            self.bluetooth_.text = str("Bluetooth (" + statusString +")" )
    

    def disconnectbtn_clk(self):                                    # Disconnect Button - Disconnecting from the Bluetooth Device
        global bluetooth                                            # Access the bluetooth variable 
        global statusString                                         # Access the status string variable

        try:                                                        # TRY Disconnect from the bluetooth IF you are stil connected
            string_ = "DIS"                                         # Load the disconnect Message
            length_ = len(string_)                                  # Get the length of the string
            string_send = str(length_) + str(string_)               # Combine the strings and send the message to the Bluetooth
            bluetooth.write(b""+str.encode(str(string_send)))       # Write this to the bluetooth

            bluetooth.flushInput()                                  # Remove anything from the input
            bluetooth.flushOutput()                                 # NEW (Remove if a problem) - Remove anything from the output
            bluetooth.close()                                       # Close the connection - Bluetooth should now be open to other users

            # Update the GUI on the status as before...
            print("Bluetooth Disconnected")
            self.main_status.text = str("Bluetooth Disconnected")
            statusString = "Disconnected"
            self.bluetooth_.text = str("Bluetooth (" + statusString +")" )
        except:                             # If this has FAILED - tell the user the bluetooth is already disconnected
            statusString = "Disconnected"
            self.bluetooth_.text = str("Bluetooth (" + statusString +")" )
            print("Already Disconnected")
            self.main_status.text = str("Already Disconnected")
        


# evaluation_value = 60  #Starting Value
# incrementvalue = 60
# deincrementvalue = 60

# iterations = 0
# start_ = False


# Class 2 of 4 - EvaluationWindow as FloatLayout, PERCEPTION EVALUATION SCREEN Delegate: All Functions WRT the Evaluation are located here...  
class EvaluationWindow(FloatLayout):

    def next_value_evaluation (self):                           # Get the next value in evaluation test                
        global evaluation_value                                 # Access evaluation_value Variable
        global incrementvalue                                   # Access incrementvalue Variable
        global deincrementvalue                                 # Access deincrementvalue Variable
        global statusString                                     # Access statusString Variable

        if evaluation_value < 140:                              # Set a boundary of 140 BPM (Highest value to be tested)
            evaluation_value = evaluation_value + 10            # Increment next value to the next bpm by 10
            incrementvalue = evaluation_value + 10              # Set the value after the current another 10 higher
            deincrementvalue = evaluation_value - 10            # Set the previous test value to lower than the current value
            self.current_hr.text = str(evaluation_value)        # Set label
            self.increment.text = str(incrementvalue)           # Set label
            self.deincrement.text = str(deincrementvalue)       # Set label

        if evaluation_value == 140:                             # If the Test has reached 140 (Max Value) Stop incrementing
            self.increment.text = str("N/A")                    # Tell the user they've reached the max
            evaluation_value = 140                              # Remain at 140 if they press next repeatedly


    def prev_value_evaluation (self):                           # Get the previous value in the evaluation test
        global evaluation_value                                 # Access evaluation_value Variable
        global incrementvalue                                   # Access incrementvalue Variable
        global deincrementvalue                                 # Access deincrementvalue Variable
        global statusString                                     # Access statusString Variable

        if evaluation_value > 60:                               # Set a boundary of 60 BPM (Lowest value to be tested)
            evaluation_value = evaluation_value - 10            # deincrement next value to the next bpm by 10
            incrementvalue = evaluation_value + 10              # Set the value after the current another 10 higher
            deincrementvalue = evaluation_value - 10            # Set the previous test value to lower than the current value
            self.current_hr.text = str(evaluation_value)        # Set label
            self.increment.text = str(incrementvalue)           # Set label
            self.deincrement.text = str(deincrementvalue)       # Set label

        if evaluation_value == 60:                              # If the Test has reached 60 (Min Value) Stop deincrementing
            self.deincrement.text = str("N/A")                  # Tell the user they've reached the min
            evaluation_value = 60                               # Remain at 60 if they press next repeatedly
        
        print(evaluation_value)                                 # Print to console - Tell me the current evaluation value 
    

    def start_button(self):                                     # Start Button - Starts the Evaluation
        global start_                                           # Access to start_ variable
        global bluetooth                                        # Access to bluetooth variable
        global evaluation_value                                 # Access to evaluation_value variable
        global statusString                                     # Access to statusString variable

        try:                                                            # If a bluetooth connection is established - TRY this code
            start_ = True                                               # State the evaluation has began
            print("Starting Assessment")                                # print to the console that the user has begun
            self.evaluation_status.text = str("Running")                # Tell the user that the test is running 
            print("**** Data Sending to BLE ****")                      # Print to console that data is being sent
            print("Data Out: BPM Value =", evaluation_value)            # Print to console the evaluation value that is being sent...
            statusString = "Connected"                                  # Visually show that a connection is established
            bluetooth.flushInput()                                      # Clean the input 

            string_ = "BTS" + str(evaluation_value)                     # Bpm Testing Start BTS
            length_ = len(string_)                                      # Obtain the length of the string
            string_send = str(length_) + str(string_)                   # Send the packet
        
            bluetooth.write(b""+str.encode(str(string_send)))           # These need to be bytes not unicode, plus a number
            time.sleep(0.1)		                                        # Rest

        except:                                                         # If you fail - tell the user you have disconnected
            print("Can't Start")
            statusString = "Disconnected"
        

    def end_button(self):                                               # End button -  End the assesment for the user
        print("Ending Assessmnet")                                      # print to console that the evaluation is ending
        global start_                                                   # Access start_ variable
        global iterations                                               # Access iterations variable
        global bluetooth                                                # Access bluetooth variable
        global evaluation_value                                         # Access evaluation_value variable
        global statusString                                             # Access statusString variable

        try:                                                            # If a bluetooth connection is available - Try to stop the evaluation
            self.evaluation_status.text = str("Idle")                   # Set the status of the test to idle if the test has stopped
            if start_ == True:                                          # If the test is running then stop...
                start_ = False                                          # Set the start_ command to False to stop the evaluation
                iterations += 1                                         # increment the counter
                self.it.text = str(iterations)                          # show the counter
                print(iterations)                                       # Print to the console the iteration count

            bluetooth.flushInput()                                      # Clean the input of the Port
            string_ = "BTF0"                                            # Send a finished command and a 0 for the arduino to stop the pulse
            length_ = len(string_)                                      # Get the length of the message
            string_send = str(length_) + str(string_)                   # Prepare the message
            bluetooth.write(b""+str.encode(str(string_send)))           # Write to the bluetooth
            time.sleep(0.1)		                                        # Rest
            statusString = "Disconnected"                               # Set the status to disconnected
        except:                                                         # IF you FAIL, say it cannot be disconnected
            print("Can't End")                                          # print to console the current status....
            

    def restart(self):                                                  # R Button - Restart the evaluation 
        global iterations                                               # Access the iterations variable
        global evaluation_value                                         # Access the evaluation_value variable
        global incrementvalue                                           # Access the incrementvalue variable
        global deincrementvalue                                         # Access the deincrementvalue variable
        global statusString                                             # Access the statusString variable

        # Reset Everything: ...
        iterations = 0                                                 
        evaluation_value = 60
        incrementvalue = 70
        deincrementvalue = 50
        self.it.text = str("0")
        self.current_hr.text = str(evaluation_value)
        self.increment.text = str(incrementvalue)
        self.deincrement.text = str("N/A")
        self.evaluation_status.text = str("Idle")

        try:                                                            # If a bluetooth connection is available - do the following 
            bluetooth.flushInput()                                      # Clean the input
            string_ = "BTF0"                                            # Prepare the stop message for the arduino
            length_ = len(string_)                                      # Get the length of the message
            string_send = str(length_) + str(string_)                   # Construct the packet to be sent to the aruino

            bluetooth.write(b""+str.encode(str(string_send)))           # Write to the bluetooth
            statusString = "Connected"                                  # State to the user that the system is STILL connected
            time.sleep(0.1)	                                            # Rest
        except:                                                         # If all FAILS tell the user the system is not connected
            print("Can't Restart")
            statusString = "Disconnected"


# Class 3 of 4 - SecondEvaluationWindow as FloatLayout, JND EVALUATION SCREEN Delegate: All Functions WRT the Evaluation are located here...  
class SecondEvaluationWindow(FloatLayout):

    def first_btn(self):                                        # Get the first JND value for the participant
        global user_started_Test                                # Access the user_started_Test variable
        global sheet                                            # Access the sheet (EXCEL) variable
        global ws                                               # Access the ws (EXCEL) variable
        global HR_to_test                                       # Access the HR_to_test variable
        global trial_no                                         # Access the trial_no variable
        global order_of_fastest                                 # Access the order_of_fastest variable
        global correct_response                                 # Access the correct_response variable
        global i_JND                                            # Access the i_JND variable
        global statusString                                     # Access the statusString variable
        
        try:                                                    # TRY to write to the EXCEL Document - the no. of the test and the value to be tested
            ws.write(i_JND+1,2,str(HR_to_test[7:10]))           # Write to Excel
        except:                                                 # If you fail print an error
            print("Error")
         
        user_started_Test += 1                                    

        if user_started_Test > 1 :

            if i_JND <=120:

                HR_to_test = str(sheet.cell(1+i_JND,4))     # Y - 123 , X - ABCD
                trial_no = str(sheet.cell(1+i_JND,3))
                order_of_fastest = str(sheet.cell(1+i_JND,5))
                correct_response = str(sheet.cell(1+i_JND,6))
                downCast_iterations = str(sheet.cell(1+i_JND,3))
            
                try:
                    print("User thinks the FIRST Value is faster")
                    ws.write(i_JND+1,0,str(i_JND))
                    ws.write(i_JND+1,1,"F")
                    string_ = "JND" + str(HR_to_test[7:10]) + str(order_of_fastest[6])    # JND STRING   - Send a zero to stop the pulse simulator
                    length_ = len(string_)
                    string_send = str(length_) + str(string_)
                    i_JND += 1
                    self.test_iterations_lbl_JND.text = str(i_JND) +"/"+"120"
                    print(i_JND)
                    print(string_send)

                    bluetooth.write(b""+str.encode(str(string_send)))    #These need to be bytes not unicode, plus a number
                    statusString = "Connected"
                    # self.bluetooth_.text = str("Bluetooth (" + statusString +")" )
                except:
                    print("Bluetooth Not connected")

            else:
                print("No Test Running")


    def second_btn(self):   
        print("Second")
        global user_started_Test
        global sheet
        global HR_to_test
        global trial_no
        global order_of_fastest
        global correct_response
        global i_JND
        global ws
        
        try:
            ws.write(i_JND+1,2,str(HR_to_test[7:10]))
        except:
            print("")

        user_started_Test += 1

        if user_started_Test > 1:

            if i_JND <=120:

                HR_to_test = str(sheet.cell(1+i_JND,4))     # Y - 123 , X - ABCD
                trial_no = str(sheet.cell(1+i_JND,3))
                order_of_fastest = str(sheet.cell(1+i_JND,5))
                correct_response = str(sheet.cell(1+i_JND,6))
                downCast_iterations = str(sheet.cell(1+i_JND,3)) 

                try: 
                    print("User thinks the SECOND Value is faster")

                    ws.write(i_JND+1,0,str(i_JND))
                    ws.write(i_JND+1,1,"S")

                    string_ = "JND" + str(HR_to_test[7:10]) + str(order_of_fastest[6])    # JND STRING   - Send a zero to stop the pulse simulator
                    length_ = len(string_)
                    string_send = str(length_) + str(string_)
                    i_JND += 1
                    self.test_iterations_lbl_JND.text = str(i_JND) +"/"+"120"
                    print(i_JND)
                    print(string_send)
                    bluetooth.write(b""+str.encode(str(string_send)))    #These need to be bytes not unicode, plus a number
                    statusString = "Connected"
                except:
                    print("Bluetooth Not connected")
            else:
                print("No Test Running")


    def start_test_btn(self):
        print("Start Test")
        
        global user_started_Test
        global sheet
        global HR_to_test
        global trial_no
        global order_of_fastest
        global correct_response
        global i_JND

        # Collumn E = 4, 
        HR_to_test = str(sheet.cell(1,4))     # Y - 123 , X - ABCD
        trial_no = str(sheet.cell(1,3))
        order_of_fastest = str(sheet.cell(1,5))
        correct_response = str(sheet.cell(1,6))
        downCast_iterations = str(sheet.cell(1,3)) 

        user_started_Test += 1 # increment the test
        
        # If the user has started the test send the first packet
        if user_started_Test <= 1 : 

            try:
                string_ = "JND" + str(HR_to_test[7:10]) + str(order_of_fastest[6])    # JND STRING   - Send a zero to stop the pulse simulator
                length_ = len(string_)
                string_send = str(length_) + str(string_)
                i_JND += 1
                self.test_iterations_lbl_JND.text = str(i_JND) +"/"+"120"
                bluetooth.write(b""+str.encode(str(string_send)))    #These need to be bytes not unicode, plus a number
                statusString = "Connected"
            except:
                print("Bluetooth Not connected")
        else:
            print("End test before running again")

    def end_test_btn(self):
        print("End Test")
        global i_JND
        global user_started_Test
        user_started_Test = 0   # Reset the Test
        i_JND = 0
        self.test_iterations_lbl_JND.text = "_ /_"

    def extract_result(self):
        global ws
        global saveincrement

        saveincrement = saveincrement + 1
        ws.write(0,0, str(datetime.now()))
        ws.write(1,0,"Trial")
        ws.write(1,1,"Given Answer")
        ws.write(1,2,"Value")
        wb.save("JND TEST.xls")
        ws = wb.add_sheet("A Test Sheet" + str(saveincrement))
        print("Extracting Result")


# Class 4 of 4 - MainApp - This returns the whole kivy application and the elements within program 
class MainApp(App):

    def build(self):
        return Widgets()

def show_popup():           # Function 
    global statusString
    show = EvaluationWindow()
    popupWindow = Popup(title = "Piezo Evaulation: Perception Test" + str("                               Bluetooth ")+ "(" + str(statusString) + ")", content=show, size_hint=(None, None), size=(1260,900) )
    popupWindow.open()

def show_popup2():          # Function 
    global statusString
    show = SecondEvaluationWindow()
    popupWindow = Popup(title = "Piezo Evaulation: JND Test " + str("                                              Bluetooth ")+ "(" + str(statusString) + ")", content=show, size_hint=(None, None), size=(1260,900) )
    popupWindow.open()

if __name__ == "__main__":
    MainApp().run()
