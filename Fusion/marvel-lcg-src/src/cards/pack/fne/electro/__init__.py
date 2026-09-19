from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout

# Helpers du set Electro (Fear No Evil, 60076-60085).
# Le stock du set est le compteur 'charge' pose sur l'attachement Electric
# Charge (60079), Permanent, attache a Electro.


def TrouverElectro(effect: 'Effect') -> 'Villain|None':
    return Worlds.FindCardOnField(effect, name="Electro", card_type=Villain)


def TrouverElectricCharge(effect: 'Effect') -> 'Attachment|None':
    return Worlds.FindCardOnField(effect, name="Electric Charge", card_type=Attachment)


def Charges(effect: 'Effect') -> int:
    charge = TrouverElectricCharge(effect)
    return charge.GetCounters('charge') if charge else 0


def PoserCharges(effect: 'Effect', n: 'int|str') -> None:
    charge = TrouverElectricCharge(effect)
    if charge:
        Faces.PlaceCountersOn([charge], n, 'charge', effect)


def RetirerCharges(effect: 'Effect', n: int) -> None:
    charge = TrouverElectricCharge(effect)
    if charge:
        Faces.RemoveCountersOn([charge], n, 'charge', effect)


def CapacitesDElectro(charges_par_manigance: int, charges_au_reveil: 'str|None') -> Sequence['Ability']:
    """When Revealed (I, II) : Find Electric Charge, attach it to Electro, and
    place 2[per_hero] charge counters on it. (III : place 3[per_hero] charge
    counters on Electric Charge, sans la chercher : elle y est deja.)
    [star] Forced Response : After Electro schemes, place N charge counter(s)
    on Electric Charge."""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Villain)
        if TrouverElectricCharge(effect) is None:
            Find.FindAndAttachTo(effect, this, who_perform=message.GetToPlayer(), name="Electric Charge", card_type=Attachment)
        PoserCharges(effect, charges_au_reveil or "2*")

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        PoserCharges(effect, charges_par_manigance)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_manigance),
    ]


def ChoixPayerEnergieOuDeux(joueur: 'Player', effect: 'Effect', nom: str, action: Callable[[], None]) -> Sequence['Ability']:
    """« Spend a [energy] resource or 2 resources of any type » : deux branches
    payantes, chacune offerte seulement si elle est payable (PeutCouvrirLeCout,
    lecon de Tug of War)."""
    return [
        AbilityFactory.ForChoiceAbilityWithCost(
            Cost("Y"), f"Spend [energy]: {nom}", lambda targets, res: action(),
            conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("Y"))]),
        AbilityFactory.ForChoiceAbilityWithCost(
            Cost("2"), f"Spend 2 resources: {nom}", lambda targets, res: action(),
            conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("2"))]),
    ]
