# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 14:45:15 2019

@author: diamond
"""
import PyTango

TDC=PyTango.DeviceProxy("ktof/tdc/tdc1")
Sample=PyTango.DeviceProxy("set/sample/voltage")

while True:
    
    
    
    
    
    
    
    
'''    
        def measure_sp(self):
        while True:
            if self.start_trigger==True and self.TDC.state()==PyTango.DevState.ON:
                self.TDC.write_attribute("ExposureLive", self.attr_Exposure_read)
                if len(self.attr_sp_x_read)>1:
                    self.attr_sp_x_read=[0]#np.delete(self.attr_sp_x_read,[1:],0)
                    self.attr_sp_y_read=[0]#np.delete(self.attr_sp_y_read,[1:],0)
                print len(self.attr_sp_y_read)
                print self.attr_Sample_V_max_read,self.attr_Sample_V_min_read,self.attr_Voltage_step_read

                if self.attr_Voltage_step_read>0:
                    self.steps=(self.attr_Sample_V_max_read-self.attr_Sample_V_min_read)/self.attr_Voltage_step_read+1
                    print self.steps, self.attr_Sample_V_max_read, self.attr_Sample_V_min_read, self.attr_Voltage_step_read
                    self.attr_measurements_error_read="No error"
                    self.attr_sp_x_read[0]=self.attr_Sample_V_min_read
                    for i in range(1,int(self.steps),1):
                        self.attr_sp_x_read=np.append(self.attr_sp_x_read,(self.attr_Sample_V_min_read+i*self.attr_Voltage_step_read))
                        self.attr_sp_y_read=np.append(self.attr_sp_y_read,0)
                    self.TDC.write_attribute("CmdTrig_Acquisition_Start",1)
                    time.sleep(0.1)
                    for i in range(1,int(self.steps),1):                        
                        self.HV_PS.set_output_voltage(self.attr_sp_x_read[i])
                        time.sleep(self.attr_Exposure_read)
                        self.attr_sp_y_read[i]+=self.TDC.read_attribute("Counts_Per_Sec").value
                        if self.stop_trigger==True:
                            self.TDC.write_attribute("CmdTrig_Acquisition_Stop",1)
                            self.stop_trigger=False
                            self.start_trigger=False
                            break
                        
                    #if self.TDC.state()!=PyTango.DevState.ON:
                    #    self.attr_measurements_error_read="problems with TDC server"
                    #else:
                    #    print 1
                        #for i in range(self.steps):
                         #   self.HV_PS.setVoltage(self.attr_Sample_V_min_read+i*self.attr_Voltage_step_read
                            
                elif self.attr_Voltage_step_read==0:
                    self.attr_measurements_error_read="check measuremeets parameters!"
                elif self.attr_Sample_V_max_read<self.attr_Sample_V_min_read:
                    self.attr_measurements_error_read="check measuremeets parameters!"
                self.start_trigger=False
            elif self.TDC.state()!=PyTango.DevState.ON:
                self.attr_measurements_error_read="problems with connection to TDC!"
            time.sleep(1)
'''