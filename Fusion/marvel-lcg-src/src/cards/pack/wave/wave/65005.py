from . import *

# * Instinctive Flow — evenement signature, x2 (7-8/15). SUPERPOWER. Cout 1.
# Hero Action: Flip up to 3 faceup cards in your Rising Tide area facedown.
# For each card flipped facedown this way, choose (max 1 each): deal 2
# damage to an enemy. remove 2 threat from a scheme. stun an enemy.
#
# Meme discipline « max 1 each » que 65004 Marine Patrol (voir son
# commentaire) : trois branches ici, jusqu'a trois retournements -- flipper
# le maximum force donc a prendre les trois branches, une fois chacune.
# « Hero Action » SANS parenthese (attack/thwart/defense) : aucune etiquette
# `.SetLabel(...)`, comme 01050 * Hulk ou tout evenement sans mode imprime.
# Etourdir : `Faces.GiveStatus(cibles, "Stunned", effect)`, modele vv002
# Hologram Projection (meme pack de reference que Confused).

def GetAbilities() -> Sequence['Ability']:

    def instinctive_flow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        if not isinstance(initiator, Player):
            return

        retournees = RetournerCartesRisingTide(
            effect, initiator, face_visible=True, minimum=0, maximum=3,
            prompt="Flip up to 3 faceup cards in your Rising Tide area facedown",
        )
        if not retournees:
            return

        options_restantes: List[str] = ["damage", "threat", "stun"]

        def degats(cibles: Sequence['CardFace']) -> None:
            this.DealDamage(cibles, 2, effect)
            options_restantes.remove("damage")

        def menace(cibles: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(cibles, 2, effect)
            options_restantes.remove("threat")

        def etourdir(cibles: Sequence['CardFace']) -> None:
            Faces.GiveStatus(cibles, "Stunned", effect)
            options_restantes.remove("stun")

        for _ in retournees:
            choix: List['Ability'] = []
            if "damage" in options_restantes:
                choix.append(AbilityFactory.ForChoiceAbility(
                    "Deal 2 damage to an enemy", degats,
                ).SetTarget(Enemy))
            if "threat" in options_restantes:
                choix.append(AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme", menace,
                ).SetTarget(Scheme2))
            if "stun" in options_restantes:
                choix.append(AbilityFactory.ForChoiceAbility(
                    "Stun an enemy", etourdir,
                ).SetTarget(Enemy, canbe_stunned=True))
            if not choix:
                break
            initiator.ChooseAbilities(effect, *choix)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            instinctive_flow,
        ).SetPlay().SetLabel(),
    ]
