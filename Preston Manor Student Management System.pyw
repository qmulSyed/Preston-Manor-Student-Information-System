# +----------------------------------------------------------------------------------------+
# Import libraries/modules
# +----------------------------------------------------------------------------------------+

from functools import partial
from time import strftime 
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
import datetime
import sys
import time
import winsound

# +----------------------------------------------------------------------------------------+
# Define global constants
# +----------------------------------------------------------------------------------------+

constAppTitle="Preston Manor Student Management System"
constProjectName="Classroom"

# +----------------------------------------------------------------------------------------+
# Define objects
# +----------------------------------------------------------------------------------------+

class Student:
    name=''
    attendance=''
    recentResult=''
    address=''
    email=''
    guardianName=''
    guardianPhoneNum=''
    lessonsSupposedtoBeAttended=0
    lessonsAttended=0
    
class Classroom:
    title=""
    teacher=""
    numStudents=0
    aStudents=[256]

# +----------------------------------------------------------------------------------------+
# Define global variables
# +----------------------------------------------------------------------------------------+

timeLabel=""
splashRoot=""
root=''
frame=0
canvas=0
classTitleBox=""
teacherNameBox=""
studentNumBox=""
rollNumBoxGroup=[256]
studentNameBoxGroup=[256]
attendanceBoxGroup=[256]
recentResultBoxGroup=[256]
viewDataButtonGroup=[256]
currentLessonAttendanceBoxGroup=[256]
cClassroom=Classroom()
RenderGraphButton=''
bLogonWindowOpened=False
bAuthenticationDone=False

# +----------------------------------------------------------------------------------------+
# Define functions
# +----------------------------------------------------------------------------------------+

def loadMainApp():
    global root
    global frame
    global canvas
    global cClassroom
    global classTitleBox
    global teacherNameBox
    global studentNumBox
    global RenderGraphButton
    
    root=Tk()
    
    # Set app title
    root.title(constAppTitle)
    
    # Adjust app size and location on the screen
    windowX=((root.winfo_screenwidth()/2))-(1024/2)
    windowY=((root.winfo_screenheight()/2.2))-(640/2)
    root.geometry("%dx%d+%d+%d" % (1024,640,windowX,windowY) )
    root.resizable(False, False)

    # Create the menu
    createMenu(root) # Calls a function which creates the drop down menu

    # Create an environment for scrollbar
    canvas = Canvas(root,highlightthickness=0) # Create a canvas to hold the widgets which are effected by scrollbar
    canvas.pack(side=LEFT) # Place the canvas on left side of the window
    scrollbar = Scrollbar(root, command=canvas.yview) # Create the scrollbar
    scrollbar.pack(side=LEFT, fill='y') # Place scrollbar in the left side
    canvas.configure(yscrollcommand = scrollbar.set) # Make sure the scrollbar affects the widgets in canvas
    canvas.bind('<Configure>', on_configure) # Set command for configuring canvas
    canvas.bind_all("<MouseWheel>", _on_mousewheel) # Enable mouse wheel functionality for scrollbar
    frame = Frame(canvas) # Create a frame for canvas
    canvas.create_window((0,0), window=frame, anchor='nw') # Create canvas window
    canvas.config(width=700, height=400) # Set the size of canvas window--it should only cover the content of register, not anything else.

    # Create GUI widgets such as buttons, logos and text boxes etc
    currentTime=datetime.datetime.now() # Returns the current time so it can be displayed
    currentDate=currentTime.strftime("%Y-%m-%d") # Returns the date in format Year: Month: Day
    currentTime=currentTime.strftime("%H:%M:%S") # Returns the present time in format Hours: Minutes: Seconds
    dateLabel=Label(root, text=currentDate, bg="gray95")
    dateLabel.place(x=2,y=5) # Display today's date on top left
    global timeLabel
    timeLabel=Label(root, text=currentTime, bg="gray95")
    timeLabel.place(x=970,y=5) # Display time on top right
    updateClock() # Calls a function which updates the clock every second through recursion
    classTitleBox=Entry(root,width=32,justify='center') # Create a text box for the class name
    classTitleBox.place(relx=0.5, rely=0.02, anchor=CENTER)
    classTitleBox.insert(0,"Untitled "+constProjectName)
    checkClassroomName=root.register(validateClassName)
    classTitleBox.config(validate="focusout", validatecommand =(checkClassroomName, '%P')) # Set a validate function for the class title text box
    cClassroom.title="Untitled "+constProjectName
    teacherNameBox=Entry(root,width=32,justify='center') # Create a text box for the teacher's name
    teacherNameBox.place(relx=0.5, rely=0.06, anchor=CENTER)
    teacherNameBox.insert(0,"Just Another Preston Manor Teacher")
    cClassroom.teacher="Just Another Preston Manor Teacher"
    checkTeacherName=root.register(validateTeacherName)
    teacherNameBox.config(validate="focusout", validatecommand =(checkTeacherName, '%P')) # Set a validate function for the teacher name text box
    studentNumBox=Entry(root,width=6,justify='center') # Create a text box for the number of students in class
    studentNumBox.place(relx=0.47, rely=0.09, anchor=CENTER)
    studentNumBox.insert(0,"256")
    cClassroom.numStudents=256
    checkStudentNum=root.register(validateStudentNum)
    studentNumBox.config(validate="focusout", validatecommand =(checkStudentNum, '%P')) # Set a validate function for the student number text box
    studentTxtLbl=Label(root, text="Students", bg="gray95") # Create a label which has text 'Students'
    studentTxtLbl.place(relx=0.52, rely=0.09, anchor=CENTER)
    takeRegisterButton=Button(root,text="Take Register",command=takeRegister) # Create Take Register Button
    takeRegisterButton.place(x=20,y=30)
    saveClassButton=Button(root,text="Save Class",command=saveFile) # Create Save Class Button
    saveClassButton.place(x=100,y=30)
    RenderGraphButton=Button(root,text="Render Graph",command=renderGraph) # Create Render Graph Button
    RenderGraphButton.place(x=56,y=56)
    rollNum=Label(root,text="Roll #",bg="gray95") # Create label for Roll #
    rollNum.place(x=22,y=90)
    name=Label(root,text="Name",bg="gray95") # Create label for names of students in a classroom
    name.place(x=152,y=90)
    attendaceLabel=Label(root,text="Attendance",bg="gray95") # Create label for attendance
    attendaceLabel.place(x=280,y=90)
    testResult=Label(root,text="Result",bg="gray95") # Create label for recent test result
    testResult.place(x=375,y=90)
    thisLesson=Label(root,text="Current Lesson",bg="gray95") # Create label for attendance of this lesson
    thisLesson.place(x=435,y=90)
    displayRegister(root,256) # Calls a function which displays a blank register for 256 students
    helpButton=Button(root,text="Help",command=showHelpMsg) # Create help Button
    helpButton.place(x=750,y=56) # Place the button at top right
    aboutButton=Button(root,text="About",command=showAboutMsg) # Create about Button
    aboutButton.place(x=746,y=86) # Place the button at top right
    licenseAggreementBox=Text(root,height=28,width=32) # Create a text box for the EULA
    licenseAggreementBox.place(relx=0.85, rely=0.6, anchor=CENTER)
    licenseAggreementBox.insert('1.0','''End User License Agreement:\n
1 - You must only use this
software with permission of
Preston Manor School.

2 - You must enter inputs with
honesty. This includes, but not
limited to, a student's grade
and attendance data.

3 - The password you use to
logon must be kept secret.

4 - Reverse engineering the
program without the permission
of Preston Manor School is
not allowed.

5 - Distribiting this program
without Preston Manor School's
consent is forbidden.

All copyright rights of this
software belong to:
Preston Manor School in the UK
and/or other countries.''')
    licenseAggreementBox.configure(state='disabled')

    # Bind entry boxes at the top to enter key 
    classTitleBox.bind('<Return>', enterFunctionalityForClassroomEntry)
    teacherNameBox.bind('<Return>', enterFunctionalityForTeacherEntry)
    studentNumBox.bind('<Return>', enterFunctionalityForStudentNumEntry)

    # Play initialisation sound effect
    winsound.PlaySound('Assets/Init.wav', winsound.SND_FILENAME)
    
    # Destroy splash screen
    splashRoot.withdraw()

    # Display main window
    root.update()
    
    # Set window icon
    root.iconbitmap('Assets/book-16.ico')
    
    # Begin the event listening loop for main window
    root.mainloop()

