# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-01-11
# Use at your own risk. 

from System.Collections.Generic import List
from System import Byte, Int32
from Scripts.fm_core.core_mobiles import get_yellows_in_range

# Looks up nearby npcs and attempts to accept BODs
while True:
    npcs = get_yellows_in_range(3)
    for npc in npcs:
        print("NPC {}".format(npc.Name))
        Misc.UseContextMenu(npc.Serial,"Bulk Order Info",3000)
        
        Misc.Pause(1000)
        gid = Gumps.CurrentGump()

        if gid is not None and gid != 0:
            Gumps.SendAction(gid, 1)
            print("gid {}".format(gid))
        else:
            print("No bods")
