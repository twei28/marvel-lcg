from . import *

# * Ultimate Nullifier — AMELIORATION de campagne ('Pool / Campaign, n° 285). Cout 0. ITEM. TECH. Temporary.
# Attach to a SKRULL enemy.
# Temporary.
# Attached enemy cannot activate.
# While Nullifier is attached to the villain, it gains 1[per_hero] hazard icon ([hazard]).
#
# Cartes de reference :
#  - **`magneto/49007`** Wrapped in Metal : `CanPlayThisUpgradeCard(...)` + `EnemyCannotActivate(NonKeyword,
#    "AttachedMinion")` pour « attached enemy cannot activate » (ici « AttachedEnemy » : sbire OU mechant).
#  - **`necroverse/nv006`** / **`sm/27144`** : « gains 1 hazard icon » = `ThisGainKeyword(fn, hazard=1,
#    change_on_event=...)` : l'icone est portee par l'AMELIORATION elle-meme, que `Worlds.GetHazardIcons` compte.
#  - **fiche `hazard.md`** et **`temporary.md`**.
#
# ⚠ Mots-pieges :
#  - « cannot ACTIVATE » : ni attaque ni manigance ni activation pour le sbire OU le mechant porteur ;
#  - « WHILE attached to the VILLAIN » : l'icone n'existe que sur un MECHANT ; sur un sbire : aucune ;
#  - « 1[per_hero] hazard icon » : AUTANT D'ICONES que de joueurs (solo : 1 ; 2 joueurs : 2) ;
#  - « TEMPORARY » : defaussee a la fin du round.


def GetAbilities() -> Sequence['Ability']:

    def icones_si_sur_le_mechant(effect: 'Effect', ui: List['CardFace']) -> int:
        porteur = effect.this.GetBindFace()
        if porteur is None or not Villain.IsType(porteur):
            return 0
        return Worlds.GetPlayerNumIcon(effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy, trait="SKRULL")),
        AbilityFactory.EnemyCannotActivate(
            AbilityType.NonKeyword,
            "AttachedEnemy",
        ),
        AbilityFactory.ThisGainKeyword(
            icones_si_sur_le_mechant,
            hazard=1,
            change_on_event=OnEvent.AttachedMove("This"),
        ),
    ]
