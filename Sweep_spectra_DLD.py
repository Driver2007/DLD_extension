#!/usr/bin/env python
# -*- coding:utf-8 -*-


# ############################################################################
#  license :
# ============================================================================
#
#  File :        Sweep_spectra_DLD.py
#
#  Project :     Sweep_spectra_DLD
#
# This file is part of Tango device class.
# 
# Tango is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Tango is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Tango.  If not, see <http://www.gnu.org/licenses/>.
# 
#
#  $Author :      sergey.v.babenkov$
#
#  $Revision :    $
#
#  $Date :        $
#
#  $HeadUrl :     $
# ============================================================================
#            This file is generated by POGO
#     (Program Obviously used to Generate tango Object)
# ############################################################################

__all__ = ["Sweep_spectra_DLD", "Sweep_spectra_DLDClass", "main"]

__docformat__ = 'restructuredtext'

import PyTango
import sys
# Add additional import
#----- PROTECTED REGION ID(Sweep_spectra_DLD.additionnal_import) ENABLED START -----#
import time
import threading
import numpy as np
import os
from tifffile import imsave
from PIL import Image
#----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.additionnal_import

# Device States Description
# No states for this device


class Sweep_spectra_DLD (PyTango.Device_4Impl):
    """Sweep_spectra"""
    
    # -------- Add you global variables here --------------------------
    #----- PROTECTED REGION ID(Sweep_spectra_DLD.global_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.global_variables

    def __init__(self, cl, name):
        PyTango.Device_4Impl.__init__(self,cl,name)
        self.debug_stream("In __init__()")
        Sweep_spectra_DLD.init_device(self)
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.__init__) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.__init__
        
    def delete_device(self):
        self.debug_stream("In delete_device()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.delete_device) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.delete_device

    def init_device(self):
        self.debug_stream("In init_device()")
        self.get_device_properties(self.get_device_class())
        self.attr_Sample_V_min_read = 0.0
        self.attr_Voltage_step_read = 0.0
        self.attr_Sample_V_max_read = 0.0
        self.attr_Exposure_read = 0.0
        self.attr_measurements_error_read = ""
        self.attr_Server_Save_File_Busy_read = False
        self.attr_Progress_read = 0.0
        self.attr_sp_y_read = [0.0]
        self.attr_sp_x_read = [0.0]
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.init_device) ENABLED START -----#
        self.sample=PyTango.DeviceProxy("set/sample/voltage")
        self.tdc=PyTango.DeviceProxy("ktof/tdc/tdc1")        
        self.Save_Filecounter=0
        self.Save_Directory=""
        self.Save_Filename=""         
        self.steps=0
        self.resize_spectrum_trig=False
        self.CmdTrig_sweep_Start=False
        self.change_scale_trig=False
        self.CmdTrig_stack_Start=False
        self.attr_measurements_error_read="No error"
        self.stack=np.array([[[0.0]]])
        if not 'scale_thread' in dir(self):
            self.scale_thread = threading.Thread(target=self.change_scale)
            self.scale_thread.setDaemon(True)
            self.scale_thread.start()
        if not 'spectrum_thread' in dir(self):
            self.spectrum_thread = threading.Thread(target=self.measure)
            self.spectrum_thread.setDaemon(True)
            self.spectrum_thread.start()
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.init_device

    def always_executed_hook(self):
        self.debug_stream("In always_excuted_hook()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.always_executed_hook) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.always_executed_hook

    # -------------------------------------------------------------------------
    #    Sweep_spectra_DLD read/write attribute methods
    # -------------------------------------------------------------------------
    
    def read_Sample_V_min(self, attr):
        self.debug_stream("In read_Sample_V_min()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Sample_V_min_read) ENABLED START -----#
        attr.set_value(self.attr_Sample_V_min_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Sample_V_min_read
        
    def write_Sample_V_min(self, attr):
        self.debug_stream("In write_Sample_V_min()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Sample_V_min_write) ENABLED START -----#
        self.attr_Sample_V_min_read=data
        self.change_scale_trig=True
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Sample_V_min_write
        
    def read_Voltage_step(self, attr):
        self.debug_stream("In read_Voltage_step()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Voltage_step_read) ENABLED START -----#
        attr.set_value(self.attr_Voltage_step_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Voltage_step_read
        
    def write_Voltage_step(self, attr):
        self.debug_stream("In write_Voltage_step()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Voltage_step_write) ENABLED START -----#
        self.attr_Voltage_step_read=data
        self.change_scale_trig=True      
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Voltage_step_write
        
    def read_Sample_V_max(self, attr):
        self.debug_stream("In read_Sample_V_max()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Sample_V_max_read) ENABLED START -----#
        attr.set_value(self.attr_Sample_V_max_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Sample_V_max_read
        
    def write_Sample_V_max(self, attr):
        self.debug_stream("In write_Sample_V_max()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Sample_V_max_write) ENABLED START -----#
        self.attr_Sample_V_max_read=data
        self.change_scale_trig=True
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Sample_V_max_write
        
    def read_Exposure(self, attr):
        self.debug_stream("In read_Exposure()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Exposure_read) ENABLED START -----#
        attr.set_value(self.attr_Exposure_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Exposure_read
        
    def write_Exposure(self, attr):
        self.debug_stream("In write_Exposure()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Exposure_write) ENABLED START -----#
        self.attr_Exposure_read=data
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Exposure_write
        
    def read_measurements_error(self, attr):
        self.debug_stream("In read_measurements_error()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.measurements_error_read) ENABLED START -----#
        attr.set_value(self.attr_measurements_error_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.measurements_error_read
        
    def write_Save_Filecounter(self, attr):
        self.debug_stream("In write_Save_Filecounter()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Save_Filecounter_write) ENABLED START -----#
        self.Save_Filecounter=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Save_Filecounter_write
        
    def write_Save_Directory(self, attr):
        self.debug_stream("In write_Save_Directory()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Save_Directory_write) ENABLED START -----#
        self.Save_Directory=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Save_Directory_write
        
    def write_Save_Filename(self, attr):
        self.debug_stream("In write_Save_Filename()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Save_Filename_write) ENABLED START -----#
        self.Save_Filename=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Save_Filename_write
        
    def write_CmdTrig_Save_spectrum(self, attr):
        self.debug_stream("In write_CmdTrig_Save_spectrum()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.CmdTrig_Save_spectrum_write) ENABLED START -----#
        self.SaveSpectrum()
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.CmdTrig_Save_spectrum_write
        
    def read_Server_Save_File_Busy(self, attr):
        self.debug_stream("In read_Server_Save_File_Busy()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Server_Save_File_Busy_read) ENABLED START -----#
        attr.set_value(self.attr_Server_Save_File_Busy_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Server_Save_File_Busy_read
        
    def write_CmdTrig_sweep_Start(self, attr):
        self.debug_stream("In write_CmdTrig_sweep_Start()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.CmdTrig_sweep_Start_write) ENABLED START -----#
        self.CmdTrig_sweep_Start=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.CmdTrig_sweep_Start_write
        
    def write_CmdTrig_stack_Start(self, attr):
        self.debug_stream("In write_CmdTrig_stack_Start()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.CmdTrig_stack_Start_write) ENABLED START -----#
        self.CmdTrig_stack_Start=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.CmdTrig_stack_Start_write
        
    def write_CmdTrig_Save_stack(self, attr):
        self.debug_stream("In write_CmdTrig_Save_stack()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.CmdTrig_Save_stack_write) ENABLED START -----#
        self.SaveStack()
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.CmdTrig_Save_stack_write
        
    def read_Progress(self, attr):
        self.debug_stream("In read_Progress()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Progress_read) ENABLED START -----#
        attr.set_value(self.attr_Progress_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Progress_read
        
    def read_sp_y(self, attr):
        self.debug_stream("In read_sp_y()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.sp_y_read) ENABLED START -----#
        #print len(self.attr_sp_y_read),self.attr_sp_y_read        
        attr.set_value(self.attr_sp_y_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.sp_y_read
        
    def read_sp_x(self, attr):
        self.debug_stream("In read_sp_x()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.sp_x_read) ENABLED START -----#
        #print len(self.attr_sp_x_read),self.attr_sp_x_read        
        attr.set_value(self.attr_sp_x_read)

        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.sp_x_read
        
    
    
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.read_attr_hardware


    # -------------------------------------------------------------------------
    #    Sweep_spectra_DLD command methods
    # -------------------------------------------------------------------------
    

    #----- PROTECTED REGION ID(Sweep_spectra_DLD.programmer_methods) ENABLED START -----#
    def change_scale(self):
        while True:
            if self.change_scale_trig==True and self.attr_Sample_V_min_read<self.attr_Sample_V_max_read:
                self.attr_sp_x_read=np.arange(start=self.attr_Sample_V_max_read, stop=self.attr_Sample_V_min_read-round(self.attr_Voltage_step_read,3), step=self.attr_Voltage_step_read)#=[0.0]*(int((self.attr_Sample_V_max_read-self.attr_Sample_V_min_read)/self.attr_Voltage_step_read+1))#np.delete(self.attr_sp_x_read,[1:],0)                
                self.attr_sp_y_read=[0.0]*len(self.attr_sp_x_read)
                
                self.stack=np.array([[[0.0]*self.tdc.read_attribute("Hist_Accu_XY").dim_x]*self.tdc.read_attribute("Hist_Accu_XY").dim_y]*len(self.attr_sp_x_read))
                self.stack[0,:,:]=np.array(self.tdc.read_attribute("Hist_Accu_XY").value,dtype=np.float32)
                #print self.stack.shape
                self.change_scale_trig=False
            time.sleep(1)
    def measure(self):
        while True:
            i=0
            while self.CmdTrig_sweep_Start==True:
                print "Start measurements"
                self.attr_Progress_read=round(100*i/len(self.attr_sp_x_read),3)
                self.tdc.write_attribute("ExposureAccu", self.attr_Exposure_read)
                self.sample.write_attribute("voltage_w",round(self.attr_sp_x_read[i],2))    
                while self.sample.read_attribute("voltage_r").value<self.attr_sp_x_read[i]-0.05 or self.sample.read_attribute("voltage_r").value>self.attr_sp_x_read[i]+0.05:
                    print "Delay!"
                    time.sleep(0.1)
                self.tdc.write_attribute("CmdTrig_Accumulation_Start",1)
                while self.tdc.read_attribute("Accumulation_Running").value==True:
                    print "Delay! Accumulation is running!"                    
                    time.sleep(0.1)
                time.sleep(0.2)
                self.attr_sp_y_read[i]=np.sum(self.tdc.read_attribute("Hist_Accu_T").value)
                i+=1
                if i==len(self.attr_sp_x_read):
                    self.CmdTrig_sweep_Start=False
                    self.attr_Progress_read=round(100*i/len(self.attr_sp_x_read),3)
                    i=0
                elif self.CmdTrig_sweep_Start==False:
                    self.tdc.write_attribute("CmdTrig_Accumulation_Stop",1)
                    i=0
            while self.CmdTrig_stack_Start==True:
                print "Start measurements"
                self.attr_Progress_read=round(100*i/len(self.attr_sp_x_read),3)
                self.tdc.write_attribute("ExposureAccu", self.attr_Exposure_read)
                self.sample.write_attribute("voltage_w",round(self.attr_sp_x_read[i],2))
                while self.sample.read_attribute("voltage_r").value<self.attr_sp_x_read[i]-0.05 or self.sample.read_attribute("voltage_r").value>self.attr_sp_x_read[i]+0.05:
                    print "Delay!"
                    time.sleep(0.1) 
                self.tdc.write_attribute("CmdTrig_Accumulation_Start",1)
                while self.tdc.read_attribute("Accumulation_Running").value==True:
                    print "Delay! Accumulation is running!"                    
                    time.sleep(0.1)
                self.stack[i,:,:]=np.array(self.tdc.read_attribute("Hist_Accu_XY").value,dtype=np.float32)
                i+=1

                if i==len(self.attr_sp_x_read):
                    self.CmdTrig_stack_Start=False
                    self.attr_Progress_read=round(100*i/len(self.attr_sp_x_read),3)
                    i=0
                    print 1
                elif self.CmdTrig_stack_Start==False:
                    self.tdc.write_attribute("CmdTrig_Accumulation_Stop",1)
                    i=0
                    print 2
            time.sleep(1)

    def SaveStack(self):
        now=time.strftime("%Y_%m_%d", time.gmtime())
        self.attr_Server_Save_Stack_Busy_read=True
        if self.Save_Directory=="" or self.Save_Filename=="":
            self.attr_measurements_error_read="Check file path!"
        else:
            dir_path=self.Save_Directory+"/"+now
            if os.path.isdir(dir_path)==False:
                os.mkdir(dir_path)
            else:
                file_path=dir_path+"/"+str(self.Save_Filecounter)+"_"+self.Save_Filename+".tiff"
                print (file_path)                
                if os.path.isfile(file_path)==False:
                    print self.stack.shape
                    imlist = []
                    for m in self.stack:
                        imlist.append(Image.fromarray(m))
                    imlist[0].save(file_path, compression="tiff_deflate", save_all=True, append_images=imlist[1:])
                    #im.save(file_path, compression="tiff_deflate", save_all=True)
                    #imsave(file_path, self.stack)#np.savetxt(file_path, np.c_[self.attr_sp_x_read, self.attr_sp_y_read])
                    self.file_counter=PyTango.DeviceProxy("sweep/spectra/ktof")
                    self.file_counter.write_attribute("Save_Filecounter",self.Save_Filecounter+1)
                elif self.CmdTrig_sweep_Start==True:
                    self.attr_measurements_error_read="Measurements in progress!"
                elif os.path.isfile(file_path)==True:
                    self.attr_measurements_error_read="File already exists!"
            
        self.attr_Server_Save_Stack_Busy_read=False

          
    def SaveSpectrum(self):
        now=time.strftime("%Y_%m_%d", time.gmtime())
        self.attr_Server_Save_File_Busy_read=True
        if self.Save_Directory=="" or self.Save_Filename=="":
            self.attr_measurements_error_read="Check file path!"
        else:
            dir_path=self.Save_Directory+"/"+now
            if os.path.isdir(dir_path)==False:
                os.mkdir(dir_path)
            else:
                file_path=dir_path+"/"+str(self.Save_Filecounter)+"_"+self.Save_Filename+".txt"
                print (file_path)                
                if os.path.isfile(file_path)==False:
                    np.savetxt(file_path, np.c_[self.attr_sp_x_read, self.attr_sp_y_read])
                    self.file_counter=PyTango.DeviceProxy("sweep/spectra/ktof")
                    self.file_counter.write_attribute("Save_Filecounter",self.Save_Filecounter+1)
                elif self.CmdTrig_sweep_Start==True:
                    self.attr_measurements_error_read="Measurements in progress!"
                elif os.path.isfile(file_path)==True:
                    self.attr_measurements_error_read="File already exists!"
            
        self.attr_Server_Save_File_Busy_read=False

                
    #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.programmer_methods

class Sweep_spectra_DLDClass(PyTango.DeviceClass):
    # -------- Add you global class variables here --------------------------
    #----- PROTECTED REGION ID(Sweep_spectra_DLD.global_class_variables) ENABLED START -----#
    
    #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.global_class_variables


    #    Class Properties
    class_property_list = {
        }


    #    Device Properties
    device_property_list = {
        }


    #    Command definitions
    cmd_list = {
        }


    #    Attribute definitions
    attr_list = {
        'Sample_V_min':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true"
            } ],
        'Voltage_step':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true"
            } ],
        'Sample_V_max':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true"
            } ],
        'Exposure':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE],
            {
                'Memorized':"true"
            } ],
        'measurements_error':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ]],
        'Save_Filecounter':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'Save_Directory':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'Save_Filename':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'CmdTrig_Save_spectrum':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE]],
        'Server_Save_File_Busy':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ]],
        'CmdTrig_sweep_Start':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE]],
        'CmdTrig_stack_Start':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE]],
        'CmdTrig_Save_stack':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE]],
        'Progress':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ]],
        'sp_y':
            [[PyTango.DevDouble,
            PyTango.SPECTRUM,
            PyTango.READ, 10000]],
        'sp_x':
            [[PyTango.DevDouble,
            PyTango.SPECTRUM,
            PyTango.READ, 10000]],
        }


def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(Sweep_spectra_DLDClass, Sweep_spectra_DLD, 'Sweep_spectra_DLD')
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.add_classes) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.add_classes

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed as e:
        print ('-------> Received a DevFailed exception:', e)
    except Exception as e:
        print ('-------> An unforeseen exception occured....', e)

if __name__ == '__main__':
    main()
