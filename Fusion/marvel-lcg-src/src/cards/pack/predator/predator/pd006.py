from . import *

# Shadow Counter — EVENEMENT, cout 1, [mental]. DEFENSE.
# Hero Interrupt (defense): When you would take any amount of damage, prevent 3 of that damage. Then, give Predator a cloaked
#   status card.
#
# Cartes de reference :
#  - `core/spider_man/01003` Backflip : `WhenUnitWouldTakeDamage(Interrupt, "You", op).SetPlay().SetLabel('defense')` et
#    `message.PreventDamage(n, effect)`.
#  - `ShinobiCloak` (fiche cloaked.md) : « give X a cloaked status card ».
#
# ⚠ Mots-pieges :
#  - « ANY amount of damage » : pas seulement une attaque (aucun `is_from_attack`), contrairement a Backflip ; at_least_damage=1.
#  - « prevent 3 OF THAT damage » : au plus 3, pas toute l'attaque.
#  - « THEN give Predator a cloaked status card » : apres la prevention ; la carte Cloaked posee ne reduit PAS ces degats-ci
#    (elle ne vaut que pour les PROCHAINS). Predator deja camoufle : rien (une seule carte).


def GetAbilities() -> Sequence['Ability']:

    def contre_de_l_ombre(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage(3, effect)
        Camoufler(effect, JoueurDeCetteCarte(effect))

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            contre_de_l_ombre,
        ).SetPlay().SetLabel('defense'),
    ]
