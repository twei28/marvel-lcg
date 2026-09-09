from . import *

# * Sleeper — ALLIE, cout 3, PV 3, CTR 2* / ATQ 1*. SYMBIOTE.
# Response: After Sleeper is defeated during the player phase, confuse the
#   villain.
#
# CARTE DE REFERENCE
#  - `vz002` Codex et `vz003` Mania, ses deux jumelles du set : meme
#    declencheur, meme fenetre.
#
# TEXTE CONTRE CODE
#  ⚠ « THE villain » au singulier : `Worlds.GetVillains` peut en rendre
#    plusieurs (Sinister Six, Wrecking Crew). Le texte n'en designe qu'un —
#    on confond le vilain ACTIF, et s'il y en a plusieurs la joueuse choisit.
#  ⚠ « DURING THE PLAYER PHASE » : voir vz002.
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

    def sleeper(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)

        Faces.GiveStatus(effect.targets, "Confused", effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            "This",
            sleeper,
            conditions=[pendant_la_phase_du_joueur],
        ).SetTarget(Villain, canbe_confused=True)
        .NoOutOfPlayLimit(),
    ]
