from . import *

# * Crusader — ALLIE de campagne (Aggression / Campaign, n° 263). Cout 2. THW 2** / ATK 2**, 4 PV.
# INITIATIVE. SKRULL.
# Response: After Crusader enters play, choose a player -> deal 1 damage to the villain and each
#   minion engaged with that player. Draw 1 card for each enemy defeated this way.
#
# Cartes de reference :
#  - **`ho004`** Pumpkin Bomb / **`04006`** Explosive Arrow : « deal damage to the villain and each minion
#    engaged with that player » = `SetTarget("VillainAndEngagedSamePlayerMinion")` (le choix du joueur est
#    DANS le selecteur) ; « for each enemy defeated this way » = `if_this_attack_defeats` de `DealDamage`,
#    rappele une fois PAR unite vaincue par CES degats-la.
#  - **`01083`** Mockingbird : `AfterCardEnterPlay(Response, "This", ...)` pour « After X enters play ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « INITIATIVE » est un TRAIT imprime (ligne de traits en italique), pas un mot-cle : aucune regle ne
#    l'accompagne sur la carte (voir defs/campagne_cartes_questions.md, Q1) ;
#  - « choose a PLAYER » : le joueur designe l'engagement dont les sbires sont touches ; le mechant l'est
#    toujours ;
#  - « each ENEMY defeated THIS WAY » : sbires ET mechant, mais seulement ceux que CES degats achevent ;
#  - « Response » : optionnelle, elle part apres l'entree en jeu (pas une Interruption).


def GetAbilities() -> Sequence['Ability']:

    def crusader(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()

        vaincus: List['Unit2'] = []

        def vaincu(unit: 'Unit2') -> None:
            vaincus.append(unit)

        this.DealDamage(effect.targets, 1, effect, if_this_attack_defeats=vaincu)

        if vaincus:
            joueur.DrawUp(len(vaincus), effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            crusader,
        ).SetTarget("VillainAndEngagedSamePlayerMinion"),
    ]
