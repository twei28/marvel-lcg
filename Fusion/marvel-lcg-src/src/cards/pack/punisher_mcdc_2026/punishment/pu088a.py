from . import *

# One Last Kill (1A) — MANIGANCE PRINCIPALE.
# Contents : Punisher I and II (II and III for expert mode) and one UNDERLING villain. Punishment, UNDERLING villain's set,
#   and Standard sets. One modular set (Punisher's Armory).      (portee par data/scenarios/one_last_kill_*.json)
# Setup : Find Target Lock and attach to Punisher, FOCUSED side up. Find Justice or Punishment? and reveal its setup side.
#
# Cartes de reference : fne/the_getaway/60128a.py (`WhenCardSetup("This")` + `Find.FindAndAttachTo`),
# galactic_storm/kree_sentry/gs079a.py. Target Lock entre FOCUSED (pu091a) : la face recto.
# ⚠ « attach to PUNISHER » : le vilain `Punisher`, pas le sous-fifre ; « reveal its SETUP side » : la face 5A (recto).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        punisher = Punisher(effect)
        if punisher is not None:
            Find.FindAndAttachTo(effect, punisher, who_perform=premier, name=NOM_CIBLE_ATTACHEMENT, card_type=Attachment)
        Find.FindAndReveal(effect, premier, name="Justice or Punishment?", card_type=Environment)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
    ]
