from . import *

# * Leonardo's Other Katana — AMELIORATION signature, x1. KATANA. NINJA. WEAPON.
# Cout 1, [energy]. Restricted.
# Hero Action: Choose a friendly character and exhaust 2 [[KATANA]] upgrades
#   you control -> that character gets +1 to each of their basic powers until
#   the end of the round.
# (+ l'aptitude Hero Resource OCTROYEE par tl011 : aucun code ici, voir tl011.)
#
# Cartes de reference :
#  - `ls004` Lead The Charge : `face.GainUntilRoundEnd(effect, attack=1)` ;
#    la signature de `GainUntilRoundEnd` accepte attack/defense/scheme/thwart/
#    recover (face_action.py:427) ;
#  - `32045` / `34018` : `CostFunc.Exhaust(card_type=..., trait=..., range=...)` ;
#  - `ls007` : choix d'une face parmi `Worlds.GetOnFieldFriendlyCharacters`
#    via `joueur.AskChooseFace(...)` ;
#  - `tl011` pour la ressource.
#
# Mots-pieges :
#  - « EACH of their basic powers » : ATQ, CTR (thwart), DEF ET REC (recover).
#    `attack=1, thwart=1, defense=1, recover=1` ;
#  - « friendly character » : toute identite ou tout allie de TOUS les joueurs ;
#  - « exhaust 2 [[KATANA]] » : `range=(2, 2)` ; Other Katana EST un KATANA, elle
#    peut donc compter parmi les deux (lecture litterale) ;
#  - « until the END OF THE ROUND » : `GainUntilRoundEnd`, pas fin de phase ;
#  - la ressource wild de tl012 vient de l'octroi de tl011 (decision utilisateur
#    du 15/10/2026) : sans tl011 en jeu, tl012 n'a pas de ressource.


def GetAbilities() -> Sequence['Ability']:

    def other_katana(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        candidats = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if f is not None]
        if not candidats:
            return
        choisi = joueur.AskChooseFace(candidats, effect,
                                      prompt="Choose a friendly character")
        (choisi or candidats[0]).GainUntilRoundEnd(
            effect, attack=1, thwart=1, defense=1, recover=1)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            other_katana,
        ).SetCostFunc(CostFunc.Exhaust(card_type=Upgrade, trait="KATANA",
                                       from_where=["YouControlCards"],
                                       range=(2, 2))),
    ]
