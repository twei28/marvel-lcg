from . import *

# "Chomp!" — evenement signature, x4 (al003 R, al004 B, al005 Y, al006 G).
# ATTACK. Cout 2.
# Hero Action (attack): Deal 4 damage to an enemy (6 damage instead if
#   Alligator Loki is attached to that enemy). If this attack defeats an
#   enemy, ready Alligator Loki. Otherwise, you may attach Alligator Loki to
#   that enemy.
#
# ⚠ al004, al005 et al006 n'ont PAS de module : elles portent un
# `ability_link` vers al003 (database.py:124). Le texte est le meme au mot
# pres, seule l'icone de ressource change, et c'est `desc` qui la porte.
#
# Cartes de reference :
#  - dd004 « This World Is Mine! » et 01053 Relentless Assault : attaque
#    d'evenement, `WhenInYourPlayTurn(HeroAction, op).SetPlay()
#    .SetLabel('attack').SetTarget(Enemy)`, et c'est le HEROS qui frappe ;
#  - gp002 « Here I Come! » : « If this attack defeats an enemy » ->
#    `if_this_attack_defeats=` de `DealDamage` (card_face.py:575).
#
# ⚠ « OTHERWISE, you may attach » : le rappel de defaite est declenche PENDANT
# `DealDamage` (l'effet temporaire est desinscrit avant le retour,
# card_face.py:629). Un drapeau pose dans le rappel suffit donc a savoir, au
# retour, si l'on est dans le « otherwise ».
#
# ⚠ « if Alligator Loki is attached to THAT enemy » : la cible de l'attaque,
# et elle seule. `EstAccrocheA(effect, cible)` compare par identite d'objet.
#
# ⚠ « ready Alligator Loki » : le heros, pas l'evenement. Et on le remet
# d'aplomb meme s'il etait deja pret (ReadyAll est idempotent).

def GetAbilities() -> Sequence['Ability']:

    def chomp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        heros = joueur.GetHero() if joueur else None
        if heros is None or not effect.targets:
            return
        cible = effect.targets[0]

        degats = 6 if EstAccrocheA(effect, cible, joueur) else 4
        vaincu = [False]

        def si_vaincu(unite: 'Unit2') -> None:
            Unused(unite)
            vaincu[0] = True
            Faces.ReadyAll([heros], effect)

        heros.DealDamage(
            [cible], degats, effect,
            if_this_attack_defeats=si_vaincu,
        )

        if vaincu[0] or not cible.card.IsOnField():
            return

        def accrocher(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            AccrocherLeHeros(effect, cible, joueur)

        # « you MAY attach » : facultatif, d'ou `forced=False`.
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Chomp!: attach Alligator Loki to that enemy",
                accrocher,
            ).SetHasNoTargetEffect(),
            forced=False,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chomp,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
