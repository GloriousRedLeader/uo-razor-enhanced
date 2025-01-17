# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2024-03-26
# Use at your own risk. 

from Scripts.fm_core.core_player import move_all_items_from_container
from Scripts.fm_core.core_mobiles import get_enemies
from Scripts.fm_core.core_spells import cast_until_works
from System.Collections.Generic import List 
from System import Byte, Int32
import sys
import time

# This stuff is used to detect keypresses like mouse for movement
import ctypes
from ctypes import wintypes
user32 = ctypes.WinDLL('user32', use_last_error=True)
user32.GetAsyncKeyState.restype = wintypes.SHORT
user32.GetAsyncKeyState.argtypes = [wintypes.INT]

# Globals. Put in a class one day.
CORE_LOOP_DELAY_MS = 650
#railsStartingGold = 0
railsStartingTime = 0
railsEarnedGold = 0
railsLastGold = 0

# Is right mouse button down (player moving)? Does NOT detect if player is moving
# via rails.
def is_player_moving():
    return user32.GetAsyncKeyState(0x02) & 0x8000

# Lifted this from the mining script. Returns the same thing as relative
# to player +1 based on direction. The relative function doesnt always
# work for some reason though Target.TargetExecuteRelative(Player.Serial, 1)
def get_tile_in_front(distance = 1):
    direction = Player.Direction
    playerX = Player.Position.X
    playerY = Player.Position.Y
    playerZ = Player.Position.Z
    
    if direction == 'Up':
        tileX = playerX - distance
        tileY = playerY - distance
        tileZ = playerZ
    elif direction == 'North':
        tileX = playerX
        tileY = playerY - distance
        tileZ = playerZ
    elif direction == 'Right':
        tileX = playerX + distance
        tileY = playerY - distance
        tileZ = playerZ
    elif direction == 'East':
        tileX = playerX + distance
        tileY = playerY
        tileZ = playerZ
    elif direction == 'Down':
        tileX = playerX + distance
        tileY = playerY + distance
        tileZ = playerZ
    elif direction == 'South':
        tileX = playerX
        tileY = playerY + distance
        tileZ = playerZ
    elif direction == 'Left':
        tileX = playerX - distance
        tileY = playerY + distance
        tileZ = playerZ
    elif direction == 'West':
        tileX = playerX - distance
        tileY = playerY
        tileZ = playerZ
    return tileX, tileY, tileZ

# Runs this many tiles forward according to player direction
# Not super useful, but helps with mining script or if you just
# want to go in a straight line.
def move(x):
    for _ in range(x):
        Player.Run(Player.Direction)
        Misc.Pause(200)

# Can potentially swap implementation to use this pathfinder:
# https://github.com/YulesRules/Ultima-Online-Razor-Enhanced-Pathfinding/blob/main/README.md
# The timeout value is in seconds. It is a float. 
def go_to_tile(x, y, timeoutSeconds = -1):
    if Player.Position.X == x and Player.Position.Y == y:
        return True
        
    start_time = time.time()
    route = PathFinding.Route() 
    route.X = x
    route.Y = y
    route.MaxRetry = 3
    route.IgnoreMobile = True
    route.Timeout = timeoutSeconds
    res = PathFinding.Go(route)
    
    total = "{:.2f}".format(time.time() - start_time)
    Misc.SendMessage("It took {} seconds to generate route ({})".format(total, res), 48)
    return res

# This method moves our character next to the x, y provided (not on top of it)
# the go_to_tile method is exact. This one takes a little bit more processing,
# and it is wonkie processing by the way, to find a tile adjacent to the target
# that is also closest along our path.
def go_to_adjacent_tile(x, y, timeoutSeconds = -1):

    start_time = time.time()
    path = PathFinding.GetPath(x, y, True)

    Misc.SendMessage("Timeout is {} and coords found {}".format(timeoutSeconds, len(path)))    
    if len(path) <= 2:
        Misc.SendMessage("Did not have to do any work we were already there", 48)
        return True

    # this is the secret to not standing on the monster and losing stamina
    # we are doing this because there is no way to directly interact with
    # a Tile object as it isnt exposed to python
    # In any case whats happening here is we are removing the last two entries
    # in the path which are the exact x, y (duplicated for some reason) so we stop
    # right in front of the tile
    path.RemoveAt(len(path) - 1)
    path.RemoveAt(len(path) - 1)

    res = PathFinding.RunPath(path, timeoutSeconds, useResync = False)
    
    total = "{:.2f}".format(time.time() - start_time)
    Misc.SendMessage("It took {} seconds to generate a route result of {}".format(total, res), 48)
    return res

