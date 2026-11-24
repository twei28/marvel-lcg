from . import *

# Recalled Trauma — obligation, boost 2. « Give to the Barbara Gordon player. You may flip to alter-ego form. Choose: • Exhaust Barbara
# Gordon → remove Recalled Trauma from the game. • Until the end of the next round, all cards you spend as resources are considered to
# have no resource type for the purpose of resolving card abilities. Discard this obligation. »
# Cartes de reference : `us012` Forced Leave / `th011` (obligation a deux branches, retournement), `ah001a` (CheckEffectGeneratedResources).
# ⚠ « No resource type » : le moteur n'a pas de ressource SANS type ; on convertit les ressources generees en `L` (la 5e couleur du
# moteur, qui ne vaut aucune des quatre ; effet DOCUMENTE comme provisoire dans le gabarit).


def GetAbilities() -> Sequence['Ability']:

    def recalled_trauma(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        if joueur.IsHero():
            joueur.GetIdentity().ChangeToForm(AlterEgo, effect)

        def retirer(targets) -> None:
            Faces.ExhaustAll([joueur.GetIdentity()], effect)
            Faces.RemoveAllFromGame([this], effect)

        def sans_type(targets) -> None:
            # Jusqu'a la fin du PROCHAIN round : le round courant et le suivant.
            joueur.bg_sans_type = joueur.world.round_id + 1
            Faces.DiscardAll([this], effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Exhaust Barbara Gordon → remove Recalled Trauma from the game.", retirer).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility("Cards you spend as resources have no resource type until the end of the next round.",
                                            sans_type).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, recalled_trauma),
    ]
