from . import *

# * Neurokinetic Interface
# Hero Response: After you reveal an encounter card, exhaust Neurokinetic
#   Interface → if that card was:
#   • A treachery or minion, deal 2 damage to an enemy.
#   • A side scheme or attachment, remove 2 threat from a scheme.
#
# Declencheur generique : `AbilityFactory.AfterPlayerRevealCard(..., "You",
# EncounterCard, ...)`, modele jj001b Pays the Bills (jessica_jones/
# jessica_jones/jj001b.py) et sm/27190.py (qui filtre deja sur EncounterCard).
# CORRECTIF (trouve par test_capacites.py) : `which_card=None` ne
# declenchait JAMAIS l'ability (Condition.CheckWhichCard n'a pas de
# fallback pour None, comme Condition.CheckWhichPlayer, meme piege documente
# sur Albert/ab001a.py) -> `EncounterCard`, la classe de base qui couvre
# treachery/minion/side scheme/attachment. Branche par type de la carte
# revelee via `<Type>.IsType(face)` (idiome classmethod, card_face.py:400 ;
# modele silk/52028.py). "Attachment" = un Upgrade de rencontre : meme
# classe de base `Upgrade` que les upgrades joueur dans ce moteur.

def GetAbilities() -> Sequence['Ability']:

    def neurokinetic_interface(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        revealed = message.trigger

        if Treachery.IsType(revealed) or Minion.IsType(revealed):
            ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
            cible = initiator.AskChooseFace(ennemis, effect)
            if cible:
                this.DealDamage([cible], 2, effect)
        elif SchemeSide2.IsType(revealed) or Upgrade.IsType(revealed):
            schemes = Worlds.FindCardsOnField(effect, card_type=Scheme2)
            cible = initiator.AskChooseFace(schemes, effect)
            if cible:
                this.RemoveThreatFromSchemes([cible], 2, effect)

    return [
        AbilityFactory.AfterPlayerRevealCard(
            AbilityType.HeroResponse,
            "You",
            EncounterCard,
            neurokinetic_interface,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
