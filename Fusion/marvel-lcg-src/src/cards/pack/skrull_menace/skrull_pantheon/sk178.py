from . import *

# * Nogor (178) — SBIRE unique. ELITE. SKRULL. MNG 1★, ATQ 1★, PV 4★. Etoile + 2 icones Y.
# ★ Nogor gets +1 SCH, +1 ATK and +1 hit point for each faith counter on the villain.
# When Revealed: Flip the villain.
# ★ Boost: Flip the villain.
#
# Cartes de reference :
#  - Bonus de stats sur un compteur : **`gorr/gb009`** Black Berserker (`ThisGainKeyword(fn, health=1,
#    change_on_event=...)`, valeur recalculee) + `attack=` / `scheme=` de la meme fabrique
#    (**`brawn/bw016`** pour le suivi d'un compteur par `OnEvent.Counter`).
#  - Retournement du mechant : helper `RetournerLeMechant` (modele `fne/typhoid_mary/60112`) ;
#    boost : `WhenCardBecomeBoost("This", op)` (modele sk113).
#
# ⚠ Mots-pieges : « FOR EACH faith counter ON THE VILLAIN » (le compteur du mechant, pas de Nogor) ; « +1
# hit point » = PV supplementaires (un Nogor blesse ne guerit pas quand X monte) ; trois bonus SEPARES (MNG,
# ATQ, PV) ; « Flip the VILLAIN » au When Revealed ET au Boost ; badges ★ imprimes = renvoi au texte (desc : 1, 1, 4).


def GetAbilities() -> Sequence['Ability']:

    def foi(effect: 'Effect', ui: List['CardFace']) -> int:
        Unused(ui)
        return Foi(effect)

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        RetournerLeMechant(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        RetournerLeMechant(effect)

    return [
        AbilityFactory.ThisGainKeyword(
            foi, scheme=1, attack=1, health=1,
            change_on_event=OnEvent.Counter(Villain, COMPTEUR_FOI),
        ),
        AbilityFactory.WhenThisRevealed(None, revelation),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
