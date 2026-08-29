from . import *

# Mitigated Threat
#
# « Attached card loses each [acceleration], [amplify], [crisis], and [hazard]
# icon. »
# Les quatre icones sont de vrais mots-cles du moteur (`CardFace.KEY`), donc
# modifiables par `GainKeyword`. `GiveKeywordToAttached` ne les expose pas et
# `GiveKeywordToInPlayWhenApplyThis` n'expose qu'acceleration et hazard : on
# passe donc par `WhileValid`, qui suit la valeur imprimee de la carte portante
# et applique en continu l'oppose. Un `WhileValid` ne suit qu'un entier, d'ou
# une capacite par icone.
#
# On lit la valeur IMPRIMEE et non la valeur effective : cette derniere inclut
# deja notre propre retrait, et la boucle ne convergerait pas.

ICONES = ("Acceleration", "Amplify", "Crisis", "Hazard")

CHAMP_IMPRIME = {
    "Acceleration": "printed_acceleration_icon",
    "Amplify":      "printed_amplify",
    "Crisis":       "printed_crisis",
    "Hazard":       "printed_hazard",
}


def GetAbilities() -> Sequence['Ability']:

    def retrait_icone(icone: str) -> 'Ability':
        champ = CHAMP_IMPRIME[icone]

        def combien(effect: 'Effect', last_value: int) -> int:
            porteuse = effect.this.CastTo(Upgrade).bind_face
            if porteuse is None:
                return 0
            return getattr(porteuse, champ, 0) or 0

        def applique(effect: 'Effect', diff: int, curr: int) -> None:
            porteuse = effect.this.CastTo(Upgrade).bind_face
            if porteuse is None or diff == 0:
                return
            porteuse.GainKeyword(-diff, icone, effect)

        return AbilityFactory.WhileValid(
            [OnEvent.Icons("InPlay"), OnEvent.PlayAreaCard("This")],
            lambda e, m: True,
            combien,
            applique,
        )

    def depense_ou_defausse(effect: 'Effect', message: 'Message.AfterRoundEnd') -> None:
        # « each player may spend 1 resource of any type. If any player does
        # not, discard this card. »
        this = effect.this.CastTo(Upgrade)
        tous_ont_paye = True
        for player in Worlds.GetPlayers(effect):
            if not CostFunc.Spend(Cost("1")).PayCost(effect, player):
                tous_ont_paye = False
        if not tous_ont_paye:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CardFinder()),
        *[retrait_icone(icone) for icone in ICONES],
        AbilityFactory.AfterRoundEnd(AbilityType.ForcedResponse, depense_ou_defausse),
    ]
