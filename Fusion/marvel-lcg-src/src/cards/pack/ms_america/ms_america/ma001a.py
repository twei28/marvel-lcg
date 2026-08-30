from . import *

# * Ms. America — FACE HEROS, custom « jakxin »
# PV 14 / ATQ 2 / CTR 1 / DEF 2 / MNG 4, traits STARLING + YOUNG AVENGER.
#
# Star-Gaze — Response: After you play a [[SUPERPOWER]] card, if that card's
#   printed resource was:
#     [physical] – Deal 1 damage to an enemy.
#     [energy]   – Heal 1 damage from Ms. America.
#     [mental]   – Remove 1 threat from a scheme.
#     [wild]     – Ready Ms. America.
#
# PV/ATQ/CTR/DEF/MNG sont lus NATIVEMENT depuis `desc` : rien a coder pour
# eux (bases automatiques du guide).
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE
#
# `av007` Unlikely Allies (pack agent_anti_venom) : meme structure « selon la
# ressource IMPRIMEE de la carte, telle branche », meme lecture
# `carte.printed_resource` avec un compteur par couleur, meme rendu par une
# `ForChoiceAbility` par branche passee a `player.ChooseAbilities`. `53018`
# Redwing fait de meme.
#
# Le DECLENCHEUR, lui, vient de `60037a` Echo (« After you play an aspect
# event ») : `AbilityFactory.AfterPlayerPlayedCard(AbilityType.Response,
# "You", <filtre de carte>, ...)`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « After you PLAY » -> `AfterPlayerPlayedCard`, pas `WhenPlayerPlayCard` :
#   la Response resout APRES la carte. C'est ce qui permet a ma006 Star
#   Flight (Hero Interrupt, donc AVANT) d'avoir deja donne le trait
#   SUPERPOWER a l'evenement quand Star-Gaze regarde.
# « YOU play » -> `"You"`, jamais `"AnyPlayer"` : en multijoueur la carte
#   jouee par le voisin ne declenche rien.
# « a [[SUPERPOWER]] card » -> `CardFinder(trait=TRAIT_SUPERPOWER)`. « card »
#   et non « event » : ma005/ma006/ma007 sont des AMELIORATIONS SUPERPOWER,
#   elles declenchent Star-Gaze en entrant en jeu.
# « that card's PRINTED resource » -> `printed_resource`, PAS ce qui a ete
#   depense pour la payer. Mot-piege releve : `using_res=` existe sur
#   d'autres fabriques et aurait rendu « paye avec », ce que le texte ne dit
#   pas.
# « Response » nu -> `AbilityType.Response`. Le texte n'ecrit pas « Hero
#   Response » : mais la capacite est IMPRIMEE SUR LA FACE HEROS, elle
#   n'existe donc pas en identite civile — le moteur s'en charge, la face
#   alter-ego est une autre carte.
#
# Les quatre branches vivent dans `ResoudreStarGaze` (helper du set) parce
# que ma008 Energy Infusion doit pouvoir les rejouer en forcant la couleur.


def GetAbilities() -> Sequence['Ability']:

    def star_gaze(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        player = message.GetToPlayer()
        if player is None:
            return

        couleurs = CouleursImprimeesDe(effect, message.played_face)
        ResoudreStarGaze(effect, player, couleurs)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait=TRAIT_SUPERPOWER),
            star_gaze,
        ).SetName(NOM_STAR_GAZE),
    ]
