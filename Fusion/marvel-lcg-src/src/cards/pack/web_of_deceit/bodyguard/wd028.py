from . import *

# Bodyguard (sbire)

def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)

        # « Choose to give the villain a tough status card or heal 4 damage from
        # the villain. If you cannot, put this card into play engaged with you. »
        joueur = message.GetToPlayer()
        villain = Worlds.FindVillain(effect)

        # ⚠ « IF YOU CANNOT » NE VOULAIT RIEN DIRE. Le repli n'etait pris que
        # si la partie n'avait pas de vilain, ce qui n'arrive jamais. Le vrai
        # « cannot », c'est : le vilain a DEJA un tough (un personnage n'en
        # porte qu'un) ET n'a aucun degat a soigner. Les deux options sont
        # alors sans effet, et c'est le sbire qui doit entrer en jeu.
        peut_tough = villain is not None and villain.CanGainTough()
        peut_soigner = villain is not None and villain.CastTo(Unit2).GetLostHealth() > 0
        if not peut_tough and not peut_soigner:
            joueur.DealEncounterCard(this, effect)
            return
        assert villain is not None

        def donner_tough(targets: Sequence['CardFace']) -> None:
            Faces.GiveStatus([villain], "Tough", effect)

        def soigner(targets: Sequence['CardFace']) -> None:
            this.HealthUnits([villain], 4, effect)

        # Une option sans effet n'est pas proposee : « choose to X or Y » ne
        # laisse choisir que ce qui est possible.
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Give the villain a tough status card",
                donner_tough,
                condition=peut_tough,
            ),
            AbilityFactory.ForChoiceAbility(
                "Heal 4 damage from the villain",
                soigner,
                condition=peut_soigner,
            ),
        )

    return [
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
