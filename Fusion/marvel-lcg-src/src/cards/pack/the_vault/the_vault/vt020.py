from . import *

# Craven Escape — ATTACHEMENT, x2. 2 icones de boost.
# Attach to the villain with the fewest remaining hit points and without another Craven Escape attached. If you cannot, this
#   card gains surge.
# Forced Response: After the player phase ends, shuffle attached villain into the villain deck.
#
# Cartes de reference :
#  - « Attach to the villain with the fewest remaining hit points ... If you cannot, this card gains surge » :
#    `AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Villain, check_effect_fn=...), fewest_remaining_hp=True,
#    if_cannot_gain_surge=True)` (modele gs163 Main Concern, qui prend « most » ; le filtre « sans autre Craven Escape » est la
#    condition posee SUR LE CANDIDAT, comme son « plus d'un vilain »).
#  - « After the player phase ends » : `AfterPhaseEnd(ForcedResponse, "Player", ...)` (modele gs161b, phase « Villain ») ;
#    « shuffle attached villain into the villain deck » : `Villains.ShuffleIntoVillainDeck` (brique, 25/10/2026) puis
#    `ApresDepartDUnMechant` (livret p.1 : apres le depart du dernier vilain, reveler le dessus du deck de vilains).
#
# ⚠ Mots-pieges : « WITHOUT ANOTHER Craven Escape attached » : le candidat n'a AUCUN autre exemplaire attache (la carte qui
# se pose n'est pas encore attachee) ; « fewest REMAINING hit points » = PV restants, pas PV imprimes ; le melange emporte
# les degats du vilain (la carte retourne dans le deck a PV pleins) ; l'attachement, lui, est defausse avec le reste.


def GetAbilities() -> Sequence['Ability']:

    def sans_autre_craven(effect: 'Effect', face: 'CardFace') -> bool:
        autres = [a for a in face.GetAttachedAttachments() if a is not effect.this and a.IsName("Craven Escape")]
        return not autres

    def melanger(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Unused(message)
        this = effect.this.CastTo(Attachment)
        mechant = getattr(this, 'bind_face', None)
        if mechant is None or not Villain.IsType(mechant) or not mechant.IsInPlay():
            return
        Villains.ShuffleIntoVillainDeck(mechant.CastTo(Villain), effect)
        ApresDepartDUnMechant(effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Villain, check_effect_fn=sans_autre_craven),
            fewest_remaining_hp=True,
            if_cannot_gain_surge=True,
        ),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Player", melanger),
    ]
