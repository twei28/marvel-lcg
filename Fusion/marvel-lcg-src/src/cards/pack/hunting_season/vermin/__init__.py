from cards.pack import *


def EstRat(face: 'CardFace|None') -> bool:
    return face is not None and Minion.IsType(face) and face.HasTrait("RAT")


def RatsEngages(joueur: 'Player') -> List['Minion']:
    return [f for f in joueur.engaged_minions.GetAll() if EstRat(f)]


def MenaceSurLesRats(effect: 'Effect') -> int:
    rats = Worlds.FindCardsOnField(effect, trait="RAT", card_type=Minion)
    return sum(r.CastTo(CanPlaceToken).GetTokens('threat') for r in rats)


def ResoudreSpecialEvenMoreRats(effect: 'Effect') -> None:
    """Special d'Even More Rats (hs006) : menace sur les RAT + sur le complot
    principal >= menace cible, le stade courant est accompli."""
    complot = Worlds.FindMainScheme(effect)
    if complot is None or complot.target_threat is None:
        return
    if complot.threat + MenaceSurLesRats(effect) >= complot.target_threat:
        complot.Advance(None, effect)


def DefausserEtMettreEnJeu(effect: 'Effect', joueur: 'Player', nombre: int, *, tous: bool) -> None:
    """« Discard the top N cards of the encounter deck. Put the first (hs002) /
    each (hs003) RAT minion discarded this way into play engaged with you. »"""
    defaussees = Worlds.DiscardEncounterCards(nombre, effect)
    rats = [f for f in defaussees if EstRat(f)]
    if not tous:
        rats = rats[:1]
    for rat in rats:
        rat.PutIntoPlay(joueur, effect)


def PlaceUneMenaceSurChaqueRat(effect: 'Effect') -> None:
    rats = Worlds.FindCardsOnField(effect, trait="RAT", card_type=Minion)
    if rats:
        Faces.PlaceTokensOn(rats, 1, 'threat', effect)


def ChoisirMenaceOuIndirect(effect, joueur, rat):
    source = effect.this

    def menace(cibles):
        Faces.PlaceTokensOn([rat], 1, 'threat', effect)

    def indirect(cibles):
        identite = joueur.GetIdentity()
        if identite is not None:
            identite.TakeIndirectDamage(source, 1, effect)

    joueur.ChooseAbilities(
        effect,
        AbilityFactory.ForChoiceAbility("Place 1 threat on that minion", menace),
        AbilityFactory.ForChoiceAbility("Take 1 indirect damage", indirect),
    )


def MenaceEtIndirectPourChaqueRat(effect, joueur):
    for rat in RatsEngages(joueur):
        ChoisirMenaceOuIndirect(effect, joueur, rat)
