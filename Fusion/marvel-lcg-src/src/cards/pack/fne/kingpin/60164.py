from . import *

# Bear Hug (CONDITION) — boost 2, Uses (3 grip counters) : base desc.
# If Kingpin has the MARTIAL ARTIST trait, attach to your hero. Otherwise,
#   this card gains surge.
# You cannot change to alter-ego form.
# Forced Interrupt: When you would thwart or attack, remove 1 grip counter
#   from here instead.
# Modeles : 60080 (AttachToFaceWhenPutIntoPlay sur l'identite), 60150
# Imprisoned (PlayersCannotChangeForms to_form=AlterEgo), 60182 Cop
# (WhenUnitWouldScheme + SetBeInstead) transpose a WhenUnitWouldAttack /
# WhenUnitWouldThwart("You"). La condition « Kingpin MARTIAL ARTIST » va sur
# le selecteur (check_effect_fn), pour que le « cannot » declenche le surge.

def GetAbilities() -> Sequence['Ability']:

    def kingpin_arts_martiaux(effect: 'Effect', face: 'CardFace') -> bool:
        return KingpinArtMartial(effect)

    def au_lieu(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldThwart') -> None:
        message.SetBeInstead(effect)
        Faces.RemoveCountersOn([effect.this], 1, 'grip', effect)

    selecteur = Select.From("YourHero")
    selecteur.selector_filter.AddParameter(check_effect_fn=kingpin_arts_martiaux)
    selecteur.selector_range.SetRange("All")

    def surge(effect: 'Effect', joueur: 'Player') -> None:
        ThisCardGainSurge(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlayInternal(
            selecteur,
            conditions=[lambda effect, message: not effect.this.card.area.flags.is_upgrades],
            if_cannot_operation=surge,
        ),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "You", to_form=AlterEgo),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "You", au_lieu),
        AbilityFactory.WhenUnitWouldThwart(AbilityType.ForcedInterrupt, "You", au_lieu),
    ]
