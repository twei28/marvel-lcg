from . import *

# * Casey Jones — ALLIE, cout 3, [wild]. VIGILANTE. PV 2, CTR 2*, ATQ 2*.
# Response: After Casey Jones enters play, deal 1 damage to Raphael and each
#   minion engaged with you. Place 1 rage counter on Raphael.
#
# Valide en jeu : cas `tools/cas/tmnt_raphael.py` (voir .planning/todos/2026-10-16-raphael-gabarits-processus-carte.md).
#
# CARTES DE REFERENCE
#  - `ho002` / `01083` Mockingbird : `AfterCardEnterPlay(Response, "This", op)`
#    pour « After <allie> enters play ».
#  - `30001a` : pose de compteur par `Faces.PlaceCountersOn`.
#  - `cd005` / `vp003` : `this.DealDamage(liste, 1, effect)` sur une liste mixte.
#
# TEXTE CONTRE CODE
#  ⚠ « deal 1 damage to RAPHAEL AND EACH MINION ENGAGED WITH YOU » : un seul
#    effet, une liste de cibles : le heros ET les sbires engages AVEC CE
#    JOUEUR (pas tous les sbires du terrain, piege `each` de PROCESSUS-CARTE).
#    Les degats viennent de Casey, pas d'une attaque : Yaban Hito (`tr001a`,
#    « from an attack ») ne se declenche donc PAS.
#  ⚠ « Raphael » = l'IDENTITE (decision du 15/10/2026) : en forme civile aussi,
#    l'identite (Raph) subit le degat et recoit la rage (compteurs partages
#    par les deux faces).
#  ⚠ « Place 1 rage counter » : PAS de « (to a maximum of 3) » imprime ici
#    (decision du 15/10/2026) : `plafonne=False`, la rage peut depasser 3.
#  ⚠ ATQ « 2* » et CTR « 2* » : l'etoile creuse sous la valeur = 1 degat
#    consequent (RECETTES §5), contrairement a l'etoile d'un HEROS.
#  « Response » (pas « Hero Response ») : elle part aussi en forme civile.


def GetAbilities() -> Sequence['Ability']:

    def casey_arrive(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        cibles: List['CardFace'] = []
        identite = IdentiteDuJoueur(effect, joueur)
        if identite is not None:
            cibles.append(identite)
        for sbire in Worlds.GetOnFieldMinions(effect):
            if sbire.GetEngagedPlayer() == joueur:
                cibles.append(sbire)
        if cibles:
            this.DealDamage(cibles, 1, effect)

        PlacerRage(effect, joueur, plafonne=False)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            casey_arrive,
        ),
    ]
