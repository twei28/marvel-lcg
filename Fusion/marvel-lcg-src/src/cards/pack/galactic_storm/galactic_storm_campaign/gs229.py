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
# ⚠ Aucune carte strictement identique trouvee dans le depot (une allie qui se remet elle-meme en jeu
#   apres sa propre defaite, en payant un cout, est rare) : montage assemble a partir de primitives
#   prouvees separement (WhenUnitBeDefeated, CostFunc.Spend, PutIntoPlay(under_control=True)), A VERIFIER
#   en priorite a l'etape 7 (cas de test).


def GetAbilities() -> Sequence['Ability']:

    def crystal(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        initiator = effect.GetInitiator()
        effect.this.CastTo(Ally).PutIntoPlay(initiator, effect, under_control=True)

    return [
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            crystal,
        ).SetCostFunc(CostFunc.Spend(Cost("3"))),
    ]
