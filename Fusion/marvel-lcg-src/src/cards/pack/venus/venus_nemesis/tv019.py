from . import *

# Salvaged Scales — TRAITRISE, boost 2. x2.
# When Revealed: Place 2 threat on the main scheme. If Jasper Barlow is in play, place a tough
#   status card on the villain and each minion engaged with you.
#
# CARTES DE REFERENCE
#  - `50134` / `ho015` : `this.PlaceThreatOnSchemes("MainScheme", n, effect)` ;
#    `tv017` (meme pack) : sbires engages avec le joueur de la revelation.
#
# TEXTE CONTRE CODE
#  ⚠ « 2 threat on the MAIN scheme » : le complot principal seul (pas un complot annexe).
#  ⚠ « If Jasper Barlow IS IN PLAY » : condition de PRESENCE (n'importe ou en jeu, engage avec
#    qui que ce soit) ; sans lui, SEULE la menace est posee. Nom sans l'etoile (RECETTES §6).
#  ⚠ « the VILLAIN AND EACH minion engaged WITH YOU » : le vilain + les sbires engages avec
#    le joueur de la revelation, pas ceux des autres joueurs.
#  x2 : deux exemplaires au set nemesis, un seul card_id.


def GetAbilities() -> Sequence['Ability']:

    def scales(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)
        joueur = message.GetToPlayer()
        jasper = Worlds.FindCardsOnField(effect, name=NOM_JASPER)
        if not any(f is not None and f.card.IsOnField() for f in jasper):
            return
        cibles: List['CardFace'] = []
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            cibles.append(vilain)
        if joueur is not None:
            cibles.extend(m for m in joueur.GetEngagedMinions() if m is not None)
        if cibles:
            Faces.GiveStatus(cibles, "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            scales,
        ),
    ]
