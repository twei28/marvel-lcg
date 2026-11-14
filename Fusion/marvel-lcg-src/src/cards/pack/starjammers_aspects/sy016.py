from . import *
# * Binary: Carol Danvers (Aggression, allie 5 [energy], 3*/2*, PV 4). AERIAL. STARJAMMER.
# Response: After Binary enters play, discard the top 4 cards of your deck. If you discard a printed [physical] resource, deal 3
# damage to an enemy. If you discard a printed [energy] resource, stun an enemy.
#
# Cartes de reference : dt002 Moon Knight (`DiscardDeckTopCards`... + `FacesCounter.GetPrintedResources(faces)` : `res.r / res.y` sont
# les icones IMPRIMEES, un wild (`res.g`) ne compte pas comme physique ou energie ; un `if` par ligne, car une carte peut avoir
# plusieurs icones) ; 01083 Mockingbird (stun) ; RECETTES §2.
# « If you discard a printed [physical] resource » : AU MOINS UNE des 4 cartes (une seule fois, pas une fois par carte).
# Les deux conditions sont independantes : 3 degats ET sonne si les deux icones sont defaussees.
def GetAbilities() -> Sequence['Ability']:
    def binary(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = effect.GetInitiator()
        faces = joueur.DiscardDeckTopCards(4, effect)
        if not faces:
            return
        res = FacesCounter.GetPrintedResources(faces)
        if res.r:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 3 damage to an enemy",
                    lambda targets: this.DealDamage(targets, 3, effect)
                ).SetTarget(Enemy),
            )
        if res.y:
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Stun an enemy",
                    lambda targets: Faces.GiveStatus(targets, "Stunned", effect)
                ).SetTarget(Enemy, canbe_stunned=True),
            )
    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            binary,
        ),
    ]
