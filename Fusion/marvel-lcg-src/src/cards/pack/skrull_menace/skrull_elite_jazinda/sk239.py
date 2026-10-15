from . import *

# Stealing for the Empire — COMPLOT ANNEXE x2 (Skrull Elite - Jazinda). Menace 3 (fixe), icone
# ACCELERATION (lecture du 15/10/2026), aucune icone de boost.
# When Revealed: Discard cards from the encounter deck until you discard an attachment. Reveal that
#   attachment. Then, place threat on the main scheme equal to the number of boost icons on that attachment.
#
# Cartes de reference :
#  - « Discard until X, reveal it » : **`sk144b`** Power Skrull Engineering (`Worlds.DiscardEncounterCardsUntil`
#    + `Reveal`) ; helper `RevelerPouvoirDuDeck` de paibok.
#  - « place threat on the main scheme » : **`sk139`** (`source.PlaceThreatOnSchemes([complot], n, effect)`).
#  - « number of boost icons » : **`sk106`** Wrath of the Empire (`FacesCounter.CountTotalBoostIcons`).
#
# ⚠ Mots-pieges : « until an ATTACHMENT is discarded » (n'importe quel attachement, de n'importe quel set) ;
# « Reveal THAT attachment » (la carte defaussee est revelee : elle sort de la defausse et entre en jeu) ;
# « boost icons » = les icones Y imprimees (pas l'etoile) ; « the MAIN scheme » (pas cette annexe) ; aucun
# attachement dans le deck : rien (pas de menace) ; compte lu apres la revelation (le nombre d'icones ne change pas).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        attachement = Worlds.DiscardEncounterCardsUntil(effect, card_type=Attachment)
        if attachement is None:
            return
        icones = FacesCounter.CountTotalBoostIcons([attachement])
        attachement.Reveal(joueur, effect)
        principal = Worlds.FindMainScheme(effect)
        if principal is not None and icones > 0:
            this.PlaceThreatOnSchemes([principal], icones, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
