from . import *

# The Harvest — TRAITRISE (nemesis 5/5), boost 2.
# When Revealed: Choose: • Discard an upgrade or support you control. • Take damage equal to the highest-cost upgrade or support you control.
#
# CARTES DE REFERENCE
#  - `mv016` Accept Perfection : `ChooseAbilities(effect, ForChoiceAbility(..), ForChoiceAbility(..))` ; `joueur.DiscardControlCards(effect, ...)`.
#  - `mv015` : `identite.TakeIndirectDamage(...)` ; ici des degats NORMAUX (« take damage ») : `identite.TakeDamage(this, n, effect)` (modele 01061).
#
# TEXTE CONTRE CODE
#  « an upgrade OR support » -> amelioration ou soutien (pas un allie). « highest-cost » -> le plus haut COUT IMPRIME parmi les ameliorations et
#    soutiens que le joueur controle ; sans aucun, 0 degat. « take damage » -> degats normaux sur l'identite.


def GetAbilities() -> Sequence['Ability']:

    def the_harvest(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()

        def defausser(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            joueur.DiscardControlCards(effect, upgrade=True, support=True)

        def subir(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            cartes = list(joueur.GetControlUpgrade()) + list(joueur.supports.Get())
            cout = max([int(c.paper.desc.get("Cost", "0") or 0) for c in cartes] or [0])
            identite = joueur.GetIdentity()
            if cout > 0 and identite is not None:
                identite.TakeDamage(this, cout, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Discard an upgrade or support you control", defausser),
            AbilityFactory.ForChoiceAbility("Take damage equal to the highest-cost upgrade or support you control", subir),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            the_harvest,
        ),
    ]
