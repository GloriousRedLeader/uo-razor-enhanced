# GRL DID NOT WRITE THIS.
# This beautiful script was written by someone else. Just storing it here for safekeeping.
# This is a good, very useful script.

from time import sleep
from datetime import datetime
import clr, time, sys, System

clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Data')

from System.Collections.Generic import List
from System import Byte
from System import Environment
from System.Drawing import Point, Color, Size
from System.Windows.Forms import (Application, Button, Form, BorderStyle, Label, FlatStyle, DataGridView,
 DataGridViewAutoSizeColumnsMode, DataGridViewSelectionMode, DataGridViewEditMode, RadioButton, GroupBox,
 TextBox, CheckBox, ProgressBar)
from System.Data import DataTable

import sys

def access(fname):
    rv = False
    try:
        with open(fname, 'r') as f:
            rv = True
    except:
        pass
    return rv


def getenv(name):
    rv = str(Environment.GetEnvironmentVariable(name))
    return rv


contents = []
Misc.SetSharedValue('run','False')
list= []
railcoords = []
moblist = [0x9999]
layers = ["RightHand","LeftHand","Shoes","Pants","Shirt","Head","Gloves","Ring","Neck","Waist",
"InnerTorso","Bracelet","MiddleTorso","Arms","Cloak","OuterTorso","OuterLegs","InnerLegs","Talisman"]
Misc.SetSharedValue('homeX','False')
Misc.SetSharedValue('homeY','False')
Misc.SetSharedValue('mobID','False')
BFilter = Items.Filter()
BFilter.RangeMax = 3
BFilter.OnGround = True
BFilter.Enabled = True
BFilter.Movable = True
#BFilter.Graphics = List[int]((0xA278, 0xA27F))
#BFilter.Graphics = List[int]((41592, 41599))
global wep

############################## rail recorder form  ##############################

class easyRails(Form):    
    list = []
    def __init__(self):
        self.Text = "Easy Rails"
        self.Width = 250
        self.Height = 225
        self.TopMost = True
       
        self.button = Button()
        self.button.Text = 'Add Coord'
        self.button.Width = 100
        self.button.Height = 40
        self.button.Location = Point(10, 10)
        self.button.Click += self.add
        
        self.button1 = Button()
        self.button1.Text = 'Del last Coord'
        self.button1.Width = 100
        self.button1.Height = 40
        self.button1.Location = Point(125, 10)
        self.button1.Click += self.delLast

        self.button2 = Button()
        self.button2.Text = 'Clear All'
        self.button2.Width = 100
        self.button2.Height = 40
        self.button2.Location = Point(125, 50)
        self.button2.Click += self.clear
        
        self.button3 = Button()
        self.button3.Text = 'Test Rail'
        self.button3.Width = 100
        self.button3.Height = 40
        self.button3.Location = Point(10, 50)
        self.button3.Click += self.test
        
        self.button4 = Button()
        self.button4.Text = 'INFO'
        self.button4.Width = 100
        self.button4.Height = 40
        self.button4.Location = Point(10, 90)
        self.button4.Click += self.info
        
        self.button5 = Button()
        self.button5.Text = 'SAVE'
        self.button5.Width = 75
        self.button5.Height = 30
        self.button5.Location = Point(135, 135)
        self.button5.BackColor = Color.FromArgb(10,225,10)
        self.button5.Click += self.makefile
        
        self.textbox = TextBox()
        if Misc.ReadSharedValue("railname"):
            self.textbox.Text = Misc.ReadSharedValue("railname")
        else:
            self.textbox.Text = "Rail_Name"
        self.textbox.Location = Point(10, 140)
        self.textbox.BackColor = Color.FromArgb(180,180,180)
        self.textbox.Width = 115
        
        self.Controls.Add(self.button)
        self.Controls.Add(self.button1)
        self.Controls.Add(self.button2)
        self.Controls.Add(self.button3)
        self.Controls.Add(self.button4)
        self.Controls.Add(self.button5)
        self.Controls.Add(self.textbox)
        
    def add(self, sender, event):
        list.append([(Player.Position.X),(Player.Position.Y)])        
        Misc.SendMessage('{} Total Coords'.format(len(list)))
                   
    def test(self, sender, event):
        if len(list) > 0:
            for l in list:
                go(l[0],l[1])
        else:
            Misc.SendMessage('You didnt set any Coords!',33)
            
    def delLast(self, sender, event):
        if len(list) > 0:
            del list[-1]
            Misc.SendMessage('{} Total Coords'.format(len(list)))
        else:
            Misc.SendMessage('The Coord list is Empty!',33)
            
    def clear(self, sender, event):
        list.Clear()
        Misc.SendMessage('Coord list Cleared',180)
        
    def info(self, sender, event):
        if len(list) > 0:
            Misc.SendMessage('{} Total Coords'.format(len(list)),75)
            Misc.SendMessage('Last Coords were {}'.format(list[-1]),180)
            Misc.SendMessage('Current Coords are {}'.format(str(Player.Position.X)) + ',' + (str(Player.Position.Y)),285)
        else:
            Misc.SendMessage('You didnt set any Coords!',33)
            Misc.SendMessage('Current Coords are {}'.format(str(Player.Position.X)) + ',' + (str(Player.Position.Y)),285)
            
    def makefile(self, sender, event):
        rail_file = "/".join([getenv('userprofile'), 'Documents', '{}.txt'.format(self.textbox.Text)])
        Misc.SendMessage('Saved {}.txt in Documents'.format(self.textbox.Text),30)            
        if access(rail_file):
            Misc.SendMessage('Saved {}.txt in Documents'.format(self.textbox.Text),30)            
        file = open(rail_file, 'w+')
        file.write(str(list))
        file.close()
        
form = easyRails()
Application.Run(form)