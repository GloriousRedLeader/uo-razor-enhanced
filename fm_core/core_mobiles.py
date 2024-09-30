# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from System.Collections.Generic import List
from System import Byte, Int32

# This was taken from the lumberjack script written by Credzba
# https://razorenhanced.net/dokuwiki/doku.php?id=resourcegatheringscripts
def range_mobile( mobile ):
    dist = math.sqrt( ((Player.Position.X - mobile.Position.X)**2) + ((Player.Position.Y - mobile.Position.Y)**2) )
    return dist

# This is the most inefficient thing known to man. But it does 
# kind of work. If you feed to select a list of mobiles and exclude
# some of them based on a list of serials, this will do it.
# Noterieties:  blue = 1, green = 2, gray = 3, gray crim = 4, orange = 5, red = 6, yellow = 7
def get_mobs_exclude_serials (range, checkLineOfSight = False, serialsToExclude = [], namesToExclude = []):
    fil = Mobiles.Filter()
    fil.Enabled = True
    fil.RangeMax = range
    fil.Notorieties = List[Byte](bytes([3,4,5,6]))
    fil.IsGhost = False
    fil.Friend = False
    fil.CheckLineOfSight = checkLineOfSight
    mobs = Mobiles.ApplyFilter(fil)
    
    #namesToExclude = ["omg arthur"]
    listValid = [m.Serial for m in mobs if m.Serial not in serialsToExclude and m.Name not in namesToExclude]
    #listValid = [m.Serial for m in mobs if m.Serial not in serialsToExclude]

    if len(listValid) == 0:
        return []

    fil = Mobiles.Filter()
    fil.Enabled = True
    for l in listValid:
        fil.Serials.Add(l)
    fil.RangeMax = range
    fil.Notorieties = List[Byte](bytes([3,4,5,6]))
    fil.IsGhost = False
    fil.Friend = False
    fil.CheckLineOfSight = checkLineOfSight

    mobs = Mobiles.ApplyFilter(fil)

    return mobs
    
# Find a vendor NPC by name and highlight. 
# The vendor name IS case sensitive, so a search for "john" will not match "John"
def find_vendor_by_name (vendorName, vendorRange = 10):
    fil = Mobiles.Filter()
    fil.Enabled = True
    fil.RangeMax = vendorRange
    fil.Notorieties = List[Byte](bytes([7]))
    fil.IsGhost = False
    fil.Friend = False
    fil.CheckLineOfSight = False
    mobs = Mobiles.ApplyFilter(fil)

    for m in mobs:
        if m.Name == vendorName:
            return m

    return None
