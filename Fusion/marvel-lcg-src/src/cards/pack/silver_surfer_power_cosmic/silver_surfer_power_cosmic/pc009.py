from . import *

# Lightspeed Entrance — EVENEMENT. THWART. POWER COSMIC. Cout 0, ressource
# [mental]. x2 (pc009, 2 exemplaires).
#
# Texte imprime : « Hero Response (thwart): After Silver Surfer departs a
# PLANET, remove 2 threat from a scheme. If that PLANET was Newhaven, you
# may spend a [mental] resource to ready Silver Surfer. »
#
# CARTES DE REFERENCE : voir pc008 Cosmic Blast (gabarit identique, manigance
# au lieu d'attaque). `01084` Nick Fury pour `ChooseAbilities +
# ForChoiceAbility(...).SetTarget(Scheme2)` -- ce chemin est prouve par le
# harnais sur pc006 Newhaven (ancien cas rouge resolu le 05/11/2026 : le bug
# etait dans le CAS DE TEST, pas le moteur -- `Puzzle.SetThreat('01097b', 10)`
# depassait le seuil de la manigance Rhino et l'accomplissait avant le
# contre ; corrige a 5, voir [[gainkeyword-vs-gainuntilroundend]]).


def GetAbilities() -> Sequence['Ability']:

    def est_silver_surfer_qui_part(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> bool:
        Unused(effect)
        return EstSilverSurfer(message.character_face)

    def lightspeed_entrance(effect: 'Effect', message: 'Message.AfterCharacterDepartPlanet') -> None:
        this = effect.this.CastTo(Event)
        depuis_newhaven = getattr(message.planet_face.paper, "card_id", None) == "pc006"
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def retirer_menace(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, 2, effect)
            if depuis_newhaven:
                silver_surfer = joueur.GetIdentity()
                joueur.MayChooseOneAbility(
                    effect,
                    AbilityFactory.ForChoiceAbilityWithCost(
                        Cost("B"),
                        "Ready Silver Surfer",
                        lambda cibles2, res: Faces.ReadyAll([silver_surfer], effect),
                    ),
                )

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 2 threat from a scheme",
                retirer_menace,
            ).SetTarget(Scheme2),
        )

    return [
        Ability(
            AbilityType.HeroResponse,
            Message.AfterCharacterDepartPlanet,
            [est_silver_surfer_qui_part],
            lightspeed_entrance,
        ).SetPlay().SetLabel('thwart'),
    ]