def Initialisation():
    global splashRoot
    global bLogonWindowOpened
    global bAuthenticationDone
        
    splashRoot=Tk()

    # Hide titlebar of splash
    splashRoot.overrideredirect(True)

    # Adjust splash size and location on the screen
    windowX=((splashRoot.winfo_screenwidth()/2))-(800/2)
    windowY=((splashRoot.winfo_screenheight()/2))-(600/2)
    splashRoot.geometry("%dx%d+%d+%d" % (800,600,windowX,windowY) )

    # Create/load splash GUI widgets such as logos, text and images etc
    splashBackgroundImage=PhotoImage(file="Assets/splashBackground.gif")
    splashBackground=Label(splashRoot, image=splashBackgroundImage)
    splashBackground.place(x=-2, y=-2)
    copyrightText=Label(splashRoot, text="© 2021 Preston Manor All-Through Co-Operative Trust School", fg="purple1", bg="black")
    copyrightText.place(relx=0.5, rely=0.92, anchor=CENTER)

    # Display splash
    splashRoot.update()

    # Wait for 1 second so user can see the splash screen
    time.sleep(1)

    # Ask user for name and password
    while True:
        if bLogonWindowOpened == False:
            bLogonWindowOpened=True
            authenticate()
            break
        elif bAuthenticationDone == True:
            break

    # Load the main program
    loadMainApp()

def createMenu(root):
    appMenu=Menu(root)

    # Create file menu
    fileMenu=Menu(appMenu, tearoff=0)
    fileMenu.add_command(label="Create a New "+constProjectName, command=createNewClassroom)
    fileMenu.add_command(label="Load an Existing "+constProjectName, command=loadFile)
    fileMenu.add_command(label="Save "+constProjectName, command=saveFile)
    fileMenu.add_separator()
    fileMenu.add_command(label="Quit", command=quitProgram)
    appMenu.add_cascade(label="File", menu=fileMenu)

    # Create help menu
    helpMenu=Menu(appMenu, tearoff=0)
    helpMenu.add_command(label=constAppTitle+" Help", command=showHelpMsg)
    helpMenu.add_separator()
    helpMenu.add_command(label="About "+constAppTitle, command=showAboutMsg)
    appMenu.add_cascade(label="Help", menu=helpMenu)

    # Display menu
    root.protocol("WM_DELETE_WINDOW", quitProgram)
    root.config(menu=appMenu)
    
def displayRegister(root, numStudents):
    global viewDataButtonGroup
    global currentLessonAttendanceBoxGroup
    for i in range (0,numStudents):
        rollNumBox=Entry(frame,width=5,justify='center')
        rollNumBox.grid(column=3,row=i+50,padx=25,pady=1)
        rollNumBox.insert(0,str(i+1))
        rollNumBox.configure(state='readonly')
        rollNumBoxGroup.append(rollNumBox)
        
        nameBox=Entry(frame,width=22,justify='center')
        nameBox.grid(column=4,row=i+50,padx=25,pady=1)
        nameBox.configure(state='readonly')
        studentNameBoxGroup.append(nameBox)
        
        attendanceBox=Entry(frame,width=5,justify='center')
        attendanceBox.grid(column=5,row=i+50,padx=25,pady=1)
        attendanceBox.configure(state='readonly')
        attendanceBoxGroup.append(attendanceBox)
        
        resultBox=Entry(frame,width=5,justify='center')
        resultBox.grid(column=6,row=i+50,padx=25,pady=1)
        resultBox.configure(state='disabled')
        recentResultBoxGroup.append(resultBox)
        
        thisLessonBox=Entry(frame,width=5,justify='center')
        thisLessonBox.grid(column=7,row=i+50,padx=25,pady=1)
        validateCurrentLessonAttendance=root.register(validateCurrentLessonInput)
        thisLessonBox.config(validate="key", validatecommand =(validateCurrentLessonAttendance, '%P', i))
        currentLessonAttendanceBoxGroup.append(thisLessonBox)
        
        viewDataButton=Button(frame,text="View/Edit Student Data",command=partial(showStudentData, i))
        viewDataButton.grid(column=8,row=i+50,padx=25,pady=1)
        viewDataButtonGroup.append(viewDataButton)

def updateClock():
     currentTime=strftime('%H:%M:%S')
     timeLabel.config(text=currentTime)
     timeLabel.after(1000, updateClock)

def updateRegister(studentNum):
    if int(studentNum) > cClassroom.numStudents:
        for i in range (cClassroom.numStudents,int(studentNum)):
            rollNumBox=Entry(frame,width=5,justify='center')
            rollNumBox.grid(column=3,row=i+50,padx=25,pady=1)
            rollNumBox.insert(0,str(i+1))
            rollNumBox.configure(state='readonly')
            rollNumBoxGroup.append(rollNumBox)
            
            nameBox=Entry(frame,width=22,justify='center')
            nameBox.grid(column=4,row=i+50,padx=25,pady=1)
            nameBox.configure(state='readonly')
            studentNameBoxGroup.append(nameBox)
        
            attendanceBox=Entry(frame,width=5,justify='center')
            attendanceBox.grid(column=5,row=i+50,padx=25,pady=1)
            attendanceBox.configure(state='readonly')
            attendanceBoxGroup.append(attendanceBox)
        
            resultBox=Entry(frame,width=5,justify='center')
            resultBox.grid(column=6,row=i+50,padx=25,pady=1)
            resultBox.configure(state='readonly')
            recentResultBoxGroup.append(resultBox)
        
            thisLessonBox=Entry(frame,width=5,justify='center')
            thisLessonBox.grid(column=7,row=i+50,padx=25,pady=1)
            validateCurrentLessonAttendance=root.register(validateCurrentLessonInput)
            thisLessonBox.config(validate="key", validatecommand =(validateCurrentLessonAttendance, '%P', i))
            currentLessonAttendanceBoxGroup.append(thisLessonBox)
        
            viewDataButton=Button(frame,text="View/Edit Student Data",command=partial(showStudentData, i))
            viewDataButton.grid(column=8,row=i+50,padx=25,pady=1)
            viewDataButtonGroup.append(viewDataButton)

    elif int(studentNum) == cClassroom.numStudents:
            return True # Do nothing if the value neither increases or decreases
        
    else:
            studentsToRemove=cClassroom.numStudents
            while int(studentNum) < studentsToRemove:
                rollNumBoxGroup[studentsToRemove].destroy()
                rollNumBoxGroup.pop(studentsToRemove)

                studentNameBoxGroup[studentsToRemove].destroy()
                studentNameBoxGroup.pop(studentsToRemove)

                attendanceBoxGroup[studentsToRemove].destroy()
                attendanceBoxGroup.pop(studentsToRemove)

                recentResultBoxGroup[studentsToRemove].destroy()
                recentResultBoxGroup.pop(studentsToRemove)
                
                currentLessonAttendanceBoxGroup[studentsToRemove].destroy()
                currentLessonAttendanceBoxGroup.pop(studentsToRemove)

                viewDataButtonGroup[studentsToRemove].destroy()
                viewDataButtonGroup.pop(studentsToRemove)

                studentsToRemove=studentsToRemove-1

                if (len(cClassroom.aStudents)) > (int(studentNum)+1):
                    cClassroom.aStudents.pop()

