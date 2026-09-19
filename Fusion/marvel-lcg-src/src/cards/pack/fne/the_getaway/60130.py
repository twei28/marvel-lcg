from . import *

# Escort Vehicle (VEHICLE) — Guard, Patrol : bases desc.
# If the number of speed counters on the main scheme is at least:
#   • 3 – This minion gains toughness.  • 6 – ...also quickstrike.
#   • 9 – ...also surge.
# ThisGainKeyword(check_fn) recalcule sur OnEvent.Counter(MainScheme, 'speed')
# (modele 60091 Chameleon pour le recalcul sur evenement).

def GetAbilities() -> Sequence['Ability']:

    def seuil(n: int):
        def check(effect: 'Effect', ui: List['CardFace']) -> int:
            return 1 if CompteursDeVitesse(effect) >= n else 0
        return check

    # ⚠ OnEvent.Counter prend un TYPE : la chaine "MainScheme" est une
    # Sequence et leve `assert not isinstance(check_rule, Sequence)`
    # (card_type.py:247) a CHAQUE compteur pose pendant que le sbire est en
    # jeu (15 tracebacks par partie d'autoplay, vus par l'agent B le 18/09).
    evenement = OnEvent.Counter(MainScheme, 'speed')
    return [
        AbilityFactory.ThisGainKeyword(seuil(3), toughness=1, change_on_event=evenement),
        AbilityFactory.ThisGainKeyword(seuil(6), quickstrike=1, change_on_event=evenement),
        AbilityFactory.ThisGainKeyword(seuil(9), surge=1, change_on_event=evenement),
    ]
