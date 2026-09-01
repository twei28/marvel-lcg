from . import *

# Throg and Loki — complot annexe nemesis. Boost 2, Hazard 1, Menace
#   2[per_hero] (tout dans `desc`).
# Alligator Loki can attack only Throg.
# When Revealed: If Throg is not in play, search the encounter deck and
#   discard pile for him and reveal him.
#
# Cartes de reference :
#  - 40168a Stryfe's Grasp : « X can attack only Y » ->
#    `UnitCannotAttackTarget(CardFinder(name=X), can_only_attack=CardFinder(
#    name=Y))` (do_attack.py:1011) ;
#  - an015 Back from Hel : `Search.EncounterCard(include_discard_pile=True)`
#    puis `face.Reveal(None, effect)` ;
#  - an011 : `WhenThisRevealed(None, op)` sur un complot annexe (`SchemeSide2`).
#
# ⚠ « THROG » designe ici le sbire NEMESIS al019 pour la recherche (il n'y a
# que lui dans le deck de rencontre) : `card_ids=["al019"]`. Pour la
# restriction d'attaque, `CardFinder(name="Throg")` couvre les deux Throgs :
# al002 est un sbire de JOUEUR, jamais attaquable par son maitre de toute
# facon, donc aucun effet de bord.
# ⚠ « If Throg is not in play » : `Worlds.FindCardOnField(card_ids=)`, sur
# tout le plateau (un Throg engage chez un autre joueur compte comme en jeu).
# ⚠ La restriction ne vise que l'attaque : Alligator Loki peut encore
# contrer et defendre. Et « attack » couvre les attaques d'evenement
# (Chomp! sur le vilain est refuse tant que le complot est en jeu) : c'est
# `CheckIfUnitCanBeAttackBy`, la porte que toute attaque franchit.

def GetAbilities() -> Sequence['Ability']:

    def throg_and_loki(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(SchemeSide2)
        Unused(this)
        joueur = message.GetToPlayer()

        if Worlds.FindCardOnField(effect, card_ids=["al019"]) is not None:
            return
        throg = Search.EncounterCard(
            effect,
            joueur,
            include_discard_pile=True,
            card_ids=["al019"],
        )
        if throg is not None:
            throg.Reveal(joueur, effect)

    return [
        *AbilityFactory.UnitCannotAttackTarget(
            CardFinder(name=NOM_HEROS),
            can_only_attack=CardFinder(name="Throg"),
        ),
        AbilityFactory.WhenThisRevealed(
            None,
            throg_and_loki,
        ),
    ]