# range is the number of tiles to search for monsters in each "sector"
# autoLootBufferMs is the time in MS to stand around like an idiot before moving
# on after a monster dies. Gives the auto looter a little bit of extra time to grab
# gold. 0 means its disabled and no wait.
# pathFindingTimeoutSeconds is a float that represents number of seconds before quitting
# on a path. It is a value passed to the pathfinding method. The Pathfinding algorithm 
# could go on for days. Instead of derping, just give up after this many seconds and 
# move on with your life.
def do_route(path, range = 6, autoLootBufferMs = 0, pathFindingTimeoutSeconds = 3.0):
    sectorId = 0
    for coord in path:
        sectorId = sectorId + 1
        serialsToExclude = []

        while True:
            rails_stats("report_head")
            
            if not go_to_tile(coord[0],coord[1], pathFindingTimeoutSeconds):
                Misc.SendMessage("Cant make it to target, aborting this coord", 38)
                break
            
            Player.HeadMessage(48, "Weve arrived at sector {}".format(sectorId))
            Misc.Pause(1000)
            
            #eligible = get_mobs_exclude_serials(range, True, serialsToExclude) 
            eligible = get_enemies(range, serialsToExclude) 

            if len(eligible) > 0:  
                Player.HeadMessage(48, "Found {} things to attack ({}) filtered".format(len(eligible), len(serialsToExclude)))    
                nearest = Mobiles.Select(eligible, 'Nearest')
                
                goToNearestAttempts = 3
                while Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=range:            
                    Mobiles.Message(nearest,68,"^ {} tiles ^".format(Player.DistanceTo(nearest)),False)
                    
                    res = go_to_tile(nearest.Position.X, nearest.Position.Y, pathFindingTimeoutSeconds)
                    #res = go_to_adjacent_tile(nearest.Position.X, nearest.Position.Y, pathFindingTimeoutSeconds)
                    
                    Misc.Pause(50)
                    
                    if res == False or (Player.DistanceTo(nearest) > 1 and goToNearestAttempts <= 0):
                        serialsToExclude.append(nearest.Serial)
                        Mobiles.Message(nearest,38,"^ {} tiles ^".format(Player.DistanceTo(nearest)),False)
                        Player.HeadMessage(38, "Giving up on this monster")
                        break
                    elif Player.DistanceTo(nearest) > 1:
                        goToNearestAttempts = goToNearestAttempts - 1
                        Mobiles.Message(nearest,28,"^ {} tiles ^".format(Player.DistanceTo(nearest)),False)
                        Player.HeadMessage(28, "Monster too far, attempt {}".format(goToNearestAttempts))
                    else:
                        pass
                    
                    Misc.Pause(250)
                        
                # Always pause for some amount because the world will end
                rails_stats("report_head")
                Misc.Pause(1000)
                
                # Pause a little longer if we are prioritizing gold so the auto looter can have a moment
                # dont do this in shitty places like deceipt.
                # The check for goToNearestAttempts is a general rule that tells us whether the monster
                # got away or not. It is more likely that there is loot and the monster is dead if attempts 
                # is greater than zero.
                if autoLootBufferMs > 0 and goToNearestAttempts > 0:
                    #Player.HeadMessage(48, "Pausing a little extra for more loot")
                    Misc.Pause(autoLootBufferMs)
            else:
                Player.HeadMessage(48, "Nothing left in sector")
                break
    Player.HeadMessage(48, "Done in this zone!")
    
    
# Goes to monsters in range. 
def defend(
    # range is the number of tiles to search for monsters in each "sector"
    range = 6, 
    
    # autoLootBufferMs is the time in MS to stand around like an idiot before moving
    autoLootBufferMs = 0, 
    
    # pathFindingTimeoutSeconds is a float that represents number of seconds before quitting
    # on a path. It is a value passed to the pathfinding method. The Pathfinding algorithm 
    # could go on for days. Instead of derping, just give up after this many seconds and 
    # move on with your life.
    pathFindingTimeoutSeconds = 3.0
):
    rails_stats("start")   
    
    while True:
        rails_stats("report_head")
        Misc.Pause(2000)
        
        eligible = get_enemies(range) 
        if len(eligible) > 0:  
            Player.HeadMessage(48, "Found {} things to attack".format(len(eligible)))    
            nearest = Mobiles.Select(eligible, 'Nearest')
            
            while Mobiles.FindBySerial(nearest.Serial) is not None and Player.DistanceTo(nearest)<=range:            
                Mobiles.Message(nearest,68,"^ {} tiles ^".format(Player.DistanceTo(nearest)),False)
                
                res = go_to_tile(nearest.Position.X, nearest.Position.Y, pathFindingTimeoutSeconds)
                
                Misc.Pause(250)
            
            # Pause a little longer if we are prioritizing gold so the auto looter can have a moment
            # dont do this in shitty places like deceipt.
            # The check for goToNearestAttempts is a general rule that tells us whether the monster
            # got away or not. It is more likely that there is loot and the monster is dead if attempts 
            # is greater than zero.
            if autoLootBufferMs > 0 and goToNearestAttempts > 0:
                Player.HeadMessage(48, "Pausing a little extra for more loot")
                Misc.Pause(autoLootBufferMs)
        else:
            Player.HeadMessage(48, "Nothing left in sector")
            Misc.Pause(1000)

