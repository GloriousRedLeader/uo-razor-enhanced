from Scripts.fm_core.core_pets import run_vet_loop

# My pet serials. Swap these with yours. Use Razor Enhanced's "Inspect" button.
petSerials = [0x009895A7, 0x009895BE, 0x0098AAFC, 0x0098AAF9]

# This is the public API you should use when running a pet heal bot
# in the background. You will need to get your pet serials first. To do that
# use razor enhanced, go to scripts, and click the "Inspect" button at top right.
# Target your pet and it will display the serial. Done.
run_vet_loop (
    
    # An array of serials for your pets. You must provide this.
    # To get the serials you can use razor and press "Inspect Entities",
    # but really all of these programs have this feature and most clients
    # to too.
    petSerials = petSerials, 
    
    # Container where your bandages live. Defautls to player backpack. You can change
	# this to a different bag. Use Razor Enhanced and click "Inspect" to get your preferred
	# bag's serial.
    containerSerial = Player.Backpack, 
    
    # Only bandage things when their health is below this percent.
    healthPercent = 95, 
    
    # Wait this long in between bandage attempts. This is a dumb
    # program, it doesnt know when fingers slip, or even whether
    # fingers can slip bandaging an aneemal.
    bandageDelayMs = 8000,
    
    # Wait this long after rezzing a pet before doing anythign else,
    # otherwise it may start bandaging something else (bandage time is faster than rez time?)
    rezDelayMs = 3000,
    
    # Optionally provide a heal spell name if you really want to get serious
    # Currently will only use this if pet is < 50% health. Can have things like
    # "Greater Heal" or "Close Wounds".
    healSpellName = None
)