#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  6 15:35:20 2019

@author: Bellinda

1.Set temperature
2.check time and oly measure while time is between some delta T 
(wait for stability)
3.Measure V(t) for some time and average
4. write V and T to file 
5. Set new temperature
want real time plot

Lock in can do trace scan
plot voltage and the error 
find the error 

Parameters (min T, max T, step T)
"""

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import tkinter as Tk
import Amplifier
import temperaturecon
import Multimetercommand


from tkinter import filedialog

import visa 
resource_manager = visa.ResourceManager()

amplification = 100.0#also could be 1000
res_ref = 1.0# reference resistor we know the resistance very well, error 1%

#gobal defintion that defines how we can calculate the Resistance of the sample 

def Rsample_value(Vref,Vsample):
    Reval=(1/amplification)*(Vsample/Vref)*res_ref
    return Reval

class interface:
    def __init__(self):
        ''' 
        Array is fized length 
        '''
        self.running = False
        self.recur_id = None #events associated with the call back
        self.fnm='myfile.txt'
        self.write_f('Time, Temp(K)\n',create=True)
        self.start_time=dt.datetime.now()
#        self.my_Amp = Amplifier(9)
#        self.my_Temp = Temp_con(9) 
#        self.my_mult = Multimeter(9)
        #dumby values when no machine is attached
        self.my_Amp = None
        self.my_Temp = None
        self.my_mult = None
        self.Tnow=100#my_Temp.set_temp()
        self.Vref=[]
        self.Vsample=[]
        self.Temp=[]
        self.Rsample=[]
        self.Time=[]
        self.run_gui()
    
    def write_f(self, wstring,create=False):
        if create == True:
            mode = 'w'#create a new file
        else:
            mode = 'a' #append data to the existing file
        with open(self.fnm,mode) as tofile: #open myfile.txt, wa make a new file if doesnt exist or append to a file
            tofile.write(wstring) #write to tofile, 
            
            
        
    def quit_exec(self): #commands for close buttons
        #self.root.after_cancel(self.recur_id)
        #self.recur_id=None
        #self.root.quit()
        self.root.destroy()

        
#    def start_exec(self): #command for start button
#        if self.running:
#            print ('stopping')
#            self.start_time=dt.datetime.now()
#            self.running = False
#            self.root.after_cancel(self.recur_id)
#            self.recur_id=None
#            self.runbuttonlabel.set('START')
#        elif not self.running:
#            print ('starting')
#            self.runbuttonlabel.set('STOP')
#            self.running = True
#            self.root.after(1000, self.query_T)
            
    def start_exec(self):
        '''
        Similar to above, this starts and stops operation 
        of the main data-writing functionality of this gu
        intention is to initiate a callback every 1 s.
        '''
        if not self.running:
            self.running = True
            self.runbuttonlabel.set('STOP')
            self.recur_id = self.root.after(1000,self.Task)
            
        else:
            self.runbuttonlabel.set('START')
            self.running = False
            self.root.after_cancel(self.recur_id)#after funciton is reiteration
            self.recur_id = None
            
    def Task(self):
        '''
        want temperature reading
        Resistance 
        Voltage
        All three devices are hooked up
        
        can make attribute 
        '''
        
#        self.Vref.append(my_mult.do_ac_measure())
#        self.Vsample.append(my_Amp.do_volt_measure())
#        self.Temp.append(my_Temp.do_K_measure())
        self.Vref.append(1)
        self.Vsample.append(2)
        self.Temp.append(3)
        self.Rsample.append(Rsample_value(self.Vref[-1],self.Vsample[-1]))
        self.timenow=dt.datetime.now()
        dT=(self.timenow- self.start_time).total_seconds()
        self.write_str='{:0.04f},{:0.04f},{:0.04f},{:0.04f},{:0.04f}\n'.format(dT,
                        self.Temp[-1],self.Vref[-1],self.Vsample[-1],self.Rsample[-1])
        self.write_f(self.write_str)
        self.recur_id =self.root.after(1000,self.Task)
        
#        
#    '''
#    Define write function separately 
#    '''
#            
#    def query_T(self):
#        Tread=my_Temp.do_K_measure()
#        timenow = dt.datetime.now()
#        dT=(timenow- self.start_time).total_seconds()
#        self.Tnow=Tread
#        write_str='{:0.04f},{:0.04f}\n'.format(dT,self.Tnow)
#        self.write_f(write_str)
#        #self.TString.set('Temperature {:0.04f}K'.format(self.Tnow))
#        self.recur_id =self.root.after(1000, self.query_T)
#    
#    def query_R(self):
#        Rread=my_mult.Multimeter(9) 
#        timenow = dt.datetime.now()
#        dT=(timenow- self.start_time).total_seconds()
#        self.Rnow=Rread
#        write_str='{:0.04f},{:0.04f}\n'.format(dT,self.Rnow)
#        self.write_f(write_str)
#        self.RString.set('Temperature {:0.04f}K'.format(self.Rnow))
#        self.recur_id =self.root.after(1000, self.query_R)
#    
#    def query_V(self):
#        Vread=my_Amp.do_volt_measure()
#        timenow = dt.datetime.now()
#        dT=(timenow- self.start_time).total_seconds()
#        self.Vnow=Vread
#        write_str='{:0.04f},{:0.04f}\n'.format(dT,self.Vnow)
#        self.write_f(write_str)
#        self.VString.set('Temperature {:0.04f}K'.format(self.Vnow))
#        self.recur_id =self.root.after(1000, self.query_V)

    def file_save(self):
        '''
        Open a save-file dialog. if the filename does not end with a 
        ".txt", we fix this. If the file does not exist,
        a new file is created. Otherwise, the existing file is overwritten.
        '''
        self.fnm = filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("text files","*.txt"),("all files","*.*")))
        if self.fnm[-4:]!='.txt':
            self.fnm = self.fnm + '.txt'
        print(self.fnm)
        write_string = 'Time (s), Temperature (K), Vreference(V), Vsample(V), Rsample (Ohm)\n'
        self.write_f(write_string,create=True)
        print('wrote header to file!')


        
    def run_gui(self):
        '''
        Define the structure of the gui window.
        We have 3 buttons: start/stop, browse, and quit
        '''
    
        self.root = Tk.Tk() #creates the window
        self.root.wm_title('UBC GUI Tutorial') #name of the window
        self.runbuttonlabel=Tk.StringVar()
        self.runbuttonlabel.set('START')
#Start stop button changes label once clicked
        self.startstop=Tk.Button(master=self.root,textvariable=self.runbuttonlabel, command=self.start_exec)
        self.startstop.grid(row=3,column=1)

        self.quit_b=Tk.Button(master=self.root,text='CLOSE', command=self.quit_exec)
        self.quit_b.grid(row=3,column=0)
      
        #save button
        self.sv_button = Tk.Button(master=self.root,text='SAVE',command=self.file_save)
        self.sv_button.grid(row=3,column=2)
        
        Tk.mainloop()
        
if __name__ == "__main__":
    '''
    main sequence
    define the instance of interface
    run the mainloop
    
    '''

    my_interface = interface()
    my_interface.root.mainloop()



                