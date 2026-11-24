from . import *
# * Corsair: Christopher Summers (Basic, allie 4 [energy], 2*/2*, PV 3). STARJAMMER.
# Interrupt: After you play Corsair from your hand, tuck each card you used to pay for him under here.
# [star] Response: After you attack or thwart with Corsair, add a card tucked under him to your hand.
#
# Cartes de reference : 53018 Spectrum (« After you play X from your hand » = `AfterPlayerPlayedCard(Response, "You", "This", op)` +
# `.SetTarget("UsedToPayForThis")` + `this.TuckCardUnderHere(effect.targets, effect)`) ; `AfterUnitAttackOrThwart` (do_attack.py:1156) ;
# cr001a (cartes glissees sous une carte : `GetPlacedCardArea`).
# ⚠ TEXTE CONTRADICTOIRE (question en attente) : « Interrupt » + « After you play » : une Interruption part AVANT. Code en REPONSE (le
# modele 53018 imprime « Response » pour ce meme texte). ⚠ « each card you used to pay » : les cartes de la main depensees en ressource ;
# Corsair doit etre JOUE depuis la main. « add a card tucked under him » : une seule, au choix du joueur.
def GetAbilities() -> Sequence['Ability']:
    def corsair_joue(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        if effect.targets:
            this.TuckCardUnderHere(effect.targets, effect)
    def corsair_reprend(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Ally)
        joueur = JoueurDe(effect)
        glissees = Glissees(this)
        if joueur is None or not glissees:
            return
        choisie = glissees[0] if len(glissees) == 1 else joueur.AskChooseFace(
            glissees, effect, prompt="Add a card tucked under Corsair to your hand", forced=True)
        if choisie is not None:
            Faces.AddToHand([choisie], joueur, effect)
    def une_carte_glissee(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        return bool(Glissees(effect.this))
    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            "This",
            corsair_joue,
        ).SetTarget("UsedToPayForThis", range=(1, "All")),
        AbilityFactory.AfterUnitAttackOrThwart(
            AbilityType.Response,
            "This",
            corsair_reprend,
            conditions=[une_carte_glissee],
        ),
    ]
