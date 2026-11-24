from . import *

# * Hell Lord — ATTACHEMENT (TITLE). Attach to Mephisto.
# Reduce the amount of damage Mephisto takes from identities by 1 for each BARGAIN attachment they control.
# Forced Response: After an identity with a BARGAIN attachment attacks Mephisto, for each BARGAIN attachment they control, look at 1 card in
# Damnation -> shuffle each card looked at this way back into its owner's deck.
#
# Cartes de reference : fne/typhoid_mary/60117 (`WhenUnitWouldTakeDamage` sur le vilain porteur, condition `message.trigger is GetBindFace()`),
# night_thrasher/nt001b (`Faces.ShuffleAllTo(cartes, deck, effect)`), `Search.SearchForCard(.., faces=.., not_move=True)` pour le choix
# parmi les cartes de TOUTES les piles de Damnation.
# ⚠ Une Forced Response avec `.SetTarget(..)` ne se resout JAMAIS (aucun precedent, aucune erreur) : le choix se fait dans l'operation.
#
# ⚠ Mots-pieges : « damage Mephisto takes FROM IDENTITIES » (pas les allies : `PactsDeLIdentiteSource` vaut 0 hors identite) ;
# « THEY control » = les pactes de l'identite qui attaque, pas ceux des autres joueurs ; « INTO ITS OWNER'S deck » : le deck du
# proprietaire de la carte (sa pile de Damnation d'origine), pas celui de l'attaquant ; « 1 card PER pact » : jamais plus de cartes que
# la Damnation n'en contient.


def GetAbilities() -> Sequence['Ability']:
    def le_vilain_attache(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return message.trigger is effect.this.CastTo(Attachment).GetBindFace()

    def reduit(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        pacts = PactsDeLIdentiteSource(message.source)
        valeur = min(pacts, message.will_take_damage)
        if valeur > 0:
            message.ReduceDamage(valeur, effect)

    def attaque_sur_le_vilain(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        vilain = effect.this.CastTo(Attachment).GetBindFace()
        cibles = [c for groupe in message.attacked_targets for c in (groupe if isinstance(groupe, (list, tuple)) else [groupe])]
        return vilain is not None and vilain in cibles and PactsDuJoueur(message.attacker.GetControlByPlayer()) != []

    def regarde_et_remelange(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        joueur = message.attacker.GetControlByPlayer()
        a_regarder = len(PactsDuJoueur(joueur))
        for _ in range(a_regarder):
            # « look at 1 card in Damnation » : une carte, au choix du joueur, parmi toutes les piles (les restantes seulement).
            carte = Search.SearchForCard(effect, joueur, faces=ToutesLesDamnations(effect), not_move=True)
            if carte is None:
                return
            proprietaire = carte.card.area.GetOwnerPlayer()
            Faces.ShuffleAllTo([carte], proprietaire.player_deck, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, reduit, conditions=[le_vilain_attache]),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, Identity, regarde_et_remelange, conditions=[attaque_sur_le_vilain]),
    ]
