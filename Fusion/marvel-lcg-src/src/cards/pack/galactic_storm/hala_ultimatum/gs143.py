from . import *

# * Hala — ENVIRONNEMENT, unique. LOCATION. PLANET.
# Enters play with 2 hideout counters, plus 2[per_hero] additional hideout counters.
# Scour the Planet — Action: Search the encounter deck and discard pile for a KREE minion and reveal it ->
#   draw 1 card. (Limit once per round per player.)
#
# Cartes de reference :
#  - « enters play with N, plus M[per_hero] additional » : composition non couverte par
#    `AbilityFactory.ThisEnterPlayWithCounters` (qui ne sait que « N » OU « N[per_hero] », pas une somme) :
#    calcul direct `2 + 2 * Worlds.GetPlayerNumIcon(effect)` + `Faces.PlaceCountersOn` (modele du moteur,
#    `game/ability/factory/counter.py`).
#  - « Action: search ... and reveal it -> draw 1 card », utilisable par n'importe quel joueur :
#    `AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, fn).AnyPlayerCanDoThis().LimitOncePerRoundPerPlayer()`
#    (modele `next_evol/next_evolution_campaign/40190b.py`).
#  - « search the encounter deck AND discard pile » : `ChercherEtReveleMinionKree(..., avec_defausse=True)`
#    (hala_ultimatum/__init__.py), contrairement a la recherche de mise en place de gs141a qui ne porte que
#    sur le deck.
#
# ⚠ Mots-pieges : « Limit once per round PER PLAYER » (pas une limite globale, piege recurrent du GUIDE §3) ;
# « plus 2[per_hero] ADDITIONAL » (s'ajoute aux 2 fixes, pas a leur place).


def GetAbilities() -> Sequence['Ability']:

    def entree_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        this = effect.this.CastTo(Environment)
        total = 2 + 2 * Worlds.GetPlayerNumIcon(effect)
        Faces.PlaceCountersOn([this], total, 'hideout', effect)

    def fouiller_la_planete(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        face = ChercherEtReveleMinionKree(effect, joueur, avec_defausse=True)
        if face is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", entree_en_jeu),
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, fouiller_la_planete)
            .SetName("Scour the Planet")
            .AnyPlayerCanDoThis()
            .LimitOncePerRoundPerPlayer()),
    ]
