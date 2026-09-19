from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout

# Helpers du set Typhoid Mary (Fear No Evil, 60110-60120).
# Le vilain est une carte RECTO-VERSO (Typhoid Mary / Bloody Mary), sur une
# face au hasard a la mise en place, retournee a la fin de chaque phase du
# mechant. On ne le vainc pas : chaque « defaite » pose un jeton damage sur
# Disturbed Psyche et remet ses PV ; Establish Trust vaincue pose un jeton
# threat. Trois jetons = victoire. Modele du vilain : MaGog 39001a/b.


def TrouverMary(effect: 'Effect') -> 'Villain|None':
    """La face active, quelle qu'elle soit."""
    for nom in ("Typhoid Mary", "Bloody Mary"):
        v = Worlds.FindCardOnField(effect, name=nom, card_type=Villain)
        if v:
            return v
    return None


def TrouverDisturbedPsyche(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name="Disturbed Psyche", card_type=Environment)


def TrouverMaryWalker(effect: 'Effect') -> 'Attachment|None':
    return Worlds.FindCardOnField(effect, name="Mary Walker", card_type=Attachment)


def MaryActive(effect: 'Effect', nom: str) -> bool:
    """« If Typhoid Mary is activating » / « If Bloody Mary is activating » :
    la face VISIBLE du vilain porte ce nom."""
    v = TrouverMary(effect)
    return v is not None and v.IsName(nom)


def JetonsPsyche(effect: 'Effect') -> int:
    env = TrouverDisturbedPsyche(effect)
    if env is None:
        return 0
    return env.GetTokens('damage') + env.GetTokens('threat')


def VerifierVictoire(effect: 'Effect') -> None:
    """If there are 3 or more tokens here, the players win the game!"""
    if JetonsPsyche(effect) >= 3 and not Worlds.IsGameOver(effect):
        Worlds.SetGameOver(True, effect)


def FlipMaryWalkerVersEstablishTrust(effect: 'Effect', joueur: 'Player') -> None:
    """« flip it and reveal Establish Trust » : l'attachement Mary Walker
    (113b) se retourne en manigance Establish Trust (113a), qui est revelee."""
    mw = TrouverMaryWalker(effect)
    if mw is None:
        return
    mw.card.Flip(effect, call_reveal=False)
    face = mw.card.face
    face.Reveal(joueur, effect)


def CapacitesDeMary(pv: str) -> Sequence['Ability']:
    """Forced Interrupt : When <Mary> would be defeated, place 1 damage token
    on Disturbed Psyche instead and reset her hit points to N[per_hero]."""
    def vaincue(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(EncounterVillain)
        message.SetBeInstead(effect)
        this.ResetHealth(effect, num=pv)
        env = TrouverDisturbedPsyche(effect)
        if env:
            Faces.PlaceTokensOn([env], 1, 'damage', effect)
        VerifierVictoire(effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, "This", vaincue),
    ]
