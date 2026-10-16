from . import *

# Yo Ko Giri — evenement signature, x2. ATTACK. SKILL. Cout 3, [wild].
# Hero Action (attack): Deal 5 damage to an enemy. This attack gains piercing.
#   If you paid for this card with [energy][mental][physical] resources, you
#   may return this card to your hand.
#
# Cartes de reference :
#  - `ls003` Impale : `this.DealDamage(effect.targets, n, effect,
#    property=AttackProperty(piercing=True))` ;
#  - `62004` Knuckle Sandwich / `18012` Clobber : « return this event to your
#    hand » par `ChooseAbilities(... 'Decline')` et `Faces.ReturnToHand([this],
#    joueur, effect)`.
#
# Mots-pieges :
#  - « This attack gains PIERCING » : inconditionnel (pas de choix) ;
#  - « paid with [energy][mental][physical] resources » : LECTURE LITTERALE =
#    au moins UNE de chaque couleur. DECISION UTILISATEUR (15/10/2026) : au moins
#    UNE ressource de chaque couleur ; on teste HasColor sur chacune des trois
#    (une ressource wild compte pour toute couleur, regle du jeu) ;
#  - « you MAY return » : optionnel -> deux branches, dont « Decline » ;
#  - libelle `(attack)`.


def GetAbilities() -> Sequence['Ability']:

    def yo_ko_giri(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 5, effect,
                        property=AttackProperty(piercing=True))

        if joueur is None:
            return
        payees = effect.GetPaidResources()
        # « [energy][mental][physical] » = au moins une de chaque couleur.
        if payees.HasColor("Y") and payees.HasColor("B") and payees.HasColor("R"):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Return this card to your hand",
                    lambda cibles: Faces.ReturnToHand([this], joueur, effect),
                ),
                AbilityFactory.ForChoiceAbility(
                    "Decline",
                    lambda cibles: None,
                ),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            yo_ko_giri,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
