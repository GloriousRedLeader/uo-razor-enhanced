# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-12-17
# Use at your own risk. 

from System.Collections.Generic import List
from System import Byte, Int32

# InsaneUO Christmas Helper that will loot stockings

STOCKING_ID = 0x2BDC

while True:
    items = Items.FindAllByID(STOCKING_ID,-1, -1, 10, False)
    for item in items:
        print("Found stocking {}".format(item.Name))
        Misc.WaitForContext(item.Serial, 10000)
        Misc.ContextReply(item.Serial, 0)
        Misc.Pause(1000)    
    
    Misc.Pause(500)  