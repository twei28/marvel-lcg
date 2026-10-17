from . import *

# Keep the Momentum — RESSOURCE [wild], Taijutsu (TMNT Shinobi, Inkwire).
# Max 2 per deck.
# Response: After you spend this card on an event, return 1 Taijutsu event from your discard pile to your hand.
#
# Mots-cles : aucun (classe Taijutsu, fiche shinobi.md ; `desc.MaxPerDeck = "2"`).
#
# Cartes de reference :
#  - « After you spend this card to pay for a <filtre> » : `42008` Avian Anatomy (`AfterYouSpendThisCard(Response, op,
#    to_pay_card=CardFinder2("AERIAL", Event))`) ;
#  - « return 1 X from your discard pile to your hand » : `jennika/tj011` Sosaiken et `se004` Shihan (`EstShinobi(face,
#    "Taijutsu")` + `Faces.AddToHand`), choix du joueur `AskChooseFaces`.
#
# TEXTE CONTRE CODE
#  ⚠ « spend this card ON AN EVENT » : la carte payee est un evenement (pas un allie, une amelioration...) ; de
#    n'importe quelle classe.
#  ⚠ « 1 TAIJUTSU event » : un EVENEMENT portant la classe Taijutsu (pas une amelioration Taijutsu, pas un evenement d'une
#    autre classe) ; une Dual Taijutsu evenement en est un aussi ; l'evenement qu'on est en train de payer n'est pas
#    encore en defausse.
#  ⚠ « Response » nu (pas « Hero Response ») ; « from YOUR discard pile ».


def GetAbilities() -> Sequence['Ability']:

    def keep_the_momentum(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        candidats = [f for f in joueur.discard_pile.Get() if Event.IsType(f) and EstShinobi(f, "Taijutsu")]
        if not candidats:
            return
        if len(candidats) == 1:
            choisie = candidats
        else:
            choisie = joueur.AskChooseFaces(candidats, (1, 1), effect, prompt="Return 1 Taijutsu event to your hand")
        if choisie:
            Faces.ReturnToHand(list(choisie), joueur, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            keep_the_momentum,
            to_pay_card=CardFinder(card_type=Event),
        ),
    ]
