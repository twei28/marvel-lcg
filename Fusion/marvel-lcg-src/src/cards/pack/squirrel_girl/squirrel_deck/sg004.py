from . import *

# The Lookout
# Response: After The Lookout enters play, look at the top card of the
#   encounter deck.
#
# Capacite ajoutee le 28/08/2026 : cet ecureuil n'en avait aucune (il etait le
# « corps nu » du deck, 1 THW et rien d'autre). Le visuel finalise en porte
# desormais une, et c'est le visuel qui fait foi.
#
# Modeles officiels du meme effet : Redwing (lj020), un allie « Companion »
# — qui comme les ecureuils ne compte pas dans la limite d'allies et ne peut
# pas defendre — et Melinda May (50023) ; tous deux passent par
# `LookAtDeck("EncounterDeck", 1, effect)`.
#
# `PasDeDiscorde` comme sur les autres ecureuils : Discord in the Branches
# (sg020) rend blanches les capacites imprimees des SQUIRREL.


def GetAbilities() -> Sequence['Ability']:

    def reperer(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        if joueur is None:
            return
        joueur.LookAtDeck("EncounterDeck", 1, effect)

    return [
        *Ecureuil(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            reperer,
            conditions=[PasDeDiscorde],
        ),
    ]
