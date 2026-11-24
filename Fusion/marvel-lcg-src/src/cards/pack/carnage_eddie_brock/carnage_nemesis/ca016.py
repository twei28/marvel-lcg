from . import *

# * Meticulous Targeting : COMPLOT ANNEXE (paysage), menace de depart 2 par joueur, Amplify 1, boost 2. Set « Carnage Nemesis ».
# When Revealed: Find Torment and reveal him. (If he is already in play, he engages you.) Torment activates against you. If no enemy activated this way, this card gains surge.
#
# CARTES DE REFERENCE
#  - « Find X and reveal it ; if already in play, it engages you » : `find.md` (`Search.EncounterCard(.., include_discard_pile=True, include_set_aside=True, name=..)` + `face.Reveal(joueur, effect)`), `Worlds.FindCardOnField` pour « deja en jeu » ; engagement : `ar014` (`Minion.EngagePlayer(joueur, effect)`).
#  - « X activates against you » : `bw021` (Imperius Rex) / `11051` : `ennemi.DoActivate(joueur, effect)` ; rend `None` quand l'ennemi n'a pas pu s'activer (`enemy.py:303`).
#  - « If no enemy activated this way, this card gains surge » : `this.GainSurge(1, effect)` (my015).
#  - Menace de depart par joueur (`StartingThreat 2*`) et Amplify 1 : lus nativement dans `desc` (fiche mots-cles/amplify.md), aucun code.
#
# TEXTE CONTRE CODE
#  « FIND Torment and REVEAL him » : en jeu -> il s'engage avec le joueur ; sinon recherche dans le deck, la defausse et la zone de cote, puis revelation (son When Revealed resout, son Quickstrike frappe). « Torment ACTIVATES against YOU » : une activation (attaque ou manigance selon l'etat du joueur) contre le joueur qui revele.
#  « If NO enemy activated this way » : Torment introuvable OU activation impossible -> surge. Chiffres : menace de depart 2 par joueur, Amplify 1, boost 2.


def GetAbilities() -> Sequence['Ability']:

    def meticulous_targeting(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.GetToPlayer()

        torment = Worlds.FindCardOnField(effect, name=NOM_TORMENT, card_type=Enemy)
        if torment is not None:
            if Minion.IsType(torment) and torment.CastTo(Minion).engaged_player is not joueur:
                torment.CastTo(Minion).EngagePlayer(joueur, effect)
        else:
            torment = Search.EncounterCard(
                effect,
                joueur,
                include_discard_pile=True,
                include_set_aside=True,
                name=NOM_TORMENT,
            )
            if torment is not None:
                torment.Reveal(joueur, effect)

        a_active = None
        if torment is not None and torment.IsInPlay():
            a_active = torment.CastTo(Enemy).DoActivate(joueur, effect)
        if a_active is None:
            this.GainSurge(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            meticulous_targeting,
        ),
    ]
