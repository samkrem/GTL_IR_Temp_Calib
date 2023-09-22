# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:48:16 2023

@author: sammykrem
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk #python gui toolkit
#import numpy as np
import time
import random
#import socket
import pickle
import nidaqmx
from nidaqmx.constants import AcquisitionType
#import math
import multiprocessing
#from PIL import ImageTk,Image


cond=False
len1 = 70
len3=70
a = 298

timePXI = [0]*len1
timemdot = [0]*150
taskList=[]

data_f= open(r"C:\\Users\\User\\Documents\\PythonScripts\\IRSensCalib_%d.txt" % random.randint(100, 5000), 'wb')
pointsPXISlot9ch05 = [a]*len1 #need to figure this out

voltagePoints = [0]*len3
#voltage data is collectd by samples[0] (tasklist)
tc1Points= [0]*len3
tc2Points= [0]*len3
tc3Points= [0]*len3
tc12avgPoints=[0]*len3
calibVoltagePoints=[]
calibTCPoints=[]


slope1=[0]*len3  #avg of plate temp/voltage
slope2=[0]*len3 #ambient temp/voltage
t0 = time.time()
class ResizingCanvas(tk.Canvas):
    def __init__(self,parent,**kwargs):
        tk.Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        self.config(width=self.width, height=self.height)
        self.scale("all",0,0,wscale,hscale)
def main():
    Loop_Active = True

    root = tk.Tk() #creates window
    root.title('Real Time Plot')
    root.configure(background = 'lightgrey')
    myframe = tk.Frame(root)
    myframe.pack(fill="both", expand="yes") #adds frame in real time plot
    
    root.state("zoomed") 
    mycanvas = ResizingCanvas(myframe,width=500, height=400, bg="lightgrey", highlightthickness=0) #resizing window
    mycanvas.pack(fill="both", expand="yes")
 #for IR sensor   
    fig1 = Figure(facecolor = "lightgrey");
    ax1 = fig1.add_subplot(111)
    pos1 = ax1.get_position()
    pos1 = [pos1.x0, pos1.y0 + 0.25, pos1.width, pos1.height - 0.2]
    ax1.set_position(pos1)

    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1.get_tk_widget().place(relx = 0.01, rely=0.54, relwidth = 0.3, relheight = 0.55) #NEED TO ADJUST POSITION
   
    # fig11 = Figure(facecolor = "lightgrey");
    # canvas11 = FigureCanvasTkAgg(fig11, master=root)
    
#for TC    
    fig2 = Figure(facecolor = "lightgrey");
    ax2 = fig2.add_subplot(111)
    pos2 = ax2.get_position()
    pos2 = [pos2.x0, pos2.y0 + 0.25, pos2.width, pos2.height - 0.2]
    ax2.set_position(pos2)

    canvas2 = FigureCanvasTkAgg(fig2, master=root)
    canvas2.get_tk_widget().place(relx = 0.305, rely=0.54, relwidth = 0.3, relheight = 0.55)

    # fig12 = Figure(facecolor = "lightgrey");
    # canvas12 = FigureCanvasTkAgg(fig12, master=root)

