from Scripts.fm_core.core_rails import do_route, rails_stats, run_rail_loop_single
from Scripts.fm_core.core_routes import new_haven_noob_dungeon
from Scripts.fm_core.core_routes import new_haven_skeleton_town
from Scripts.fm_core.core_routes import deceipt_1
from Scripts.fm_core.core_routes import deceipt_1_full
from Scripts.fm_core.core_routes import deceipt_3_full
from Scripts.fm_core.core_routes import tortuga_champ_spawn

# Run a single route. The only required argument is a set of coordinates. You can get more fancy
# By providing runes for banks, vendors and of course the starting patth. It will attempt to recall
# to the bank and deposit items if you provide the runebook information - but that is buggy. I wouldn't
# recommend it.
run_rail_loop_single(
    # (Required) This is a list of coordinates to travel. See core_routes for a list of available, pre-defined routes.
	# You can generate your own using the rails tool. It's easy. Just load up the script in fm_tools/RailRecorder.py
	# and start adding points. Walk to a location, click add point. When you're done hit save. Open the file. It 
	# will contain a list of coordinates you can paste here. Your character will walk around like an idiot.
    path = deceipt_1_full,

    # (Optional) This is the runebook serial that contains our farm location rune.
    # Provide this if you also provide banking / vendor runebooks.
    pathRunebookSerial = None,
    
    # (Optional) The gump button for the recall / sacred journey spell (different per server)
    # See the recall() method for full explanation on how to get this. This should take
    # us to the start of the farming route (make sure it is close to first coord!)
    # Provide this if you also provide banking / vendor runebooks.
    pathRuneGumpButton = None,
    
    # (Optonal) Runebook containing location to our bank. This is optional, do not need it only 
    # if we want to deposit gold periodically.
    # Note: If you do not provide a rune back to the path, then it will just stop at the bank.
    bankRunebookSerial = None,
    
    # (Optional) Gump button for the recall / sacred journey spell in runebook that takes us
    # to the bank, see recall spell for info on how to get this.
    # Note: If you do not provide a rune back to the path, then it will just stop at the bank.
    bankRuneGumpButton = None,
    
    # (Optional) An array of tuples where (<runebook serial>, <gump button>)
    # Note: If you do not provide a rune back to the path, then it will just stop at the vendors.
    vendorRunebookSerialsAndGumpButtons = [],
    
    # If cleanup britain is available on your server you can set details below.
    cubRunebookSerial = None,
    
    # If cleanup britain is available on your server you can set details below.
    cubRuneGumpButton = None,

    # If cleanup britain is available on your server you can set details below.
    # This is a bag in your inventory, probably something from auto looter.
    # This script will transfer ALL items in this bag into the cub container,
    # so be carefuL!!!!!
    cubSourceContainerSerial = None,
    
    # If cleanup britain is available on your server you can set details below.
    # This is the serial of the chest in britain. Use inspector.
    cubDestinationContainerSerial = None,
    
    # Percent of weight we can hold. If we exceed this, go back to bank / vendors and offload.
    # Default is offload when 80% full.
    weightThreshold = 0.80,
    
    # Number of tiles to scan for nearby monsters. If you set this too high it will
    # try to find monsters through walls and in other maps and waste time.
    attackRange = 5,    
    
    # Number of seconds to allow before giving up when going from one coord to another.
    # Default is 3 seconds.
    pathFindingTimeoutSeconds = 5.0,
    
    # Give a little extra time to loot when a monster dies. This is useful. A nice value
    # is about 2000ms.
    autoLootBufferMs = 2000
)