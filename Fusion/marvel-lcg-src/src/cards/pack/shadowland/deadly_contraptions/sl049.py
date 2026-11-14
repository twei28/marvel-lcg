from . import *

# Path of a Thousand Cuts — COMPLOT ANNEXE. Menace de depart 5 (fixe), boost ★ seul.
# Every step is a test of resilience. (citation)
# Forced Interrupt : When you choose the "Avoid" effect or the "Trip" effect on a TRAP! card, take 2 indirect damage.
# ★ Boost : Deal 1 damage to each character you control.
#
# Cartes de reference : `QuandOnChoisitUnEffetDePiege` (ce module), punisher_mcdc_2026/punishers_armory/pu118 (`TakeIndirectDamage`), shadows_in_the_night/sl010 (`DealDamage`).
# ⚠ Mots-pieges : « Avoid OR Trip » : jamais Disarm ; « YOU choose » : le joueur qui choisit ; « 2 INDIRECT damage » : sur l'identite, indirects (pas dirigeables sur un allie) ;
#  Boost : 1 degat DIRECT a CHAQUE personnage (identite + allies) du joueur contre qui l'activation a lieu.


def GetAbilities() -> Sequence['Ability']:

    def avoid_ou_trip(effect: 'Effect', message: 'QuandOnChoisitUnEffetDePiege') -> bool:
        return message.effet in (PIEGE_AVOID, PIEGE_TRIP)

    def indirects(effect: 'Effect', message: 'QuandOnChoisitUnEffetDePiege') -> None:
        message.GetToPlayer().GetIdentity().TakeIndirectDamage(effect.this, 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        effect.this.DealDamage(list(joueur.GetControlCharacters()), 1, effect)

    return [
        Ability(AbilityType.ForcedInterrupt, QuandOnChoisitUnEffetDePiege, [avoid_ou_trip], indirects),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
