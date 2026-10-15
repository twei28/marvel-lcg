from . import *

# Skrull Warrior — SBIRE x2 (Skrull Society). SKRULL. SCH 2, ATK 2, 4 PV,
# Guard, ★ + 1 boost.
# ★ Boost: If this attack is undefended, you are stunned.
#
# Carte de reference : **`04145`** (`WhenCardBecomeBoost(..., is_undefended_attack=True)`).
# ⚠ « YOU are stunned » : l'identite du joueur attaque (meme en alter ego, la
# carte d'etat se pose). Guard : desc, natif.


def GetAbilities() -> Sequence['Ability']:

    def sonne(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GetToPlayer().GetIdentity().GainStatus("Stunned", effect)

    return [AbilityFactory.WhenCardBecomeBoost("This", sonne, is_undefended_attack=True)]
