from . import *

# Prayer to Sl'gur't (x3, 182) — TRAITRISE. 1 icone Y + etoile de boost.
# When Revealed: If Sl'gur't is in play, she activates against you. Otherwise, flip the villain.
# ★ Boost: If Sl'gur't is not in play, flip the villain.
#
# Cartes de reference : voir `sk181` (meme texte, Sl'gur't au lieu de Kly'bn).
#
# ⚠ Mots-pieges : « if SL'GUR'T is in play » (face visible) ; « SHE activates against YOU » ; Boost : condition
# INVERSEE (« is NOT in play »).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        slgurt = Worlds.FindCardOnField(effect, name=NOM_SLGURT, card_type=Villain)
        if slgurt is not None:
            slgurt.DoActivate(joueur, effect)
        else:
            RetournerLeMechant(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        if not EstEnJeu(effect, NOM_SLGURT):
            RetournerLeMechant(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
