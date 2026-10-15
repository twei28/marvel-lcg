from . import *

# * Mikey (face alter-ego) — TEENAGER. MUTANT. TURTLE.
# REC 3 — HS 6 / PV 11
# Setup: Put the I'm Here to Help player side scheme into play.
# Action: Discard 1 card from your hand -> search your deck and discard pile
#   for up to 2 NUNCHUCK upgrades and put them into play, exhausted. (Shuffle.)
#
# Regle de l'insert : « When using the Alter-Ego ability to place the NUNCHUCK
# into play, they enter play exhausted. »
#
# Cartes de reference :
#  - Setup + fouille du deck : `aa001b` (Agatha) et `jubilee/47001b` :
#    `WhenCardSetup("This", op)` + `Search.PlayerCard(include_player_deck=True,
#    finder=CardFinder(card_ids=[...]))` puis `PutIntoPlay` ;
#  - action d'alter-ego imprimee SUR la face alter-ego : `si001b` —
#    `AbilityType.Action` (jamais AlterEgoAction, reserve aux AUTRES cartes) ;
#  - cout « defausse 1 carte de la main » : `sunfire/sf010` —
#    `CostFunc.Discard("YourHandCards", range=(1, 1))` ;
#  - mise en jeu inclinee : `Face.PutIntoPlay(player, effect, exhaust=True)`
#    (face_on_event.py:170), recherche + mise en jeu : `next_evol/40019` Lock and Load.
#
# ⚠ Mots-pieges :
#  - « up to 2 » : deux recherches successives, `may=True` pour pouvoir
#    s'arreter. Le « (Shuffle.) » est le comportement PAR DEFAUT de Search.
#  - « deck AND discard pile » : include_discard_pile=True.
#  - « NUNCHUCK upgrades » : trait NUNCHUCK ET type Upgrade.
#  - Setup : la manigance tm009 est dans le deck de depart (hero_deck, 15
#    cartes dont elle). # TODO-QUESTION (question 1 : lecture « Put ... into
#    play » = fouille du deck, tm009 etant l'une des 15 cartes du deck).
#  - Le « → » est un COUT : defausser avant de chercher ; sans carte en main
#    l'Action n'est pas jouable.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        manigance = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            finder=CardFinder(card_ids=["tm009"]),
        )
        if manigance:
            manigance.PutIntoPlay(initiator, effect)

    def chercher_les_nunchucks(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return
        for _ in range(2):
            face = Search.PlayerCard(
                effect,
                initiator,
                include_player_deck=True,
                include_discard_pile=True,
                trait="NUNCHUCK",
                card_type=Upgrade,
                may=True,
            )
            if not face:
                break
            face.PutIntoPlay(initiator, effect, exhaust=True)

    return [
        AbilityFactory.WhenCardSetup(
            "This",
            mise_en_place,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chercher_les_nunchucks,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
