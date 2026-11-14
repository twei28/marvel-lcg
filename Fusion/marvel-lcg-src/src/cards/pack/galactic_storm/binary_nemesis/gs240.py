from . import *

# Energy Transfer — TRAITRISE nemesis (Binary Nemesis 4/5, 5/5). 1 icone de boost. x2.
# When Revealed: Discard each [energy] resource from your hand. If no card was
#   discarded this way, take 3 damage.
#
# Cartes de reference :
#  - **`skrull_menace/hulkling_kajislav_nemesis/sk036`** (meme auteur) : traitrise
#    nemesis, `WhenThisRevealed(None, op)` avec `message.GetToPlayer()`.
#  - « take 3 damage » : `identite.TakeDamage(this, 3, effect)` (`jubilee/47031`).
#  - « each [energy] resource from your hand » : meme lecture que Burnout
#    (gs001a), helper `CartesEnergieEnMain` (cartes portant au moins une icone
#    [energy], vue EN MAIN donc apres Energy Conversion).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « YOUR hand » : le joueur qui revele la carte.
#  - « IF NO CARD was discarded THIS WAY » : seulement si la defausse n'a rien
#    pris (main sans [energy]) ; une seule carte defaussee suffit a eviter les
#    3 degats (contre-cas).
#  - « TAKE 3 damage » : l'identite, quelle que soit sa forme.


def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        cartes = CartesEnergieEnMain(joueur)
        defaussees = Faces.DiscardAll(cartes, effect) if cartes else []
        if not defaussees:
            joueur.GetIdentity().TakeDamage(this, 3, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation,
        ),
    ]
