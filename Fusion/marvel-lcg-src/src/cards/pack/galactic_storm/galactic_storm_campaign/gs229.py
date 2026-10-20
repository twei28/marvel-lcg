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
#    under_control=True)`, modele direct pour « put ... into play under your control ».
#  - cout optionnel "Spend 3 resources of any type" : `CostFunc.Spend(Cost("3"))` (meme notation que le
#    cout imprime d'une carte, generique, aucune couleur imposee — contrairement a Requirement).
#
# ⚠ Mots-pieges :
#  - « When Defeated » sur l'allie LUI-MEME (pas un observateur externe) : la capacite s'offre au moment
#    ou Crystal est vaincue, le joueur peut refuser de payer (cout optionnel, pas une Reponse forcee) ;
#  - « of any type » : pas de Requirement sur CE paiement, contrairement au Requirement d'entree en jeu.
# ⚠⚠ ETAPE 7 FAITE, CARTE EN ECHEC CONFIRME (21/10/2026). Cas de test ecrit
#   (`[gsc] gs229`, `tools/cas/campagne_galactic_storm.py`) : `effect.this.CastTo(Ally).PutIntoPlay(joueur,
#   effect, under_control=True)` rend FAUX (verifie en instrumentant la valeur de retour : un cas de debug
#   dedie confirme `ok=False`), silencieusement, sans lever d'erreur. Piste la plus probable (NON
#   confirmee, pas eu le temps de creuser plus loin) : `Ally.OnPutIntoPlay` (`card_type/ally.py:92`) appelle
#   `Faces.MoveAllTo([self], player.allies, by_effect)`, qui echoue — `face.card.MoveToArea(...)` a
#   peut-etre une precondition qui refuse de deplacer une carte depuis la defausse DANS LA MEME fenetre de
#   resolution que celle ou elle vient d'y entrer (contrairement a `32173b`, qui deplace une AUTRE carte,
#   restee facedown sous un Environment, jamais passee par le chemin normal de defaite). Cout
#   (`CostFunc.Spend`) laisse en place (conforme au texte imprime) mais N'EST PAS la cause : le meme echec
#   survient cout retire. A reprendre avec plus de temps : soit un `Faces.MoveAllTo` direct vers
#   `player.allies` plutot que via `PutIntoPlay`, soit une instrumentation du moteur pour voir la raison
#   exacte du refus de `MoveToArea`.


def GetAbilities() -> Sequence['Ability']:

    def crystal(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        joueur = effect.this.GetControlByPlayer() or effect.GetInitiator()
        effect.this.CastTo(Ally).PutIntoPlay(joueur, effect, under_control=True)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.Response,
            "This",
            crystal,
        ).SetCostFunc(CostFunc.Spend(Cost("3"))),
    ]
