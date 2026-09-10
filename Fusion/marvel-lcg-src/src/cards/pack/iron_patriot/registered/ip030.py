from . import *

# * Ares — SBIRE du deck REGISTERED (17/20). 6 PV, ATQ 3, MNG 2, boost 4.
# AVENGER. OLYMPUS. ELITE.
# Toughness.
# [star] Forced Response: Ares's attacks gain piercing. After Ares attacks and
#   damages a character, stun that character.
# War Tactician — Special: Search your deck for an ATTACK or DEFENSE event and
#   add it to your hand. (Shuffle.)
#
# ⚠ LA LIGNE ETOILEE MELANGE DEUX CHOSES SOUS UNE SEULE ETIQUETTE : « Ares's
# attacks gain piercing » est un etat PERMANENT, pas une Reponse. Seule la
# seconde phrase est la Reponse. On monte donc DEUX capacites, comme le fait
# `04058` * Crossbones, qui imprime la meme paire.
#
# CARTES DE REFERENCE
#  - `04027` * Crossfire : `UnitAttackGainKeyword("This", piercing=True)`.
#  - `01118` * Sonic Converter : « After ... attacks and damages a character,
#    stun that character », mot pour mot.
#  - `25023` * The Bifrost : `Search.PlayerCard(..., include_player_deck=True)`.
#
# TEXTE CONTRE CODE
#  ⚠ « an ATTACK or DEFENSE event » : le trait, pas le mot-cle de jeu. Les deux
#    au choix, d'ou `traits=[...]` (liste OU) et `card_type=Event`.
#  ⚠ « ADD IT TO YOUR HAND » : la carte va en main, elle n'est pas jouee.
#  ⚠ « (Shuffle.) » : `Search` remelange deja le deck fouille.
#  ⚠ Toughness est une BASE NATIVE de sbire.


def GetAbilities() -> Sequence['Ability']:

    def etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        if message.attacked is not None:
            Faces.GiveStatus([message.attacked], "Stunned", effect)

    def tacticien(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            card_type=Event,
            traits=["ATTACK", "DEFENSE"],
        )
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
        AbilityFactory.AfterUnitAttackAndDamageUnit(
            AbilityType.ForcedResponse,
            "This",
            "Character",
            etourdir,
            target_in_play=True,
        ),
        SpecialRegistered("War Tactician", tacticien),
    ]
