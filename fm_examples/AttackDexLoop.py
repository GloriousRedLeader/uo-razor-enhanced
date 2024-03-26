from Scripts.fm_core.core_attack import run_dex_loop

Misc.SendMessage("Starting Dex Loop")

run_dex_loop(
    specialAbilityType = 3,
    specialAbilityDelayMs = 1000,
    useDiscord = 1,
    discordDelayMs = 10000,
    useConsecrateWeapon = 1,
    consecrateWeaponDelayMs = 10000,
    useDivineFury = 1,
    divineFuryDelayMs = 10000,
    useHonor = 0
)