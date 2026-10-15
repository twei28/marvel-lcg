from . import *

# Slaying the False Gods 2A (174A) — complot principal, face A (un 2A sans menace avance seul en 2B).
# When Revealed: Search the encounter deck and discard pile for Strengthen the Faith side scheme,
#   reveal it and place 2[per_hero] additional threat on it.
#
# Cartes de reference :
#  - **`01136`** Ultron / sk145a : `Search.EncounterCard(include_discard_pile=True, name=...)` +
#    `face.Reveal(joueur, effect)` ; **`01180`** Legions of Hydra : « place 2 additional threat here »
#    apres la revelation (`Faces.PlaceTokensOn([...], "2*", 'threat', effect)`, le « 2* » = 2 par joueur).
#
# ⚠ Mots-pieges : « Search the encounter deck AND DISCARD PILE » (les deux) ; « reveal it » (la carte
# ENTRE EN JEU avec sa menace de depart, puis on ajoute) ; « 2[per_hero] ADDITIONAL threat on IT » (sur le
# complot annexe revele, pas sur le complot principal ; 2 par joueur, en plus de sa menace de depart) ;
# aucune copie trouvee (les deux sont deja en jeu) : rien ne se passe, la recherche melange le deck
# (comportement natif). Cette face n'est PAS jouee quand le stade 1 finit par « Advance to stage 2B ».


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(effect, include_discard_pile=True, name="Strengthen the Faith", card_type=EncounterSideScheme)
        if face is None:
            return
        face.Reveal(joueur, effect)
        if face.IsInPlay():
            Faces.PlaceTokensOn([face], "2*", 'threat', effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelation),
    ]