def loadFile():
    filePath = askopenfilename(initialdir = "Classrooms/",
        filetypes=[("Preston Manor Classroom Files", "*.pmc")]
    ) # Open a small window which lets the user select a PMC file to view from 'Classrooms' folder
    if not filePath:
        return False # If the user decides to not load a file, dont do anything just return False
    with open(filePath, "r") as fileToRead: # Open the file as 'fileToRead'
        if readFileHeader(fileToRead) == True: # If the header is successfully loaded then read student data
            if readStudentData(fileToRead)== True: # If all student data is valid then return True; file was successfully loaded
                return True
            else:
                return False # Return False if file fails to load due to invalid data
        else:
            return False # Return False if file fails to load due to invalid data

def readFileHeader(readFile):
    for i in range(0,3): # Read first three lines of file that contain metadata through for loop iteration
        currentLine=readFile.readline() # Set the current line as the line which the program is reading from the file
        if i == 0: # If first line is being read then
            if validateFileClassroomTitle(currentLine)== False: # Read the first line as classroom title and validate it
                return False # Stop loading the file if invalid data is in the file
        elif i == 1: # If second line is being read then
            if validateFileTeacherName(currentLine)== False: # Read the second line as teacher name and validate it
                return False # Stop loading the file if invalid data is in the file
        else: # If third line is being read then
            if validateFileStudentNum(currentLine) == False: # Read the third  line as number of students in class and validate it
                return False # Stop loading the file if invalid data is in the file
    return True # If all metadata is successfully valdiated and loaded then continue to load data of students in classroom

