# This is an example of how to find a vendor in a sea of vendors.
# If the vendor is on your screen and within range it should be able to find
# it. Just provide the vendor name.
# When it finds the vendor text will appear above its head so you can find it.
from Scripts.core.core_mobiles import find_vendor_by_name

# Just replace this with your vendors name and walk around mashing this script. 
# 100k
VENDOR_NAME = "Minion"
VENDOR_NAME = "Dread Mongbat"
VENDOR_NAME = "Guy the Vendor"

# Search within this many tiles
VENDOR_RANGE = 15

vendor = find_vendor_by_name(vendorName = VENDOR_NAME, vendorRange = VENDOR_RANGE)

if vendor != None:
    for i in range(1, 3):
        Mobiles.Message(vendor,78,"^ IM HERE ^",False)
        Mobiles.Message(vendor,48,"^ IM HERE ^",False)
        Mobiles.Message(vendor,28,"^ IM HERE ^",False)
        Misc.Pause(1500)
else:
    Player.HeadMessage(28, "Could not find that vendor")