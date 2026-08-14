from . import *

# FBI Investigation

def GetAbilities() -> Sequence['Ability']:

    def enquete(effect: 'Effect', message: 'Message.AfterUnitDefeatedScheme') -> None:
        # « Forced Response: After a card you control defeats a side scheme,
        # place 1 clue counter here. Then, if there are at least 3 clue counters
        # here, discard this card and place 1 pursuit counter on Pursued by the
        # Past. »
        #
        # La seule carte du set qui joue POUR les heros : trois manigances
        # abattues et l'obligation part. Mais elle nourrit Pursued by the Past
        # en s'en allant — chez Fisk, rien n'est gratuit.
        this = effect.this.CastTo(Obligation)
        Faces.PlaceCountersOn([this], 1, 'clue', effect)
        if this.GetCounters('clue') >= 3:
            Faces.DiscardAll([this], effect)
            CompteursDePoursuite(effect, 1)

    return [
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.ForcedResponse,
            "YouControlCharacter",
            SchemeSide2,
            enquete,
        ),
    ]
