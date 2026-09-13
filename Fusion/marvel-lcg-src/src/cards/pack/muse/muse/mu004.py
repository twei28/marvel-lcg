from . import *

# Graffitied Streets — ENVIRONNEMENT. LOCATION. 1 icone de boost.
# Uses (3[per_hero] graffiti counters).
# Forced Interrupt: When you play a card with your identity's picture on it,
#   place 1 threat on the main scheme.
# Action: Exhaust a character you control → remove graffiti counters from here
#   equal to that character's THW. (Limit once per round per player.)
#
# CARTES DE REFERENCE
#  - `ih004` Asteroid Belt et `27174a` Public Outcry : l'environnement a
#    compteurs `Uses`. BASE AUTOMATIQUE au format `"N,nom"` — ici
#    `"3*,graffiti"`. Le moteur pose les compteurs a l'entree en jeu ET
#    DEFAUSSE LA CARTE quand le dernier part : c'est ainsi que l'environnement
#    se retire, il n'y a rien a scripter pour cela.
#  - `mu003` pour la meme fenetre « quand on joue une carte signature ».
#  - `an004` / `vp001a` pour `PlaceThreatOnSchemes("MainScheme", 1, effect)`.
#
# ⚠ Le compteur `graffiti` a ete DECLARE dans `CardFace.COUNTER` : sans lui,
# `IsCounter` refuse le nom et la carte tombe des la creation de la partie
# (lecon payee par `ih004`).
#
# TEXTE CONTRE CODE
#  ⚠ « When YOU play » ici, contre « when A PLAYER plays » sur `mu003` : les
#    deux cartes n'ont PAS la meme portee, et c'est imprime ainsi. Sur un
#    environnement, « vous » designe chaque joueur pour lui-meme — la menace se
#    pose donc a chaque carte signature, de qui que ce soit. `"AnyPlayer"` rend
#    exactement cela.
#  ⚠ « equal to that character's THW » : le CTR du personnage incline, pas le
#    sien a lui. Un allie a 1 de CTR retire 1 compteur ; un heros a 3 en retire
#    3. C'est la seule facon de vider la carte.
#  ⚠ « Exhaust a character YOU CONTROL » : le COUT (la fleche). Une carte deja
#    inclinee ne paie pas.
#  ⚠ « Limit once per round PER PLAYER » : `LimitOncePerRoundPerPlayer`, et
#    surtout pas `LimitOncePerRound` — a quatre joueurs la carte partirait
#    quatre fois plus lentement.
#  ⚠ « Action » NUE : jouable aussi en forme alter-ego, d'ou `AbilityType.Action`.


def GetAbilities() -> Sequence['Ability']:

    def taguer(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Environment)
        Unused(message)

        this.PlaceThreatOnSchemes("MainScheme", 1, effect)

    def effacer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        Unused(message)

        inclines = effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards
        if not inclines:
            return
        ctr = inclines[0].CastTo(Unit2).thwart
        if ctr > 0:
            Faces.RemoveCountersOn([this], ctr, 'graffiti', effect)

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.ForcedInterrupt,
            "AnyPlayer",
            None,
            taguer,
            conditions=[
                lambda effect, message:
                    PorteLImageDe(message.played_face, message.to_player)
            ],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            effacer,
        ).SetCostFunc(CostFunc.Exhaust("YouControlUnit"))
        .LimitOncePerRoundPerPlayer(),
    ]
