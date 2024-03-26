from Scripts.fm_core.core_pets import run_vet_loop

# Two Dogs
#petSerials = [0x005C14B6, 0x005C13B8]

# Crappy dog
#petSerials = [0x007B8E89]

# Just the good dog
petSerials = [0x007B83C9]

# Both
#petSerials = [0x007B83C9, 0x007B8E89]

run_vet_loop (
    petSerials,
    containerSerial = 0x4139FCCE,
    healthPercent = 95,
    bandageDelayMs = 1500,
    healSpellName = "Close Wounds"
)