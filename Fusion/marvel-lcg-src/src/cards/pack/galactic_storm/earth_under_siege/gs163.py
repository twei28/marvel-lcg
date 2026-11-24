from . import *

# Main Concern — ATTACHEMENT (Earth Under Siege). CONDITION.
# Attach to the villain with the most remaining hit points. If there is only 1 villain in play, this card
#   gains surge.
# Players cannot deal damage to other villains.
# [star] Boost: Attach to the villain with the most remaining hit points.
#
# Pas de "When Revealed" imprime (verifie sur le scan) : l'attache resout nativement a l'entree en jeu,
# comme sk196 Super-Skrull Enhancement (meme absence de mot-cle).
#
# Cartes de reference :
#  - « Attach to the villain with the most remaining hit points » : `AbilityFactory.AttachToFaceWhenPutIntoPlay`
#    (modele sk196, `most_remaining_hp=True`) ; `Filter.One(..., most_remaining_hp=True)` pour le Boost
#    (modele sk098 Impostor).
#  - « If there is only 1 villain in play, this card gains surge » : condition posee SUR LE CANDIDAT du
#    selecteur (`check_effect_fn=lambda effect, face: len(Villains.All(effect)) > 1`) : avec un seul
#    mechant, AUCUN candidat ne passe le filtre -> `if_cannot_gain_surge=True` (ThisCardGainSurge, meme
#    mecanique que if_cannot_operation/if_cannot_attach_to, `attachment.py`).
#  - « Players cannot deal damage to other villains » : `AbilityFactory.WhenDamageWouldBeDealtTo`
#    (modele `next_evol/mister_sinister/40144.py`, `Message.WhenFaceWouldDealDamage` + `SetBeInstead`),
#    cible TOUT mechant SAUF celui porte par `effect.this.bind_face` (l'hote de CETTE copie).
#  - « [star] Boost: Attach to the villain with the most remaining hit points » : carte deja attachee,
#    revelee comme carte de boost de son hote -> peut DEMENAGER vers un autre mechant devenu plus riche en
#    PV (modele `WhenCardBecomeBoost`, sk196). Pas de clause de surge sur cette ligne (texte imprime).
#
# ⚠ Mots-pieges : « OTHER villains » = tous sauf l'hote actuel (pas tous les mechants) ; « Players cannot
# deal damage » = restriction des CARTES JOUEUR seulement (`who_deal_damage="Player"`), le mechant actif
# peut toujours s'infliger des degats entre mechants via ses propres effets si besoin (aucun cas connu
# dans ce lot) ; la restriction tombe automatiquement si la carte quitte le jeu (condition lue sur
# `effect.this.bind_face`, jamais sur une copie figee).


def GetAbilities() -> Sequence['Ability']:

    def pas_seul(effect: 'Effect', face: 'CardFace') -> bool:
        Unused(face)
        return len(Villains.All(effect)) > 1

    def reattacher_au_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        this = effect.this.CastTo(Attachment)
        mechant = Filter.One(Villains.All(effect), effect, most_remaining_hp=True)
        if mechant is not None:
            this.AttachTo2(mechant, effect)

    def bloquer_autre_mechant(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        message.SetBeInstead(effect)

    def pas_lhote(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> bool:
        return message.target is not getattr(effect.this, 'bind_face', None)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Villain, check_effect_fn=pas_seul),
            most_remaining_hp=True,
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.WhenDamageWouldBeDealtTo(
            AbilityType.ForcedInterrupt,
            Villain,
            bloquer_autre_mechant,
            who_deal_damage="Player",
            conditions=[pas_lhote],
        ),
        AbilityFactory.WhenCardBecomeBoost("This", reattacher_au_boost),
    ]
