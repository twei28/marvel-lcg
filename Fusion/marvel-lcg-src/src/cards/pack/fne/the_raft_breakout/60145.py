from . import *

# * Baron Zemo (ELITE, HYDRA, PRISONER) — Villainous : base.
# Treat each ally with threat on it as a DECEIVED minion with a blank text
#   box. Its SCH is equal to its base THW and it does not take consequential
#   damage.
# When Revealed: Place 1 threat on an ally without threat on it. It engages
#   its controller.
# Gabarit `deceived_minion` (pack "") comme `influenced_minion` (60100).
# ⚠ Harnais du 18/09/2026 : le cadre GiveKeywordToInPlayWhenApplyThis(apply=)
# ne sait pas DEFAIRE la conversion sur retrait du jeton (la face alliee,
# echangee, est ignoree par `is_setting_as` et l'evenement Token(Ally) ne voit
# plus qu'un sbire) ; et TreatAsMinion pose sur Zemo des temporaires qu'on ne
# peut pas retirer. Trois ecouteurs explicites, conversion inline
# (ConvertirEnDeceived / RendreLAllie, __init__.py) :
#   1. jeton threat pose sur un allie -> conversion (et Zemo entre en jeu ->
#      les allies qui en portent deja) ;
#   2. dernier jeton retire d'un sbire DECEIVED -> il redevient allie ;
#   3. Zemo quitte le jeu -> chaque sbire DECEIVED redevient allie, jetons
#      conserves (FAQ du livret) ;
#   4. sbire DECEIVED vaincu -> `Card.CheckIfCanDiscard` remet la face
#      imprimee, l'allie va dans la defausse de son proprietaire (natif).

def GetAbilities() -> Sequence['Ability']:

    def jeton_pose(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> None:
        ConvertirEnDeceived(message.trigger, effect)

    def allie_avec_menace(effect: 'Effect', message: 'Message.AfterCardPlacedToken') -> bool:
        face = message.trigger
        return message.token_name == 'threat' and Ally.IsType(face) and face.IsInPlay() \
            and face.GetTokens('threat') > 0 and not face.card.IsAsOtherCard()

    def jeton_retire(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> None:
        RendreLAllie(message.trigger, effect)

    def deceived_sans_menace(effect: 'Effect', message: 'Message.AfterCardRemovedToken') -> bool:
        face = message.trigger
        return message.token_name == 'threat' and EstUnDeceived(face) and face.GetTokens('threat') <= 0

    def entre_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        for allie in list(Worlds.GetOnFieldAllies(effect)):
            if allie.GetTokens('threat') > 0 and not allie.card.IsAsOtherCard():
                ConvertirEnDeceived(allie, effect)

    def quitte_le_jeu(effect: 'Effect', message: 'Message.WhenCardLeavePlay') -> None:
        for sbire in list(Worlds.GetOnFieldMinions(effect)):
            if EstUnDeceived(sbire):
                RendreLAllie(sbire, effect)

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        allies = [a for a in Worlds.GetOnFieldAllies(effect) if a.GetTokens('threat') <= 0]
        if not allies:
            return
        cible = allies[0] if len(allies) == 1 else joueur.AskChooseFace(allies, effect)
        if cible is not None:
            Faces.PlaceTokensOn([cible], 1, 'threat', effect)

    return [
        Ability(AbilityType.NonKeyword, Message.AfterCardPlacedToken, [allie_avec_menace], jeton_pose),
        Ability(AbilityType.NonKeyword, Message.AfterCardRemovedToken, [deceived_sans_menace], jeton_retire),
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", entre_en_jeu),
        AbilityFactory.WhenCardLeavePlay(AbilityType.NonKeyword, "This", quitte_le_jeu),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