#for calibration
    fig3=Figure(facecolor= "lightgrey");
    ax3 = fig3.add_subplot(111)
    pos3 = ax3.get_position()
    pos3 = [pos3.x0, pos3.y0 + 0.25, pos3.width, pos3.height - 0.2]
    ax3.set_position(pos3)

    canvas3 = FigureCanvasTkAgg(fig3, master=root)
    canvas3.get_tk_widget().place(relx = 0.605, rely=0.54, relwidth = 0.3, relheight = 0.55)
    
    fig4=Figure(facecolor= "lightgrey");
    ax4 = fig4.add_subplot(111)
    pos4 = ax4.get_position()
    pos4 = [pos4.x0, pos4.y0 + 0.25, pos4.width, pos4.height - 0.2]
    ax4.set_position(pos4)

    canvas4 = FigureCanvasTkAgg(fig4, master=root)
    canvas4.get_tk_widget().place(relx = 0.01, rely=0, relwidth = 0.3, relheight = 0.55)
    
    fig5=Figure(facecolor= "lightgrey");
    ax5 = fig5.add_subplot(111)
    pos5 = ax5.get_position()
    pos5 = [pos5.x0, pos5.y0 + 0.25, pos5.width, pos5.height - 0.2]
    ax5.set_position(pos5)

    canvas5 = FigureCanvasTkAgg(fig5, master=root)
    canvas5.get_tk_widget().place(relx = 0.305, rely=0, relwidth = 0.3, relheight = 0.55)
    
     #GUI interface
     #create main window 
         #need title like "IR Temperature Sensor Plot"
     #Windows inside main window 
         #time vs IR temp sens voltage values graph
         #time vs thermocouple temperature values graph
         #Thermocouple temperature vs voltage values graph with calibration button that plots the points
 
    
    
    def get_PXI_data(): #called in plot_data
        global sample1, sample2, sample3, sample4, c, timePXI, pointsPXISlot9ch05
        sample1 = taskList[0].read()
        voltage=sample1[0]
        voltagePoints[:len1-1] = voltagePoints[1:len1]
        voltagePoints[len1-1] = voltage
    
       
        sample2 = taskList[1].read()
       
        temperature1=sample2[0]
        tc1Points[:len1-1] = tc1Points[1:len1]
        tc1Points[len1-1] = temperature1
        
        
        temperature2=sample2[1]
        tc2Points[:len1-1] = tc2Points[1:len1]
        tc2Points[len1-1] = temperature2
        
          
        temperature3=sample2[2]
        tc3Points[:len1-1] = tc3Points[1:len1]
        tc3Points[len1-1] = temperature3 
      
        for i in range(len3):
            try:
                tc12avgPoints[i]=(tc1Points[i]+tc2Points[i])/2
                slope1[i]=tc12avgPoints[i]/voltagePoints[i]#(tc1Points[i]+tc2Points[i])/(2*voltagePoints[i])
                slope2[i]=(tc3Points[i])/(voltagePoints[i])
                
            except ZeroDivisionError:
                slope1[i]=0
                slope2[i]=0
  
        timePXI[:len1-1] = timePXI[1:len1]
        timePXI[len1-1] = time.time() - t0  
        
        if timePXI[len1-1] > 80:
            c = 1
        return
    def plot_data(): #called during while loop
        global cond, data, data_f, mff, gamma, c, Ap, At, cp, area, rpm, t0, pr, R, kt, M, P1, P2, P3, P4, P5, Pt, Ps, b, venturistatic, mdot1, mdot2, pointsmdot1, pointsmdot2, samples, temp1, temp2, s170, points170, points50b, time170, timePXI, pointsPXI2, points170_1, pointsPXI3, totalp_avg, staticp_avg, pointsPXI4, pointsPXI5, Pt01, Pt02, Pt03, Pt21, Pt22, Pt22
        if (cond == True):
            ax1.cla()
            ax1.grid()          
            ax2.cla()
            ax2.grid()
            ax3.cla()
            ax3.grid()
            ax4.cla()
            ax4.grid()
            ax5.cla()
            ax5.grid()
            get_PXI_data()
            
            timemdot[:149] = timemdot[1:150]
            timemdot[149] = time.time() - t0
            if (time.time() - t0) < 80:
                ax1.set_xlim(0,80)
                ax2.set_xlim(0,80)
                ax3.set_xlim(0,80)
                ax5.set_xlim(0,80)
            
            pickle.dump((voltagePoints[len3-1], tc1Points[len3-1], tc2Points[len3-1], tc3Points[len3-1] ,slope1[len3-1], slope2[len3-1],  timePXI[len1-1]), data_f)



            #need these lines
            ax1.plot(timePXI, voltagePoints, marker = 'o', color = 'orchid', label ="Voltage = %s V" % round(voltagePoints[len1-1],2))
            ax1.set_title('Voltage [V] vs time [s]');
            ax1.set_xlabel('time [s]')
            ax1.set_ylabel('Voltage [V]')

            ax1.legend(bbox_to_anchor=(1.05,-0.15), fontsize=8)
            canvas1.draw()
          
            ax2.plot(timePXI, tc1Points, marker = 'o', color = 'darkorange', label ="Upperplate Temp = %s C" % round(tc1Points[len1-1],1))
            ax2.plot(timePXI, tc2Points, marker = 'o', color = 'royalblue', label ="Lowerplate Temp = %s C" % round(tc2Points[len1-1],1))
            ax2.plot(timePXI, tc12avgPoints, marker = 'o', color = 'purple', label ="Avg Plate Temp = %s C" % round(tc12avgPoints[len1-1],1))

            ax2.set_title('Upper Plate Temp [C] vs time [s]');
            ax2.set_xlabel('time [s]')
            ax2.set_ylabel('Upper Plate Temperature [C]]')

            ax2.legend(bbox_to_anchor=(1.05,-0.15), fontsize=8)
            canvas2.draw()
            
            
        
               
            
            ax3.plot(timePXI, slope1, marker = 'o', color = 'mediumblue', label ="Plate Temperature/Voltage = %s V/C" % round(slope1[len1-1],1))
            ax3.plot(timePXI, slope2, marker = 'o', color = 'forestgreen', label ="Ambient Temperature/Voltage = %s V/C" % round(slope2[len1-1],1))
          
            ax3.set_title('Temperature/Voltage [V/C] vs time [s]');
            ax3.set_xlabel('time [s]')
            ax3.set_ylabel('Temperature/Voltage [V/C]')
            ax3.legend(bbox_to_anchor=(1.05,-0.15), fontsize=8)
            canvas3.draw()
            
            ax4.set_title('tcPoints vs Voltage [V]');
            ax4.set_xlabel('Voltage [V]')
            ax4.set_ylabel('Temperature [C]')
            
            
            ax5.plot(timePXI, tc3Points, marker = 'o', color = 'darkorange', label ="Ambient Temperature = %s C" % round(tc3Points[len1-1],1))

            ax5.set_title('Ambient Temperature [C] vs time [s]');
   
            ax5.set_xlabel('time [s]')
            ax5.set_ylabel('Ambient Temperature [C]');
            ax5.legend(bbox_to_anchor=(1.05,-0.15), fontsize=8)
            canvas5.draw()
    def plot_start():
        global cond,  data_f, s, tni, taskList
    
        taskList = []
        #IR Sensor
        tni1 = nidaqmx.Task()
        tni1.ai_channels.add_ai_voltage_chan_with_excit('PXI1Slot9/ai5:6',  terminal_config =  nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL, min_val=-10.0, max_val=10.0, bridge_config= nidaqmx.constants.BridgeConfiguration.NO_BRIDGE, voltage_excit_source=nidaqmx.constants.ExcitationSource.EXTERNAL, voltage_excit_val=10.0, use_excit_for_scaling=True) #nidaqmx.constants.TerminalConfiguration.DIFFERENTIAL
        tni1.timing.cfg_samp_clk_timing(20,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) # samps_per_chan = 10000)
        tni1.in_stream.relative_to = nidaqmx.constants.ReadRelativeTo.MOST_RECENT_SAMPLE

        #thermocouple
        tni2 = nidaqmx.Task()
        tni2.ai_channels.add_ai_thrmcpl_chan('PXI1Slot2/ai0:3', units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)
        # tni2.ai_channels.add_ai_thrmcpl_chan('PXI1Slot2/ai1:2', units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)
        # tni2.ai_channels.add_ai_thrmcpl_chan('PXI1Slot2/ai2:3', units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)

        tni2.timing.cfg_samp_clk_timing(20,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) # samps_per_chan = 10000)
        tni2.in_stream.relative_to = nidaqmx.constants.ReadRelativeTo.MOST_RECENT_SAMPLE
        
        # tni3 = nidaqmx.Task()
        # tni3.ai_channels.add_ai_thrmcpl_chan('PXI1Slot2/ai1:2', units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)
        # tni3.timing.cfg_samp_clk_timing(20,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) # samps_per_chan = 10000)
        # tni3.in_stream.relative_to = nidaqmx.constants.ReadRelativeTo.MOST_RECENT_SAMPLE
      
        # tni4 = nidaqmx.Task()
        # tni4.ai_channels.add_ai_thrmcpl_chan('PXI1Slot2/ai2:3', units=nidaqmx.constants.TemperatureUnits.DEG_C, thermocouple_type=nidaqmx.constants.ThermocoupleType.K)
        # tni4.timing.cfg_samp_clk_timing(20,sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS) # samps_per_chan = 10000)
        # tni4.in_stream.relative_to = nidaqmx.constants.ReadRelativeTo.MOST_RECENT_SAMPLE
    
        taskList.append(tni1)
        taskList.append(tni2)
        # taskList.append(tni3)
        # taskList.append(tni4)
        tni1.start()
        tni2.start()
        # tni3.start()
        # tni4.start()
        print("Tasklist: ",taskList)
        #start plots
        data_f = open(r"C:\\Users\\User\\Documents\\PythonScripts\\IRSensCalib_%d.txt" % random.randint(100, 5000), 'wb')    
        cond = True
    def plot_stop():
        global Loop_Active, s170, s118, cond
        Loop_Active = False
        cond = False
        # -------stop and close PXI-------
        for tni in taskList:
            tni.stop()
        for tni in taskList:
            tni.close()
        taskList.clear()
        
        print("connections closed")
        
        data_f.close()
        root.destroy()
        p1.terminate()
    def pause():
        global cond
        data_f.close()
        cond = False
    
    def resume():
        global cond, data_f
        data_f = open(r"C:\\Users\\User\\Documents\\PythonScripts\\IRSensCalib_%d.txt" % random.randint(100, 5000), 'wb')    
        cond = True
    def calibrate():
        global cond, data_f
        # slope=[0]*len3
        # for i in range(len3):
        #     try:
        #         slope[i]=tcPoints[i]/voltagePoints[i]
        #     except ZeroDivisionError:
        #         slope[i]=0
        # calibVoltPts= [voltagePoints[0], voltagePoints[len3-1]]
        # calibTcPoints=[tcPoints[0], tcPoints[len3-1]]
        calibVoltagePoints.append(voltagePoints[len3-1])
        calibTCPoints.append((tc1Points[len3-1]+tc2Points[len3-1])/2)
        # calibTCPoints.append(tc3Points[len3-1])


       
        ax4.scatter(calibVoltagePoints,calibTCPoints, color="mediumaquamarine")
        tcAvg=round((tc1Points[len3-1]+tc2Points[len3-1])/2,2)
        ax4.plot(calibVoltagePoints,calibTCPoints, color="mediumaquamarine", label ="(Voltage,Temperature) = %s , %s" % (round(voltagePoints[len3-1],2),tcAvg))

        ax4.legend(bbox_to_anchor=(1.05,-0.15),fontsize=8)

        canvas4.draw()
        # canvas4.flush_events()
        # time.sleep(0.1)

        #need to code what this does

     #-------create button-------
    root.update();
    start = tk.Button(root, text = "   Start    ", bg = "grey", font = ('calbiri',14),command = lambda: plot_start())
    start.place(relx = 0.8, rely = 0.2)
     
    root.update();
    stop = tk.Button(root, text = "    Stop   ", bg = "grey", font = ('calbiri',14), command = lambda: plot_stop())
    stop.place(relx = 0.9, rely = 0.2)
     
    root.update();
    stop = tk.Button(root, text = "  Pause  ", bg = "grey", font = ('calbiri',14), command = lambda: pause())
    stop.place(relx = 0.8, rely = 0.3)
     
    root.update();
    stop = tk.Button(root, text = "Resume", bg = "grey", font = ('calbiri',14), command = lambda: resume())
    stop.place(relx = 0.9, rely = 0.3)
     
    root.update()
    calib=tk.Button(root, text = "Calibrate", bg = "grey", font = ('calbiri',14), command = lambda: calibrate())
    calib.place(relx = 0.05, rely = 0.4)

    while Loop_Active:
        try:
            root.update()
            if (cond == True):
                plot_data()
           
        except KeyboardInterrupt:

            # -------stop and close cdaq-------
            for tni in taskList:
                tni.stop()
            for tni in taskList:
                tni.close()
            taskList.clear()
            print("connections closed")
            
            data_f.close()
            root.destroy()
            p1.terminate()
if __name__ == "__main__":
        print("in if __name__ == __main__: ")
        p1 = multiprocessing.Process(target = main)
        p1.start()
        p1.join()
