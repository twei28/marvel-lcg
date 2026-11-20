from . import *

# Midtown Memories (5) — PISTE. Response : While in Midtown, after you thwart a scheme, look at the top two cards of the encounter deck. Tuck one
#   of them here. Then, if there are 3 or more cards tucked here, add this card to the victory display, reveal the top LEAD card, and draw 1 card.
#
# Cartes de reference : fiche tuck.md (`TuckCardUnderHere`, `GetPlacedCardArea().GetSize()`), `AbilityFactory.AfterUnitThwartScheme`, fiche piste-lead.md.
# ⚠ « look at the top two » : les deux du dessus (deck a une seule carte : cette carte) ; le joueur choisit LA carte glissee, l'autre reste sur le deck.

def GetAbilities() -> Sequence['Ability']:

    def apres(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this
        joueur = Joueur(effect)
        dessus = list(Worlds.GetEncounterDeckCards(effect))[:2]
        if not dessus:
            return
        choisie = dessus[0] if len(dessus) == 1 else joueur.AskChooseFace(dessus, effect)
        if choisie is not None:
            this.TuckCardUnderHere([choisie], effect)
        if this.GetPlacedCardArea().GetSize() >= 3:
            PisteTerminee(effect, joueur)

    def un_contre_de_moi(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> bool:
        joueur = Joueur(effect)
        return joueur is not None and Identity.IsType(message.trigger) and ControlePar(message.trigger, joueur) and EnLieu("pu034")(effect, message)

    # ⚠ la fabrique `AfterUnitThwartScheme` ne sait pas lire "You" (elle passe la chaine telle quelle a `CheckWhichCard`) : Ability a la main.
    return [Ability(AbilityType.Response, Message.AfterUnitThwartScheme, [un_contre_de_moi], apres)]
