from . import *

# Resistance — EVENEMENT, cout 2, [wild]. DEFENSE. SUPERPOWER. x2.
# Hero Interrupt (defense): When you would take any amount of damage from an attack,
#   prevent all damage from that attack. You may remove 2 dredge counters from Venus to
#   draw 3 cards.
#
# CARTES DE REFERENCE
#  - `bl006` Vampiric Reflexes (pack blade) : MEME premiere phrase mot pour mot
#    (`WhenUnitWouldTakeDamage(HeroInterrupt, "You", op, is_from_attack=True).SetPlay()
#    .SetLabel('defense')` + `message.PreventDamage("All", effect)`), puis un choix facultatif.
#  - `dz010` Rich Angel : meme squelette.
#
# TEXTE CONTRE CODE
#  ⚠ « When YOU would take ... from an ATTACK » -> l'identite, degats d'attaque seulement :
#    une traitrise passe (`is_from_attack=True`).
#  ⚠ « prevent ALL damage from that attack » -> `PreventDamage("All")`.
#  ⚠ « You MAY remove 2 dredge counters ... to draw 3 cards » : facultatif, retrait = cout,
#    offert apres la prevention.
#  x2 : deux exemplaires au deck, un seul card_id.


def GetAbilities() -> Sequence['Ability']:

    def resistance(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage("All", effect)
        joueur = JoueurDeCetteCarte(effect)
        ProposerRetraitDragage(
            effect, joueur, 2,
            "Remove 2 dredge counters to draw 3 cards",
            lambda cibles: joueur.DrawUp(3, effect))

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            resistance,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
    ]