def readStudentData(readFile):
    cClassroom.aStudents.clear() # Delete all students in the current classroom before opening the file
    cClassroom.aStudents=[256] # Set the maximum number of students a class can have as 256
    for i in range(0,cClassroom.numStudents): # Repeat this code equal to the total number of students in class
        for j in range(0,8): # Repeat the code below 8 times
            currentLine=readFile.readline() # Read a line from the file which usr wants to open
            if j == 0:
                currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation
                if validateName(currentLine): # Read and validate the line as student name
                    currentStudent=Student() # Create a student object
                    cClassroom.aStudents.append(currentStudent) # Add the last created student to the classroom
                    cClassroom.aStudents[i+1].name=currentLine # Set the student name as thhe current line
                    studentNameBoxGroup[i+1].configure(state="normal") # Make text box which dispalys student name editable
                    studentNameBoxGroup[i+1].delete(0, 'end') # Delete all data currently stored in that textbox
                    studentNameBoxGroup[i+1].insert(0,currentLine) # Insert the student name read from file into the textbox
                    studentNameBoxGroup[i+1].configure(state="readonly") # Make the textbox read only
                else: # If the input is invalid
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has one invalid student name.") # Show error message
                    return False # Stop loading the file if it contains invalid contents
            elif j == 1:
                currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation
                if validateStudentResult(currentLine):
                    cClassroom.aStudents[i+1].result=currentLine # Read and validate the line as student result
                    recentResultBoxGroup[i+1].configure(state="normal") # Make text box which dispalys student result editable
                    recentResultBoxGroup[i+1].delete(0, 'end') # Delete all data currently stored in that textbox
                    recentResultBoxGroup[i+1].insert(0,currentLine) # Insert the data read from file into the textbox
                    recentResultBoxGroup[i+1].configure(state="readonly") # Make the textbox read only
                else: # If the input is invalid
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has one invalid student result.") # Show error message
                    return False # Stop loading the file if it contains invalid contents
            elif j == 2:
                currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation
                if validateStudentAddress(currentLine):
                    cClassroom.aStudents[i+1].address=currentLine # Read and validate the line as student address
                else: # If the input is invalid
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has one invalid student address.") # Show error message
                    return False # Stop loading the file if it contains invalid contents
            elif j == 3:
                currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation
                if validateEmail(currentLine):
                    cClassroom.aStudents[i+1].email=currentLine  # Read and validate the line as student email
                else: # If the input is invalid
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has one invalid email.") # Show error message
                    return False # Stop loading the file if it contains invalid contents
            elif j == 4:
                currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation
                if validateName(currentLine):
                    cClassroom.aStudents[i+1].guardianName=currentLine # Read and validate the line as student guardian name
                else:
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has one invalid name of guardian.") # Show error message
                    return False # Stop loading the file if it contains invalid contents
            elif j == 5:
                currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation
                if validatePhoneNum(currentLine):
                    cClassroom.aStudents[i+1].guardianPhoneNum=currentLine # Read and validate the line as student guardian phone number
                else:
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has one invalid phone number of guardian.") # Show error message
                    return False # Stop loading the file if it contains invalid contents
            elif j == 6:
                currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation
                if validateLessonsSupposedtoBeAttended(currentLine):
                    cClassroom.aStudents[i+1].lessonsSupposedtoBeAttended=int(currentLine) # Read and validate the line as student's lessons supposed to be attended
                else:
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has invalid number of total student lessons. Please contact school's IT team.") # Show error message
                    return False # Stop loading the file if it contains invalid contents
            elif j == 7:
                if i < cClassroom.numStudents-1:
                    currentLine=currentLine[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space must be removed for proper validation however this doesnt happen if last line of file is read
                if validateLessonsAttended(cClassroom.aStudents[i+1].lessonsSupposedtoBeAttended, currentLine):
                    cClassroom.aStudents[i+1].lessonsAttended=int(currentLine) # Read and validate the line as lessons which a student attended
                    cClassroom.aStudents[i+1].attendance=int(100*(cClassroom.aStudents[i+1].lessonsAttended)/(cClassroom.aStudents[i+1].lessonsSupposedtoBeAttended)) # Set attendance percentage
                    attendanceBoxGroup[i+1].configure(state="normal") # To put content in the attendance text box, first it should be made editable 'normal'
                    attendanceBoxGroup[i+1].delete(0, 'end') # Delete previous content in that text box to add new one
                    attendanceBoxGroup[i+1].insert(0,str(cClassroom.aStudents[i+1].attendance)+'%') # Add the attendance calculated above to that in format '99%'
                    attendanceBoxGroup[i+1].configure(state="readonly") # Make the attendance text box read only
                    highlightOnRegister(i+1)
                else:
                    messagebox.showerror(title=None, message="Please open a valid PMC file. The recently opened file has invalid number of student lessons attended. Please contact school's IT team.") # Show error message
                    return False # Stop loading the file if it contains invalid contents

    return True
        
def renderGraph():
    # Try to import matplotlib
    try:
        import matplotlib.pyplot as plt # Import the module
    except: # If the module cant be imported then
        messagebox.showerror(title=None, message=("matplotlib is not installed on this computer thus this program will not be able to render graphs.")) # Show error message
        RenderGraphButton.config(state="disabled") # Disable Render Graph button as the feature wont work without matplotlib
        return False
    if len(cClassroom.aStudents) < 2:
        messagebox.showerror(title=None, message=("There are no results available for the students in this class. Please input the results of students then use this feature.")) # show error
        return False # Dont continue if results of students are not available
    xList = ['A*', 'A', 'B', 'C', 'D', 'E', 'U'] # The labels that appear on the x-side of graph
    yStudentsGettingA_Star=0 # Variable for number of students getting A*
    yStudentsGettingA=0 # Variable for number of students getting A
    yStudentsGettingB=0 # Variable for number of students getting B
    yStudentsGettingC=0 # Variable for number of students getting C
    yStudentsGettingD=0 # Variable for number of students getting D
    yStudentsGettingE=0 # Variable for number of students getting E
    yStudentsGettingU=0 # Variable for number of students getting U
    yStudentsGettingGrades = [0,0,0,0,0,0,0] # List that stores the values on y axis of graph
    for i in range(0,len(cClassroom.aStudents)-1): # Repeat the code below for each student
        if cClassroom.aStudents[i+1].result == 'A*': # If a student's grade is A* then
            yStudentsGettingA_Star=yStudentsGettingA_Star+1 # Increment the number of students getting A*
        elif cClassroom.aStudents[i+1].result == 'A':
            yStudentsGettingA=yStudentsGettingA+1
        elif cClassroom.aStudents[i+1].result == 'B':
            yStudentsGettingB=yStudentsGettingB+1
        elif cClassroom.aStudents[i+1].result == 'C':
            yStudentsGettingC=yStudentsGettingC+1
        elif cClassroom.aStudents[i+1].result == 'D':
            yStudentsGettingD=yStudentsGettingD+1
        elif cClassroom.aStudents[i+1].result == 'E':
            yStudentsGettingE=yStudentsGettingE+1
        elif cClassroom.aStudents[i+1].result == 'U':
            yStudentsGettingU=yStudentsGettingU+1
    yStudentsGettingGrades = [yStudentsGettingA_Star,yStudentsGettingA,yStudentsGettingB,yStudentsGettingC,yStudentsGettingD,yStudentsGettingE,yStudentsGettingU] # Update the list
    plt.close() # Close previously created graph windows if they are open
    plt.figure(num='Preston Manor Classroom Graph') # Assign the title of window
    plt.title("Pupil Progress Graph") # Title of the graph
    plt.xlabel('Grade') # Assign the title of the x axis
    plt.ylabel("Number of Students Getting Grade") # Assign the title of the y axis
    plt.bar(xList, yStudentsGettingGrades, color=['purple','green','green','yellow','red','red','red'], edgecolor='black') # Create bar graph
    legendContent={'A*':'purple', 'A - B':'green', 'C':'yellow','D - U':'red'} # Define content which is shown in legend
    labels = list(legendContent.keys()) # Define labels in the legend
    handles = [plt.Rectangle((0,0),1,1, color=legendContent[label]) for label in labels] # Create handles to hold the legend
    plt.legend(handles,labels) # Show legend for the graph
    plt.show() # Display bar graph in a small window
    
def showStudentData(studentNumber):
    studentDataWindowRoot=Tk()

    # Set window title
    studentDataWindowRoot.title("Object Editor")

    # Adjust window size and location on the screen
    windowX=((studentDataWindowRoot.winfo_screenwidth()/2))-(314/2)
    windowY=((studentDataWindowRoot.winfo_screenheight()/2))-(270/2)
    studentDataWindowRoot.geometry("%dx%d+%d+%d" % (314,270,windowX,windowY) )
    studentDataWindowRoot.resizable(False, False)

    # Set values that are displayed
    try:
        studentName=cClassroom.aStudents[studentNumber+1].name # Set variable for student name
        attendance=cClassroom.aStudents[studentNumber+1].attendance # Set variable for attendance
        recentResult=cClassroom.aStudents[studentNumber+1].result # Set variable for result
        address=cClassroom.aStudents[studentNumber+1].address # Set variable for address
        email=cClassroom.aStudents[studentNumber+1].email # Set variable for email
        guardianName=cClassroom.aStudents[studentNumber+1].guardianName # Set variable for Guardian Name
        guardianPhoneNum=cClassroom.aStudents[studentNumber+1].guardianPhoneNum # Set variable for guardian phone num
        totalLessons=cClassroom.aStudents[studentNumber+1].lessonsSupposedtoBeAttended # Set variable for attendance (total lessons)
        lessonsAttended=cClassroom.aStudents[studentNumber+1].lessonsAttended # Set variable for attendance (total lessons attended)
    except:
        print("DEBUG MESSAGE: Student is not successfully loaded") # Show warning message to developers when the program is being debugged

    # Set window icon
    studentDataWindowRoot.iconbitmap('Assets/student.ico')

    # Show student name
    studentNameLabel=Label(studentDataWindowRoot, text="Student Name", bg="gray95") # Declare label
    studentNameLabel.place(x=1,y=5) # Place label in window
    studentNameEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student name
    studentNameEntry.place(x=210,y=14, anchor=CENTER) # Place text box in window
    try:
        studentNameEntry.insert(0,studentName) # Insert data in the text box
    except:
        studentNameEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Show student attendance
    studentAttenanceLabel=Label(studentDataWindowRoot, text="Attendance", bg="gray95") # Declare label
    studentAttenanceLabel.place(x=1,y=30) # Place label in window
    studentAttendanceEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the attendance
    studentAttendanceEntry.place(x=210,y=39, anchor=CENTER) # Place text box in window
    try:
        studentAttendanceEntry.insert(0,str(attendance)+'%') # Insert data in the text box
        studentAttendanceEntry.config(state='readonly') # Make entry read only
    except:
        studentAttendanceEntry.insert(0,"") # Insert empty string in the text box if no data is available
        studentAttendanceEntry.config(state='readonly') # Make entry read only

    # Show student result
    studentResultLabel=Label(studentDataWindowRoot, text="Recent Result", bg="gray95") # Declare label
    studentResultLabel.place(x=1,y=55) # Place label in window
    studentResultEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student attribute
    studentResultEntry.place(x=210,y=64, anchor=CENTER) # Place text box in window
    try:
        studentResultEntry.insert(0,recentResult) # Insert data in the text box
    except:
        studentResultEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Show student address
    studentAddressLabel=Label(studentDataWindowRoot, text="Address", bg="gray95") # Declare label
    studentAddressLabel.place(x=1,y=80) # Place label in window
    studentAddressEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student attribute
    studentAddressEntry.place(x=210,y=89, anchor=CENTER) # Place text box in window
    try:
        studentAddressEntry.insert(0,address) # Insert data in the text box
    except:
        studentAddressEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Show student email
    studentEmailLabel=Label(studentDataWindowRoot, text="Email", bg="gray95") # Declare label
    studentEmailLabel.place(x=1,y=105) # Place label in window
    studentEmailEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student attribute
    studentEmailEntry.place(x=210,y=114, anchor=CENTER) # Place text box in window
    try:
        studentEmailEntry.insert(0,email) # Insert data in the text box
    except:
        studentEmailEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Show student Guardian's name
    guardianNameLabel=Label(studentDataWindowRoot, text="Guardian's Name", bg="gray95") # Declare label
    guardianNameLabel.place(x=1,y=130) # Place label in window
    guardianNameEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student attribute
    guardianNameEntry.place(x=210,y=139, anchor=CENTER) # Place text box in window
    try:
        guardianNameEntry.insert(0,guardianName) # Insert data in the text box
    except:
        guardianNameEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Show student Guardian's Phone Nymber
    guardianPhoneNumLabel=Label(studentDataWindowRoot, text="Guardian's Phone #", bg="gray95") # Declare label
    guardianPhoneNumLabel.place(x=1,y=155) # Place label in window
    guardianPhoneNumEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student attribute
    guardianPhoneNumEntry.place(x=210,y=164, anchor=CENTER) # Place text box in window
    try:
        guardianPhoneNumEntry.insert(0,guardianPhoneNum) # Insert data in the text box
    except:
        guardianPhoneNumEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Show student total lessons
    studentTotalLessonsLabel=Label(studentDataWindowRoot, text="Total Lessons", bg="gray95") # Declare label
    studentTotalLessonsLabel.place(x=1,y=180) # Place label in window
    studentTotalLessonsEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student attribute
    studentTotalLessonsEntry.place(x=210,y=189, anchor=CENTER) # Place text box in window
    try:
        studentTotalLessonsEntry.insert(0,totalLessons) # Insert data in the text box
    except:
        studentTotalLessonsEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Show student lessons attended
    studentLessonsAttendedLabel=Label(studentDataWindowRoot, text="Lessons Attended", bg="gray95") # Declare label
    studentLessonsAttendedLabel.place(x=1,y=205) # Place label in window
    studentLessonsAttendedEntry=Entry(studentDataWindowRoot,width=32,justify='left') # Create a text box for the student attribute
    studentLessonsAttendedEntry.place(x=210,y=214, anchor=CENTER) # Place text box in window
    try:
        studentLessonsAttendedEntry.insert(0,lessonsAttended) # Insert data in the text box
    except:
        studentLessonsAttendedEntry.insert(0,"") # Insert empty string in the text box if no data is available

    # Create Save Changes button
    saveChangesButton=Button(studentDataWindowRoot,text="Save Changes",bg='MediumPurple1',activebackground='MediumPurple2',command=partial(objectEditor_SaveChanges, studentNumber+1
                                                                                       ,studentNameEntry,studentResultEntry,
                                                                                       studentAddressEntry,studentEmailEntry
                                                                                       ,guardianNameEntry,guardianPhoneNumEntry,
                                                                                       studentTotalLessonsEntry, studentLessonsAttendedEntry,
                                                                                       studentAttendanceEntry)) # Define button
    saveChangesButton.config( height = 1, width = 15 ) # Change button size
    saveChangesButton.place(x=95, y=230)
    studentDataWindowRoot.bind('<Return>', lambda event, argument =(studentNumber+1) :objectEditor_SaveChanges(argument,studentNameEntry,studentResultEntry,
                                                                                                               studentAddressEntry,studentEmailEntry,
                                                                                                               guardianNameEntry,guardianPhoneNumEntry,
                                                                                                               studentTotalLessonsEntry,studentLessonsAttendedEntry,
                                                                                                               studentAttendanceEntry)) # bind save changes button to enter key

    # Display window
    studentDataWindowRoot.mainloop()

def objectEditor_SaveChanges(studentNum, studentNameEntry, studentResultEntry, studentAddressEntry, studentEmailEntry,
                             guardianNameEntry, guardianPhoneNumEntry,
                             studentTotalLessonsEntry,studentLessonsAttendedEntry,
                             studentAttendanceEntry):
    while studentNum >= len(cClassroom.aStudents):
        currentStudent=Student() # Create a student object
        cClassroom.aStudents.append(currentStudent) # Add the last created student to the classroom
        
    studentToEdit=cClassroom.aStudents[studentNum] # Student that needs to be edited
    studentNameToValidate=studentNameEntry.get() # Student attribute needs to be validated
    studentResultToValidate=studentResultEntry.get() # Student attribute needs to be validated
    studentAddressToValidate=studentAddressEntry.get() # Student attribute needs to be validated
    studentEmailToValidate=studentEmailEntry.get() # Student attribute needs to be validated
    guardianNameToValidate=guardianNameEntry.get() # Student attribute needs to be validated
    guardianPhoneNumToValidate=guardianPhoneNumEntry.get() # Student attribute needs to be validated
    studentTotalLessonsToValidate=studentTotalLessonsEntry.get() # Student attribute needs to be validated
    studentLessonsAttendedToValidate=studentLessonsAttendedEntry.get() # Student attribute needs to be validated

    # Edit object name
    if validateName(studentNameToValidate) == False: # Validate student name
        messagebox.showerror(title=None, message="Please input a valid student name. A name must start with uppercase and must be atleast two characters long") # Show error
        studentNameEntry.delete(0, 'end') # Delete invalid input in entry
        studentNameEntry.insert(0,studentToEdit.name) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.name=studentNameToValidate # Edit the attribute of student if user enters valid input
        studentNameBoxGroup[studentNum].config(state='normal')
        studentNameBoxGroup[studentNum].delete(0,'end') # Delete the value in entry in register
        studentNameBoxGroup[studentNum].insert(0,studentToEdit.name) # Reset the value in entry in register
        studentNameBoxGroup[studentNum].config(state='readonly')

    # Edit object result
    if validateStudentResult(studentResultToValidate) == False: # Validate student result
        messagebox.showerror(title=None, message="Please input a valid student grade. A grade must be uppercase and between A* to U") # Show error
        studentResultEntry.delete(0, 'end') # Delete invalid input in entry
        studentResultEntry.insert(0,studentToEdit.result) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.result=studentResultToValidate # Edit the attribute of student if user enters valid input
        recentResultBoxGroup[studentNum].config(state='normal')
        recentResultBoxGroup[studentNum].delete(0,'end') # Delete the value in entry in register
        recentResultBoxGroup[studentNum].insert(0,studentToEdit.result) # Reset the value in entry in register
        recentResultBoxGroup[studentNum].config(state='readonly')
        highlightOnRegister(studentNum) # Highlight student in register based on the result

    # Edit object address
    if validateStudentAddress(studentAddressToValidate) == False: # Validate student address
        messagebox.showerror(title=None, message="Please input a valid address. At minimum a address must contain 6 characters.") # Show error
        studentAddressEntry.delete(0, 'end') # Delete invalid input in entry
        studentAddressEntry.insert(0,studentToEdit.address) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.address=studentAddressToValidate # Edit the attribute of student if user enters valid input

    # Edit object email
    if validateEmail(studentEmailToValidate) == False: # Validate student email
        messagebox.showerror(title=None, message="Please input a valid email address for student.") # Show error
        studentEmailEntry.delete(0, 'end') # Delete invalid input in entry
        studentEmailEntry.insert(0,studentToEdit.email) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.email=studentEmailToValidate # Edit the attribute of student if user enters valid input

    # Edit object guardian name
    if validateName(guardianNameToValidate) == False: # Validate student's guardian name
        messagebox.showerror(title=None, message="Please input a valid guardian name. A name must start with uppercase and must be atleast two characters long") # Show error
        guardianNameEntry.delete(0, 'end') # Delete invalid input in entry
        guardianNameEntry.insert(0,studentToEdit.guardianName) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.guardianName=guardianNameToValidate # Edit the attribute of student if user enters valid input

    # Edit object guardian phone number
    if validatePhoneNum(guardianPhoneNumToValidate) == False: # Validate student's guardian phone num
        messagebox.showerror(title=None, message="Please input a valid guardian phone number. A valid value is 11 characters long and numeric.") # Show error
        guardianPhoneNumEntry.delete(0, 'end') # Delete invalid input in entry
        guardianPhoneNumEntry.insert(0,studentToEdit.guardianPhoneNum) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.guardianPhoneNum=guardianPhoneNumToValidate # Edit the attribute of student if user enters valid input

    if  studentLessonsAttendedToValidate.isnumeric() == False: # Make sure lessons attended value is a number to avoid errors:
        messagebox.showerror(title=None, message="Please input a valid number of students'lessons attended. This must be a numeric value less than or equal to total lessons") # Show error
        studentLessonsAttendedEntry.delete(0, 'end') # Delete invalid input in entry
        studentLessonsAttendedEntry.insert(0,studentToEdit.lessonsAttended) # Reset the value in entry
        return False # Dont continue if validation fails

    # Edit object lessons total
    if validateLessonsSupposedtoBeAttended(studentTotalLessonsToValidate) == False or int(studentTotalLessonsToValidate) < int(studentLessonsAttendedToValidate): # Validate student's lessons
        messagebox.showerror(title=None, message="Please input a valid number of students' total lessons. Total lessons must be a numeric value >= lessons attended.") # Show error
        studentTotalLessonsEntry.delete(0, 'end') # Delete invalid input in entry
        studentTotalLessonsEntry.insert(0,studentToEdit.lessonsSupposedtoBeAttended) # Reset the value in entry
        studentLessonsAttendedEntry.delete(0, 'end') # Delete invalid input in entry
        studentLessonsAttendedEntry.insert(0,studentToEdit.lessonsAttended) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.lessonsSupposedtoBeAttended=int(studentTotalLessonsToValidate) # Edit the attribute of student if user enters valid input

    # Edit object lessons attended
    if  validateLessonsAttended(int(studentTotalLessonsToValidate),studentLessonsAttendedToValidate) == False: # Validate student's lessons
        messagebox.showerror(title=None, message="Please input a valid number of students'lessons attended. This must be a numeric value less than or equal to total lessons") # Show error
        studentLessonsAttendedEntry.delete(0, 'end') # Delete invalid input in entry
        studentLessonsAttendedEntry.insert(0,studentToEdit.lessonsAttended) # Reset the value in entry
        return False # Dont continue if validation fails
    else:
        studentToEdit.lessonsAttended=int(studentLessonsAttendedToValidate) # Edit the attribute of student if user enters valid input
        attendancePercentage=int(100*(studentToEdit.lessonsAttended)/(studentToEdit.lessonsSupposedtoBeAttended)) # Calculate attendance percentage
        studentToEdit.attendance=attendancePercentage # Update students' attendance
        studentAttendanceEntry.config(state='normal') # Make entry editable
        studentAttendanceEntry.delete(0, 'end') # Delete outdated data in entry
        studentAttendanceEntry.insert(0,str(attendancePercentage)+'%') # Insert updated data in the text box
        studentAttendanceEntry.config(state='readonly') # Make entry read only
        attendanceBoxGroup[studentNum].config(state='normal') # Make entry editable
        attendanceBoxGroup[studentNum].delete(0, 'end') # Delete outdated data in entry
        attendanceBoxGroup[studentNum].insert(0,str(attendancePercentage)+'%') # Insert updated data in the text box
        attendanceBoxGroup[studentNum].config(state='readonly') # Make entry read only

def quitProgram():
    sys.exit()

def takeRegister():
    currentLessonAttendanceBoxGroup[1].focus()

def enterFunctionalityForClassroomEntry(inp):
    teacherNameBox.focus()

def enterFunctionalityForTeacherEntry(inp):
    studentNumBox.focus()

def enterFunctionalityForStudentNumEntry(inp):
    takeRegister()

# Function which sets the commands for confirung the scrollregion in canvas
def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox('all')) # Update scrollregion when canvas is configured

