from . import *

# Phoenix Specimen Brainwashing — attachement de l'ennemi juré. PSIONIC. Pas d'icone de boost.
# Attach to your identity.
# [star] Forced Response: After the end of the villain phase, discard 1 card from your hand at random, place X threat on a
# scheme, where X is equal to the numeral in the printed resource cost of that card.
# Hero Action: Spend a [mental] resource -> discard this card.
#
# Cartes de reference : `tg016` Chomped (`AttachToFaceWhenPutIntoPlay("YourIdentity")` pour un ATTACHEMENT « attach to your
# identity ») ; `AfterPhaseEnd(ForcedResponse, "Villain", ..)` (uw014) ; `.SetCost(Cost("B"))` d'une Hero Action payee en
# ressource ; `PlaceThreatOnSchemes(cibles, n, effect)` (« a scheme » : le joueur choisit).
#
# Mots-pieges : « the END of the villain phase » ; « at random » ; « place X threat on A scheme » (un complot au choix du
# joueur, choisi APRES la defausse puisque X en depend) ; main vide : X = 0, rien n'est pose.


def GetAbilities() -> Sequence['Ability']:

    def brainwashing(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Attachment)
        identite = this.bind_face
        if identite is None:
            return
        joueur = identite.GetControlByPlayer()
        faces = joueur.DiscardRandomHandCards(1, effect)
        x = CoutImprime(faces[0]) if faces else 0
        if x <= 0:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                f"Place {x} threat on a scheme",
                lambda cibles: this.PlaceThreatOnSchemes(cibles, x, effect),
            ).SetTarget(Scheme2, can_place_threat=True),
        )

    def se_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            "YourIdentity",
        ),
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Villain",
            brainwashing,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            se_defausser,
        ).SetCost(Cost("B")),
    ]
