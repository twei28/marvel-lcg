from . import *

# "Doom Prevails" — evenement signature. SPELL. Cout 3.
# Hero Action: Look at the top 3 cards of the encounter deck. Deal X damage
#   among enemies in play where X equals the number of icons ([star] and
#   [boost]) in those encounter cards' boost areas. If you paid for this card
#   with only [mental] resources, also remove X threat from among schemes in
#   play.
#
# Cartes de reference :
#  - comptage d'icones de boost : 15004 Hex Bolt et ho014,
#    `FacesCounter.CountTotalBoostIcons(faces)` (recette moteur §2) ;
#  - lecture du dessus du deck rencontre SANS le defausser :
#    `Worlds.GetEncounterDeck(effect).GetTops(3)` — la carte dit « look
#    at », les cartes RESTENT en place, contrairement a ho014 qui defausse ;
#  - degats repartis entre plusieurs ennemis : 01046 Energy Daggers ;
#  - retrait de menace sur plusieurs manigances : le litteral `"EachScheme"`
#    de `RemoveThreatFromSchemes` (card_face.py:707), comme bt007a.
#
# ⚠ « LOOK AT the top 3 cards » : on REGARDE, on ne defausse pas. Les trois
# cartes restent sur le deck rencontre dans leur ordre — c'est la difference
# avec « discard the top card of the encounter deck », qui les envoie a la
# defausse (aa014, ho014).
#
# ⚠ « among enemies » / « among schemes » : la repartition appartient au
# joueur. `DealDamage` sur une cible unique choisie serait plus simple mais
# trahirait le texte : on passe donc par la selection multiple du moteur.
#
# ⚠ X peut valoir 0 (trois cartes sans icone de boost) : la carte est alors
# jouee pour rien, ce qui est le comportement imprime.

def GetAbilities() -> Sequence['Ability']:

    def doom_prevails(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        deck = Worlds.GetEncounterDeck(effect)
        sommet = deck.GetTops(3)
        x = FacesCounter.CountTotalBoostIcons(sommet)
        if x <= 0:
            return

        ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
        if ennemis:
            cible = initiator.AskChooseFace(ennemis, effect)
            if cible:
                this.DealDamage([cible], x, effect)

        if effect.GetPaidResources().OnlyHasColor("B"):
            this.RemoveThreatFromSchemes("EachScheme", x, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            doom_prevails,
        ).SetPlay(),
    ]
