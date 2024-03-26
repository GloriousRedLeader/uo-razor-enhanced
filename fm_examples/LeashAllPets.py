from Scripts.fm_core.core_pets import leash_pets

petSerials = [0x007B83C9, 0x007B8E89]

Player.HeadMessage(78, "Attempting to leash {} pets".format(len(petSerials)))

leash_pets(
    petSerials,
    containerSerial = 0x4139FCCE
)