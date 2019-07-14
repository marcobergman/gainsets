#!/usr/bin/env python
import wx
import socket
from signalk import kjson
import time


PARAMETER_X="wind.direction"
PARAMETER_Y="wind.speed"
SIGNALK_IP="10.10.10.3"
SIGNALK_PORT=21311

class GainSet(wx.Frame):

    def __init__(self, parent, title):
        super(GainSet, self).__init__(parent, title = title, size=(900,500))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        def GetSignalkValue (name):
            connection = socket.create_connection((SIGNALK_IP, SIGNALK_PORT))
            request = {'method' : 'get', 'name' : name}
            print request
            connection.send(kjson.dumps(request)+'\n')
            line=connection.recv(1024)
            try:
                msg = kjson.loads(line.rstrip())
                value = msg[name]["value"]
            except:
                value = ""
            connection.close();
            return value

        def SetSignalkValue (name, value):
            # Write one value to signalk
            connection = socket.create_connection((SIGNALK_IP, SIGNALK_PORT))
            request = {'method' : 'set', 'name' : name, 'value' : value}
            print request
            connection.send(kjson.dumps(request)+'\n')
            connection.close();

        ap_pilot = GetSignalkValue ("ap.pilot") 
        print "ap_pilot = " + ap_pilot
        ap_prefix = "ap.pilot." + ap_pilot + "."
        ap_prefix = ap_prefix.replace("pilot..", "")
        print "ap_prefix = " + ap_prefix

        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(0,0)

        # Pointers to Current GainSet
        self.value_xp = 0
        self.value_yp = 0

        # to prevent suerfluous updates of signalk
        self.previous_p = ''
        self.previous_i = ''
        self.previous_d = ''

        ##
        ## Set up Statictext
        ##
        text1 = wx.StaticText(panel, label = "wind angle")
        sizer.Add(text1, pos = (0, 0), flag = wx.ALL, border = 3)
        text2 = wx.StaticText(panel, label = "boat speed")
        sizer.Add(text2, pos = (1, 0), flag = wx.ALL, border = 3)
        text3 = wx.StaticText(panel, label = "low")
        sizer.Add(text3, pos = (2, 2), flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        text4 = wx.StaticText(panel, label = "medium")
        sizer.Add(text4, pos = (2, 3), flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        text5 = wx.StaticText(panel, label = "high")
        sizer.Add(text5, pos = (2, 4), flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        text6 = wx.StaticText(panel, label = "close hauled")
        sizer.Add(text6, pos = (4, 0), flag = wx.ALL, border = 3)
        text7 = wx.StaticText(panel, label = "beam reach")
        sizer.Add(text7, pos = (5, 0), flag = wx.ALL, border = 3)
        text8 = wx.StaticText(panel, label = "broad reach")
        sizer.Add(text8, pos = (6, 0), flag = wx.ALL, border = 3)
        text9 = wx.StaticText(panel, label = "running")
        sizer.Add(text9, pos = (7, 0), flag = wx.ALL, border = 3)
        text10 = wx.StaticText(panel, label = "p")
        sizer.Add(text10, pos = (9, 0), flag = wx.ALL, border = 3)
        text11 = wx.StaticText(panel, label = "i")
        sizer.Add(text11, pos = (10, 0), flag = wx.ALL, border = 3)
        text12 = wx.StaticText(panel, label = "d")
        sizer.Add(text12, pos = (11, 0), flag = wx.ALL, border = 3)

        # Set up initial GainSets
        # For now, gainset data sits in label of StaticText. To be changed, of course.
        GainSet = {};
        for x in range(1,5):
            for y in range (1,4):
                GainSet[x,y] = wx.StaticText(panel, label = "?")
                sizer.Add(GainSet[x,y], pos = (x+3, y+1), flag = wx.ALL, border = 3)

        ##
        ## Setup up controls
        ##
        text_x = wx.SpinCtrl(panel, max=180)
        sizer.Add(text_x, pos = (0,1), flag = wx.EXPAND|wx.ALL)

        slider_x = wx.Slider(panel, id=wx.ID_ANY, value=0, minValue=0, maxValue=180,
         style=wx.SL_HORIZONTAL, size=wx.DefaultSize,
        validator=wx.DefaultValidator)
        sizer.Add(slider_x, pos = (0,2), flag = wx.EXPAND|wx.ALL)
        def OnChange_slider_x(event):
            text_x.SetValue(slider_x.GetValue());
            OnChange_xy(event)
        slider_x.Bind(wx.EVT_SCROLL, OnChange_slider_x)

        text_y = wx.SpinCtrl(panel, max=10)
        sizer.Add(text_y, pos = (1,1), flag = wx.EXPAND|wx.ALL)

        slider_y = wx.Slider(panel, id=wx.ID_ANY, value=0, minValue=0, maxValue=10,
         style=wx.SL_HORIZONTAL, size=wx.DefaultSize,
         validator=wx.DefaultValidator)
        sizer.Add(slider_y, pos = (1,2), flag = wx.EXPAND|wx.ALL)
        def OnChange_slider_y(event):
            text_y.SetValue(slider_y.GetValue());
            OnChange_xy(event)
        slider_y.Bind(wx.EVT_SCROLL, OnChange_slider_y)

        text_y1 = wx.TextCtrl(panel, value="2")
        sizer.Add(text_y1, pos = (3,2), flag = wx.EXPAND|wx.ALL)
        text_y2 = wx.TextCtrl(panel, value="4")
        sizer.Add(text_y2, pos = (3,3), flag = wx.EXPAND|wx.ALL)
        text_y3 = wx.TextCtrl(panel, value="6")
        sizer.Add(text_y3, pos = (3,4), flag = wx.EXPAND|wx.ALL)
        text_x1 = wx.TextCtrl(panel, value="60")
        sizer.Add(text_x1, pos = (4,1), flag = wx.EXPAND|wx.ALL)
        text_x2 = wx.TextCtrl(panel, value="135")
        sizer.Add(text_x2, pos = (5,1), flag = wx.EXPAND|wx.ALL)
        text_x3 = wx.TextCtrl(panel, value="165")
        sizer.Add(text_x3, pos = (6,1), flag = wx.EXPAND|wx.ALL)
        text_x4 = wx.TextCtrl(panel, value="180")
        sizer.Add(text_x4, pos = (7,1), flag = wx.EXPAND|wx.ALL)
        text_p = wx.TextCtrl(panel)
        sizer.Add(text_p, pos = (9,1), flag = wx.EXPAND|wx.ALL)
        text_i = wx.TextCtrl(panel)
        sizer.Add(text_i, pos = (10,1), flag = wx.EXPAND|wx.ALL)
        text_d = wx.TextCtrl(panel)
        sizer.Add(text_d, pos = (11,1), flag = wx.EXPAND|wx.ALL)

        ##
        ## Choosing the current GainSet
        ##
        def SetLabel(label, bold_flag):
            # Called from SetCurrentGainset()
            # Make LABEL (point of sail or High Medium Low) of current GainSet bold, and the others not
            label_label = label.GetLabel()
            if (bold_flag):
                label.SetLabelMarkup("<b>"+label_label+"</b>")
            else:
                label.SetLabelMarkup(label_label)

        def SetCurrentGainset():
            # Set LABELS bold or not
            # Called when x or y has changed
            SetLabel(text3, (self.value_yp == 1))
            SetLabel(text4, (self.value_yp == 2))
            SetLabel(text5, (self.value_yp == 3))
            SetLabel(text6, (self.value_xp == 1))
            SetLabel(text7, (self.value_xp == 2))
            SetLabel(text8, (self.value_xp == 3))
            SetLabel(text9, (self.value_xp == 4))

            # Make GAINSET ITSELF bold, and the others not. Set PID parameters in lower controls
            for x in range(1,5):
                for y in range (1,4):
                    GainSetLabel = GainSet[x,y].GetLabel()
                    if (x == self.value_xp and y == self.value_yp):
                        GainSet[x,y].SetLabelMarkup("<b>"+GainSetLabel+"</b>") # i.e., bold
                        if (GainSetLabel != "?"):
                            # Set PID parameters
                            text_p.SetValue(GainSetLabel.split(" ")[0].split("=")[1])
                            text_i.SetValue(GainSetLabel.split(" ")[1].split("=")[1])
                            text_d.SetValue(GainSetLabel.split(" ")[2].split("=")[1])
                        #else:
                            #text_p.SetValue("")
                            #text_i.SetValue("")
                            #text_d.SetValue("")
                    else:
                        GainSet[x,y].SetLabelMarkup(GainSetLabel) # i.e., not bold


        def OnChange_xy(event):
            old_value_xp = self.value_xp
            old_value_yp = self.value_yp

            value_x = int(text_x.GetValue())
            value_x1 = int(text_x1.GetValue())
            value_x2 = int(text_x2.GetValue())
            value_x3 = int(text_x3.GetValue())
            value_x4 = int(text_x4.GetValue())

            if 0 <= value_x <= value_x1:
                self.value_xp = 1
            if value_x1 < value_x <= value_x2:
                self.value_xp = 2
            if value_x2 < value_x <= value_x3:
                self.value_xp = 3
            if value_x3 < value_x <= value_x4:
                self.value_xp = 4

            value_y = int(text_y.GetValue())
            value_y1 = int(text_y1.GetValue())
            value_y2 = int(text_y2.GetValue())
            value_y3 = int(text_y3.GetValue())

            if 0 <= value_y <= value_y1:
                self.value_yp = 1
            if value_y1 < value_y <= value_y2:
                self.value_yp = 2
            if value_y2 < value_y <= value_y3:
                self.value_yp = 3

            if (self.value_xp != old_value_xp or self.value_yp != old_value_yp):
                SetCurrentGainset()

        self.Bind(wx.EVT_TEXT, OnChange_xy, text_x)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_y)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_x1)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_x2)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_x3)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_x4)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_y1)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_y2)
        self.Bind(wx.EVT_TEXT, OnChange_xy, text_y3)

        ##
        ## Changing the PID parameters
        ##
        def OnChange_pid(event):
            # If any of parameters P, I, D change, update the Current GainSet
            if (text_p.GetValue() != ""):
                GainSetLabel = "P=" + text_p.GetValue() + " I="+ text_i.GetValue() + " D=" + text_d.GetValue()
                GainSet[self.value_xp,self.value_yp].SetLabelMarkup("<b>"+GainSetLabel+"</b>")
                if (checkAutoWrite.IsChecked()):
                    WriteGainSet(0)
            else:
                GainSet[self.value_xp,self.value_yp].SetLabelMarkup("<b>?</b>")
        self.Bind(wx.EVT_TEXT, OnChange_pid, text_p)
        self.Bind(wx.EVT_TEXT, OnChange_pid, text_i)
        self.Bind(wx.EVT_TEXT, OnChange_pid, text_d)

        # When manually changing the parameters, disable AutoWrite
        def UncheckAutoWrite (event):
            checkAutoWrite.SetValue(False)
        text_p.Bind(wx.EVT_SET_FOCUS, UncheckAutoWrite);
        text_i.Bind(wx.EVT_SET_FOCUS, UncheckAutoWrite);
        text_d.Bind(wx.EVT_SET_FOCUS, UncheckAutoWrite);

        panel.SetSizerAndFit(sizer)

        def ReadParameters(event):
            x = GetSignalkValue (PARAMETER_X)
            y = GetSignalkValue (PARAMETER_Y)
            text_x.SetValue(x)
            text_y.SetValue(y)
            slider_x.SetValue(x)
            slider_y.SetValue(y)
            OnChange_xy(0)
            SetCurrentGainset()

        buttonReadParameters = wx.Button(panel, label = "ReadFromSystemK")
        sizer.Add(buttonReadParameters, pos = (0, 3),flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        buttonReadParameters.Bind(wx.EVT_BUTTON, ReadParameters)

        ##
        ## Write gainsets (PID parameters) to signalk: manually, by button press,
        ##  or automatically upon each selection change
        ##

        def WriteGainSet(event):
            # Write all current PID parameters to SystemK, only if changed
            if (text_p.GetValue() != ""):
                p=text_p.GetValue()
                i=text_i.GetValue()
                d=text_d.GetValue()
                if p != self.previous_p: SetSignalkValue (ap_prefix + 'P', p)
                if i != self.previous_i: SetSignalkValue (ap_prefix + 'I', i)
                if d != self.previous_d: SetSignalkValue (ap_prefix + 'D', d)
                self.previous_p = p
                self.previous_i = i
                self.previous_d = d
                # And when they have never been recorded as a GainSet, do it now
                GainSetLabel = "P=" + text_p.GetValue() + " I="+ text_i.GetValue() + " D=" + text_d.GetValue()
                GainSet[self.value_xp,self.value_yp].SetLabelMarkup("<b>"+GainSetLabel+"</b>")

        # The button
        buttonWrite = wx.Button(panel, label = "WriteToSystemK" )
        sizer.Add(buttonWrite, pos = (10, 3), flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        buttonWrite.Bind(wx.EVT_BUTTON, WriteGainSet)

        # The checkbox
        checkAutoWrite = wx.CheckBox(panel, label="Automatic")
        sizer.Add(checkAutoWrite, pos = (11, 3), flag = wx.ALIGN_CENTER|wx.ALL, border = 3)

        def ReadGainSet(event):
            # Read
            text_p.SetValue(str(GetSignalkValue (ap_prefix + "P")))
            text_i.SetValue(str(GetSignalkValue (ap_prefix + "I")))
            text_d.SetValue(str(GetSignalkValue (ap_prefix + "D")))

        buttonReadGainSet = wx.Button(panel, label = "ReadFromSystemK")
        sizer.Add(buttonReadGainSet, pos = (10, 4),flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        buttonReadGainSet.Bind(wx.EVT_BUTTON, ReadGainSet)

        ##
        ## Save to disk
        ##
        def SaveGainSets(event):
          # Save to disk
            GainSetData = {}
            for x in range(1,5):
                for y in range (1,4):
                    GainSetLabel = GainSet[x,y].GetLabel()
                    GainSetData[str(x) + ':' + str(y)] = GainSetLabel
            file = open('/home/pi/.openplotter/gainsets.conf', 'w')
            file.write(kjson.dumps(GainSetData)+'\n')
            file.close()

        # The Save button
        buttonSave = wx.Button(panel, label = "Save")
        sizer.Add(buttonSave, pos = (13, 4),flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        buttonSave.Bind(wx.EVT_BUTTON, SaveGainSets)


	def Action (event):
		SetSignalkValue ("servo.position", 1000)
		SetSignalkValue ("servo.position_command", 1500)

        # The ACTION button
	buttonAction = wx.Button(panel, label = "Action!")
        sizer.Add(buttonAction, pos = (11, 4),flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
	buttonAction.Bind(wx.EVT_BUTTON, Action)

        ##
        ## Load from disk
        ##
        def LoadGainSets(event):
            # Load from disk
            file = open('/home/pi/.openplotter/gainsets.conf')
            GainSetData = kjson.loads(file.readline())
            file.close()
            for name, value in GainSetData.items():
                x = name.split(":")[0]
                y = name.split(":")[1]
                GainSet[int(x),int(y)].SetLabel(value)
            buttonSave.Enable()
            OnChange_xy(0)
            SetCurrentGainset()

        # The Load button
        buttonLoad = wx.Button(panel, label = "Load")
        sizer.Add(buttonLoad, pos = (13, 3),flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        buttonLoad.Bind(wx.EVT_BUTTON, LoadGainSets)

        ##
        ## Read parameters x and y (i.c., wind angle and boat speed) from signal K,
        ##  both manually or automatically, each second
        ##

        # ReadParameter timer mechanism
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, ReadParameters, self.timer)

        checkAutoRead = wx.CheckBox(panel, label="Automatic")
        sizer.Add(checkAutoRead, pos = (1, 3), flag = wx.ALIGN_CENTER|wx.ALL, border = 3)
        checkAutoRead.Bind(wx.EVT_CHECKBOX, self.onToggle)

        sizer.AddGrowableCol(0)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableCol(4)

        OnChange_xy(0)

        buttonSave.Disable() # don't save until you've loaded something

    # Strangely enough, this had to be one level higher
    def onToggle(self, event):
      if self.timer.IsRunning():
          self.timer.Stop()
      else:
          self.timer.Start(1000)

    #

app = wx.App()
GainSet(None, title = 'GainSet concept')
app.MainLoop()

