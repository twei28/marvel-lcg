from . import *

# * Alexei Shostakov
# Rescue the Shield — Action: Spend 1 resource of any type -> search your deck
#   and discard pile for Red Guardian's Shield and add it to your hand.
#   (Limit once per round).
#
# Le pendant alter-ego de « Shield Launch » : quand le bouclier a ete perdu
# (defausse), c'est ici qu'on va le rechercher. Modele : Clint Barton (04001b)
# pour le couple `Search.PlayerCard` + `SetCost(Cost("1"))`, Odinson (06001b)
# pour la limite par round.
#
# Le bouclier est une amelioration : `card_type=Upgrade` restreint la recherche
# et evite toute ambiguite de nom.
#
# NOTE : le texte de Kajislav ne dit pas « Shuffle your deck », contrairement
# aux cartes officielles equivalentes. `Search.PlayerCard` melange de toute
# facon (c'est `not_move=True` qui l'en empeche) ; on garde le comportement par
# defaut du moteur, identique a celui de toutes les autres recherches du jeu.


def GetAbilities() -> Sequence['Ability']:

    def rescue_the_shield(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        joueur = effect.GetInitiator()
        if joueur is None:
            return

        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            card_type=Upgrade,
            name=NOM_BOUCLIER,
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        (AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            rescue_the_shield,
        )
            .SetName("Rescue the Shield")
            .SetCost(Cost("1"))
            .LimitOncePerRound()),
    ]
