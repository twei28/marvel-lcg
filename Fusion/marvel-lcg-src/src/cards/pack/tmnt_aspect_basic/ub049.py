from . import *

# Snow and Shadow — EVENEMENT 2 [mental], aspect Basic (TMNT Aspects, Inkwire).
# Team-Up (Alopex and Nobody). Max 1 per deck.
# Hero Action: Ready Alopex and Nobody. Cloak a friendly character. Daze an enemy.
#
# NOUVELLE. Cartes de reference : 62023 (Team-Up + selecteurs supplementaires `SetTarget2/3`, cibles decalees) ;
# Team-Up : `effect.targets` = les deux personnages nommes (`HasTeamUp.GetTeamUpUnits`), qu'on redresse
# (`Faces.ReadyAll`). « Cloak » : fiche cloak.md (`GiveStatus(..., "Cloaked")`) ; « Daze » : fiche daze.md
# (`GiveStatus(..., "Dazed")`, un seul Dazed par personnage). Alopex = heros ta001, Nobody = allie ta002.
# TEXTE CONTRE CODE : « Ready Alopex AND Nobody » (les deux) ; « Cloak A friendly character » (au choix,
#   pas forcement l'un des deux) ; « Daze AN ENEMY ».


def GetAbilities() -> Sequence['Ability']:

    def snow_and_shadow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.ReadyAll([t for t in effect.targets if t is not None], effect)
        Faces.GiveStatus(effect.targets2, "Cloaked", effect)
        Faces.GiveStatus(effect.targets3, "Dazed", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, snow_and_shadow)
        .SetPlay().SetLabel()
        .SetTarget("TeamUp")
        .SetTarget2(Friend, range=(1, 1))
        .SetTarget3(Enemy, range=(1, 1)),
    ]
