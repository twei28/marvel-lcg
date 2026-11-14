from . import *

# Seeing Red — TRAITRISE NEMESIS x2 (3/5, 4/5). Boost 1.
# Discard the top 2 cards from your deck. If a card with a printed [physical] resource was discarded this way, take 2
# indirect damage.
#
# Cartes de reference :
#  - `ch021` Downtown Attack (meme auteur) : `WhenThisRevealed(None, op)` + `message.GetToPlayer()` +
#    `this.DealIndirectDamage(identite, N, effect)` (degats INDIRECTS, repartis par le joueur).
#  - `10026` Abomination : `FacesCounter.GetPrintedResources([face]).r` pour « a printed [physical] resource ».
#  - `Player.DiscardDeckTopCards(n, effect)` rend la LISTE des cartes defaussees.
#
# ⚠ Mots-pieges :
#  - Texte SANS « When Revealed » imprime : c'est l'effet de la traitrise, il part a la revelation.
#  - « If A card ... was discarded THIS WAY » : au moins UNE des 2 cartes defaussees, et 2 degats au total (pas 2 par
#    carte rouge).
#  - « INDIRECT » : le joueur repartit entre son identite et ses allies, sans defense possible.
def GetAbilities() -> Sequence['Ability']:

    def seeing_red(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        faces = joueur.DiscardDeckTopCards(2, effect)
        if any(FacesCounter.GetPrintedResources([f]).r > 0 for f in faces if f is not None):
            identite = joueur.GetIdentity()
            if identite is not None:
                this.DealIndirectDamage(identite, 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            seeing_red,
        ),
    ]
