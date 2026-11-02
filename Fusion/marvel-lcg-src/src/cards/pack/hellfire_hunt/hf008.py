from . import *

# Psionic Soulmates : soutien Basic, cout 2. Team-Up (Betsy Braddock et Rachel Summers), Max 1 per deck.
# Response: After you play a PSIONIC card, shuffle that card into your deck and exhaust this card -> draw 1 card.
#
# Cartes de reference : sy007 / 01128 (Team-Up, `desc.TeamUp`), bg011 (`message.played_face`), `Faces.ShuffleAllTo([face], deck, effect)` (Hera),
# `AbilityFactory.AfterPlayerPlayedCard` (play.py), `CostFunc.Exhaust("This")`.
# ⚠ TEAM-UP : pas de `desc.TeamUp` (le chargeur l'exige pour les EVENEMENTS avec `.SetTarget("TeamUp")` ; KeyError sur un soutien) : la condition « Betsy Braddock
# ET Rachel Summers en jeu » est portee par la Response (`PersonnageEnJeu`, __init__.py), comme hc022 Divas (docs/reference/mots-cles/teamup.md). Le deckbuilder
# n'applique donc aucune restriction Team-Up a cette carte (ecart note).
# ⚠ « that card » : la carte PSIONIC qu'on vient de jouer (evenement : deja en defausse ; allie : en jeu) ; le melange est FACULTATIF ?
# Non : « shuffle ... and exhaust this card -> draw 1 » : c'est la Response ENTIERE qui est facultative (toutes les Response le sont).
def GetAbilities() -> Sequence['Ability']:
    def equipe_presente(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        return PersonnageEnJeu(effect, ["Betsy Braddock", "Psylocke"]) and PersonnageEnJeu(effect, ["Rachel Summers", "Marvel Girl"])

    def soulmates(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        joueur = JoueurDe(effect)
        face = message.played_face
        if face is not None:
            Faces.ShuffleAllTo([face], joueur.player_deck, effect)
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait="PSIONIC"),
            soulmates,
            conditions=[equipe_presente],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
