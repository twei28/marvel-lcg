from . import *

# * Patriot's Shield — AMELIORATION signature, custom « CptScorp »
# Cout 1, ressource [wild], trait ITEM.
#
# You get +1 DEF.
# Hero Interrupt: When you would take damage from an attack, you may move 1
#   of that damage here. When Patriot's Shield reaches 3 damage, discard it.
#
# C'est la carte que la face alter-ego `pt001b` va chercher dans le deck et
# la defausse (voir pt001b.py, et le piege de l'etoile d'unicite : le nom
# effectif est « Patriot's Shield », SANS le « * »).
#
# ---------------------------------------------------------------------------
# CAPACITE 1 : « You get +1 DEF »
#
# Carte de reference : `03009` Captain America's Shield, meme structure
# (amelioration ITEM posee sur l'identite qui donne +1 DEF), ecrite
# `*AbilityFactory.GiveKeywordToAttached(..., defense=1)`. Ici la cible-chaine
# `"You"` suffit : la carte ne nomme pas son porteur (contrairement a `03009`,
# qui s'attache explicitement a Captain America), elle se pose donc sur
# l'identite du controleur via la capacite « Play » par defaut d'une
# amelioration (card_type/upgrade.py:14-18).
#
# ⚠ Rend une LISTE d'abilites (l'etoile n'est pas optionnelle).
#
# ---------------------------------------------------------------------------
# CAPACITE 2 : LES DEGATS S'ACCUMULENT **SUR LA CARTE**
#
# Carte de reference : `04065` Crossbones' Armor, le seul modele du depot
# pour « les degats vont sur cette carte, et a N degats elle est defaussee ».
# Elle ecrit `Faces.PlaceCountersOn([this], degats, 'damage', effect)` puis
# `if this.GetCounters('damage') >= 5: Faces.DiscardAll([this], effect)`.
#
# TROIS differences avec le modele, toutes voulues :
#
#  1. `04065` deplace TOUS les degats (`message.SetBeInstead(effect)` +
#     `message.will_take_damage`). Ici le texte dit « move **1** OF that
#     damage » : UN SEUL POINT. On emploie donc
#     `message.PreventDamage(1, effect)` (sender_damage.py:808-817), qui
#     retire exactement 1 point de ce que l'identite va encaisser, et on pose
#     1 compteur `damage` sur le bouclier. Le reste des degats passe.
#     `SetBeInstead` aurait tout annule : c'est la lecture inverse.
#  2. Le seuil est 3, pas 5.
#  3. `04065` est un `ForcedInterrupt` ; ici le texte imprime « Hero
#     Interrupt » et « you MAY » : `AbilityType.HeroInterrupt` non force, que
#     le moteur propose au joueur au lieu de l'imposer.
#
# « MOVE 1 OF THAT DAMAGE » : le point PART de l'identite et ARRIVE sur la
# carte (mot-piege `instead` du PROCESSUS-CARTE §5, lecon The Spot). Sans le
# `PreventDamage`, l'identite ET le bouclier encaisseraient.
#
# « from an attack » -> `is_from_attack=True` : les degats de trahison ne
# declenchent rien.
#
# `at_least_damage=1` est le defaut de la fabrique : la capacite n'est pas
# proposee pour 0 degat.
#
# « When Patriot's Shield reaches 3 damage, discard it. » : le controle est
# fait DANS le meme handler, juste apres la pose du compteur — c'est ainsi
# que `04065` l'ecrit, et cela evite une seconde capacite qui devrait ecouter
# la pose de compteurs.


def GetAbilities() -> Sequence['Ability']:

    def patriots_shield(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        if message.will_take_damage <= 0:
            return

        # « move 1 of that damage here » : 1 point, pas tous.
        message.PreventDamage(1, effect)
        Faces.PlaceCountersOn([this], 1, 'damage', effect)

        if this.GetCounters('damage') >= DEGATS_MAX_SUR_LE_BOUCLIER:
            Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            defense=1,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "YourIdentity",
            patriots_shield,
            is_from_attack=True,
        ),
    ]