# Enable mousewheel movement for scrollbar
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/75)), "units") # Whenever mousewheel is moved up or down, the scrollbar moves in that direction

def highlightOnRegister(studentNum):
    if cClassroom.aStudents[studentNum].result == 'A*' or cClassroom.aStudents[studentNum].result == 'A':
        studentNameBoxGroup[studentNum].configure(fg='forest green') # Highlgiht bright pupils' names with green color
        return True
    elif cClassroom.aStudents[studentNum].result == 'B' or cClassroom.aStudents[studentNum].result == 'C':
        studentNameBoxGroup[studentNum].configure(fg='black') # Highlight middle performing sudents' names with black/default colour
        return True
    else:
        studentNameBoxGroup[studentNum].configure(fg='red') # Highlight poor performing sudents' names with red colour
        return True

def createNewClassroom():
    updateRegister(0) # Delete all previous students
    cClassroom.numStudents=0 # Set number of students in class to 0
    
    updateRegister(5) # Add 5 students to class
    cClassroom.numStudents=5 # Set number of students in class to 5
    
    classTitleBox.delete(0,'end') # Delete outsated data in classroom title text box
    classTitleBox.insert(0,'Untitled Classroom') # Add new data to classroom text box
    
    teacherNameBox.delete(0,'end') # Delete outsated data in text box
    teacherNameBox.insert(0,'Just Another Preston Manor Teacher') # Add new data to text box
    
    studentNumBox.delete(0,'end') # Delete outsated data in text box
    studentNumBox.insert(0,'5') # Add new data to text box

