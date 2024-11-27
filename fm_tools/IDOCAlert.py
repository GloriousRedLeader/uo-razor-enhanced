# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from System.Collections.Generic import List
from System import Byte, Int32

from System.Collections.Generic import List
from System import Int32

class IDOCScanner(object):
    global signs
    ignore = []
    fil = None
    signs = List[Int32]((0x0BD2, 0x0B96, 0x0BA4, 0x0BA6, 0x0BA8, 0x0BAA, 
                        0x0BAC, 0x0BAE, 0x0BB0, 0x0BB4, 0x0BB6, 0x0BB8,
                        0x0BBA, 0x0BBC, 0x0BBE, 0x0BC0, 0x0BC2, 0x0BC4,
                        0x0BC6, 0x0BC8, 0x0BCA, 0x0BCC, 0x0BCE, 0x0BD0,
                        0x0BD2, 0x0BD4, 0x0BD6, 0x0BD8, 0x0BDA, 0x0BDC,
                        0x0BDE, 0x0BE0, 0x0BE2, 0x0BE4, 0x0BE6, 0x0BE8,
                        0x0BEA, 0x0BEC, 0x0BEE, 0x0BF0, 0x0BF2, 0x0BF4,
                        0x0BF6, 0x0BF8, 0x0BFA, 0x0BFC, 0x0BFE, 0x0C00,
                        0x0C02, 0x0C04, 0x0C06, 0x0C08, 0x0C0A, 0x0C0C,
                        0x0C0E, 0x0C0F, 0x0BB2))

    def __init__(self):
        self.fil = Items.Filter()
        self.fil.Enabled = True
        self.fil.OnGround = True
        self.fil.Movable = True
        self.fil.Graphics = signs
        self.fil.RangeMax = 30

    def Main(self):
        while True:
            Misc.Pause(100)
            items = Items.ApplyFilter(self.fil)
            for item in items:
                if item.Serial in self.ignore:
                    continue
                Items.WaitForProps(item, 3000)
                props = Items.GetPropStringList(item)
                if len(props) > 4:
                    condition = props[4].ToLower()
                    if "danger" in condition:
                        Misc.SendMessage("[House : IDOC found.]", 38)
                        Misc.SendMessage("[House : IDOC found.]", 38)
                        Misc.SendMessage("[House : IDOC found.]", 38)
                        Player.HeadMessage(38,"IDOC")
                        Player.HeadMessage(38,"IDOC")
                        Player.HeadMessage(38,"IDOC")
                        self.ignore.append(item.Serial)
                    elif "greatly" in condition:
                        Misc.SendMessage("[House : Greatly found.]", 38)
                        self.ignore.append(item.Serial)
                    elif "fairly" in condition:
                        #Misc.SendMessage("[House : Fairly found.]", 48)
                        self.ignore.append(item.Serial)
                    elif "somewhat" in condition:
                        #Misc.SendMessage("[House : Somewhat found.]", 48)
                        self.ignore.append(item.Serial)
                    elif "slightly" in condition:
                        #Misc.SendMessage("[House : Slightly found.]", 48)
                        self.ignore.append(item.Serial)
                    elif "new" in condition:
                        #Misc.SendMessage("[House : Like New found.]", 48)
                        self.ignore.append(item.Serial)
                    else:
                        Misc.NoOperation()
                else:
                    # Skip this item and add it to the ignore list to avoid repeated attempts
                    self.ignore.append(item.Serial)
                    Misc.SendMessage(f"Item {item.Serial} skipped due to insufficient properties.", 55)

Misc.SendMessage('Starting IDOC Scanner...' ,88)
IS = IDOCScanner()
IS.Main()