from . import *

# Bodyguard

def GetAbilities() -> Sequence['Ability']:

    def garde_du_corps(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)

        # « Search the encounter deck for the minion with the highest printed
        # hit points and put it into play with you with Bodyguard attached to
        # it. » Le sbire le plus costaud du deck : dans le scenario Shocker,
        # c'est Rhino, et le livret le dit (p.15).
        joueur = message.GetToPlayer()
        sbires = CardFinder(card_type=Minion).Checks(
            Worlds.GetEncounterDeckCards(effect))
        if not sbires:
            return
        sbires = sorted(sbires, key=lambda x: x.printed_health)
        sbire = sbires[-1]
        sbire.PutIntoPlay(joueur, effect)
        this.AttachTo2(sbire, effect)

    def sbire_vaincu(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        # « When attached minion is defeated, shuffle it into the encounter deck
        # from the encounter discard pile. » Le sbire n'est pas retire : il
        # revient dans le deck, et le Bodyguard, lui, part a la defausse.
        this = effect.this.CastTo(Attachment)
        sbire = this.GetBindFace()
        if sbire:
            Faces.ShuffleAllTo([sbire], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            garde_du_corps
        ),
        # ⚠ Rend une LISTE, comme `GiveKeywordToInPlayWhenApplyThis` : sans
        # l'etoile, la carte se construit avec une liste dans sa liste et le
        # moteur plante des la generation. `test_cards` ne le voit pas — il
        # appelle `GetAbilities` sans les poser sur une carte.
        *AbilityFactory.GiveKeywordToAttached(
            trait=["ELITE"],
            guard=1,
            health=2,
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.ForcedInterrupt,
            "Attached",
            sbire_vaincu,
        ),
    ]
