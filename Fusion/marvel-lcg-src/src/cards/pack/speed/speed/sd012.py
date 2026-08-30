from . import *

# Top Speed (2/2) — exemplaire physique 2 de 2, contenu identique a sd011
# (voir ce fichier pour le detail des modeles, dont le point risque « la carte
# qu'on est en train de payer part quand meme »).


def GetAbilities() -> Sequence['Ability']:

    class Supplement:
        # Retenu entre le `CostFunc` (qui pose la question) et `res_fn` (qui
        # rend les ressources) : meme technique que `SiphonState` dans 58006.
        valeur = 0

    def supplement_disponible(effect: 'Effect') -> int:
        return 2 if IlYAUnCompteurExplosifEnJeu(effect) else 1

    def demander_le_supplement(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        Supplement.valeur = 0

        joueur = effect.GetInitiator()
        if joueur is None:
            return True

        supplement = supplement_disponible(effect)

        def prendre_le_supplement(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Supplement.valeur = supplement
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.effect.RegisterTemp(
                    AbilityFactory.PlayersCannotPlayCardWhile(joueur),
                    unregister_after_exec=False,
                    until_turn_end=True,
                )

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Generate {supplement} additional [energy] resource(s) — you cannot play cards for the rest of the turn",
                prendre_le_supplement,
            ).SetHasNoTargetEffect(),
            forced=False,
        )
        return True

    def ressources_generees(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        return Resources("Y" * (1 + Supplement.valeur))

    def ressources_annoncees(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this, message)

        return Resources("Y" * (1 + supplement_disponible(effect)))

    return [
        AbilityFactory.DoDiscardThisToGenerateResources(
            AbilityType.Interrupt,
            res_fn=ressources_generees,
        ).SetCostFunc(CostFunc.Custom(None, demander_le_supplement)),
        AbilityFactory.CheckThisCanDropPay(ressources_annoncees),
    ]
