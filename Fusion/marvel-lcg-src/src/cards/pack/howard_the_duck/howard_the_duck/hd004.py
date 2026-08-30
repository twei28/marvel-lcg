from . import *

# Mallard Magic (2/2)
# Exemplaire physique 2 de 2 (RES energie), contenu identique a hd003 (voir
# ce fichier pour le detail du modele repris).


def GetAbilities() -> Sequence['Ability']:

    def mallard_magic(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def sonner_et_frapper(targets: Sequence['CardFace']) -> None:
            if not targets:
                return
            Faces.GiveStatus(targets, "Stunned", effect)
            this.DealDamage(targets, 5, effect)

        def desorienter_et_nettoyer(targets: Sequence['CardFace']) -> None:
            if targets:
                Faces.GiveStatus(targets, "Confused", effect)

            def retirer(schemes: Sequence['CardFace']) -> None:
                if schemes:
                    this.RemoveThreatFromSchemes(schemes, 4, effect)

            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 4 threat from a scheme",
                    retirer,
                ).SetLabel('thwart').SetTarget(Scheme2),
            )

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun an enemy and deal 5 damage to it",
                sonner_et_frapper,
            ).SetLabel('attack').SetTarget(Enemy, canbe_stunned=True),
            AbilityFactory.ForChoiceAbility(
                "Confuse an enemy and remove 4 threat from a scheme",
                desorienter_et_nettoyer,
            ).SetLabel('thwart').SetTarget(Enemy, canbe_confused=True),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mallard_magic,
        ).SetPlay().SetLabel(),
    ]
