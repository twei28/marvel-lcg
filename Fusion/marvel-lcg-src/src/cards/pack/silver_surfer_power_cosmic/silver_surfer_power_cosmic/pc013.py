from . import *

# Cosmic Awareness — AMELIORATION. POWER COSMIC. PREPARATION. Cout 0,
# ressource [wild].
#
# Texte imprime : « Interrupt: When a minion engages a player, choose a
# PLANET → that minion arrives at that PLANET and is confused. Shuffle this
# card into your deck. (The minion is still engaged with that player while
# at the planet and after departing.) »
#
# CARTES DE REFERENCE
#  - `AbilityFactory.WhenMinionEngagePlayer(Interrupt, CardFinder(), None,
#    op)` : « when a minion engages A player » (n'importe lequel, pas
#    seulement vous).
#  - `GiveStatus` (modele `puzzle.py`/`bl005` modele indirect) : poser
#    Confused via `Faces.GiveStatus([cible], "Confused", effect)`.
#  - `Faces.ShuffleAllTo([this], joueur.player_deck, effect)` pour « shuffle
#    this card into your deck ».
#
# TEXTE CONTRE CODE
#  « the parenthese » n'est qu'un rappel de regle (l'engagement normal du
#    moteur n'est jamais modifie par ce pack : decision du 04/11/2026, un
#    ennemi a une planete reste engage mais inerte) : rien a coder de plus.
#  « IS CONFUSED » : statut officiel du moteur, pas le blocage maison de ce
#    pack — les deux cohabitent (le sbire ne peut de toute facon pas agir a
#    la planete, le Confused mord si jamais il en repart avant la fin du
#    round joueur suivant).


def GetAbilities() -> Sequence['Ability']:

    def cosmic_awareness(effect: 'Effect', message: 'Message.WhenMinionEngagePlayer') -> None:
        this = effect.this
        if not effect.targets:
            return
        minion = message.trigger
        planete = effect.targets[0]
        ArriverA(effect, minion, planete)
        Faces.GiveStatus([minion], "Confused", effect)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is not None:
            Faces.ShuffleAllTo([this], joueur.player_deck, effect)

    return [
        AbilityFactory.WhenMinionEngagePlayer(
            AbilityType.Interrupt,
            CardFinder(),
            None,
            cosmic_awareness,
        ).SetTarget(card_type=Support, trait="PLANET"),
    ]
