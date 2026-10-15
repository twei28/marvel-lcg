from . import *

# Hypnotized — ATTACHEMENT x2 (Paibok). CONDITION. Etoile de boost.
# Attach to your identity.
# As an additional cost to change form, you must spend 1 resource of any type.
# Hero Action: Spend [energy][energy] resources → discard this card.
# [star] Boost: Discard 1 card from your hand.
#
# Cartes de reference :
#  - Cout supplementaire de changement de forme : **`jubilee 47023`** Grounded (`AdditionalCostToChangeForm(
#    "You", CostFunc.Spend(Cost("2", ...)))`) et `jj 61030` Work-Life Balance ; ici l'attache est une
#    carte RENCONTRE (pas une obligation) : cible « AttachedIdentity ».
#  - Boost « discard 1 card from your hand » : **`synthezoid 57062`** Superspeed (le joueur CHOISIT la carte).
#  - Attache : `27166` Webbed Up.
#
# ⚠ Mots-pieges : « to change FORM » = les DEUX sens (heros -> alter ego et retour), sans `to_form` ;
# « 1 resource OF ANY TYPE » = `Cost("1")` ; cout de defausse : `[energy][energy]` = `YY` (eclairs ; verifie
# contre sk044 Lazerfist, meme auteur : RES=Y) ; « Hero Action » : jouable en forme heros seulement
# (un joueur en alter ego doit d'abord payer 1 ressource pour changer de forme).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        main = list(joueur.hand_cards.Get())
        if main:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard 1 card from your hand",
                    lambda choisies: Faces.DiscardAll(list(choisies), effect),
                ).SetTarget(main, range=(1, 1), not_move=True),
            )

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.AdditionalCostToChangeForm("AttachedIdentity", CostFunc.Spend(Cost("1"))),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("YY")),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
