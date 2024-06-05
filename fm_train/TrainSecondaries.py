#------Vars

#arrange these in the order that you would like to train the skill.  Remove any if you do not want to train them.
#order = ["picking","detect", "taste","camp","hide","arms","item", "removetrap"]
#order = ["picking","detect", "taste","camp","hide","arms","item"]

order = ["camp"]
#order = ["taste"]

mainpack = Mobiles.FindBySerial( Player.Serial ).Backpack

#using picks in your backpack?  Script cannot detect if picks outside of backpack are missing
useOwnPicks = True

if "camp" in order:  
    kindlingId = 0x0DE1
    kindling = Items.FindByID(int(kindlingId),0,mainpack.Serial,-1,False)
    

if "item" in order or "arms" in order:
    weaponId = Target.PromptTarget("Target a weapon or armor")
    
if "taste" in order:
    foodId = Target.PromptTarget("Target a food")
    
if "picking" in order:
    lockedBox = Target.PromptTarget("Target training lockbox")
    
    lockPickId = 0x14FC
    lockPicks = Items.FindByID(int(lockPickId),0,mainpack.Serial,-1,False)
    
    if useOwnPicks == False:
        lockPicks = Target.PromptTarget("Target lockpicks")

        
longPause = 10500
shortPause = 1200


#----------


if "removetrap" in order:
    #----------Remove Trap heavily stolen from Pacho of Heritage server.  All credit goes to them.
    #   Increase this to see the gump getting solved, will make the puzzle time longer
    visual_delay = 1
    #   Lower this if you have a good connection.
    #   Will make the logs spam more with the message telling you to wait before using another skill
    timeout_delay = 1000
    from datetime import datetime

    trap_box = Target.PromptTarget("Target a circuit trap training kit")
    initial_skill = Player.GetRealSkillValue("Remove Trap")
    box_gump = 653724266
    box_gump = 1731444441
    up = 1
    right = 2
    down = 3
    left = 4
    messages = {
        "success":"You successfully disarm the trap!",
        "fail":"You fail to disarm the trap and reset it",
        "wait":"You must wait a few moments to use another skill"
    }
    run_data = {
        "coords": [0,0],
        "used_coords": [[0,0]],
        "size": 3,
        "good_steps": [],
        "incoming_dir": left,
        "last_dir": up,
        "successive_fails": 0,
        "time_started":datetime.now()
    }
    fails = 0
    runs = 1
    avg_reset_time = 0
    last_puzzle_time = 0

    #------------------end Remove Trap vars



