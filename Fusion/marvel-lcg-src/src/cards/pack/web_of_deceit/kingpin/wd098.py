from . import *

# Controlling the Narrative

def GetAbilities() -> Sequence['Ability']:

    def cible(effect: 'Effect') -> 'CardFace|None':
        # « Attach to the non-permanent side scheme with the most remaining
        # threat without another copy of Controlling the Narrative attached. »
        candidates = []
        for manigance in Worlds.GetSideSchemes(effect):
            if manigance.CastTo(HasPermanent).permanent:
                continue
            if manigance.GetInventoryDeck().FindCards(name="Controlling the Narrative"):
                continue
            candidates.append(manigance)
        if not candidates:
            return None
        return sorted(candidates, key=lambda x: x.threat)[-1]

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        hote = cible(effect)
        if hote:
            this.PutIntoPlay(message.GetToPlayer(), effect)
            this.AttachTo2(hote, effect)
        else:
            # « If you cannot, this card gains surge. »
            ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
        # « Attached scheme gains the [acceleration][crisis] icons. »
        #
        # Ni `acceleration_icon` ni `crisis` ne sont des parametres nommes de
        # `GiveKeywordToAttached` — ce sont pourtant deux mots-cles que
        # `CardFace.Gain` sait donner. On passe donc par `apply`, la porte que
        # la fabrique laisse ouverte pour exactement ce cas.
        *AbilityFactory.GiveKeywordToAttached(
            apply=lambda effect, face, diff:
                face.Gain(effect, diff, acceleration_icon=1, crisis=1),
        ),
    ]
