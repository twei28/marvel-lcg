from . import *

# Punish the Defector — COMPLOT ANNEXE NEMESIS de Lyja (n° 67, 2/5). Menace de depart 2[per_hero].
# Hazard (icone), 2 icones boost.
# When Revealed: Search the encounter deck for a TREACHERY card and discard it. Shuffle the
#   encounter deck.
#
# Cartes de reference :
#  - **`sk103`** / **`sk102`** (Skrull Empire) et RECETTES §2 : « Search the encounter deck »
#    = `Search.EncounterCards(...)` ; la carte trouvee quitte le deck pour la zone de
#    traitement, c'est a l'appelant de la consommer (ici `Faces.DiscardAll`).
#  - Helper du set `ChercherTraitrisesRencontre` (lyja/__init__.py) : recherche d'une
#    traitrise, deck melange meme sans resultat.
#  - **`01107`** Breakin' & Takin' (Hazard) : l'icone Hazard est lue dans `desc` (« Hazard »,
#    fiche `hazard.md`), aucun script.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « a TREACHERY card » : type Treachery OU trait TREACHERY (decision du 15/10/2026).
#  - « and DISCARD it » : defausse (la traitrise va dans la defausse rencontre, ou chez son
#    proprietaire si c'est une carte joueur ; Paibok, s'il est en jeu, l'intercepte).
#  - « Shuffle the encounter deck » : toujours, meme sans resultat.
#  - « Search the encounter deck » : c'est le joueur a qui la carte est revelee qui cherche.
#  - Hazard : icone lue dans desc (lecture de l'auteur : Punish the Defector = Hazard, 15/10/2026).


def GetAbilities() -> Sequence['Ability']:

    def punir(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        joueur = message.GetToPlayer()
        trouvees = ChercherTraitrisesRencontre(effect, joueur, 1)
        Faces.DiscardAll(trouvees, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, punir),
    ]