def remTrap():
    global runs
    global fails
    global avg_reset_time
    global last_puzzle_time
    global run_data
    global visual_delay
    global timeout_delay
    global trap_box
    global initial_skill
    global box_gump
    global up
    global down
    global left
    global right
    global messages
    # Resets the system
    def reset(data):
        data["coords"] = [0,0]
        data["used_coords"] = [[0,0]]
        data["size"] = 3
        data["good_steps"] = []
        data["incoming_dir"] = left
        data["last_dir"] = up
        data["successive_fails"] = 0
        data["time_started"] = datetime.now()
        if Gumps.HasGump():
            Gumps.CloseGump(box_gump)
        
    #   Get the next dir
    def getNextDir(last_dir, incoming_dir, cur_coords, used_coords, size, cycle=0):
        # Prevents recursion from happening too much.  It shouldn't recalculate enough to go around
        if cycle > 3:
            Misc.SendMessage("Recursion too deep! Aborting recalculation...", 0x80)
            return last_dir
        next_dir = (last_dir)%4 + 1
        if (next_dir == incoming_dir) or (next_dir == left and cur_coords[0] == 0) or (next_dir == up and cur_coords[1] == 0) or (next_dir == right and cur_coords[0] == (size-1)) or (next_dir == down and cur_coords[1] == (size-1)):
            next_dir = getNextDir(next_dir, incoming_dir, cur_coords, used_coords, size, cycle + 1)
        displacement = getDisplacement(next_dir)
        new_coords = [cur_coords[0] + displacement[0], cur_coords[1] + displacement[1]]
        coords_traveled = False
        for coord in used_coords:
            if coord[0] == new_coords[0] and coord[1] == new_coords[1]:
                coords_traveled = True
                break
        if coords_traveled:
            next_dir = getNextDir(next_dir, incoming_dir, cur_coords, used_coords, size, cycle + 1)
        if (cur_coords[0] == (size-1) and next_dir == up) or (cur_coords[1] == (size-1)and next_dir == left) or (cur_coords[0] == 0 and next_dir == left) or (cur_coords[1] == 0 and next_dir == up):
            #Misc.SendMessage("Wrong way: " + dirStr(next_dir) + " Size: " + str(size) + " Coords: " + str(cur_coords), 0x80)
            next_dir = getNextDir(next_dir, incoming_dir, cur_coords, used_coords, size, cycle + 1)
        return next_dir
    def getDisplacement(dir):
        if dir == up:
            return [0, -1]
        elif dir == right:
            return [1, 0]
        elif dir == down:
            return [0, 1]
        elif dir == left:
            return [-1, 0]
        else:
            return [0, 0]
    def getReverseDir(dir):
        if dir == up:
            return down
        elif dir == right:
            return left
        elif dir == down:
            return up
        elif dir == left:
            return right
    def dirStr(dir):
        if dir == up:
            return "up"
        elif dir == right:
            return "right"
        elif dir == down:
            return "down"
        elif dir == left:
            return "left"
        else:
            return "unknown: " + str(dir)
    ###
    def expMovingAvg(new_val, cur_avg, n):
        return (new_val - cur_avg)*(2/float(n+1))+cur_avg
    ###
    #Actual program
    reset(run_data)
    Journal.Clear()
    while Player.GetRealSkillValue("Remove Trap") < Player.GetSkillCap("Remove Trap"):
        Target.Cancel()
        gains = Player.GetRealSkillValue("Remove Trap") - initial_skill
        #Misc.SendMessage("Skill: " + str("{0:.1f}".format(Player.GetRealSkillValue("Remove Trap"))) + " Skillgain since start: " + str("{0:.1f}".format(gains)), 0x60)
        #Misc.SendMessage("Runs: " + str(runs) + " Fails: " + str(fails), 0x80)
        #Misc.SendMessage(" Avg fails/run: " + str("{0:.1f}".format((0.0+fails)/runs), 0x80))
        #Misc.SendMessage(" Avg skillgain/run: " + str("{0:.1f}".format(gains/runs)), 0x80)
        #Misc.SendMessage(" Avg puzzle time: " + str(avg_reset_time), 0x80)
        Player.UseSkill("Remove Trap")
        Target.WaitForTarget(timeout_delay, False)
        while Journal.Search(messages["wait"]):
            Journal.Clear()
            Player.UseSkill("Remove Trap")
            Misc.Pause(visual_delay)
            Target.WaitForTarget(timeout_delay, False)
        Target.TargetExecute(trap_box)
        Gumps.WaitForGump(box_gump, timeout_delay)
        Misc.Pause(visual_delay)
        Journal.Clear()
        if not Gumps.HasGump():
            Target.Cancel()
            continue
        gump_data = Gumps.LastGumpRawData()
        # Count of grey points that are possible to traverse.  Used to get the board size instead of a skill level
        midpoint_count = gump_data.count("9720")
        # 3x3 has 7 midpoints
        if midpoint_count == 7:
            run_data["size"] = 3
        else:
            run_data["size"] = 4
        if run_data["size"] == 0:
            Misc.SendMessage("Puzzle size indeterminate, stopping script", 0x110)
            break
        Misc.SendMessage("Puzzle Size: " + str(run_data["size"]), 0x60)
        # Executes all known good steps for this box run
        Misc.SendMessage("Executing known steps: " + str(map(lambda x : dirStr(x), run_data["good_steps"])), 0x80)
        Misc.SendMessage("Used coords: " + str(run_data["used_coords"]), 0x80)
        for step in run_data["good_steps"]:
            Gumps.SendAction(box_gump, step)
            Gumps.WaitForGump(box_gump, timeout_delay)
            Misc.Pause(visual_delay)
            
        while not (Journal.Search(messages["success"]) or Journal.Search(messages["fail"])):
            run_data["next_dir"] = getNextDir(run_data["last_dir"], run_data["incoming_dir"], run_data["coords"], run_data["used_coords"], run_data["size"])
            Misc.SendMessage("Trying " + dirStr(run_data["next_dir"]) + ", previous try " + dirStr(run_data["last_dir"]) + ", came from " + dirStr(run_data["incoming_dir"]), 0x49)
            Gumps.SendAction(box_gump, run_data["next_dir"])
            Gumps.WaitForGump(box_gump, timeout_delay)
            run_data["last_dir"] = run_data["next_dir"]
            if Gumps.HasGump():
                displacement = getDisplacement(run_data["last_dir"])
                run_data["coords"] = [run_data["coords"][0] + displacement[0],run_data["coords"][1] + displacement[1]]
                run_data["good_steps"].append(run_data["last_dir"])
                run_data["used_coords"].append([run_data["coords"][0], run_data["coords"][1]])
                run_data["incoming_dir"] = getReverseDir(run_data["last_dir"])
                run_data["successive_fails"] = 0
                Misc.Pause(visual_delay)
            else:
                break
        if Journal.Search(messages["success"]):
            Misc.SendMessage("Succeeded", 0x39)
            runs = runs + 1
            last_puzzle_time = datetime.now() - run_data["time_started"]
            avg_reset_time = expMovingAvg(last_puzzle_time.total_seconds(), avg_reset_time, runs-1)
            Misc.SendMessage("Solve time: " + str(last_puzzle_time), 0x39)
            reset(run_data)
        elif Journal.Search(messages["fail"]):
            Misc.SendMessage("Failed", 0x39)
            run_data["successive_fails"] = run_data["successive_fails"]+1
            fails = fails + 1
            if run_data["successive_fails"] > 3:
                Misc.SendMessage("Too many successive fails, resetting...", 0x80)
                if Gumps.HasGump():
                    Gumps.CloseGump(box_gump)
                reset(run_data)
        else:
            Misc.SendMessage("Timed out", 0x39)
    Misc.SendMessage("Training complete!", 0x90)

