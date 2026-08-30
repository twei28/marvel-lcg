from . import *

# * Hulkling (Teddy Altman) — allie signature, custom « CptScorp »
# Cout 3, [physical], ATQ 1*, CTR 1*, 3 PV. Traits KREE / SKRULL /
# YOUNG AVENGER. Aucun mot-cle imprime.
# Interrupt: When Hulkling attacks, he gets +1 ATK for each boost icon on the
#   top card of the encounter deck. Then, discard that card.
#
# Declencheur -> `AbilityFactory.WhenUnitWouldAttackUnit(AbilityType.
# Interrupt, "This", None, ...)` (game/ability/factory/do_attack.py:175).
# Modeles : Befuddle (`cyclops/33033.py`) et Surprise Move (`iceman/
# 46015.py`), les deux cartes du depot qui augmentent l'ATQ d'une attaque en
# cours via `message.GainAttackForThisAttack(valeur, effect)`
# (game/message/sender/sender_damage.py:436).
#
# `is_basic_attack` volontairement laisse a None (defaut) : le texte imprime
# dit « When Hulkling attacks », sans restreindre a l'attaque de BASE. Befuddle
# et Surprise Move, eux, impriment « makes a basic attack » et passent donc
# `is_basic_attack=True` — la difference est voulue, pas un oubli.
#
# Bonus -> helper de pack `IconesBoostDuDessus` (voir wiccan/__init__.py),
# lui-meme calque sur Astral Projection (09003) : LookAtDeck + CountTotal
# BoostIcons. Le joueur consulte est le CONTROLEUR de l'allie
# (`this.GetControlByPlayer()`), pas `effect.GetInitiator()` : une interruption
# declenchee pendant la phase du vilain n'a pas forcement d'initiateur joueur.
#
# « Then, discard that card » -> `Worlds.DiscardEncounterTopCard(effect)`
# (worlds.py:577), la meme brique que Falcon (53001a) et le Pistolet d'Agent
# 13 (ag008). La defausse n'est PAS conditionnee au nombre d'icones : le texte
# la pose apres un point, sans « if ». Elle a donc lieu meme a 0 icone et meme
# quand l'obligation wc018 a eteint le comptage (« boost icons cannot be
# COUNTED », pas « la carte n'est plus defaussee »).
#
# Cas limite : deck de rencontre vide -> 0 icone, `DiscardEncounterTopCard`
# rend None, aucune erreur.
#
# ATQ 1* et CTR 1* (valeurs par joueur) sont lues nativement dans `desc` par
# le moteur : aucun code (voir PROCESSUS-CARTE, « bases automatiques »).

def GetAbilities() -> Sequence['Ability']:

    def hulkling(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Ally)

        joueur = this.GetControlByPlayer()
        icones = IconesBoostDuDessus(effect, joueur)
        if icones > 0:
            message.GainAttackForThisAttack(icones, effect)

        Worlds.DiscardEncounterTopCard(effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.Interrupt,
            "This",
            None,
            hulkling,
        ),
    ]
