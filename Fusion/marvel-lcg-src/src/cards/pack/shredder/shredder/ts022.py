from . import *

# Throne of the Jonin — COMPLOT ANNEXE. Menace 1[per_hero], icone CRISE, 2 icones de boost.
# When Revealed: Search the encounter deck and discard pile for a FOOT CLAN
#   attachment and reveal it. (Shuffle.) If you cannot, place 2[per_hero] threat
#   on this scheme.
#
# Cartes de reference : `01095` (Search.EncounterCard puis Reveal) ; `mts 21188`
# (le joueur qui revele cherche) ; `PlaceThreatOnSchemes([this], "2*", effect)`
# (`ts004b` pour poser de la menace sur CE complot).
#
# Mots-pieges : « a FOOT CLAN ATTACHMENT » (type Attachment ET trait : Bladed
# Armor, Kuro Kabuto, Kira no Ken en font partie) ; « If you CANNOT » = aucune
# trouvee ; le surplus de menace est « 2 par joueur » en PLUS de la menace de
# depart.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        joueur = message.GetToPlayer()
        face = Search.EncounterCard(
            effect, joueur,
            include_discard_pile=True,
            card_type=Attachment,
            trait="FOOT CLAN",
        )
        if face:
            face.Reveal(joueur, effect)
        else:
            this.PlaceThreatOnSchemes([this], "2*", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
