from . import *

# Precognition (evenement, cout 2, SUPERPOWER THWART, mental) — x2
# Hero Action (thwart): Remove 4 threat from a scheme.
# Special: Confuse an enemy.
#
# ⚠ HOMONYME : `40004` Precognition (pack next_evol) porte exactement ce nom.
# Le `card_id` prefixe regle la collision cote donnees ; ne jamais chercher
# cette carte PAR NOM.
#
# Modeles : 01060 For Justice (contre sur evenement, cible `Scheme2`), ab007
# pour le Special nomme.

def GetAbilities() -> Sequence['Ability']:

    def precognition(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 4, effect)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = message.GetToPlayer() or effect.GetInitiator()
        cible = ChoisirUnEnnemi(joueur, effect)
        if cible:
            Faces.GiveStatus([cible], "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            precognition,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),

        # ⚠ `.NoOutOfPlayLimit()` : ce Special se resout depuis la MAIN (Hera)
        # ou pendant le paiement (Tempest), jamais depuis la table. Sans ce
        # drapeau, le moteur ignore l'effet d'une carte hors jeu et le message
        # `WhenResolveSpecialAbility` tombe dans le vide (vu le 11/09/2026).
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            special,
        ).NoOutOfPlayLimit(),
    ]
