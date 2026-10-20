from . import *

# * Lilandra (Lilandra Neramani) — ALLIE de scenario (Majestrix's Verdict), sans cout. SHI'AR. STARJAMMER.
# PV 4, CTR 1, ATQ 2 (1 degat consecutif).
# Does not count against your ally limit.
# Forced Response: After Lilandra enters play, reveal the set aside Shi'ar Throne side scheme.
# If Lilandra is removed from the game, the players lose the game.
#
# Cartes de reference :
#  - « Does not count against your ally limit » : `ThisNotCountAllyLimit()`, modele OFFICIEL 50091 Rescued Captive.
#  - « After X enters play, reveal the set aside side scheme » : `AfterCardEnterPlay(ForcedResponse, "This")`
#    (modele 01083 Mockingbird pour le declencheur) + `SetupCards.Reveal(only_set_aside=True)` (setup_cards.py).
#  - « If Lilandra is removed from the game, the players lose » : `AfterCardLeavePlay("This")` (porte
#    NoOutOfPlayLimit) quand la destination est la zone des cartes retirees ; `Worlds.SetGameOver(False)`
#    (modele 50089b). Lilandra GLISSEE et retiree par 2A : `RetirerDeLaPartie` (gs118a) applique la meme regle.
#
# ⚠ Mots-pieges : « reveal the SET ASIDE Shi'ar Throne SIDE SCHEME » : rien si le Trone est deja en jeu (face
# manigance ou soutien) ; « REMOVED FROM THE GAME » ≠ vaincue (vaincue, elle est glissee sous la prison).


def GetAbilities() -> Sequence['Ability']:

    def reveler_le_trone(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        SetupCards.Reveal(effect, only_set_aside=True, name=TRONE, card_type=SchemeSide2)

    def retiree(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> bool:
        return message.into_area is effect.world.area_removed

    def defaite(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        Unused(message)
        if not effect.world.is_game_over:
            Worlds.SetGameOver(False, effect)

    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, "This", reveler_le_trone),
        AbilityFactory.AfterCardLeavePlay(AbilityType.NonKeywordBold, "This", defaite, conditions=[retiree]),
    ]
