from . import *

# "It's a Stinkin' Skrull!" (x2) — TRAITRISE NEMESIS de Lyja (n° 68, 3/5, 4/5). 1 icone boost.
# When Revealed: Search the encounter deck for a TREACHERY card and discard it. (Shuffle.)
#   If no TREACHERY card was discarded this way, this card gains surge.
#
# Cartes de reference :
#  - **sk067** (meme dossier) : la recherche + la defausse d'une traitrise du deck rencontre.
#  - **`01188`** Caught Off Guard, **`53042`** Techno : « if ... this card gains surge » =
#    `ThisCardGainSurge(effect)` (cards/pack/__init__.py) dans la branche de repli.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « if NO TREACHERY card was DISCARDED this way » : le critere est la DEFAUSSE reelle
#    (`Faces.DiscardAll` rend les cartes effectivement defaussees). Si Paibok intercepte la
#    defausse, rien n'est defausse : la carte gagne Surge (lecture litterale).
#  - « (Shuffle.) » : parenthese = rappel du melange de la recherche.
#  - Carte nemesis : melangee dans le deck rencontre avec le set nemesis du joueur ; elle
#    se cherche elle-meme (c'est une traitrise) : elle est deja revelee, donc hors du deck.


def GetAbilities() -> Sequence['Ability']:

    def stinkin_skrull(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        trouvees = ChercherTraitrisesRencontre(effect, joueur, 1)
        defaussees = Faces.DiscardAll(trouvees, effect)
        if not defaussees:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, stinkin_skrull),
    ]