def saveFile():
    filePath = asksaveasfilename(
        defaultextension="pmc",
        filetypes=[("Preston Manor Classroom Files", "*.pmc")],
        initialdir="Classrooms/") # Open a small window which lets the user select a PMC file to save in 'Classrooms' folder
    if not filePath:
        return False # If the user decides to not save a file, dont do anything just return False
    with open(filePath, "w") as fileToSave: # Write the file as 'fileToSave'
        if writeFileHeader(fileToSave) == True: # If the header is successfully saved then write student data
            if writeStudentData(fileToSave)== True: # If all student data is valid then return True; file was successfully save
                return True
            else:
                return False # Return False if file fails to save due to errors
        else:
            return False # Return False if file fails to save due to errors

def writeFileHeader(saveFile):
    for i in range(0,3): # Write first three lines of file that contain metadata through for loop iteration
        if i == 0: # If first line is being written then
            saveFile.write(cClassroom.title+'\n') # Save class title
        elif i == 1: #If second line is being written then
            saveFile.write(cClassroom.teacher+'\n') # Save class teacher name
        else: #If third line is being written then
            saveFile.write(str(cClassroom.numStudents)+'\n') # Save class number of students
    return True

def writeStudentData(saveFile):
    for i in range(0,cClassroom.numStudents): # Repeat this code equal to the total number of students in class
        for j in range(0,8): # Repeat the code below 8 times
            if j == 0:
                saveFile.write(cClassroom.aStudents[i+1].name+'\n') # Save student name
            elif j == 1:
                saveFile.write(cClassroom.aStudents[i+1].result+'\n') # Save student result
            elif j == 2:
                saveFile.write(cClassroom.aStudents[i+1].address+'\n') # Save student address
            elif j == 3:
                saveFile.write(cClassroom.aStudents[i+1].email+'\n') # Save student email
            elif j == 4:
                saveFile.write(cClassroom.aStudents[i+1].guardianName+'\n') # Save student guardian name
            elif j == 5:
                saveFile.write(cClassroom.aStudents[i+1].guardianPhoneNum+'\n') # Save student guardian phonr number
            elif j == 6:
                saveFile.write(str(cClassroom.aStudents[i+1].lessonsSupposedtoBeAttended+1)+'\n') # Save student total lessons
            elif j == 7:
                if i < cClassroom.numStudents-1: # If last student in not being saved then add a new line to file
                    if currentLessonAttendanceBoxGroup[i+1].get() == '/' or currentLessonAttendanceBoxGroup[i+1].get() == 'L':
                        saveFile.write(str(cClassroom.aStudents[i+1].lessonsAttended+1)+'\n') # Save student lessons attended
                    else:
                        saveFile.write(str(cClassroom.aStudents[i+1].lessonsAttended)+'\n') # Save student lessons attended
                else: # If last student in being saved then make sure empty line is not added to the file
                    if currentLessonAttendanceBoxGroup[i+1].get() == '/' or currentLessonAttendanceBoxGroup[i+1].get() == 'L':
                        saveFile.write(str(cClassroom.aStudents[i+1].lessonsAttended+1)) # Save student lessons attended
                    else:
                        saveFile.write(str(cClassroom.aStudents[i+1].lessonsAttended)) # Save student lessons attended
    return True

