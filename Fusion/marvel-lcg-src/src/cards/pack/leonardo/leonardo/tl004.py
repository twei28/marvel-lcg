from . import *

# Vigilant — evenement signature, x2. THWART. Cout 2, [physical].
# Hero Action (thwart): Remove 3 threat from a scheme. If you paid for this
#   card with a [mental] resource, ready a [[KATANA]] upgrade you control.
#
# Cartes de reference :
#  - `ls001a` / `an004` : `.SetTarget(Scheme2, has_threat=True)` +
#    `this.RemoveThreatFromSchemes(effect.targets, n, effect)` ;
#  - `ls004` Lead The Charge : un second choix en cours d'effet par
#    `ChooseAbilities(effect, ForChoiceAbility(...).SetTarget(...))` ;
#  - `ls006` pour `effect.GetPaidResources().HasColor(...)`.
#
# Mots-pieges :
#  - « a scheme » : principale OU annexe ;
#  - « if you PAID ... with a [mental] resource » : au moins une mentale ;
#  - « a [[KATANA]] upgrade YOU CONTROL » : `from_where=["YouControlCards"]`,
#    `canbe_ready=True` (inutile de redresser une arme prete) ;
#  - la menace est retiree D'ABORD, le redressement ensuite ;
#  - libelle `(thwart)`.


def GetAbilities() -> Sequence['Ability']:

    def vigilant(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

        if joueur is not None and effect.GetPaidResources().HasColor("B"):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Ready a KATANA upgrade you control",
                    lambda cibles: Faces.ReadyAll(
                        [f for f in cibles if f is not None], effect),
                ).SetTarget(Upgrade, trait="KATANA",
                            from_where=["YouControlCards"], canbe_ready=True),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vigilant,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2, has_threat=True),
    ]