# Crappy way of reporting gold per hour
def rails_stats(
    # clear | start | reset = setse initial values and times to 0
    # report_head = flashes data above player head
    # report = Prints message in journal
    option
):
    #global railsStartingGold
    global railsStartingTime
    global railsEarnedGold
    global railsLastGold
    if option == "clear" or option == "start" or option == "reset":
        #railsStartingGold = Player.Gold
        railsStartingTime = time.time()       
        railsEarnedGold = 0
        railsLastGold = Player.Gold
    #elif option == "report":
        #hours = (time.time() - railsStartingTime) / 60 / 60
        #hoursFormatted = "{:.2f}".format(hours)
        #earnedGold = Player.Gold - railsStartingGold
        #earnedGoldFormatted = "{:,}".format(earnedGold)
        #if hours == 0:
        #    goldPerHour = 0
        #else:
        #    goldPerHour = "{:,.2f}".format(earnedGold / hours)
        #Misc.SendMessage("Total hours: {} Earned Gold: {} Gold Per Hour: {}".format(hoursFormatted, earnedGoldFormatted, goldPerHour)) 
    elif option == "report_head" or option == "report":
        hours = (time.time() - railsStartingTime) / 60 / 60
        
        if  Player.Gold < railsLastGold:
            railsEarnedGold = railsEarnedGold + Player.Gold
            railsLastGold = Player.Gold
            print("< Earned Gold: {}".format(railsEarnedGold))
        elif railsLastGold != Player.Gold:
            railsEarnedGold = railsEarnedGold + Player.Gold - railsLastGold
            railsLastGold = Player.Gold
            print("!= Earned Gold: {}".format(railsEarnedGold))
            
        #earnedGold = Player.Gold - railsStartingGold
        #if Player.Gold - railsStartingGold < 0:
        #    railsEarnedGold = railsEarnedGold + Player.Gold
        #    railsStartingGold = 0
        #else:
        #    railsEarnedGold = railsEarnedGold + Player.Gold - railsStartingGold
        
        if hours == 0:
            goldPerHour = 0
        else:
            goldPerHour = "{:,.0f}".format(railsEarnedGold / hours)
        Player.HeadMessage(253, "[GPH: {}]".format(goldPerHour))    

# Run a single route. The only required argument is a set of coordinates. 
# You can find a list of coordinates predefined in fm_core/core_routes.py
def run_rail_loop_single(

    # (Required) This is a list of coordinates to travel. See core_routes for a list of available, pre-defined routes.
    # You can generate your own using the rails tool. It's easy. Just load up the script in fm_tools/RailRecorder.py
    # and start adding points. Walk to a location, click add point. When you're done hit save. Open the file. It 
    # will contain a list of coordinates you can paste here. Your character will walk around like an idiot.
    path = None,

    # (Required) Number of tiles to scan for nearby monsters. If you set this too high it will
    # try to find monsters through walls and in other maps and waste time.
    attackRange = 5,    
    
    # (Required) Number of seconds to allow before giving up when going from one coord to another.
    # Default is 3 seconds.
    pathFindingTimeoutSeconds = 5.0,
    
    # Give a little extra time to loot when a monster dies. This is useful. A nice value
    # is about 2000ms.
    autoLootBufferMs = 2000
):
    rails_stats("start")        

    while True:
        if Player.Weight < Player.MaxWeight - 40:
            do_route(path, range = attackRange, autoLootBufferMs = autoLootBufferMs, pathFindingTimeoutSeconds = pathFindingTimeoutSeconds)
            rails_stats("report")
        else:
            Player.HeadMessage(48, "Stopping because max weight reached")
            break