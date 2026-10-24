from . import *

# Cosmic Strength — Evenement, cout 3, ressource [energy]. COSMIC. SUPERPOWER.
# Hero Interrupt: When you make a basic attack, choose one:
#  • You get +7 ATK for that attack.
#  • Discard The Silver Surfboard -> You get +9 ATK for that attack and it gains overkill.
#
# Cartes de reference :
#  - `10003` Hulk Smash (hlk) : `WhenUnitMakeAttack(HeroInterrupt, "You", op, is_basic_attack=True).SetPlay()`,
#    `message.GainATKForThisAttack(n, effect)` et `message.GainOverKill(effect)`.
#  - `08013` / `14004` : le « choose one » dans UN module, par `ChooseAbilities` (pas de liste blanche).
#
# ⚠ Mots-pieges :
#  - « basic attack » : `is_basic_attack=True` ; l'attaque d'un evenement ne declenche pas la carte.
#  - « +7 » et « +9 » : l'option 2 REMPLACE l'option 1 (+9 et non +16), elle ne s'y ajoute pas.
#  - « Discard The Silver Surfboard -> » : la defausse est un COUT, l'option n'existe que si la planche est en jeu.
#  - « it gains overkill » : l'attaque, uniquement dans l'option 2.


def GetAbilities() -> Sequence['Ability']:

    def force_cosmique(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def plus_sept(cibles: Sequence['CardFace']) -> None:
            message.GainATKForThisAttack(7, effect)

        def plus_neuf(cibles: Sequence['CardFace']) -> None:
            planche = LaPlanche(effect, joueur)
            if planche is None:
                return
            Faces.DiscardAll([planche], effect)
            message.GainATKForThisAttack(9, effect)
            message.GainOverKill(effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "You get +7 ATK for that attack",
                plus_sept,
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Discard The Silver Surfboard → +9 ATK and overkill",
                plus_neuf,
                condition=LaPlanche(effect, joueur) is not None,
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            force_cosmique,
            is_basic_attack=True,
        ).SetPlay().SetLabel(),
    ]
