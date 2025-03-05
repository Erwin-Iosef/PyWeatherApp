#-------------------------------------------------------------------------------
# Name:         PyweatherApp.pyw
# Purpose:
#
# Author: Erwin-Iosef
#
# Created:      12-10-2024
#	using GUIpy by  Gerhard Röhner
#       https://github.com/groehner/guipy/
#
# Sun-Valley-ttk-theme by https://github.com/rdbende/Sun-Valley-ttk-theme/tree/main
#
# Copyright:    (c)  2024
# Licence: Nothing
# Made possible by wttr.in
#-------------------------------------------------------------------------------

#Commented code is for debugging#
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo
from modules import requests
import sqlite3
from modules import sv_ttk
#from PyQt5.QtWidgwts import QApplication, QMessagebox
class app(ttk.Frame):

    def __init__(self):
        self.i=-1
        self.root = tk.Tk()
        super().__init__(self.root)
        self.root.geometry('612x480')
        self.root.title('Welcome to the Weather Program')
        self.create_widgets()
        self.mainloop()
        

    def create_widgets(self):
        sv_ttk.set_theme("light")
        self.dasd = tk.Menu(tearoff=0)
        self.lWeatherProgram = ttk.Label(anchor='n')
        self.lWeatherProgram.place(x=224, y=24, width=152, height=24)
        self.lWeatherProgram['text'] = 'Weather Program'
        self.bRun = ttk.Button()
        self.bRun.place(x=144, y=376, width=80, height=30)
        self.bRun['text'] = 'Run'
        self.bRun['command'] = self.bRun_Command
        self.bExit = ttk.Button()
        self.bExit.place(x=392, y=376, width=80, height=30)
        self.bExit['text'] = 'Exit'
        self.bExit['command'] = self.bExit_Command
        self.outputfilewrite = ttk.Checkbutton()
        self.outputfilewrite.place(x=310, y=208, width=32, height=32)
        self.outputfilebool = tk.IntVar()
        self.outputfilewrite['variable'] = self.outputfilebool
        self.lEnterthenameoftheCity = ttk.Label()
        self.lEnterthenameoftheCity.place(x=112, y=88, width=232, height=24)
        self.lEnterthenameoftheCity['anchor'] = 'w'
        self.lEnterthenameoftheCity['text'] = 'Enter the name of the City:'
        self.lSelecttheoutputformat = ttk.Label()
        self.lSelecttheoutputformat.place(x=112, y=152, width=152, height=24)
        self.lSelecttheoutputformat['anchor'] = 'w'
        self.lSelecttheoutputformat['text'] = 'Select the output format:'
        self.lWriteOutputfile = ttk.Label()
        self.lWriteOutputfile.place(x=112, y=208, width=140, height=24)
        self.lWriteOutputfile['anchor'] = 'w'
        self.lWriteOutputfile['text'] = 'Write Output file'
        self.WriteSQLDatabase = ttk.Label()
        self.WriteSQLDatabase.place(x=112, y=245, width=165, height=24)
        self.WriteSQLDatabase['anchor'] = 'w'
        self.WriteSQLDatabase['text'] = 'Write into SQL database'
        self.databasefilewrite = ttk.Checkbutton()
        self.databasefilewrite.place(x=310, y=242, width=32, height=32)
        self.databasefilebool = tk.IntVar()
        self.databasefilewrite['variable'] = self.databasefilebool
        
        self.EraseSQLDatabase = ttk.Label()
        self.EraseSQLDatabase.place(x=112, y=280, width=185, height=24)
        self.EraseSQLDatabase['anchor'] = 'w'
        self.EraseSQLDatabase['text'] = 'Erase SQL database(Table)'    
        self.databasefileerase = ttk.Checkbutton()
        self.databasefileerase.place(x=310, y=279, width=32, height=32)
        self.databasefileerasebool = tk.IntVar()
        self.databasefileerase['variable'] = self.databasefileerasebool
        
        self.cityname = ttk.Entry()
        self.cityname.place(x=408, y=88, width=160, height=25)
        self.cityname['font'] = ('Segoe UI', 9)
        self.citynameCV = tk.StringVar()
        self.citynameCV.set('')
        self.cityname['textvariable'] = self.citynameCV
        self.options={'Choose Output':'', 'Weather condition':'%c%C', 'Humidity':'%h', 'Temperature (Actual)':'%c%t %f', 'Wind':'%c%w', 'Moon phase 🌑🌒🌓🌔🌕🌖🌗🌘':'%m', 'Moon day':'%M', 'Precipitation (mm/3 hours)':'%c%p', 'Pressure (hPa)':'%c%P', 'UV index (1-12)':'%c%u',}
        self.outputformatCV = tk.StringVar(self.root)
        self.outputformatCV.set(list(self.options.keys())[0])
        self.outputformat = ttk.OptionMenu(self.root, self.outputformatCV, *self.options.keys())
        self.outputformat.place(x=408, y=152, width=160, height=32)
        self.outputformat['text'] = 'Select'
        self.TimeDisplay = ttk.LabelFrame()
        self.TimeDisplay.place(x=400, y=224, width=176, height=104)
        self.TimeDisplay['labelanchor'] = 'n'
        self.TimeDisplay['text'] = 'Display Time'
        self.cbLocalTime = ttk.Checkbutton(self.TimeDisplay)
        self.cbLocalTime.place(x=24, y=8, width=128, height=32)
        self.cbLocalTimeCV = tk.IntVar()
        self.cbLocalTimeCV.set(0)
        self.cbLocalTime['variable'] = self.cbLocalTimeCV
        self.cbLocalTime['text'] = 'Local Time'
        self.cbCurrentTime = ttk.Checkbutton(self.TimeDisplay)
        self.cbCurrentTime.place(x=24, y=40, width=128, height=32)
        self.cbCurrentTimeCV = tk.IntVar()
        self.cbCurrentTimeCV.set(0)
        self.cbCurrentTime['variable'] = self.cbCurrentTimeCV
        self.cbCurrentTime['text'] = 'Current Time'
        self.toggletheme = ttk.Button()
        self.toggletheme.place(x=112, y=320, width=144, height=32)
        self.toggletheme['text'] = 'Toggle theme'
        self.toggletheme['command'] = sv_ttk.toggle_theme
        pass

    def getkeyvals(self):
        self.selected_key = self.outputformatCV.get()  # Get the selected key from the optionMenu
        self.selected_value = self.options[self.selected_key]
        return self.selected_value
    def bRun_Command(self):
        self.outputdisform=self.getkeyvals()
        if self.cbCurrentTimeCV.get()==True and self.cbLocalTimeCV.get()==True:
         self.TimeDisplay="%T %Z"
        elif self.cbLocalTimeCV.get()==True:
          self.TimeDisplay="%Z"
        elif self.cbCurrentTimeCV.get()==True:
          self.TimeDisplay="%T"
        else:
         self.TimeDisplay=""
        print("----CONSOLE LOG----\n")
        if not self.cityname.get():
            showinfo("Warning", "Enter a name")
        else:
            url = f'https://wttr.in/{self.citynameCV.get()}?format=%l: {self.outputdisform}+ {self.TimeDisplay}'
            #f'https://wttr.in/{self.cityname}?format({self.outputformat[selected_value],self.TimeDisplayRB0,self.TimeDisplayRB1})'
            try:
                data = requests.get(url)
                self.output = data.text
            except:
                self.output = "Error Occurred"
            #Print Weather forecast
            print(url)
            print(self.selected_value,self.selected_key)
            print(self.output)
            showinfo(self.outputformatCV.get(),self.output)
        if self.outputfilebool.get():
          with open('weather.log', 'a',encoding='utf-8') as file:
           file.write(self.outputformatCV.get()+'\n')
           file.write(self.output)
		  
        if self.databasefilebool.get():
         self.i+=1
         self.outputvalrea=data.text.split()
         
         #print(self.outputvalrea)
         if self.cbCurrentTimeCV.get()==True and self.cbLocalTimeCV.get()==True:
             if len(self.outputvalrea)<5:
                 self.outputvalrea.insert(2,'')
         else: 
             if self.cbLocalTimeCV.get()==False:
                 self.outputvalrea.append('')
             if self.cbCurrentTimeCV.get()==False:
                 self.outputvalrea.insert(-1,'')
         if len(self.outputvalrea)>5:
            self.concatextra=[' '.join(self.outputvalrea[2:4])]
            self.outputvalrea=self.outputvalrea[:2] + self.concatextra + self.outputvalrea[4:]
         print(self.outputvalrea)
         if len(self.outputvalrea)==4:
             self.outputval=''.join(self.outputvalrea[1:2])
         else:
             self.outputval=''.join(self.outputvalrea[1:3])
         #print("here's ouput", self.outputval)
         self.current_time=''.join(self.outputvalrea[-1])
         self.local_time=''.join(self.outputvalrea[-2]) 
        #print(self.current_time,self.local_time)
         self.database()
        pass

    def bExit_Command(self):
        quit()
        pass

    def database(self):
        conn = sqlite3.connect('Weather.db')
		# Create a cursor object using the cursor() method
        cursor = conn.cursor()
        if self.databasefileerasebool.get():
         print("Erasing Table First")
         cursor.execute('DROP TABLE IF EXISTS WeatherReport')
         conn.commit()
		# Create table
        cursor.execute('''CREATE TABLE IF NOT EXISTS WeatherReport (
        			"SI.NO" integer(10) PRIMARY KEY, 
        			 Place varchar(20), 
        			"Output Format" varchar(20),
        			"OutputFile Writebool" varchar(20),
        			"Local Time" varchar(20),
        			"Current_Time" varchar(20))''')
        cursor.execute('''INSERT OR REPLACE INTO WeatherReport("SI.NO",Place,"Output Format","OutputFile Writebool","Local Time","Current_Time")
        VALUES(?, ?, ?, ?, ?, ?)''',
       (self.i,
        self.citynameCV.get(),
        self.outputval,
        self.outputfilebool.get(),
        self.local_time,
        self.current_time))

        conn.commit()
        columns = [description[0] for description in cursor.fetchall()]
        #print(columns)
        showtable=tk.messagebox.askokcancel(title="Show SQL Table", message="Would you like to see the table?")
        cursor.execute('SELECT * FROM WeatherReport')
        rows=cursor.fetchall()
        rowsval=print(*rows,sep='\n')
        #with open('weather.log', 'a',encoding='utf-8') as file:
         #print(*rows,sep='\n',file=file)
         
        if showtable==True:
         message="\n".join([str(row) for row in rows])
         print(f"Showing Table{message}")
         showinfo("SQL Table",message)	
        #Close the connection
        conn.close()

app()
