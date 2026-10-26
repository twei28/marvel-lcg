from . import *
# * Bruce Wayne — ALTER EGO. « Bruce Wayne begins the game with a Deterrence deck » : BeginGameWithSetAside pose les 15 cartes de dissuasion
# de cote, MonterLeDeckDeDissuasion en fait choisir 8 au Setup (modele 09001b Doctor Strange, ip001b Iron Patriot : deck annexe).
# « Actually... a Trillionaire » — Action : reduce the cost of the next ARMOR/ITEM/LOCATION/TECH/VEHICLE/WEAPON card played this round by 1.
# (Limit once per round.) Modele : il001b (`Worlds.UpdateNextCardPlayCost`), le filtre par traits passe par `check_face_fn`.
TRAITS_COUTEUX = ("ARMOR", "ITEM", "LOCATION", "TECH", "VEHICLE", "WEAPON")
def GetAbilities() -> Sequence['Ability']:
    def trillionaire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        Worlds.UpdateNextCardPlayCost(
            joueur, -1, effect,
            finder=CardFinder(check_face_fn=lambda f: any(f.HasTrait(t) for t in TRAITS_COUTEUX)),
            in_this="Round",
        )
    return [
        AbilityFactory.BeginGameWithSetAside(IDS_DISSUASION, MonterLeDeckDeDissuasion),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, trillionaire).SetName("Actually... a Trillionaire").LimitOncePerRound(),
    ]
