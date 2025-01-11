# Razor Enhanced Scripts for Ultima Online by
#   GRL  
#   https://github.com/GloriousRedLeader/uo-razor-enhanced
#   2025-01-11
# Use at your own risk. 

from Scripts.fm_core.core_rails import do_route, rails_stats, run_rail_loop_single
from Scripts.fm_core.core_routes import new_haven_noob_dungeon

# Run a single route. The only required argument is a set of coordinates. 
# You can find a list of coordinates predefined in fm_core/core_routes.py
run_rail_loop_single(

    # (Required) This is a list of coordinates to travel. See core_routes for a list of available, pre-defined routes.
	# You can generate your own using the rails tool. It's easy. Just load up the script in fm_tools/RailRecorder.py
	# and start adding points. Walk to a location, click add point. When you're done hit save. Open the file. It 
	# will contain a list of coordinates you can paste here. Your character will walk around like an idiot.
    path = new_haven_noob_dungeon,
    
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