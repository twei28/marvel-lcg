from . import *

# * Codex (Dylan Brock) — ALLIE, cout 2, PV 2, CTR 1* / ATQ 2*. SYMBIOTE.
# Response: After Codex is defeated during the player phase, discard the top
#   card of your deck. If that card is a Venomized (black) card, return Codex
#   to your hand.
#
# CARTES DE REFERENCE
#  - `ab011` (pack albert) : le montage `AfterUnitBeDefeated(..., "This", ...)`.
#  - `gb010` Necro-Raven (pack gorr, maison) : `joueur.DiscardDeckTopCards(1,
#    effect)`, qui REND les faces defaussees — c'est ainsi qu'on relit celle
#    du dessus.
#  - `deck.py:106` (`phase.IsPlayerPhase("AnyPlayer")`) : la fenetre « during
#    the player phase ».
#
# TEXTE CONTRE CODE
#  ⚠ « DURING THE PLAYER PHASE » n'est pas decoratif : un allie mis K.O.
#    pendant la phase du vilain ne revient PAS. Sans cette condition la carte
#    serait bien plus forte que ce qui est imprime.
#  ⚠ « return Codex TO YOUR HAND » : Codex est deja dans la defausse quand la
#    capacite se resout (il vient d'etre vaincu) — `Faces.ReturnToHand` part
#    donc de la defausse, ce qui est le comportement voulu.
#  ⚠⚠ SANS `.NoOutOfPlayLimit()` LA CAPACITE NE PART JAMAIS. Quand la Reponse
#    resout, l'allie est DEJA dans la defausse, et le controle de zone
#    generique (`CheckNotOutOfPlay`, effect_checker.py) refuse toute capacite
#    portee par une carte hors jeu. C'est le cas de TOUTE capacite « After this
#    card is defeated » imprimee sur la carte elle-meme — idiome du depot,
#    documente sur `tt013` Fifty-One (pack texas_twister). MESURE le
#    09/09/2026 : les trois cas etaient ROUGES sans cet appel.
def GetAbilities() -> Sequence['Ability']:

    def pendant_la_phase_du_joueur(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        return effect.world.phase.IsPlayerPhase("AnyPlayer")

    def codex(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = this.GetControlByOrOwner()
        if not Player.IsType(joueur):
            return
        defaussees = joueur.DiscardDeckTopCards(1, effect)
        if any(EstUneCarteVenomized(c) for c in defaussees):
            Faces.ReturnToHand([this], joueur, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            "This",
            codex,
            conditions=[pendant_la_phase_du_joueur],
        ).NoOutOfPlayLimit(),
    ]
