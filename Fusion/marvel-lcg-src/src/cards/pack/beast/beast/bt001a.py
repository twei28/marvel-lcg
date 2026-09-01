from . import *

# * Beast — heros. X-MEN. MUTANT. CTR 1 / ATQ 2 / DEF 3, MNG 5, 13 PV.
# Thick Skinned — Response: When you take 0 damage when defending, search for
#   any card in your deck or discard pile and place it in your hand.
#
# Cartes de reference :
#  - le declencheur « 0 degat en defendant » : la fabrique
#    `AfterUnitDefendAgainstAttack` porte DEJA le drapeau `take_no_damage`
#    (do_attack.py:288), et son message expose `taken_damage`. Aucune carte
#    officielle ne l'emploie sur une identite, mais le drapeau existe pour ca :
#    inutile de recompter les degats a la main.
#  - la recherche : 04001b * Clint Barton, « search your deck and discard pile
#    for Hawkeye's Bow and add it to your hand », soit
#    `Search.PlayerCard(effect, player, include_player_deck=True,
#    include_discard_pile=True, ...)` puis `player.GainCard(face, effect)`
#    (recette moteur §2). Comparable parce que les deux zones fouillees et la
#    destination (la main) sont les memes ; Beast ne pose simplement AUCUN
#    filtre la ou Clint Barton nomme sa carte.
#
# ⚠ « any card » : ni nom, ni trait, ni type. On ne passe donc aucun critere a
# `Search.PlayerCard` — mettre `card_type=...` par reflexe restreindrait la
# carte sans que le texte le demande.
#
# ⚠ « when DEFENDING » : le declencheur exige que Beast ait ete le defenseur
# declare, pas seulement qu'il ait encaisse 0. Encaisser 0 d'une attaque non
# defendue (grace a Toughness, par exemple) ne declenche rien : c'est
# `who_defense="You"` qui le garantit, la fabrique ne part que sur une vraie
# defense.
#
# ⚠ « take 0 damage » couvre AUSSI la defense qui absorbe tout par la DEF
# seule : avec DEF 3 imprime, une attaque a 3 ou moins declenche la capacite.
# C'est le coeur du personnage, pas un cas limite.

def GetAbilities() -> Sequence['Ability']:

    def thick_skinned(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.Response,
            "You",
            thick_skinned,
            take_no_damage=True,
        ).SetName("Thick Skinned"),
    ]
