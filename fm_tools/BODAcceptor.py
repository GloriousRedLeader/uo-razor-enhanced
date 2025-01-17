# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-01-11
# Use at your own risk. 

from System.Collections.Generic import List
from System import Byte, Int32
from Scripts.fm_core.core_mobiles import get_yellows_in_range
from Scripts.fm_core.core_items import BOD_STATIC_ID
from Scripts.fm_core.core_items import BOD_BOOK_STATIC_ID
#from Scripts.fm_core.core_player import find_in_container_by_id


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
    
    bods = Items.FindAllByID(itemid = BOD_STATIC_ID,color = -1, container = Player.Backpack.Serial, range = 1)
    for bod in bods:
        bodBook = Items.FindByID(itemid = BOD_BOOK_STATIC_ID, color = bod.Hue, container = Player.Backpack.Serial, range = 3)
        if bodBook is not None:
            print("Moving {} to {}".format(bod.Name, bodBook.Name))
            Items.Move(bod.Serial, bodBook.Serial, 1)
            Misc.Pause(650)
    
