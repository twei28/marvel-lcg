from . import *


def GetAbilities() -> Sequence['Ability']:
    def retirer_une(effect: 'Effect', this: 'CardFace') -> None:
        this.RemoveThreatFromSchemes([this], 1, effect)

    def goblins_ultimatum(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)
        joueur = effect.GetInitiator()
        identite = joueur.GetIdentity()
        ameliorations = AmeliorationsDe(joueur)

        def epuiser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            if Faces.ExhaustAll([identite], effect):
                retirer_une(effect, this)

        def defausser(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            face = joueur.AskChooseFace(ameliorations, effect, prompt="Discard an upgrade you control")
            if face and Faces.DiscardAll([face], effect):
                retirer_une(effect, this)

        def subir(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            identite.TakeDamage(this, 2, effect)
            retirer_une(effect, this)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust your hero", epuiser, condition=identite.CanExhaust()),
            AbilityFactory.ForChoiceAbility("Discard 1 upgrade you control", defausser, condition=bool(ameliorations)),
            AbilityFactory.ForChoiceAbility("Take 2 damage", subir),
        )

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(message)
        premier = Worlds.GetFirstPlayer(effect)
        Find.FindAndReveal(effect, premier, name="Punisher No More", card_type=Obligation)
        Faces.DiscardAll([this], effect)

    return [
        # « except from its own abilities » : seule une capacite de CETTE carte peut en retirer.
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            conditions=[lambda effect, message: getattr(message, "by_face", None) is not effect.this],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            goblins_ultimatum,
        ),
        AbilityFactory.WhenPhaseEnd(
            AbilityType.ForcedInterrupt,
            "Player",
            fin_de_phase,
        ),
    ]
