from . import *

# * Peter Parker (face alter-ego) — CIVILIAN. PV 10, REC 4, main 6.
# Gumshoe — Action: Discard the top card of the encounter deck -> choose to
#   either tuck that card here (to a maximum of 3) or remove threat from a
#   scheme equal to the number of boost icons discarded.
#   (Limit once per round.)
#
# ⚠ « PETER PARKER » EST LE QUATRIEME DU DEPOT : `01001b` (Spider-Man
# officiel), `sr001b` (spider_man_rainy), `as001b` (armored_spidey) et
# `bt014`, un ALLIE du pack beast. Voir le `__init__.py` du set pour ce que
# cela coute a l'obligation `sn011`.
#
# ⚠ ET LE ZIP NUMEROTE LES DEUX FACES A L'ENVERS, comme tous les packs de
# Rainy : « 0.1 » est l'ALTER-EGO (Peter Parker), « 0.2 » le HEROS. Verifie
# sur les libelles imprimes ALTER-EGO / HERO, pas sur le nom de fichier.
#
# CARTES DE REFERENCE
#  - `15004` / `ho014` : `Worlds.DiscardEncounterTopCard(effect)`, qui rend la
#    carte defaussee, et `FacesCounter.CountTotalBoostIcons` pour ses icones.
#  - `ho009` : `CostFunc.Custom(None, fn)`, le cout arbitraire dont le `False`
#    bloque le paiement.
#  - `01151` Under Attack / `br007` : `ChooseAbilities` a deux branches.
#
# TEXTE CONTRE CODE
#  ⚠ LA FLECHE EST APRES « Discard the top card of the encounter deck » :
#    defausser est le COUT, le choix est l'effet. La difference se voit quand
#    le deck de rencontre est vide — le cout ne peut pas etre paye, et
#    l'Action n'est pas proposee du tout.
#  « CHOOSE TO EITHER ... OR ... » -> deux branches exclusives, pas les deux.
#    Le pilote prend la PREMIERE par defaut (RECETTES §2), les cas forcent
#    donc explicitement celle qu'ils mesurent.
#  ⚠ « tuck THAT card here » -> la carte qu'on vient de defausser, pas une
#    autre. Mot-piege « that » (`wd022`) : on garde la reference exacte rendue
#    par le cout, on ne va pas repecher « une carte » de la defausse.
#  « (to a maximum of 3) » -> plafond de la PILE, applique par
#    `GlisserSousIdentite`. Pile pleine, la branche « tuck » ne fait rien —
#    et c'est bien ce que dit la carte, qui ne propose pas de repli.
#  « equal to the number of boost icons DISCARDED » -> les icones de LA carte
#    defaussee, pas celles de la pile. C'est `sn014` qui compte la pile.
#  « (Limit once per ROUND.) » -> `.LimitOncePerRound()`.


def GetAbilities() -> Sequence['Ability']:

    def defausser_le_dessus(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        """Le COUT : « Discard the top card of the encounter deck »."""
        Unused(cibles)
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return False
        # « THAT card » : on garde la reference exacte pour le corps.
        setattr(effect, "_sn001b_carte_defaussee", face)
        return True

    def gumshoe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        defaussee = getattr(effect, "_sn001b_carte_defaussee", None)
        if defaussee is None:
            return

        def glisser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            GlisserSousIdentite(effect, [defaussee], joueur)

        def deblayer(cibles: Sequence['CardFace']) -> None:
            valeur = IconesDeBoost([defaussee])
            if valeur > 0:
                effect.this.RemoveThreatFromSchemes(cibles, valeur, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Tuck that card under your identity", glisser),
            AbilityFactory.ForChoiceAbility(
                "Remove threat equal to the boost icons discarded",
                deblayer).SetTarget(Scheme2),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            gumshoe,
        ).SetCostFunc(CostFunc.Custom(None, defausser_le_dessus))
        .LimitOncePerRound()
        .SetName("Gumshoe"),
    ]
