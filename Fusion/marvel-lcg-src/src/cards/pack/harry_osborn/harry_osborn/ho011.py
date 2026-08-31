from . import *

# * Goblin Glider — amelioration signature. EARTH-6160. TECH. VEHICLE. Cout 3.
# Green Goblin gets +1 ATK and gains the AERIAL trait.
# Hero Action: Exhaust Goblin Glider -> ready Green Goblin.
#
# Cartes de reference :
#  - +1 ATK et trait AERIAL en continu : an008 * Siri's Dress, meme
#    `GiveKeywordToAttached("You", attack=1, trait="AERIAL")` (le trait et le
#    bonus visent la meme cible, un seul appel) ;
#  - le redressement : 01034/an002 ne conviennent pas, le bon modele est le
#    couple `CostFunc.Exhaust("This")` + `Faces.ReadyAll([hero], effect)`
#    de an001a Frenzy (redressement d'identite) transpose en Hero Action.
#
# ⚠ Le trait AERIAL donne par le planeur active ho008 (2 menaces), ho010
# (confusion payante) et les cartes basiques a verrou AERIAL : c'est LA piece
# maitresse TECH du kit, et le [[AERIAL]] disparait si le planeur quitte le
# jeu (rien a scripter : GiveKeywordToAttached est continu par construction).

def GetAbilities() -> Sequence['Ability']:

    def ready_goblin(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        if hero is not None:
            Faces.ReadyAll([hero], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            attack=1,
            trait="AERIAL",
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ready_goblin
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
