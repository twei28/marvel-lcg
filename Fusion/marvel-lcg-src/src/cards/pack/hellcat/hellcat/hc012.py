from . import *
# * She-Hulk (Jennifer Walters) — ALLIEE signature ALTERNATIVE, cout 3,
# [mental]. AVENGER. GAMMA. CTR 2 (1 conseq.) / ATQ 2 (1 conseq.), 3 PV.
# She-Hulk gets +1 hit point for each [mental] resource used to pay for her.
# Response: After She-Hulk attacks and defeats a minion, search your discard
#   pile for an event with a printed [mental] resource and add it to your hand.
#
# Ajoutee par l'auteur « sur demande » a la place d'Iron Man : deck
# `hellcat_she_hulk` (decision utilisateur du 11/09/2026).
# Modeles : 28018 Moon Girl (`AfterYouPlayThisFromHand` + `paid_resources`),
# 01051 Tigra (`AfterUnitAttackAndDefeatUnit(Response, "This", Minion)`),
# `Gain(effect, 1, health=n)` pour des PV permanents (face_gain.py:13).
# ⚠ ForcedResponse pour les PV : c'est un effet passif, sans choix du joueur.

def GetAbilities() -> Sequence['Ability']:

    def pv_bonus(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        n = message.paid_resources.GetColor("B")
        if n > 0:
            this.Gain(effect, 1, health=n)

    def she_hulk(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        face = Search.PlayerCard(effect, joueur, include_player_deck=False, include_discard_pile=True, card_type=Event, has_printed_res="B")
        if face is not None:
            Faces.AddToHand([face], joueur, effect)

    return [
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.ForcedResponse,
            pv_bonus,
        ),
        AbilityFactory.AfterUnitAttackAndDefeatUnit(
            AbilityType.Response,
            "This",
            Minion,
            she_hulk,
        ),
    ]
