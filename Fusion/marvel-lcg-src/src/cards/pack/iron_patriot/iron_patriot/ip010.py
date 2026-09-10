from . import *

# Deceptive Guard — EVENEMENT, cout 1, RES [physical]. DEFENSE. TACTIC. x2.
# Alter-Ego Interrupt: When an enemy schemes -> this activation removes threat
#   instead of placing it.
# Hero Interrupt (defense): When an enemy attacks you -> prevent all damage
#   from that attack.
#
# ⚠⚠ DEUX CAPACITES DE JEU SUR LA MEME CARTE. Le moteur l'interdit par defaut
# (`factory.py`, `assert play_count == 1`) : `ip010` a du etre DECLARE dans la
# liste des exceptions, comme `ls005` To Arms! et `br004` Hammer Twirl. Fait le
# 09/09/2026, AVANT d'ecrire ce module — la lecon ls005 dit que l'ordre
# inverse coute une journee de deck injouable.
#
# CARTES DE REFERENCE
#  - `21061` Shield Spell : « Hero Interrupt (defense) ... prevent all damage »,
#    par `WhenUnitWouldTakeDamage(..., is_from_attack=True)` +
#    `message.PreventDamage("All", effect)`. Montage repris tel quel.
#  - `SetRemoveThreatInsteadOfPlacing` (sender_enemy.py:213) : la primitive
#    EXISTE, et elle dit exactement la phrase imprimee. Ne rien reecrire.
#
# TEXTE CONTRE CODE
#  ⚠ La carte est une DEFENSE en forme heros et un CONTRE en forme civile :
#    c'est la meme carte qui protege des deux cotes, et c'est ce qui justifie
#    ses deux capacites de jeu.
#  ⚠ « prevent ALL damage » et non « reduce » : `PreventDamage("All", ...)`.
#  ⚠ L'Interruption d'alter ego n'a PAS d'etiquette `defense` : on ne defend
#    pas en civil. Seule celle de heros la porte.


def GetAbilities() -> Sequence['Ability']:

    def detourner_la_manigance(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        Unused(effect.this)
        message.SetRemoveThreatInsteadOfPlacing(effect)

    def encaisser(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        Unused(effect.this)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldScheme(
            AbilityType.AlterEgoInterrupt,
            Enemy,
            detourner_la_manigance,
        ).SetPlay(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            encaisser,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
    ]
