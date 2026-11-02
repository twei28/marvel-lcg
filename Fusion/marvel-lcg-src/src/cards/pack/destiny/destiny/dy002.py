from . import *

# * Glimpse of the Future : AMELIORATION signature PERMANENTE (CONDITION. PSIONIC.), sans cout, mise en jeu a la mise en place. Permanent. Setup.
# Precognition — Action: Exhaust Glimpse of the Future -> look at the top 3 cards of the encounter deck. Tuck one under this card so that only its boost field is visible and shuffle the other two into the encounter
# deck. Discard it at the end of the round. (« Discard it at the end of the round » : precision du FR 1.2, absente de la beta EN 1.0.)
#
# CARTES DE REFERENCE
#  - `40004` Precognition (Cable) : `joueur.LookAtDeck("EncounterDeck", n, effect)` + choix d'une face.
#  - `sn014` / `su012` : `TuckCardUnderHere(face, effect)` sous une carte ; `peek=True` garde la carte visible (zone des cartes glissees, `GetPlacedCardArea`).
#  - `bw016` : `WhenRoundEnd(ForcedInterrupt, None, op)` pour une action de fin de round.
#  - `permanent.md`, `setup.md` : mots-cles lus NATIVEMENT dans `desc`, aucun script.
#
# TEXTE CONTRE CODE
#  « the top 3 cards of the encounter deck » : 3 cartes (moins si le deck est plus court). « Tuck ONE under this card » : le joueur choisit, la carte reste visible (zone de boost seule lisible). « shuffle THE OTHER TWO
#    into the encounter deck » : les deux autres restent dans le deck, qui est melange. « Discard it at the end of the round » : toute carte glissee ici est defaussee (defausse RENCONTRE) en fin de round.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def precognition(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        faces = joueur.LookAtDeck("EncounterDeck", 3, effect)
        if not faces:
            return
        choisie = joueur.AskChooseFace(faces, effect, prompt="Tuck one card under Glimpse of the Future", not_move=True)
        if choisie is None:
            return
        this.TuckCardUnderHere([choisie], effect, peek=True)
        reste = [f for f in faces if f is not choisie]
        Faces.ShuffleAllTo(reste, "EncounterDeck", effect)

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        glissees = list(this.GetPlacedCardArea().Get())
        if glissees:
            Faces.DiscardAll(glissees, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            precognition,
        ).SetName("Precognition")
        .SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.WhenRoundEnd(
            AbilityType.ForcedInterrupt,
            None,
            fin_de_round,
        ),
    ]
