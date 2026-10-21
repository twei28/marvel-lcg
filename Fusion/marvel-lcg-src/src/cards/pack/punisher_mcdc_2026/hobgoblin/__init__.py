from cards.pack import *

# Set Hobgoblin (pack MC×DC 2026 « La ville ne dort jamais »).
#
# « PUMPKIN BOMB » : l'aptitude commune du set, imprimee sur Hobgoblin's Glider (pu073) :
#   Special : Discard a card from the encounter deck. If that card is a :
#     - Treachery : place 1 threat on the main scheme.
#     - Minion or side scheme : take 1 indirect damage.
#     - Other : discard 3 cards from the encounter deck.
# Tout le set dit « resolve the "Pumpkin Bomb" ability » (une, deux ou trois fois) : ce module en fait UNE
# fonction, `PumpkinBomb`, et `ResoudrePumpkinBomb` la repete. Le Glider l'expose aussi comme aptitude Special
# nommee (`WhenResolveSpecialAbility(...).SetName("Pumpkin Bomb")`, modele sm/sinister_six/27100b.py).
#
# Cartes de reference : `Worlds.DiscardEncounterCards(n, effect)` (renvoie les cartes defaussees),
# `PlaceThreatOnSchemes`, `TakeIndirectDamage` sur l'identite (fne/the_getaway/60133.py).
#
# ⚠ « Take 1 indirect damage » : le JOUEUR qui resout (celui qui est attaque, qui revele, qui subit...). Pas de
# carte a defausser (deck vide) : rien ne se passe, pas de remelange.

def PumpkinBomb(effect: 'Effect', joueur: 'Player') -> None:
    cartes = Worlds.DiscardEncounterCards(1, effect)
    if not cartes:
        return
    carte = cartes[0]
    if Treachery.IsType(carte):
        schemes = Worlds.GetMainSchemes(effect)
        if schemes:
            effect.this.PlaceThreatOnSchemes(schemes[:1], 1, effect)
    elif Minion.IsType(carte) or EncounterSideScheme.IsType(carte):
        joueur.GetIdentity().TakeIndirectDamage(effect.this, 1, effect)
    else:
        Worlds.DiscardEncounterCards(3, effect)


def ResoudrePumpkinBomb(effect: 'Effect', joueur: 'Player', fois: int=1) -> None:
    for _ in range(fois):
        if effect.world.is_game_over:
            return
        PumpkinBomb(effect, joueur)


def TrouverHobgoblin(effect: 'Effect') -> 'Villain|None':
    for v in Worlds.GetVillains(effect):
        if v.paper.name.strip("* ") == "Hobgoblin":
            return v
    return None
