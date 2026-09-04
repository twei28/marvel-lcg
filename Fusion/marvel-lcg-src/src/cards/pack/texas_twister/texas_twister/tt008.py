from . import *

# Spin It to the Left! — AMELIORATION, cout 2, [physical]. ROTATION. SUPERPOWER.
# Texas Twister gets +1 THW and +1 DEF.
# Forced Interrupt: When a [[ROTATION]] card enters play, discard this card.
# Forced Response: After you make a basic attack, discard this card.
#
# ⚠ LA PAIRE tt008 / tt009 EST UN CHOIX EXCLUSIF, ET C'EST TOUT L'INTERET.
# Les deux portent le trait ROTATION et se defaussent l'une l'autre : on ne
# peut jamais tourner a gauche ET a droite. Chacune interdit en plus le
# pouvoir de base qu'elle ne renforce pas — la gauche (CTR/DEF) meurt sur une
# ATTAQUE de base, la droite (ATQ/DEF) meurt sur un CONTRE de base.
#
# CARTES DE REFERENCE
#  - `06009` Mjolnir : `GiveKeywordToAttached`, bonus continu d'une
#    amelioration de heros.
#  - `14001a` Quicksilver : `AfterUnitUseBasicPower`, ici filtre sur le SEUL
#    pouvoir ATK.
#
# TEXTE CONTRE CODE
#  « When a ROTATION card ENTERS PLAY » -> `WhenCardWouldEnterPlay`, une
#    INTERRUPTION : la carte part AVANT que l'autre n'arrive. ⚠ Il faut
#    s'exclure soi-meme (`face is not this`), sinon l'amelioration se
#    defausserait a sa propre mise en jeu.
#  « After you make a BASIC ATTACK » -> `powers=["ATK"]` seulement. Ecrire les
#    trois pouvoirs rendrait la carte inutilisable des le premier contre.


def GetAbilities() -> Sequence['Ability']:

    def se_defausser(effect: 'Effect', message: 'Message2') -> None:
        Unused(message)
        Faces.DiscardAll([effect.this], effect)

    def ceder_la_place(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        """⚠ SE PROTEGER DE SOI-MEME, ET LE GARDE VA DANS L'OPERATION.

        `WhenCardWouldEnterPlay` (card_move.py:6) ne prend NI `conditions=`, ni
        rien d'equivalent, et `Ability` n'a PAS de methode `AddConditions` :
        le filtre doit donc etre ecrit ici. Sans lui, l'amelioration se
        defausserait a sa PROPRE entree en jeu et n'existerait jamais — le
        moteur avale l'anomalie, la carte se paierait pour rien.
        """
        carte = getattr(message, "trigger", None)
        if carte is None or carte is effect.this:
            return
        se_defausser(effect, message)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS),
            thwart=1,
            defense=1,
        ),
        AbilityFactory.WhenCardWouldEnterPlay(
            AbilityType.ForcedInterrupt,
            CardFinder(trait=TRAIT_ROTATION),
            ceder_la_place,
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            "You",
            se_defausser,
            powers=["ATK"],
        ),
    ]