def barker(skillName, initialSkill):
    
    gains = Player.GetRealSkillValue(skillName) - initialSkill
    gains = str("{0:.1f}".format(gains))
    skillValue = round(Player.GetRealSkillValue(skillName), 2)
    skillValue = str("{0:.1f}".format(skillValue))
    Misc.SendMessage("Skill: " + str(skillValue) +"\n" + "Skillgain since start: " + str(gains), 0x50)

def armsLore():
    skillName = "Arms Lore"
    initialSkill = Player.GetRealSkillValue(skillName)
    while Player.GetSkillCap(skillName) > Player.GetSkillValue(skillName):
        barker(skillName, initialSkill)
        Player.UseSkill(skillName)
        Target.WaitForTarget(shortPause, False)
        Target.TargetExecute(weaponId)
        Misc.Pause(shortPause)
    Misc.SendMessage("All done with " + str(Player.GetRealSkillValue(skillName)) + "!.", 0x60)

def itemId():
    skillName = "Item ID"
    initialSkill = Player.GetRealSkillValue(skillName)
    while Player.GetSkillCap(skillName) > Player.GetSkillValue(skillName):
        barker(skillName, initialSkill)
        Player.UseSkill(skillName)
        Target.WaitForTarget(shortPause, False)
        Target.TargetExecute(weaponId)
        Misc.Pause(shortPause)
    Misc.SendMessage("All done with " + str(Player.GetRealSkillValue(skillName)) + "!.", 0x60)

def tasteId():
    skillName = "Taste ID"
    initialSkill = Player.GetRealSkillValue(skillName)
    while Player.GetSkillCap(skillName) > Player.GetSkillValue(skillName):
        barker(skillName, initialSkill)
        Player.UseSkill(skillName)
        Target.WaitForTarget(shortPause, False)
        Target.TargetExecute(foodId)
        Misc.Pause(shortPause)    
    Misc.SendMessage("All done with " + str(Player.GetRealSkillValue(skillName)) + "!.", 0x60)

def detectHidden():  
    skillName = "Detect Hidden"
    initialSkill = Player.GetRealSkillValue(skillName)  
    while Player.GetSkillCap(skillName) > Player.GetSkillValue(skillName):
        barker(skillName, initialSkill)
        Player.UseSkill(skillName)
        Target.WaitForTarget(shortPause, False)
        Target.Self()
        Misc.Pause(shortPause)
    Misc.SendMessage("All done with " + str(Player.GetRealSkillValue(skillName)) + "!.", 0x60)

def hiding():   
    skillName = "Hiding"
    initialSkill = Player.GetRealSkillValue(skillName)
    while Player.GetSkillCap(skillName) > Player.GetSkillValue(skillName):
        barker(skillName, initialSkill)
        Player.UseSkill(skillName)
        Misc.Pause(longPause)
    Misc.SendMessage("All done with " + str(Player.GetRealSkillValue(skillName)) + "!.", 0x60)
    
def lockPicking():
    skillName = "Lockpicking"
    initialSkill = Player.GetRealSkillValue(skillName)
    while Player.GetSkillCap(skillName) > Player.GetSkillValue(skillName):
        barker(skillName, initialSkill)
        if useOwnPicks == True:
            lockPickCount = Items.BackpackCount(lockPickId,-1)
            if lockPickCount < 1:
                Misc.SendMessage("Ran out of lockpicks.  Moving on to next skill", 0x60)
                break
            
        Items.UseItem(lockedBox)
        Misc.Pause(shortPause)
        Items.UseItem(lockPicks)
        Target.WaitForTarget(shortPause, False)
        Target.TargetExecute(lockedBox)
        Misc.Pause(shortPause)
    
def camping():
    skillName = "camping"
    initialSkill = Player.GetRealSkillValue(skillName)
    while Player.GetSkillCap(skillName) > Player.GetSkillValue(skillName):
        barker(skillName, initialSkill)
        kindlingCount = Items.BackpackCount(kindlingId,-1)
        if kindlingCount < 1:
            Misc.SendMessage("Ran out of kindling.  Moving on to next skill", 0x60)
            break
        Items.UseItem(kindling)
        Misc.Pause(shortPause)


def main(skillList):
    for skill in skillList:
        if skill == "arms":
            armsLore()
        if skill == "item":
            itemId()
        if skill == "taste":
            tasteId()
        if skill == "detect":
            detectHidden()
        if skill == "hide":
            hiding()
        if skill == "removetrap":
            remTrap()
        if skill == "picking":
            lockPicking()
        if skill == "camp":
            camping()
            

main(order)
        