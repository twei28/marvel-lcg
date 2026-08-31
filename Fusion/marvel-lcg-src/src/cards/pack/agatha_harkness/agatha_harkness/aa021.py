from . import *

# Coven of Chaos — evenement d'aspect LEADERSHIP (carte bonus du pack).
# SPELL. Cout 1.
# Play only if your identity has the MYSTIC trait.
# Alter-Ego Action: Put a MYSTIC ally in any player's discard pile into play
#   under its owner's control.
#
# Cartes de reference (RECETTES) :
#  - la condition de jeu : ma024 * Noh-Varr's Ship, `.SetPlay(
#    only_if_your_identity_has_trait="MYSTIC")` ;
#  - la mise en jeu depuis une defausse : `face.PutIntoPlay(owner, effect)`
#    (faces.py:406, meme API que aa001b/aa014) — « under its OWNER's
#    control » : le proprietaire de la carte, pas le joueur qui lance le
#    sort (piege « you control » de l'etape 5, inverse ici).

def GetAbilities() -> Sequence['Ability']:

    def coven_of_chaos(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        for face in effect.targets:
            if face is None:
                continue
            owner = face.GetOwner()
            if isinstance(owner, Player):
                face.PutIntoPlay(owner, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            coven_of_chaos
        ).SetPlay(only_if_your_identity_has_trait="MYSTIC")
        .SetTarget(CardFinder(card_type=Ally, trait="MYSTIC"),
                   range=(1, 1), from_where=["PlayersDiscardPile"]),
    ]
