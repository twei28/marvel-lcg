from . import *

# Manipulated Memories — ATTACHEMENT (Seeds of Corruption), x2. CONDITION. ★ + 1 icone de boost.
# Attach to your identity.
# Each event card in your hand gains requirement ([mental]).
# Hero Action: Spend 2 resources of the same type → discard this card.
# ★ Boost: If this activation is a scheme, you are confused. Otherwise, you are stunned.
#
# Cartes de reference :
#  - **`agatha_harkness/aa018`** Death's Embrace : attachement de rencontre `AttachToFaceWhenPutIntoPlay(
#    "YourIdentity")` + regle de cout sur les cartes JOUEES par le porteur (`EachCardYouPlayCostAdditional
#    Resource`, qui passe par `Message.WhenCalculateEffectCost`) + `PlayerActionToDiscardThis(HeroAction)` +
#    `WhenCardBecomeBoost("This", op, during_scheme=True)`.
#  - « Spend 2 resources of the same type » : **`sm/27181`** Snitches Get Stitches (`SetCost(Cost("2",
#    same_type=True))`).
#  - « gains requirement ([mental]) » : fiche mots-cles/requirement.md (« 2 dont au moins 1 mentale », PAS un
#    cout en plus) ; aucune carte ne GAGNE un Requirement : on reecrit le cout calcule (`message.cost`) comme le
#    fait `HasCost.GetPrintedCostWithRequirement` (cout - 1 generique + [mental]).
#
# ⚠ Mots-pieges : « YOUR identity » (le joueur qui revele) ; « each EVENT card in YOUR HAND » (evenements du
# porteur seulement, en main : pas les allies, pas la main d'un autre joueur) ; requirement = contrainte de
# couleur INCLUSE dans le cout (un evenement a 0 doit quand meme payer 1 [mental]) ; evenement qui exige DEJA
# une [mental] : inchange ; « 2 resources of the SAME TYPE » ; Boost : « you » = le joueur active ; « If this
# activation is a SCHEME » -> Desoriente, « Otherwise » (attaque) -> Sonne.


def GetAbilities() -> Sequence['Ability']:

    def evenement_en_main_du_porteur(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        this = effect.this
        if not this.IsInPlay() or not message.is_play:
            return False
        porteur = this.GetBindFace() if this.bind_face is not None else None
        if porteur is None:
            return False
        carte = message.check_effect.this
        if carte is None or not Event.IsType(carte):
            return False
        joueur = porteur.GetControlBy()
        if not Player.IsType(joueur):
            return False
        # Jouee DEPUIS la main : au calcul du cout la carte est en main (rendu des options) ou deja posee dans
        # la zone de traitement du joueur (paiement, journal du cas gs218 : « placee sur la table » AVANT le
        # paiement).
        return carte.card.area in (joueur.hand_cards, joueur.area_processing)

    def exiger_une_mentale(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        Unused(effect)
        cout = message.cost
        if cout.rbyga.b >= 1:
            return
        if cout.rbyga.a >= 1:
            message.cost = (cout - 1) + Cost("B")
        else:
            message.cost = cout + Cost("B")

    def confus(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    def sonne(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenCalculateEffectCost(
            AbilityType.NonKeyword,
            exiger_une_mentale,
            conditions=[evenement_en_main_du_porteur],
        ),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("2", same_type=True)),
        AbilityFactory.WhenCardBecomeBoost("This", confus, during_scheme=True),
        AbilityFactory.WhenCardBecomeBoost("This", sonne, during_attack=True),
    ]
