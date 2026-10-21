from . import *
from game.selector import Select

# Hell's Kitchen (1) — LIEU (environnement LOCATION).
# Allies and minions in Hell's Kitchen cannot thwart or scheme and gain toughness.
# Action: Confuse and give a tough status card to your identity → search the encounter deck for a minion and reveal it.
#
# Cartes de reference : ip018 (`Ability(NonKeyword, Message.CheckIfUnitCanThwart, ..., SetCannotThwart)` ecrite a la main), sk024 / 32008
# (`Faces.GiveStatus`), `Search.EncounterCard(effect, joueur, include_discard_pile=False, card_type=Minion)` (bw002, ar014),
# 27150 (`CostFunc.Custom(None, fn)`), pu035 (effet continu par lieu : `AfterPlayerMovedInCity`), pu033.
# ⚠ « allies and minions IN Hell's Kitchen » : les allies des joueurs presents et les sbires ENGAGES avec eux (`JoueurDuPersonnage`).
# ⚠ « cannot THWART » = les allies (un sbire ne contre pas) ; « cannot SCHEME » = les sbires : leur manigance est annulee (`SetBeInstead` :
# rien n'arrive, pas de boost), l'activation d'attaque d'un sbire n'est pas touchee. Ni l'identite du joueur ni le vilain ne sont concernes.
# ⚠ « gain toughness » : mot-cle gagne en cours de partie, SANS carte de statut (RECETTES-MOTEUR : `GainToughness` ne pose pas de statut).
# ⚠ « Confuse AND give a tough status card » : COUT, les deux a la fois ; une identite deja confuse ou deja Tough ne peut pas payer.

def GetAbilities() -> Sequence['Ability']:

    def ici(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = JoueurDuPersonnage(face)
        return joueur is not None and Ville.Occupe(effect, joueur, effect.this)

    def tenace_ici(effect: 'Effect', face: 'CardFace') -> int:
        return 1 if ici(effect, face) else 0

    def allie_ici(effect: 'Effect', message: 'Message.CheckIfUnitCanThwart') -> bool:
        return Ally.IsType(message.check_unit) and ici(effect, message.check_unit)

    def sbire_ici(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> bool:
        sbire = message.trigger
        return Minion.IsType(sbire) and ici(effect, sbire)

    def peut_payer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        identite = effect.GetInitiator().GetIdentity()
        return not identite.IsConfused() and not identite.IsTough()

    def payer(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        if not cibles:
            return False
        Faces.GiveStatus(list(cibles), "Confused", effect)
        Faces.GiveStatus(list(cibles), "Tough", effect)
        return True

    def chercher_un_sbire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        sbire = Search.EncounterCard(effect, joueur, include_discard_pile=False, card_type=Minion)
        if sbire is not None:
            sbire.Reveal(joueur, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Ally | Minion), toughness=1, get_new_value=tenace_ici,
            change_on_event=OnEvent.TemplateTrigger(Message.AfterPlayerMovedInCity),
        ),
        Ability(AbilityType.NonKeyword, Message.CheckIfUnitCanThwart, [allie_ici], lambda effect, message: message.SetCannotThwart(effect)),
        Ability(AbilityType.ForcedInterrupt, Message.WhenUnitWouldScheme, [sbire_ici], lambda effect, message: message.SetBeInstead(effect)),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, chercher_un_sbire, conditions=[Ville.AuLieu, peut_payer])
        .SetCostFunc(CostFunc.Custom(
            Select.From("YourIdentity", finder=CardFinder(canbe_status=["Confused"])), payer)),
    ]
