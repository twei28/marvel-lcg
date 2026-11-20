from . import *

# * Crystal (CRYSTALIA AMAQUELIN) — ALLIE de campagne (Identity-Specific / Campaign, n° 229). Cout 3.
# THW 2 / ATK 2, 4 PV. INHUMAN.
# Honorary. Requirement ([energy][mental][physical]).
# When Defeated: Spend 3 resources of any type -> put Crystal into play under your control.
#
# « Requirement » : base automatique (desc.Requirement = "YBR", fiche mots-cles/requirement.md),
# AUCUN script.
#
# Cartes de reference :
#  - **`mut_gen/mutant_genesis_campaign/32173b`** : `face.CastTo(Ally).PutIntoPlay(initiator, effect,
#    under_control=True)`, modele pour « put ... into play under your control » — MAIS sur une AUTRE
#    carte (restee facedown sous un Environment), jamais la carte qui se defait elle-meme.
#  - **`game/operate/run_at.py`** `RunAt.AfterEventEnd` / **`game/ability/factory/card_move.py`**
#    `AfterCardLeavePlayInternal` (forme tuple) : le motif « differer une operation a l'evenement APRES »
#    via `effect.RegisterTemp(ability, unregister_after_exec=True)` pose PENDANT la reaction courante.
#
# ⚠⚠ PIEGE TROUVE EN ECRIVANT LE CAS DE TEST (21/10/2026), resolu par instrumentation directe :
#  - `WhenUnitBeDefeated` (forme "When") fire AVANT que la carte quitte reellement le jeu : a ce moment,
#    `effect.this.card.area` est ENCORE la zone de jeu (confirme : `card.area.flags.is_in_play` vrai,
#    `this.IsInPlay()` vrai). Appeler `PutIntoPlay(..., under_control=True)` a cet instant essaie de
#    deplacer la carte vers la zone ou elle est DEJA (`CheckIfCanMove` : `if self.area == into_area: return
#    False`) : `PutIntoPlay` rend donc `False` silencieusement, sans lever d'erreur.
#  - `AfterUnitBeDefeated(ability_type, "This", ...)` pose comme ABILITY STANDARD (dans `GetAbilities()`)
#    NE SE DECLENCHE JAMAIS pour la carte elle-meme : ses capacites sont deja desenregistrees au moment ou
#    l'evenement "After" de SA PROPRE defaite part (confirme : aucune trace, meme avec un operateur trivial
#    qui ne fait que poser de la menace).
#  - **Solution qui marche** (confirmee par cas de test, `ok=True`) : depuis la reaction `WhenUnitBeDefeated`
#    (qui, elle, se declenche bien), **differer** la remise en jeu via `effect.this.effect.RegisterTemp(...,
#    unregister_after_exec=True)` sur une ability TEMPORAIRE liee a `Message.AfterUnitBeDefeated` — enregistree
#    PENDANT que la carte est encore active, elle survit jusqu'a l'evenement "After" reel, qui arrive
#    APRES le deplacement vers la defausse.
#
# ⚠ Mots-pieges :
#  - « When Defeated » sur l'allie LUI-MEME (pas un observateur externe) : la capacite s'offre au moment
#    ou Crystal est vaincue, le joueur peut refuser de payer (cout optionnel, pas une Reponse forcee) ;
#  - « of any type » : pas de Requirement sur CE paiement, contrairement au Requirement d'entree en jeu.


def GetAbilities() -> Sequence['Ability']:

    def revenir(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Unused(message)
        joueur = effect.this.GetControlByPlayer() or effect.GetInitiator()
        effect.this.CastTo(Ally).PutIntoPlay(joueur, effect, under_control=True)

    def crystal(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        effect.this.effect.RegisterTemp(
            AbilityFactory.AfterUnitBeDefeated(AbilityType.Temp2, "This", revenir),
            unregister_after_exec=True,
        )

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Response,
            "This",
            crystal,
        ).SetCostFunc(CostFunc.Spend(Cost("3"))),
    ]
