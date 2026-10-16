from . import *

# * Baxter Blaster — ATTACHEMENT (Baxter's Lab 5/22). TECH. WEAPON. Boost : etoile seule.
# Attach to Baxter Stockman.
# [star] Forced Response: After Baxter Stockman attacks and damages a friendly character, daze them.
# Hero Action: Exhaust your hero or spend 2 resources of any type -> discard this card.
# [star] Boost: Attach Baxter Blaster to Baxter Stockman.
#
# Cartes de reference : `01118` Sonic Converter (« Attach to Klaw » + « After Klaw attacks and damages
# a character, stun that character » = `AttachToFaceWhenPutIntoPlay` + `AfterUnitAttackAndDamageUnit(
# ForcedResponse, ..., "Character", target_in_play=True)` + `PlayerActionToDiscardThis`) ; `aa018`
# pour « Exhaust your hero OR spend … » en DEUX actions (RECETTES §5/§3) ; `04132` Red Skull's Luger pour
# « Boost: Attach … to X » = `WhenThisBoostAttachTo`.
#
# DECISION UTILISATEUR (16/10/2026, Q1) : le scan imprime une etoile dans la case ATQ de l'attachement (« ATK ★ »)
# sans qu'AUCUN texte ne definisse sa valeur. Lecture provisoire : AUCUN bonus d'ATQ (l'etoile ne
# signale que la capacite etoilee du texte). Voir .planning/tmnt/baxter-questions.md, Q1.
#
# Mots-pieges : « Baxter Stockman » = le VILAIN (tx001-tx003, jamais le sbire td015) ; « attacks AND
# damages » (aucune carte si le coup est entierement prevenu) ; « daze THEM » = le personnage touche ;
# « Exhaust your HERO » (forme heros) / « spend 2 resources of ANY type » (`Cost("2")`) = deux couts
# alternatifs, deux capacites ; « hero action » : reservee a la forme heros.


def GetAbilities() -> Sequence['Ability']:

    def hebeter(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacked], "Dazed", effect)

    baxter = CardFinder(card_ids=IDS_BAXTER, card_type=Villain)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(baxter),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            baxter,
            "Character",
            hebeter,
            target_in_play=True,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Exhaust("YourHero")),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("2")),
        AbilityFactory.WhenThisBoostAttachTo(baxter),
    ]
