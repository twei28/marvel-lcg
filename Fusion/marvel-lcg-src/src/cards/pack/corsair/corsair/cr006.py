from . import *
# Ace Pilot. Amelioration SKILL, cout 2.
#
# Hero Response: After you play an ATTACK or THWART event, exhaust Ace Pilot → ready your identity and a VEHICLE you
#   control.
#
# Cartes de reference : 47004 Jubilee's Coat (`AfterPlayerPlayedCard(HeroResponse, "You", CardFinder2(...), op)` +
# `Exhaust("This")`) ; `traits=[...]` d'un CardFinder est un OU (RECETTES §4).
# ⚠ « your identity AND a VEHICLE » : les DEUX se redressent. Sans VEHICLE en jeu, l'identite se redresse quand meme.
def GetAbilities() -> Sequence['Ability']:
    def pilote(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        Faces.ReadyAll([joueur.GetIdentity()], effect)
        vehicules = [f for f in Worlds.FindCardsOnField(effect, trait="VEHICLE")
                     if f.IsInPlay() and f.GetControlByPlayer() is joueur]
        if not vehicules:
            return
        choisi = vehicules[0] if len(vehicules) == 1 else joueur.AskChooseFace(
            vehicules, effect, prompt="Ready a VEHICLE you control", forced=True)
        if choisi is not None:
            Faces.ReadyAll([choisi], effect)
    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(traits=["ATTACK", "THWART"], card_type=Event),
            pilote,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
