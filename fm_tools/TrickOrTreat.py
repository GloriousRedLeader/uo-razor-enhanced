# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 
from System.Collections.Generic import List
from System import Byte, Int32

# Trick or treat event. Targets nearest yellow npc and does the needful.

# This is the most inefficient thing known to man. But it does 
# kind of work. If you feed to select a list of mobiles and exclude
# some of them based on a list of serials, this will do it.
# Noterieties:  blue = 1, green = 2, gray = 3, gray crim = 4, orange = 5, red = 6, yellow = 7
#def get_mobs_exclude_serials (range, checkLineOfSight = False, serialsToExclude = [], namesToExclude = []):
    

fil = Mobiles.Filter()
fil.Enabled = True
fil.RangeMax = 3
fil.Notorieties = List[Byte](bytes([7]))
fil.IsGhost = False
fil.Friend = False
fil.CheckLineOfSight = False
mobs = Mobiles.ApplyFilter(fil)

mob = Mobiles.Select(mobs,"Nearest")

if mob is not None:
    #Player.HeadMessage(38, "Targeting {}".format(mob.Name))
    Player.ChatSay("trick or treat")
    Target.WaitForTarget(4000, False)
    Target.TargetExecute(mob)