from . import *

# * Double-Cross — MANIGANCE ANNEXE DE JOUEUR 0 [mental], aspect Justice (Elektra Natchios 34). Menace 2 par joueur. Victory 0.
# When Defeated: If there is not already a copy of Double-Cross in the victory display, shuffle the set-aside Backstab, Misdirect,
#   and Sabotage treachery cards into the top 10 cards of the encounter deck (or the whole deck if there are fewer than 10 cards).
#
# MOTS-CLES (fiches lues) : linked.md (les trois traitrises portent `desc.Linked = "Double-Cross"` : le moteur les fabrique dans
# `world.aside_deck` a l'entree de cette carte ; c'est CETTE carte qui decide de leur sort), victory (Victory 0 : desc.Victory "0").
#
# CARTES DE REFERENCE
#  - `43021` Specialized Training : « When Defeated » d'une manigance de joueur liee = `WhenSchemeBeDefeated(WhenDefeated, "This", fn)`.
#  - `63023` Hunting Shadows (meme pack) : `Worlds.GetEncounterDeck`, `Card.MoveToTop`, `Deck.Shuffle(effect, only_for_most_top=N)`.
#
# TEXTE CONTRE CODE
#  ⚠ « If there is NOT ALREADY a copy IN THE VICTORY DISPLAY » : seule la 1re copie vaincue declenche l'effet ; la carte vaincue n'est
#    pas encore dans la pile de victoire pendant « When Defeated » (cas : une 2e copie deja dans la pile -> rien ne bouge).
#  ⚠ « the SET-ASIDE » Backstab, Misdirect, Sabotage : les trois cartes de la zone de mise de cote, pas celles deja revelees.
#  ⚠ « into the TOP 10 cards » : on melange ces 3 cartes avec les 10 premieres du deck (13 cartes) ; « or the whole deck if fewer than 10 » :
#    avec moins de 10 cartes, tout le deck est melange avec elles.


def GetAbilities() -> Sequence['Ability']:

    def double_cross(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)
        for face in Worlds.VictoryDisplay(effect).Get(True):
            if face.paper.card_id == "63034" and face is not effect.this:
                return
        cartes = [f for f in Worlds.GetSetAsideAreaCards(effect) if f.paper.card_id in ("63035", "63036", "63037")]
        if not cartes:
            return
        paquet = Worlds.GetEncounterDeck(effect)
        n = min(10, paquet.GetSize())
        for face in cartes:
            face.card.MoveToTop(paquet, effect)
        paquet.Shuffle(effect, only_for_most_top=n + len(cartes))

    return [
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            double_cross,
        ),
    ]
