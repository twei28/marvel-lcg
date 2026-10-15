from . import *

# * M'lanz — SBIRE (paquet IMPOSTOR, face B). IMPOSTOR. REVEALED. SKRULL. 4 PV, SCH 1, ATQ 2.
# When Revealed: Heal all damage from M'lanz and put her into play engaged with you.
# [star] <b>Forced Interrupt</b>: When M'lanz attacks you, also resolve her attack against each other hero.
#
# Cartes de reference :
#  - « When Revealed: Heal all damage from X and put it into play engaged with you » : **`gambit 37034`** Psionic Shield
#    (`HealthUnits([unite], "All", effect)`) et **`sk098`** (le sbire engage le joueur qui revele) ; helper `SbireImpostor()`.
# ★ Forced Interrupt « When X attacks you, also resolve her attack against each other hero » : **`core 01130`** Whirlwind et
# **`sk162`** Angar the Screamer (meme texte : `WhenUnitAttackYou` + `message.AlsoResolveThisAttackTo`).
#
# ⚠ Mots-pieges : « heal ALL damage » (un allie retourne arrive blesse) ; « engaged with YOU » : le joueur qui revele
# (pour un allie retourne : celui qui le controlait avant, livret p. 16) ; la face sbire quitte le jeu vers la DEFAUSSE
# IMPOSTOR (livret p. 16, liaison `BindDiscardPile`).


def GetAbilities() -> Sequence['Ability']:
    def tous_les_heros(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.AlsoResolveThisAttackTo(Worlds.GetOnFieldHeroes(effect))

    return [
        *SbireImpostor(),
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", tous_les_heros),
    ]
