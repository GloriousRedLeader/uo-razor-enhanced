from Scripts.core.core_mobiles import find_vendor_by_name

print("FINDING VENDOR")

vendor = find_vendor_by_name(vendorName = "Jess", range = 15)

if vendor != None:
    Mobiles.Message(vendor,78,"^ IM HERE ^",False)
    Mobiles.Message(vendor,48,"^ IM HERE ^",False)
    Mobiles.Message(vendor,28,"^ IM HERE ^",False)