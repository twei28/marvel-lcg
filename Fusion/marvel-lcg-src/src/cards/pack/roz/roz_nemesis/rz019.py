from . import *

# * Minotaur — ATTACHEMENT nemesis, boost 2. CREATURE. SCH -2 / ATK +3★.
# Attach to Dario Agger. If you cannot, this card gains incite 1 and surge.
# Dario Agger gets +3 hit points and gains retaliate 1.
# [star] Dario Agger attacks gain overkill.
#
# CARTES DE REFERENCE (PROCESSUS-CARTE etape 2)
#  - « Attach to X. If you cannot, ... » : `01163` Genetically Enhanced (`AttachToFaceWhenPutIntoPlay(finder,
#    if_cannot_gain_surge=True)` + `GiveKeywordToAttached(...)`) ; `50070` Night Vision Goggles (attache par nom).
#  - bonus d'un attachement : `13029` Beetle Armor (`health=N`), `GiveKeywordToAttached(attack=, scheme=,
#    retaliate=, health=)` (asset.py:6). Les SCH -2 / ATK +3 IMPRIMES a gauche de la carte sont des BONUS
#    de l'attache (aucun attachement n'imprime de stats dans `desc`).
#  - [star] overkill : `ho016` / `50107b` : `UnitAttackGainKeyword(<qui>, overkill=True)`.
#  - Incite CONDITIONNEL : `jj021` / `ap018` : `*AbilityFactory.ThisGainIncite(fn, incite=1, change_on_event=OnEvent.CardInPlay(...))`
#    (actif a la revelation, hors jeu) ; Renfort conditionnel : `if_cannot_gain_surge=True` (`01163`).
#
# MOTS-PIEGES
#  - « Dario Agger » : le sbire NOMME (`CardFinder(name="Dario Agger")`), pas « le sbire aux PV les plus hauts ».
#  - « IF YOU CANNOT, this card gains incite 1 AND surge » : les deux SEULEMENT si Dario n'est pas en jeu ; ils ne
#    s'appliquent pas quand elle s'attache.
#  - « +3 hit points AND retaliate 1 » (de Dario) : deux mots-cles ; « SCH -2 / ATK +3 » : bonus imprimes.
#  - « [star] attacks gain overkill » : permanente, toujours active (convention 04125) ; ne vaut que pour Dario.
def GetAbilities() -> Sequence['Ability']:

    def sans_dario(effect: 'Effect') -> int:
        # 1 tant que Dario Agger n'est PAS en jeu : alors la carte gagne Incite 1 (et Renfort, plus bas).
        return 0 if Worlds.FindCardOnField(effect, name=NOM_DARIO) else 1

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_DARIO),
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.ThisGainIncite(
            sans_dario,
            incite=1,
            change_on_event=OnEvent.CardInPlay(CardFinder(name=NOM_DARIO)),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_DARIO),
            health=3,
            retaliate=1,
            attack=3,
            scheme=-2,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "AttachedMinion",
            overkill=True,
        ),
    ]
