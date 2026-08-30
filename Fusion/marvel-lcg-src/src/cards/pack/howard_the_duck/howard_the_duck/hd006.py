from . import *

# Quack Attack (2/2)
# Exemplaire physique 2 de 2 (RES energie), contenu identique a hd005 (voir
# ce fichier pour le detail du modele repris).


# CORRECTIF (30/08/2026) : la capacite PRINCIPALE portait `SetLabel()` VIDE ; seul
# le `ForChoiceAbility` imbrique portait un label. Mesure : un label pose sur une
# ability imbriquee ne livre PAS la capacite aux statuts. Sonne et Desoriente
# ecoutent `AfterPlayerTriggerAbility(label=...)` sur l'ability JOUEE
# (`cards/pack/status/`), et la carte passait donc en force. Modele : la carte
# OFFICIELLE 18004 Crosscounter, meme forme, qui pose ses trois labels imprimes
# sur l'ability principale.


def GetAbilities() -> Sequence['Ability']:

    def quack_attack(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)

        message.PreventDamage(2, effect)

        valeur = NombreDeManigancesEnVictoire(effect)
        if valeur <= 0:
            return

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def frapper(targets: Sequence['CardFace']) -> None:
            if targets:
                this.DealDamage(targets, valeur, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 damage to an enemy for each side scheme in the victory display",
                frapper,
            ).SetLabel('attack').SetTarget(Enemy),
        )

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            quack_attack,
        ).SetPlay().SetLabel('attack', 'defense'),
    ]
