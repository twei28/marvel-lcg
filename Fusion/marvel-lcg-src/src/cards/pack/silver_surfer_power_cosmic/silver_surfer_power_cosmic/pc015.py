from . import *

# Tactical Navigation — EVENEMENT. POWER COSMIC. TACTIC. Cout 1, ressource
# [mental]. x2 (pc015, 2 exemplaires).
#
# Texte imprime : « Hero Interrupt: When an enemy attacks, choose a PLANET.
# Silver Surfer arrives at that planet, then departs. Declare Silver Surfer
# the defender of that attack without exhausting him. »
#
# CARTES DE REFERENCE
#  - `rr012` Nigh-Invulnerability (sentry) : `WhenUnitWouldAttack(HeroInterrupt,
#    Enemy, op).SetPlay().SetLabel('defense')` + `message.DeclareDefender(
#    heros, effect)` — modele exact de « declare X the defender without
#    exhausting ».
#  - `pc004`/`pc011` : arrivee puis depart immediat (`ArriverA` puis
#    `Departir`).
#
# TEXTE CONTRE CODE
#  « choose a PLANET » : cible libre, pas forcement une ou Silver Surfer est
#    deja alle. « Silver Surfer arrives... then departs » : avant la
#    declaration de defenseur, dans l'ordre imprime — mais comme aucune
#    carte de ce pack ne reagit a CE depart-la autrement qu'en texte deja
#    couvert par pc008/pc009/pc015 elles-memes (meme famille), l'ordre n'a
#    pas d'effet observable ici au-dela du texte. « WITHOUT EXHAUSTING him » :
#    `DeclareDefender` seul, jamais `Faces.ExhaustAll`.


def GetAbilities() -> Sequence['Ability']:

    def tactical_navigation(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or not effect.targets:
            return
        silver_surfer = joueur.GetIdentity()
        planete = effect.targets[0]
        ArriverA(effect, silver_surfer, planete)
        Departir(effect, silver_surfer)
        message.DeclareDefender(silver_surfer, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            tactical_navigation,
        ).SetPlay().SetLabel('defense')
        .SetTarget(card_type=Support, trait="PLANET"),
    ]
