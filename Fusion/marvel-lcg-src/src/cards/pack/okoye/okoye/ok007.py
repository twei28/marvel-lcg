from . import *

# Angelic Warfare (2/2)
# Exemplaire physique 2 de 2, contenu identique a ok006 (voir ce fichier pour
# le detail du modele repris).


def GetAbilities() -> Sequence['Ability']:

    def angelic_warfare(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def creer(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            for _ in range(2):
                CreerJetonEtMettreEnJeu(ID_JETON_MIDNIGHT_ANGEL, initiator, effect)

        def redresser_et_donner(targets: Sequence['CardFace']) -> None:
            Faces.ReadyAll([initiator.GetIdentity()], effect)
            if targets:
                Faces.GiveStatus(targets, "Tough", effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Create 2 Midnight Angel allies and put them into play",
                creer,
            ),
            AbilityFactory.ForChoiceAbility(
                "Ready Okoye and give up to 3 allies a tough status card",
                redresser_et_donner,
            ).SetTarget("YourAlly", canbe_tough=True, range=("Zero", 3)),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            angelic_warfare,
        ).SetPlay(),
    ]
