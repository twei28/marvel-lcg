from . import *

# Prayer to Kly'bn (x3, 181) — TRAITRISE. 1 icone Y + etoile de boost.
# When Revealed: If Kly'bn is in play, he activates against you. Otherwise, flip the villain.
# ★ Boost: If Kly'bn is not in play, flip the villain.
#
# Cartes de reference :
#  - « activates against you » : **`sm/venom/27082`**, **`sm/goblin_gear/27136`** (`villain.DoActivate(joueur,
#    effect)`, attaque en forme heros, manigance en alter ego) ;
#  - retournement : `RetournerLeMechant` (modele `fne/typhoid_mary/60112`) ; boost : `WhenCardBecomeBoost`.
#
# ⚠ Mots-pieges : « if KLY'BN is in play » (la FACE visible du mechant porte ce nom : face Sl'gur't visible =
# Kly'bn n'est PAS en jeu) ; « HE activates against YOU » (le joueur qui revele) ; « Otherwise, flip the villain »
# (retourne vers Kly'bn) ; Boost : la condition est INVERSEE (« is NOT in play »).


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        klybn = Worlds.FindCardOnField(effect, name=NOM_KLYBN, card_type=Villain)
        if klybn is not None:
            klybn.DoActivate(joueur, effect)
        else:
            RetournerLeMechant(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        if not EstEnJeu(effect, NOM_KLYBN):
            RetournerLeMechant(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
