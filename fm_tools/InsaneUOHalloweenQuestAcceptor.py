
cnt = 0
while True:
    cnt = cnt + 1
    Mobiles.UseMobile(0x0000035E)
    Gumps.WaitForGump( 0x4c4c6db0,10000)
    Misc.Pause(500)
    Gumps.SendAction(0x4c4c6db0,7)
    Gumps.WaitForGump( 0x4c4c6db0,10000)

    GOOD_MOBS = ["100 Wraith", "100 Spectre", "100 Bogle", "100 Shade", "100 Ghoul"]

    gd = Gumps.GetGumpData(0x4c4c6db0)
    print(gd)
    found = 0
    for g in gd.gumpData:
        print(g)
        for gm in GOOD_MOBS:
            if gm == g:
                found = found + 1
                
    if found == 3:
        print("DONE GOT IT!")
        break
                
    Misc.Pause(500)
    print("FOUND", found)

print("Total count", cnt)
            
    
#for g in gd.stringList:
#    print(g)