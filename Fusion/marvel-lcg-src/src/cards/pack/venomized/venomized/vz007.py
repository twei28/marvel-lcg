from . import *

# Backed into a Corner — EVENEMENT, cout 1, RES [energy]. DEFENSE.
# Hero Interrupt (defense): When you would take any amount of damage, prevent
#   an amount of damage equal to your DEF and ATK combined.
#
# CARTES DE REFERENCE
#  - `16052` Booster Boots et `27183b` Impact-Dampening Suit : « When you would
#    take any amount of damage », c'est-a-dire `WhenUnitWouldTakeDamage` sur
#    "YourIdentity".
#  - `message.PreventDamage(n, effect)` (`sender_damage.py:133`) : PREVENIR
#    n'est pas REDUIRE. Le moteur distingue les deux, et le texte dit bien
#    « prevent ».
#
# TEXTE CONTRE CODE
#  ⚠ « ANY amount of damage » : pas seulement une attaque. Les degats
#    indirects et ceux d'une traitrise passent aussi -> aucun filtre
#    `is_from_attack`.
#  ⚠ « YOUR DEF and ATK » : les deux caracteristiques du HEROS, la somme.
#    C'est la jumelle defensive de vz013 (ATQ+CTR) et vz010 (CTR+DEF) : les
#    trois cartes lisent le heros de la meme facon.
#  ⚠ Etiquette `defense` : la carte compte comme une defense, ce qui la rend
#    incompatible avec un heros deja incline pour defendre.
def GetAbilities() -> Sequence['Ability']:

    def backed_into_a_corner(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        heros = effect.GetInitiator().GetHero()
        message.PreventDamage(heros.defense + heros.attack, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "YourIdentity",
            backed_into_a_corner
        ).SetPlay().SetLabel('defense'),
    ]
