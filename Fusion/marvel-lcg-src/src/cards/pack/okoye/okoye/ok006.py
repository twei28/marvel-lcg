from . import *

# Angelic Warfare (1/2)
# Hero Action: Create 2 Midnight Angel allies and put them into play.
# Hero Action: Ready Okoye and give up to 3 allies a tough status card.
#
# Exemplaire physique 1 de 2 (ok006, ok007). Deux "Hero Action" imprimees sur
# le meme evenement = un choix a la resolution (modele Adored Ones/ok004),
# pas deux capacites separees. "give up to 3 allies a tough status card" :
# modele trors/04017.py (Ready for Action, `Faces.GiveStatus(targets, "Tough",
# effect)` + `.SetTarget("YourAlly", canbe_tough=True)`), etendu a "up to 3"
# via `range=("Zero", 3)`.


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
