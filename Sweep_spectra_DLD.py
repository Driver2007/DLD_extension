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
import tifffile
from PIL import Image

import subprocess
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import pickle
import os.path
import os
SCOPES = ['https://www.googleapis.com/auth/drive']
from skimage import img_as_float, img_as_int
from apiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import zipfile

class internet_tools:
    def __init__(self):
        self.upload_progress=0.0
        self.download_link=""
    def upload_file_to_gdrive(self,filepath,filename):
        """upload zip file to google drive
        usage: self.upload_file_to_gdrive(path,filename)
        path - path to file
        filename - full file name
        
        to check upload progress - check variable self.upload_progress
        Note: file credentials in mandatory
        retuen: download link
        """
        self.upload_progress=0.0
        if not os.path.isfile(filepath):
            print ("path not found")
            return
        print ("continue upload")
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        service = build('drive', 'v3', credentials=creds)

                # Call the Drive v3 API
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if items:
            for item in items:
                 if filename==item['name']:
                    service.files().delete(fileId=item['id']).execute()
        media = MediaFileUpload(filepath, mimetype='image/tiff', chunksize=256*1024, resumable=True)

        file_metadata = {'name': filename}

        file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id')

        response = None
        while not response:
            status, response = file.next_chunk()
            if status:
                self.upload_progress=int(status.progress() * 100)
                #print (f"upload progres={self.upload_progress}%")
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        if items:
            for item in items:
                if filename==item['name']:
                    self.download_link="https://drive.google.com/file/d/" + item['id']+'/view'
        return self.download_link

    def send_email(self, filelink, email_address, make_screenshot=True):
        time.sleep(1)
        msg = MIMEMultipart()
        gmail_user = "pressure.uni.mainz@gmail.com"
        gmail_pwd = "pressureunimainz"
        FROM = "pressure.uni.mainz@gmail.com"
        TO = email_address     
        SUBJECT = "Microscope status"+str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        TEXT = ""
        TEXT+=("Link to downdload lat measured file "+ filelink)+"\n"
        if make_screenshot:
            screenshot_path="screenshot.png"
            subprocess.run(["scrot", screenshot_path])
            with open(screenshot_path, "rb") as file:
                part = MIMEApplication(file.read(),Name=os.path.basename(screenshot_path))
            msg.attach(part)
        msg.attach(MIMEText(TEXT))
        attempts=0
        while (os.system("ping -c 1 www.googleapis.com"))!=0:
            attempts+=1
            if attempts==10:
                return
            time.sleep(1)
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.ehlo()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, msg.as_string())
            print ('successfully sent the mail')
        except:
            print ("failed to send mail")
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
        del self.stack
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
        self.attr_Check_stack_Saved_read = False
        self.attr_Check_spectrum_Saved_read = False
        self.attr_Check_stack_NotSaved_read = False
        self.attr_Check_spectrum_NotSaved_read = False
        self.attr_energy_slice_read = 0.0
        self.attr_Check_scale_set_read = False
        self.attr_full_file_path_read = ""
        self.attr_upload_progress_read = 0
        self.attr_download_link_read = ""
        self.attr_sp_y_read = [0]
        self.attr_sp_x_read = [0.0]
        self.attr_image_to_show_read = [[0]]
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.init_device) ENABLED START -----#
        #self.sample=PyTango.DeviceProxy("set/sample/voltage")
        self.tdc=PyTango.DeviceProxy("ktof/tdc/tdc1")
        self.Save_Filecounter=0
        self.Save_Directory=""
        self.Save_Filename=""         
        self.steps=0
        self.resize_spectrum_trig=False
        self.CmdTrig_measure_Start=False
        self.change_scale_trig=False
        self.CmdTrig_stack_save=False
        self.CmdTrig_spectrum_save=False
        self.upload_running=False
        self.send_status=True
        self.manual_upload=False
        self.email_address=""
        now = datetime.datetime.now()
        self.nowhour=now.hour
        
        self.iseg=False
        self.srs=False
        
        self.attr_measurements_error_read="No error"
        #self.stack=np.array([[[0]]])
        self.slice_to_show=0
        self.show_slice_trg=False
        self.stop_measurements=False
        if not 'scale_thread' in dir(self):
            self.scale_thread = threading.Thread(target=self.change_scale)
            self.scale_thread.setDaemon(True)
            self.scale_thread.start()
        if not 'spectrum_thread' in dir(self):
            self.spectrum_thread = threading.Thread(target=self.measure)
            self.spectrum_thread.setDaemon(True)
            self.spectrum_thread.start()
        if not 'show_thread' in dir(self):
            self.show_thread = threading.Thread(target=self.show)
            self.show_thread.setDaemon(True)
            self.show_thread.start()
        if not 'big_brother_thread' in dir(self):
            self.big_brother_thread = threading.Thread(target=self.big_brother)
            self.big_brother_thread.setDaemon(True)
            self.big_brother_thread.start()
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
        self.Filename=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Save_Filename_write
        
    def write_CmdTrig_Save_spectrum(self, attr):
        self.debug_stream("In write_CmdTrig_Save_spectrum()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.CmdTrig_Save_spectrum_write) ENABLED START -----#
        self.CmdTrig_spectrum_save=True
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.CmdTrig_Save_spectrum_write
        
    def read_Server_Save_File_Busy(self, attr):
        self.debug_stream("In read_Server_Save_File_Busy()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Server_Save_File_Busy_read) ENABLED START -----#
        attr.set_value(self.attr_Server_Save_File_Busy_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Server_Save_File_Busy_read
        
    def write_CmdTrig_measure_Start(self, attr):
        self.debug_stream("In write_CmdTrig_measure_Start()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.CmdTrig_measure_Start_write) ENABLED START -----#
        self.CmdTrig_measure_Start=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.CmdTrig_measure_Start_write
        
    def write_CmdTrig_Save_stack(self, attr):
        self.debug_stream("In write_CmdTrig_Save_stack()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.CmdTrig_Save_stack_write) ENABLED START -----#
        self.CmdTrig_stack_save=True
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.CmdTrig_Save_stack_write
        
    def read_Progress(self, attr):
        self.debug_stream("In read_Progress()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Progress_read) ENABLED START -----#
        attr.set_value(self.attr_Progress_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Progress_read
        
    def read_Check_stack_Saved(self, attr):
        self.debug_stream("In read_Check_stack_Saved()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Check_stack_Saved_read) ENABLED START -----#
        attr.set_value(self.attr_Check_stack_Saved_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Check_stack_Saved_read
        
    def read_Check_spectrum_Saved(self, attr):
        self.debug_stream("In read_Check_spectrum_Saved()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Check_spectrum_Saved_read) ENABLED START -----#
        attr.set_value(self.attr_Check_spectrum_Saved_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Check_spectrum_Saved_read
        
    def read_Check_stack_NotSaved(self, attr):
        self.debug_stream("In read_Check_stack_NotSaved()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Check_stack_NotSaved_read) ENABLED START -----#
        attr.set_value(self.attr_Check_stack_NotSaved_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Check_stack_NotSaved_read
        
    def read_Check_spectrum_NotSaved(self, attr):
        self.debug_stream("In read_Check_spectrum_NotSaved()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Check_spectrum_NotSaved_read) ENABLED START -----#
        attr.set_value(self.attr_Check_spectrum_NotSaved_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Check_spectrum_NotSaved_read
        
    def read_energy_slice(self, attr):
        self.debug_stream("In read_energy_slice()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.energy_slice_read) ENABLED START -----#
        attr.set_value(self.attr_energy_slice_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.energy_slice_read
        
    def write_slice_counter(self, attr):
        self.debug_stream("In write_slice_counter()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.slice_counter_write) ENABLED START -----#
        self.slice_to_show=data
        self.show_slice_trg=True
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.slice_counter_write
        
    def read_Check_scale_set(self, attr):
        self.debug_stream("In read_Check_scale_set()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.Check_scale_set_read) ENABLED START -----#
        attr.set_value(self.attr_Check_scale_set_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.Check_scale_set_read
        
    def write_sample_iseg(self, attr):
        self.debug_stream("In write_sample_iseg()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.sample_iseg_write) ENABLED START -----#
        if data==True:
            self.iseg=True        
            PyTango.DeviceProxy("sweep/spectra/ktof").write_attribute("sample_srs",False)
            self.sample=PyTango.DeviceProxy("ktof/logic/lens1")
        else:
            self.iseg=False
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.sample_iseg_write
        
    def write_sample_srs(self, attr):
        self.debug_stream("In write_sample_srs()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.sample_srs_write) ENABLED START -----#
        if data==True:
            self.srs=True
            PyTango.DeviceProxy("sweep/spectra/ktof").write_attribute("sample_iseg",False)        
            self.sample=PyTango.DeviceProxy("srs/power/supply1")
        else:
            self.srs=False
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.sample_srs_write
        
    def read_full_file_path(self, attr):
        self.debug_stream("In read_full_file_path()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.full_file_path_read) ENABLED START -----#
        attr.set_value(self.attr_full_file_path_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.full_file_path_read
        
    def write_email_address(self, attr):
        self.debug_stream("In write_email_address()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.email_address_write) ENABLED START -----#
        self.email_address=data
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.email_address_write
        
    def read_upload_progress(self, attr):
        self.debug_stream("In read_upload_progress()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.upload_progress_read) ENABLED START -----#
        attr.set_value(self.attr_upload_progress_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.upload_progress_read
        
    def read_download_link(self, attr):
        self.debug_stream("In read_download_link()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.download_link_read) ENABLED START -----#
        attr.set_value(self.attr_download_link_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.download_link_read
        
    def write_send_email(self, attr):
        self.debug_stream("In write_send_email()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.send_email_write) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.send_email_write
        
    def write_manual_upload(self, attr):
        self.debug_stream("In write_manual_upload()")
        data = attr.get_write_value()
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.manual_upload_write) ENABLED START -----#
        self.manual_upload=True
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.manual_upload_write
        
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
        
    def read_image_to_show(self, attr):
        self.debug_stream("In read_image_to_show()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.image_to_show_read) ENABLED START -----#
        attr.set_value(self.attr_image_to_show_read)
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.image_to_show_read
        
    
    
            
    def read_attr_hardware(self, data):
        self.debug_stream("In read_attr_hardware()")
        #----- PROTECTED REGION ID(Sweep_spectra_DLD.read_attr_hardware) ENABLED START -----#
        
        #----- PROTECTED REGION END -----#	//	Sweep_spectra_DLD.read_attr_hardware


    # -------------------------------------------------------------------------
    #    Sweep_spectra_DLD command methods
    # -------------------------------------------------------------------------
    

    #----- PROTECTED REGION ID(Sweep_spectra_DLD.programmer_methods) ENABLED START -----#
    def big_brother(self):
        while True:
            if self.CmdTrig_measure_Start==True:
                now = datetime.datetime.now()
                if self.nowhour!=now.hour or self.manual_upload==True:
                    self.manual_upload=False
                    self.nowhour=now.hour
                    while os.path.isfile(self.attr_full_file_path_read)==False:
                        time.sleep(1)
                    while self.upload_running==True:
                        time.sleep(1)
                    self.upload()
            time.sleep(1)
            


    def show(self):
        while True:
            if self.show_slice_trg==True and (self.slice_to_show>=0 and self.slice_to_show<=len(self.attr_sp_x_read)):
                self.attr_image_to_show_read=self.stack[self.slice_to_show,:,:] 
                self.attr_energy_slice_read=self.attr_sp_x_read[self.slice_to_show]    
                self.show_slice_trg==False
                #print ("new slice")
            if self.show_slice_trg==True:
                self.show_slice_trg=False
            time.sleep(1)

    def change_scale(self):
        while True:
            if self.change_scale_trig==True and self.attr_Voltage_step_read!=0.0 and self.attr_Sample_V_min_read<self.attr_Sample_V_max_read:
                self.attr_sp_x_read=np.arange(start=self.attr_Sample_V_min_read, 
						stop=self.attr_Sample_V_max_read+round(self.attr_Voltage_step_read,3), 
						step=round(self.attr_Voltage_step_read,3), 
						dtype=np.float32)
                #print (self.attr_sp_x_read)                
                self.attr_sp_y_read=[0]*len(self.attr_sp_x_read)
                if self.tdc.state()==PyTango.DevState.ON:
                    self.attr_Check_scale_set_read=True
                    self.attr_Progress_read=0
                else:
                    self.attr_Check_scale_set_read=False
                    self.attr_measurements_error_read="Check TDC"
                self.change_scale_trig=False
            time.sleep(1)

    def measure(self):
        while True:
            i=len(self.attr_sp_x_read)-1#0                
            if self.CmdTrig_measure_Start==True:
                self.sweep_spectra=PyTango.DeviceProxy("sweep/spectra/ktof")
                self.sweep_spectra.write_attribute("Save_Filecounter",self.Save_Filecounter+1)
                self.attr_full_file_path_read=self.create_file_path()
            if self.attr_full_file_path_read=="":
                self.CmdTrig_measure_Start=False
            elif self.CmdTrig_measure_Start==True:                 
                while self.CmdTrig_measure_Start==True:                
                    self.attr_Check_stack_Saved_read=False
                    self.attr_Check_spectrum_Saved_read=False
                    self.attr_Check_stack_NotSaved_read=False
                    self.attr_Check_spectrum_NotSaved_read=False
                    self.attr_Server_Save_File_Busy_read=False
                    self.Check_File_Saved=2
                    if self.attr_Check_scale_set_read==False:
                        self.attr_measurements_error_read="Check scale"
                        self.CmdTrig_measure_Start=False
                        break                    
                    if self.sample.state()!=PyTango.DevState.ON:
                        self.attr_measurements_error_read="Check ISEG"
                        self.CmdTrig_measure_Start=False
                        break
                    if self.sample.read_attribute("Sample_VSetOn").value!=True:
                        self.attr_measurements_error_read="Check Sample potential"
                        self.CmdTrig_measure_Start=False                    
                        break
                    if self.tdc.state()!=PyTango.DevState.ON:
                        self.attr_measurements_error_read="Check TDC server"                    
                        self.CmdTrig_measure_Start=False
                        break
                    self.attr_measurements_error_read="Start measurements" 
                    self.attr_Progress_read=100-round(100*i/(len(self.attr_sp_x_read)-1),3)#round(100*i/len(self.attr_sp_x_read),3)
                    self.tdc.write_attribute("ExposureAccu", self.attr_Exposure_read)
                    self.sample.write_attribute("Sample_VUSet",round(self.attr_sp_x_read[i],3)) 
                    #self.sample.write_attribute("voltage_w",round(self.attr_sp_x_read[i],2))
                    dx=0.05
                    if self.srs==True:                        
                        dx=0.001
                    if self.iseg==True:
                        dx=0.05
                    while self.sample.read_attribute("Sample_VURead").value<self.attr_sp_x_read[i]-dx or self.sample.read_attribute("Sample_VURead").value>self.attr_sp_x_read[i]+dx:
                        #print "Delay!"
                        time.sleep(0.1)
                    self.tdc.write_attribute("CmdTrig_Accumulation_Start",1)
                    k=0.0
                    while self.tdc.read_attribute("Accumulation_Running").value==True:
                        #print "Delay! Accumulation is running!"
                        time.sleep(0.2)
                        k+=0.2
                        if k>3*self.attr_Exposure_read:
                            self.stop_measurements=True
                            break
                    if self.stop_measurements==True:
                        self.attr_measurements_error_read="Check TDC server"                    
                        self.CmdTrig_measure_Start=False
                        break
                    time.sleep(1)
                        
                    self.attr_sp_y_read[i]=np.sum(self.tdc.read_attribute("Hist_Accu_T").value)
                    if os.path.isfile(self.attr_full_file_path_read):
                        image = img_as_float(tifffile.imread(self.attr_full_file_path_read))
                        image=np.append(image, np.array(self.tdc.read_attribute("Hist_Accu_XY").value, dtype=np.float32)[np.newaxis , : , : ], axis=0)
                        tifffile.imwrite(self.attr_full_file_path_read, image, compress=6, photometric='minisblack')
                    else:
                        tifffile.imwrite(self.attr_full_file_path_read, np.array(self.tdc.read_attribute("Hist_Accu_XY").value, dtype=np.float32)[np.newaxis , : , : ], compress=6, photometric='minisblack')
                    now = datetime.datetime.now()
                    try:
                        if self.nowhour!=now.hour:
                            self.nowhour=now.hour
                            #a = zipfile.ZipFile(self.attr_full_file_path_read+'.zip', 'w', zipfile.ZIP_DEFLATED)
                            #a.write(self.attr_full_file_path_read)#self.Save_Directory_full,self.Save_Filename)
                            #a.close
                            it=internet_tools()
                            link=it.upload_file_to_gdrive(self.attr_full_file_path_read,self.Save_Filename)
                            it.send_email(link,"pressure.uni.mainz@gmail.com", True)
                    except:
                        pass
                    i-=1
                    if i<0:
                        self.CmdTrig_measure_Start=False
                        self.attr_Progress_read=100#-round(100*i/(len(self.attr_sp_x_read)-1),3)#round(100*i/len(self.attr_sp_x_read),3)
                        i=len(self.attr_sp_x_read)-1#0
                    elif self.CmdTrig_measure_Start==False:
                        self.tdc.write_attribute("CmdTrig_Accumulation_Stop",1)
                        i=len(self.attr_sp_x_read)-1#0
            time.sleep(1)

    def create_file_path(self):
        file_path=""
        now=time.strftime("%Y_%m_%d", time.gmtime())
        if self.Save_Directory=="" or self.Filename=="":
            self.attr_measurements_error_read="Check file path!"
            #print ("Check file path!")
            return file_path
        else:
            self.sweep_spectra=PyTango.DeviceProxy("sweep/spectra/ktof")
            self.Filename = self.Filename.replace('?', '_').replace('/','_').replace('(','_').replace(')','_').replace(':','_').replace(';','_')
            self.sweep_spectra.write_attribute("Save_Filename", self.Filename)
            dir_path=self.Save_Directory+"/"+now
            self.Save_Directory_full=dir_path
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            self.Save_Filename=str(self.Save_Filecounter)+"_"+self.Filename+".tiff"
            file_path=dir_path+"/"+self.Save_Filename
            #print (file_path)
            return file_path
    
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
        'CmdTrig_measure_Start':
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
        'Check_stack_Saved':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ]],
        'Check_spectrum_Saved':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ]],
        'Check_stack_NotSaved':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ]],
        'Check_spectrum_NotSaved':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ]],
        'energy_slice':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ]],
        'slice_counter':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true_without_hard_applied"
            } ],
        'Check_scale_set':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.READ]],
        'sample_iseg':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'sample_srs':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'full_file_path':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ]],
        'email_address':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'upload_progress':
            [[PyTango.DevLong,
            PyTango.SCALAR,
            PyTango.READ]],
        'download_link':
            [[PyTango.DevString,
            PyTango.SCALAR,
            PyTango.READ]],
        'send_email':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE],
            {
                'Memorized':"true"
            } ],
        'manual_upload':
            [[PyTango.DevBoolean,
            PyTango.SCALAR,
            PyTango.WRITE]],
        'sp_y':
            [[PyTango.DevLong64,
            PyTango.SPECTRUM,
            PyTango.READ, 10000]],
        'sp_x':
            [[PyTango.DevFloat,
            PyTango.SPECTRUM,
            PyTango.READ, 10000]],
        'image_to_show':
            [[PyTango.DevLong,
            PyTango.IMAGE,
            PyTango.READ, 2000, 2000]],
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
