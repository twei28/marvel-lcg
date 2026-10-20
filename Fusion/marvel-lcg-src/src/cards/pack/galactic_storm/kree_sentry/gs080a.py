from . import *

# Self-Destruct Sequence (2A) — MANIGANCE PRINCIPALE, stade 2 (Kree Sentry).
# When Revealed: If the Outpost Collapse Protocol side scheme is in play, place 2[per_hero] threat and 1 acceleration
#   token on it. Otherwise, search the encounter deck and discard pile for the Outpost Collapse Protocol side scheme and
#   reveal it.
#
# Cartes de reference :
#  - « When Revealed » d'une face A : `WhenThisRevealed(None, op)`, modele gs118a (Majestrix).
#  - « search the encounter deck and discard pile ... and reveal it » : `Search.EncounterCard(include_discard_pile=True,
#    ..)` + `face.Reveal(joueur, effect)`, modele fne 60185 Police Cordon.
#  - « place 2[per_hero] threat » : `PlaceThreatOnSchemes([cible], "2*", effect)` (modele gs136) ;
#    « 1 acceleration token » : `PlaceAccelerationToken(1, effect)` (modele aos 50082).
#
# ⚠ Mots-pieges : « IF the side scheme is IN PLAY » (en jeu, pas glissee ni mise de cote) ; « OTHERWISE » : la
# recherche ne se fait que si elle n'est PAS en jeu, et le Hinder 2[per_hero] de la carte revelee s'applique alors ;
# la menace ET le jeton d'acceleration vont sur la MEME carte (Outpost Collapse Protocol) ; recherche dans le deck ET la
# defausse rencontre.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        effondrement = EnJeu(effect, OUTPOST, SchemeSide2)
        if effondrement is not None:
            effect.this.PlaceThreatOnSchemes([effondrement], "2*", effect)
            effondrement.PlaceAccelerationToken(1, effect)
            return
        face = Search.EncounterCard(effect, include_discard_pile=True, name=OUTPOST, card_type=SchemeSide2)
        if face:
            face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
