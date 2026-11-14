from . import *

# Guard Assembles — TRAITRISE (Imperial Guard). 1 icone de boost.
# When Revealed: Discard cards from the encounter deck until you discard an IMPERIAL GUARD minion and reveal it.
#
# Cartes de reference :
#  - « Discard cards from the encounter deck until you discard a minion and reveal it » : `DefausserJusquAuSbireIG`
#    (imperial_guard/__init__.py), modele baxter_stockman `DefausserJusquAuSbire` + `Reveal` (tx009).
#
# ⚠ Mots-pieges : « until you discard an IMPERIAL GUARD MINION » (une traitrise ou un environnement IMPERIAL GUARD defausse en
# route ne s'arrete pas) ; « and reveal IT » = le sbire defausse ; aucun sbire dans le deck ni la defausse : rien (boucle bornee).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        sbire = DefausserJusquAuSbireIG(effect)
        if sbire is not None:
            sbire.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
