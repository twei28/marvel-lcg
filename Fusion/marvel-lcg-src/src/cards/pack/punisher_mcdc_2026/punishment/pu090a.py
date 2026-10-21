from . import *

# Justice or Punishment? (5A, mise en place) — ENVIRONNEMENT.
# Setup : Reveal the UNDERLING villain (I for standard, II for expert mode). Set their hit points to the numeral (ignoring
#   [per hero]) in their printed hit point value. Attach In the Crosshairs to them. Shuffle their encounter cards into the
#   encounter deck, following any Setup and When Revealed instructions. Flip this card.
#
# Cartes de reference : `Villains.BuildVillainDeck/RevealNextVillain/SetRule/SetActive` (game/operate/villains.py, brique
# commune §15.3), `face.ResetHealth(effect, n)` (can_health.py), `card.Flip(effect)` (pu106a).
# ⚠ « Reveal the UNDERLING villain » : le vilain de sous-fifre mis de cote par le scenario (I en standard, II en expert) ;
# « set their HP to the NUMERAL » : 14 (pas 14 par joueur) ; In the Crosshairs ajoute ensuite 5 par joueur ; « shuffle their
# encounter cards » : deja dans le deck (ensemble de rencontre du scenario) ; « flip this card » : 5B (regles permanentes).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        premier = Worlds.GetFirstPlayer(effect)
        punisher = Punisher(effect)
        mis_de_cote = [c for c in Worlds.GetSetAsideAreaCards(effect) if Villain.IsType(c) and c.HasTrait("UNDERLING")]
        if mis_de_cote:
            Villains.BuildVillainDeck(mis_de_cote[:1], effect)
            sous_fifre = Villains.RevealNextVillain(premier, effect)
            if sous_fifre is not None:
                imprime = sous_fifre.printed_health if hasattr(sous_fifre, 'printed_health') else sous_fifre.max_health
                sous_fifre.ResetHealth(effect, imprime)
                Find.FindAndPutIntoPlay(effect, premier, name="In the Crosshairs", card_type=Attachment)
        Villains.SetRule(effect, Villains.Rule(the_villain="Active"))
        if punisher is not None:
            Villains.SetActive(punisher, effect)
        this.card.Flip(effect)

    return [
        # Revelee par `Find.FindAndReveal` depuis la mise en place de pu088a : c'est la REVELATION qui declenche le Setup.
        AbilityFactory.WhenThisRevealed(None, mise_en_place),
    ]
