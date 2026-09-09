from . import *

# * Mania (Andi Benton) — ALLIE, cout 2, PV 2, CTR 2* / ATQ 1*. SYMBIOTE.
# Response: After Mania is defeated during the player phase, draw 1 card.
#
# CARTE DE REFERENCE
#  - `vz002` Codex, la carte jumelle du meme set : meme declencheur, meme
#    fenetre « during the player phase », effet plus simple. Les trois allies
#    vz002 / vz003 / vz005 forment une famille — un allie symbiote qui meurt
#    rend quelque chose.
#
# TEXTE CONTRE CODE
#  ⚠ « DURING THE PLAYER PHASE » : voir vz002. Mourir sous une attaque du
#    vilain ne fait rien piocher.
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

    def mania(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        joueur = this.GetControlByOrOwner()
        if Player.IsType(joueur):
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            "This",
            mania,
            conditions=[pendant_la_phase_du_joueur],
        ).NoOutOfPlayLimit(),
    ]
