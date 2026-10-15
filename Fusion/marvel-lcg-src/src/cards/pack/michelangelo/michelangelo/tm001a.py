from . import *

# * Michelangelo (face heros) — NINJA. TURTLE.
# THW 1 / ATQ 1 / DEF 2 — HS 5 / PV 11
# Booyakasha — Response: After you use a basic power (THW, ATK, or DEF), move
#   up to 3 threat from one scheme to another scheme. You cannot move threat
#   onto a side scheme with 5[per_hero] or more threat on it.
#
# Cartes de reference :
#  - declencheur : `ls001a` (Valiant Warrior, lady_sif) et `04032` :
#    `AfterUnitUseBasicPower(Response, "You", op)`, `powers=None` = les TROIS
#    pouvoirs de base (RECETTES-MOTEUR §1) ;
#  - cible porte par L'ABILITE (`SetTarget(Scheme2, has_threat=True)`) pour la
#    manigance SOURCE : une seule question au joueur (lecon ls001a, autoplay
#    bloque avec deux questions) ;
#  - deplacement : `Scheme.MoveThreat(n, effect, [cible])`
#    (game/card/face/base/scheme.py:155), seul precedent : `34021` Storm ;
#  - nombre « jusqu'a 3 » : `Player.DeclareNumber(min, max)`, modele `dt102`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a basic power (THW, ATK, or DEF) » : trois pouvoirs, REC exclu.
#  - « from ONE scheme to ANOTHER scheme » : deux manigances DIFFERENTES, la
#    source peut etre la principale ou une annexe, la destination aussi.
#  - « 5[per_hero] or more » : 5 x nombre de heros (`Worlds.GetPlayerNumIcon`),
#    teste SUR LA DESTINATION AVANT le deplacement. La manigance principale
#    n'est jamais concernee (« a side scheme »).
#  - « up to 3 » : plafonne aussi par la menace presente sur la source. Le
#    minimum propose est 1 (0 serait « ne rien faire », la Response est deja
#    declinable).
#  - `MoveThreat` retire par `RemoveThreatInternal` : une annexe videe est
#    VAINCUE par le moteur (comme un retrait normal), et Crise ne bloque pas
#    ce chemin. # TODO-QUESTION (voir .planning/tmnt/michelangelo-phase-a.md,
#    question 3).
#  - Le libelle n'est PAS `thwart` : deplacer n'est pas retirer.

def GetAbilities() -> Sequence['Ability']:

    def booyakasha(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        source = effect.targets[0] if effect.targets else None
        if source is None or source.threat <= 0:
            return

        limite = 5 * Worlds.GetPlayerNumIcon(effect)
        destinations = [
            s for s in Worlds.GetOnAllFieldScheme(effect)
            if s is not source and (MainScheme.IsType(s) or s.threat < limite)
        ]
        if not destinations:
            return
        destination = initiator.AskChooseFace(
            destinations, effect, prompt="Move threat onto which scheme?")
        if destination is None:
            destination = destinations[0]

        nombre = initiator.DeclareNumber(1, min(3, source.threat))
        source.MoveThreat(nombre, effect, [destination])

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "You",
            booyakasha,
        ).SetName("Booyakasha")
        .SetTarget(Scheme2, has_threat=True),
    ]