def authenticate():
    authenticateRoot=Tk()

    # Set window title
    authenticateRoot.title("Authentication")

    # Adjust window size and location on the screen
    windowX=((authenticateRoot.winfo_screenwidth()/2))-(270/2)
    windowY=((authenticateRoot.winfo_screenheight()/2))-(90/2)
    authenticateRoot.geometry("%dx%d+%d+%d" % (270,90,windowX,windowY) )
    authenticateRoot.resizable(False, False)

    # Show username label and textbox
    userNameLabel=Label(authenticateRoot, text="Username:", bg="gray95") # Declare label
    userNameLabel.place(x=1,y=5) # Place label in window
    userNameEntry=Entry(authenticateRoot,width=32,justify='left') # Create a text box for the student name
    userNameEntry.place(x=170,y=14, anchor=CENTER) # Place text box in window

    # Show password label and textbox
    passwordLabel=Label(authenticateRoot, text="Password:", bg="gray95") # Declare label
    passwordLabel.place(x=1,y=30) # Place label in window
    passwordEntry=Entry(authenticateRoot,width=32,justify='left',show="*") # Create a text box for the student name
    passwordEntry.place(x=170,y=39, anchor=CENTER) # Place text box in window

    # Create Logon button
    logonButton=Button(authenticateRoot,text="Logon",bg='MediumPurple1',activebackground='MediumPurple2',command=partial(validateUsernameAndPassword, userNameEntry
                                                                                       ,passwordEntry,authenticateRoot)) # Define button
    logonButton.config( height = 1, width = 15 ) # Change button size
    logonButton.place(x=80, y=56)

    while bAuthenticationDone==False:
        # Update window
        try:
            authenticateRoot.update()
        except:
            break

    if bAuthenticationDone==False:
        sys.exit()
        return False

    return True
    
# +----------------------------------------------------------------------------------------+
# Define different types of validation functions
# +----------------------------------------------------------------------------------------+

def validateClassName(inp):
    if len(inp) > 1:
        cClassroom.title=inp
        return True # Accept input if it contains more than one characters
    else:
        messagebox.showerror(title=None, message="Please enter a valid value in the field.\nThe name of a class must contain more than 1 characters.") # Tell user why input is rejected
        classTitleBox.delete(0, 'end') # Delete invalid input
        classTitleBox.insert(0,cClassroom.title) # Reset the value in text box
        return False # Do not accept invalid input
    
def validateTeacherName(inp):
    if len(inp) > 1 and inp[0].isupper():
        cClassroom.teacher=inp
        return True # Accept input of name if it starts with an uppercase letter and the length is greater than one.
    else:
        messagebox.showerror(title=None, message="Please enter a valid value in the field.\nA name must begin with uppercase and it must be at least 2 characters long.")#show error msg
        teacherNameBox.delete(0, 'end') # Delete invalid input
        teacherNameBox.insert(0,cClassroom.teacher)# Reset the value in text box
        return False # Do not accept invalid input
    
def validateStudentNum(inp):
    if inp.isnumeric(): # If the input is a numeric value then perform  calculations on it
        if int(inp) > 0 and int(inp) <= 256: # Make sure the numerical input is not greater than the maximum value of students in class: '256' and not less than 1
            updateRegister(inp) # Update the register if the input if valid
            cClassroom.numStudents=int(inp)
            return True # Accept valid input
        else:
             messagebox.showerror(title=None, message="Please enter a valid value in the field.\nThe number of students in class must be an integer between 1 and 256.") #show error msg
             studentNumBox.delete(0, 'end') # Delete invalid input
             studentNumBox.insert(0,str(cClassroom.numStudents)) # Reset the value in text box
             return False # Do not accept invalid input
    else:
        messagebox.showerror(title=None, message="Please enter a valid value in the field.\nThe number of students in class must be an integer between 1 and 256.") #show error msg
        studentNumBox.delete(0, 'end') # Delete invalid input
        studentNumBox.insert(0,str(cClassroom.numStudents)) # Reset the value in text box
        return False # Do not accept invalid input

def validateCurrentLessonInput(inp,studentNum):
    currentBox=int(studentNum)+1
    nextBox=int(studentNum)+2
    if inp != '':
        if inp == '/' or inp == 'L' or inp == 'N':
            if nextBox < len(currentLessonAttendanceBoxGroup):
                currentLessonAttendanceBoxGroup[nextBox].focus()
            return True
        elif len(inp) > 1:
            if inp[1]=='l' or inp[1]=='L':
                currentLessonAttendanceBoxGroup[currentBox].delete(0, 'end')
                currentLessonAttendanceBoxGroup[currentBox].insert(0,'L')
                validateCurrentLessonAttendance=root.register(validateCurrentLessonInput)
                currentLessonAttendanceBoxGroup[currentBox].config(validate="key", validatecommand =(validateCurrentLessonAttendance, '%P', currentBox-1))
                if nextBox < len(currentLessonAttendanceBoxGroup):
                        currentLessonAttendanceBoxGroup[nextBox].focus()
                return False
            elif inp[1]=='n' or inp[1]=='N':
                currentLessonAttendanceBoxGroup[currentBox].delete(0, 'end')
                currentLessonAttendanceBoxGroup[currentBox].insert(0,'N')
                validateCurrentLessonAttendance=root.register(validateCurrentLessonInput)
                currentLessonAttendanceBoxGroup[currentBox].config(validate="key", validatecommand =(validateCurrentLessonAttendance, '%P', currentBox-1))
                if nextBox < len(currentLessonAttendanceBoxGroup):
                        currentLessonAttendanceBoxGroup[nextBox].focus()
                return False
            elif inp[1]=='/':
                currentLessonAttendanceBoxGroup[currentBox].delete(0, 'end')
                currentLessonAttendanceBoxGroup[currentBox].insert(0,'/')
                validateCurrentLessonAttendance=root.register(validateCurrentLessonInput)
                currentLessonAttendanceBoxGroup[currentBox].config(validate="key", validatecommand =(validateCurrentLessonAttendance, '%P', currentBox-1))
                if nextBox < len(currentLessonAttendanceBoxGroup):
                        currentLessonAttendanceBoxGroup[nextBox].focus()
                return False
            if nextBox < len(currentLessonAttendanceBoxGroup):
                currentLessonAttendanceBoxGroup[nextBox].focus()
            return False
        elif inp=='l':
            currentLessonAttendanceBoxGroup[currentBox].insert(0,'L')
            validateCurrentLessonAttendance=root.register(validateCurrentLessonInput)
            currentLessonAttendanceBoxGroup[currentBox].config(validate="key", validatecommand =(validateCurrentLessonAttendance, '%P', currentBox-1))
            if nextBox < len(currentLessonAttendanceBoxGroup):
                currentLessonAttendanceBoxGroup[nextBox].focus()
            return False
        elif inp=='n':
            currentLessonAttendanceBoxGroup[currentBox].insert(0,'N')
            validateCurrentLessonAttendance=root.register(validateCurrentLessonInput)
            currentLessonAttendanceBoxGroup[currentBox].config(validate="key", validatecommand =(validateCurrentLessonAttendance, '%P', currentBox-1))
            if nextBox < len(currentLessonAttendanceBoxGroup):
                currentLessonAttendanceBoxGroup[nextBox].focus()
            return False
        else:
            showCurrentLessonAttendanceInputError()
            return False
    else:
        return True

