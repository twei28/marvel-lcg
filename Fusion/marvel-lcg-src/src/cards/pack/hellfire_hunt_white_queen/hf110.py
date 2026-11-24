from . import *

# Psionic Feedback. Attachement SKILL, +1 SCH / +1 ATK (desc). « Attach to White Queen. Forced Response : After White Queen flips, give her
# 1 facedown boost card. Hero Action : Spend [mental][physical] resources -> discard this card. [star] Boost : Reveal this card. »
# Icones de ressource lues contre les cartes du MEME pack (so002 = poing = [physical] R, rm004 = noeuds relies = [mental] B), puis
# `Cost("BR")`. Cartes de reference : 04075 Exo-Suit (`PlayerActionToDiscardThis(HeroAction).SetCost(Cost(...))`), 04084 (`RevealThisCard`),
# tk009 (Reponse forcee « After X flips » : `Message.AfterCardFlip`, `message.to_face`).


def GetAbilities() -> Sequence['Ability']:
    def apres_retournement(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        villain = VilainWQ(effect)
        if villain is not None:
            Faces.GiveFacedownBoostCards([villain], 1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(ChercheurWQ()),
        Ability(AbilityType.ForcedResponse, Message.AfterCardFlip,
                [lambda effect, message: Villain.IsType(message.to_face) and message.to_face.IsName(NOM_WQ)],
                apres_retournement),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BR")),
        AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard),
    ]
