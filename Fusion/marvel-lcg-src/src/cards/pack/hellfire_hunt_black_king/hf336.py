from . import *

# Ambient Energy Absorption (x2, hf336-hf337). Traitrise SKILL. « When Revealed : Choose a set-aside Sebastian Shaw attachment and reveal it. Give this
# card to the enemy who attached that attachment as a facedown boost card. Otherwise, this card gains surge. [star] Boost : Give this enemy 1 additional
# boost card for this activation. »
# Cartes de reference : 49042 Power and Decadence (`villain.GiveBoostCard(this, effect)`), ap024 (`ChooseAbilities`), 60075 ; hf118 (`ThisCardGainSurge`) ;
# boost : 02035 Intimidation / 01164 (`message.GiveBoostCardForThisActivation(face, 1, effect)` ; on passe l'ennemi qui active : sans cela le moteur ne sert que le VILAIN).
# ⚠ « Give this card to the enemy WHO ATTACHED that attachment » = l'ennemi porteur (Shaw, ou le vilain si Shaw n'est pas la) ; sans attachement de cote,
# la carte gagne surge ; « 1 additional boost card FOR THIS ACTIVATION » : une carte de boost de plus pour CETTE activation.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        candidats = AttachementsDeShawMisDeCote(effect)
        if not candidats:
            ThisCardGainSurge(effect)
            return
        titres = {}
        for f in candidats:
            titres.setdefault(f.paper.name, f)
        choix = list(titres.values())
        carte = choix[0] if len(choix) == 1 else joueur.AskChooseFace(choix, effect)
        if carte is None:
            ThisCardGainSurge(effect)
            return
        carte.Reveal(joueur, effect)
        hote = carte.bind_face
        if hote is not None and hote.IsInPlay():
            hote.GiveBoostCard(this, effect)
        else:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        ennemi = message.being_message.by_face
        if ennemi is not None:
            message.GiveBoostCardForThisActivation(ennemi, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
