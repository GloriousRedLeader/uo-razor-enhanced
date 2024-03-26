from Scripts.fm_core.core_mobiles import get_mobs_exclude_serials
from Scripts.fm_core.core_spells import cast_until_works
from System.Collections.Generic import List 
from System import Byte, Int32
import sys
import time

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
                Misc.SendMessage("Cant make it to target, aborting this rune", 38)
                break
            
            Player.HeadMessage(48, "Weve arrived at sector {}".format(sectorId))
            Misc.Pause(1000)
            
            eligible = get_mobs_exclude_serials(range, True, serialsToExclude) 

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
                    Player.HeadMessage(99, "Pausing a little extra 1s for more loot")
                    Misc.Pause(autoLootBufferMs)
            else:
                Player.HeadMessage(48, "Nothing left in sector")
                break
    Player.HeadMessage(48, "Done in this zone!")
    
# Main entry point into auto farming. Will recall to runes in different books,
# follow a path of coords assocaited with that rune, and kill stuff / loot stuff.
# Right now only works with sacred journey.
def ride_the_rails(

    # runebooks a List of constructs that contain these properties:
    #   runebook_serial: Serial for a runebook, e.g. 0x46FB3DF1
    #   attack_range: number of tiles to scan, smaller means smaller area, larger means more problems
    #   runes_enabled: 0-based index of runes in the runebook to use (must line up with index of paths)
    #   rune_paths: 3d array of coords. Index of outer array must line up with rune, e.g. rune 0 is equal
    #       to paths[0]
    runebooks, 
    
    # runebookBumpId = Open the bump inspector and get the gump id for yoru runebook, i think this 
    # differs per server for some reason, however it should be the same value for each runebook
    # on that server. Note this is different than runebook serial which IS unique per runebook.
    runebookGumpID, 
    
    # Run continuously or just once
    loopForever = True, 
    
    # autoLootBufferMs is just there in case we want to pause a little longer after a kill to
    # focus more on loot
    autoLootBufferMs = 0):
        
    rails_stats("start")
    rails_stats("report")
    
    cycles = 1
    while loopForever:
        Misc.SendMessage("Starting Cyle: {}".format(cycles))
        for runebook in runebooks:
            for i in runebook["runes_enabled"]:
                path = runebook["rune_paths"][i]

                Misc.SendMessage("Going to run rune {}".format(i))
                
                
                # Pause dex_loop so we can recall.
                #Misc.SetSharedValue("dex_loop_run", 0)
                #Misc.Pause(1000)
                
                #Misc.SetSharedValue("dex_loop_run", 0)
                #Misc.Pause(1000)
                
                
                # Stop Attack Loop so we can recall. There are just way too many
                # problems here to manage this. Theyll never know anyway.
                Misc.SetSharedValue("core_loops_enabled", 0)
                Misc.Pause(1000)
                
                def recall():
                    Journal.Clear()
                    Items.UseItem(runebook["runebook_serial"])
                    Gumps.WaitForGump(runebookGumpID, 3000)
                    if Journal.Search("Invalid Serial"):
                        Misc.SendMessage("Could not find runebook. If it is in a bag in your backpack, open the bag and it should work.", 38)
                        Player.HeadMessage(38, "Could not start auto bot, see sys message")
                        sys.exit()
                    Gumps.SendAction(runebookGumpID, (i * 10) + 7)
                
                cast_until_works(recall)                    
                #Misc.SendMessage("Trying to go", 123)
                #cast_until_works(lambda: Gumps.SendAction(runebookGumpID, (i * 10) + 7))
                #Gumps.SendAction(1431013363, (i * 10) + 7)
                Misc.Pause(3000)
                
                # Tell attack loop it can continue.
                Misc.SetSharedValue("core_loops_enabled", 1)
                
                
                
                #Misc.SendMessage("Starting Journey", 123)
                # Unpause dex_loop so we can kill stuff.
                #Misc.SetSharedValue("dex_loop_run", 1)
                
                do_route(path, runebook["attack_range"], 1000)
                rails_stats("report")
                
        cycles = cycles + 1
        

# Globals. Put in a class one day.
railsStartingGold = 0
railsStartingTime = 0

# Crappy way of reporting gold per hour
def rails_stats(option):
    global railsStartingGold
    global railsStartingTime
    if option == "clear" or option == "start" or option == "reset":
        railsStartingGold = Player.Gold
        railsStartingTime = time.time()       
    elif option == "report":
        hours = (time.time() - railsStartingTime) / 60 / 60
        hoursFormatted = "{:.2f}".format(hours)
        earnedGold = Player.Gold - railsStartingGold
        earnedGoldFormatted = "{:,}".format(earnedGold)
        if hours == 0:
            goldPerHour = 0
        else:
            goldPerHour = "{:,.2f}".format(earnedGold / hours)
        Misc.SendMessage("Total hours: {} Earned Gold: {} Gold Per Hour: {}".format(hoursFormatted, earnedGoldFormatted, goldPerHour)) 
    elif option == "report_head":
        hours = (time.time() - railsStartingTime) / 60 / 60
        earnedGold = Player.Gold - railsStartingGold
        if hours == 0:
            goldPerHour = 0
        else:
            goldPerHour = "{:,.0f}".format(earnedGold / hours)
        Player.HeadMessage(253, "[GPH: {}]".format(goldPerHour))         