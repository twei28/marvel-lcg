from . import *

# * Gwenpool — ALLIE d'ASPECT (Aggression), custom « jakxin »
# Cout 3, PV 3, ATQ 1*, CTR 1*, [wild], trait AVENGER.
#
# [star] Gwenpool gets +1 ATK for each identity-specific upgrade you control
#   (to a maximum of +2 ATK).
#
# ---------------------------------------------------------------------------
# ⚠ COLLISION DE NOMS — « GWENPOOL »
#
# Le jeu contient DEJA un pack complet `gwenpool` (prefixe `gp`, identite
# « Gwenpool », par Kajislav). Cette carte-ci est un ALLIE homonyme : deux
# cartes distinctes, meme personnage Marvel, aucune collision moteur. RIEN
# n'est corrige cote `gp`, et cette carte ne fait AUCUNE recherche par nom :
# sa seule capacite parle d'elle-meme (`"This"`).
#
# ---------------------------------------------------------------------------
# CARTE DE REFERENCE
#
# `08026` Taskmaster (pack bkw) : meme montage exact pour « X pour chaque
# carte de ta zone de jeu », `AbilityFactory.ThisGainKeyword(<compte>,
# attack=1, change_on_event=OnEvent.PlayAreaCard("YouControlCards"))`. `dt065`
# Colleen Wing et `12013` Ronin emploient la meme fabrique avec un autre
# declencheur de reevaluation.
#
# `OnEvent.PlayAreaCard("YouControlCards")` (on_event.py:183) reevalue le
# bonus des qu'une carte entre ou sort de la zone de jeu du joueur — c'est ce
# qui fait vivre le « pour chaque ».
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « IDENTITY-SPECIFIC upgrade » -> `CardFinder(card_type=Upgrade,
#   card_class='IdentitySpecific')`. `IdentitySpecific` est une classe de
#   carte a part entiere du moteur (card_player.py:33-41 et 69) : c'est la
#   classe donnee a toute carte joueur dont le `desc.Class` vaut « Hero »,
#   donc les cartes signature. Modele d'emploi : `59026` Ancient Rivalry.
#   Ce n'est PAS « une amelioration quelconque » ni « une amelioration
#   attachee a ton identite » : une amelioration signature posee sur un ALLIE
#   compte tout autant.
# « YOU CONTROL » -> `player.GetControlUpgrade(finder)`
#   (player_get.py:42) : la zone de jeu du CONTROLEUR de Gwenpool, jamais
#   celle d'un autre joueur (mot-piege `you control` du PROCESSUS-CARTE §5).
# « to a MAXIMUM of +2 ATK » -> `min(BONUS_ATK_MAX_GWENPOOL, ...)`. Sans ce
#   plafond, un deck signature bien pose donnerait +4 ou +5.
# ATQ 1* / CTR 1* : l'etoile vaut « 1 degat consecutif », lue nativement.


def GetAbilities() -> Sequence['Ability']:

    def ameliorations_signature(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        if player is None:
            return 0
        cartes = list(player.GetControlUpgrade(
            CardFinder(card_type=Upgrade, card_class='IdentitySpecific')
        ))
        for face in cartes:
            ui.append(face)
        return min(BONUS_ATK_MAX_GWENPOOL, len(cartes))

    return [
        AbilityFactory.ThisGainKeyword(
            ameliorations_signature,
            attack=1,
            change_on_event=OnEvent.PlayAreaCard("YouControlCards"),
        ),
    ]