def validateFileClassroomTitle(readline):
    readline=readline[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space is not needed and must be removed for optimisation of RAM use
    if len(readline) > 1: # Accept any input with a length greater than 1
        cClassroom.title=readline # Update the title of current classroom
        classTitleBox.delete(0, 'end') # Delete previous value in classroom textbox
        classTitleBox.insert(0,cClassroom.title) # Put the value loaded from PMC file into the text box
        return True # Accept input if it contains more than one characters
    else:
        messagebox.showerror(title=None, message=("Class name must contain more than 1 characters. The file you loaded contain invalid class name.")) # Tell user why input is rejected
        return False # Do not accept invalid input

def validateFileTeacherName(readline):
    readline=readline[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space is not needed and must be removed for optimisation of RAM use
    if len(readline) > 1 and readline[0].isupper():
        cClassroom.teacher=readline # Update the teacher name of current classroom
        teacherNameBox.delete(0, 'end') # Delete previous value in teacher name textbox
        teacherNameBox.insert(0,cClassroom.teacher) # Put the value loaded from PMC file into the text box
        return True # Accept input if it contains more than one characters
    else:
        messagebox.showerror(title=None, message=("Teacher name must start with capital letter and contain atleast 2 characters. Invalid file was opened.")) # Tell user why input is rejected
        return False # Do not accept invalid input

def validateFileStudentNum(readline):
    readline=readline[:-1] # Python adds a space (' ') to the end of strings which are read from text files, this space is not needed and must be removed for optimisation of RAM use
    if readline.isnumeric(): # Accept any numberic string eg '2' or '50'
        if int(readline) > 0 and int(readline) <= 256: # Make sure the numerical input is not greater than the maximum value of students in class: '256' and not less than 1
            updateRegister(readline) # Update the register if the input if valid
            cClassroom.numStudents=int(readline)
            studentNumBox.delete(0, 'end') # Delete previous value in students number textbox
            studentNumBox.insert(0,cClassroom.numStudents) # Put the value loaded from PMC file into the text box
            return True # Accept input if it contains more than one characters
        else:
            messagebox.showerror(title=None, message=("The number of students in class must be an integer between 1 and 256. Invalid file was opened.")) # Tell user why input is rejected
            return False # Do not accept invalid input  
    else:
        messagebox.showerror(title=None, message=("The number of students in class must be an integer between 1 and 256. Invalid file was opened.")) # Tell user why input is rejected
        return False # Do not accept invalid input

def validateName(userInput):
    if len(userInput) > 1 and userInput[0].isupper():
        return True
    else:
        return False

def validateStudentResult(userInput):
    if userInput == 'A*' or userInput == 'A' or userInput == 'B' or userInput == 'C' or userInput == 'D' or userInput == 'E' or userInput == 'U':
        return True
    else:
        return False

def validateStudentAddress(userInput):
    if len(userInput) > 5:
        return True
    else:
        return False

def validateEmail(userInput):
    if '.' in userInput and '@' in userInput: # Make sure the input contains '.' and '@'
        return True # Accept valid input
    else:
        return False # Reject invalid input

def validatePhoneNum(userInput):
    if len(userInput) == 11 and userInput.isnumeric():
        return True
    else:
        return False

def validateLessonsSupposedtoBeAttended(userInput):
    if userInput.isnumeric():
        return True
    else:
        return False

def validateLessonsAttended(totalLessons, lessonsAttended):
    if lessonsAttended.isnumeric():
        if int(lessonsAttended) <= totalLessons:
            return True
        else:
            return False
    else:
        return False

def validateUsernameAndPassword(usernameEntry,passwordEntry,authenticateRoot):
    global bAuthenticationDone
    username=usernameEntry.get()
    password=passwordEntry.get()
    if username == 'Sanctuary' and password == 'Binary5!':
        bAuthenticationDone=True
        authenticateRoot.destroy()
        return True
    else:
        messagebox.showerror(title=None, message=("Invalid username/password is entered.")) # Show error message
        authenticateRoot.focus_force() # Focus on login window
        return False

# +----------------------------------------------------------------------------------------+
# Define different types of message boxes
# +----------------------------------------------------------------------------------------+

def showCurrentLessonAttendanceInputError():
    messagebox.showerror(title=None, message="Please enter a valid value in the field.\n/ = Student is present, N = Student is absent, L = Student is late")
    
def showHelpMsg():
    messagebox.showinfo(title=None, message='''Strategy for Teachers:\n
1 - Click on the 'File' drop down menu at top left
2 - Choose to load a classroom from the options
3 - After the classroom is successfully loaded then click on 'Take Register' button at top left...If the class fails to load then contact the school's IT technicians to fix the file.
4 - The cursor will appear in a box next to a student's name
5 - If the student is present then input '/', otherwise enter 'N' for absent and 'L' for late
6 - Repeat this process for all students of class
7 - Once the register is done then click on the 'Save Class' button at top left\n
Strategy for Senior Leaders at School:\n
1 - Click on the 'File' drop down menu at top left
2 - Choose to load a classroom from the options
3 - After the classroom is successfully loaded then click on 'Render Graph' button at top left...If the class fails to load then contact the school's IT technicians to fix the file.
4 - A colourful graph should open in a new window, if this does not happen then contact school's IT team to install matplotlib on that computer
5 - Use the buttons on the bottom of the graph to zoom in/out or to save graph as a scalable vector or raster image
6 - To view/modify data of individual students: click on the 'View/Edit Student Data' button next to a student's name in register''')

def showAboutMsg():
    messagebox.showinfo(title=None, message=constAppTitle+" is developed by Syed Ali Raza from 2014 batch for his A Level Computer Science Coursework.")

def showNotYetImplementedMsg(): # For future beta builds
    messagebox.showerror(title=None, message="Sorry--this feature is not yet implemented.") # Show error message

def showFileFailedToOpenError():
    messagebox.showerror(title=None, message="The file is not valid. Please open a PMC file.")

# +----------------------------------------------------------------------------------------+
# Define the main function
# +----------------------------------------------------------------------------------------+

def main():
    Initialisation()

# +----------------------------------------------------------------------------------------+
# Execute the main function
# +----------------------------------------------------------------------------------------+

main()
