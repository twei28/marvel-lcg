from . import *

# Detonate

def GetAbilities() -> Sequence['Ability']:

    # « une amelioration que vous controlez AVEC DES COMPTEURS DESSUS » : le
    # filtre est porte par le selecteur, pas verifie apres coup, sinon le joueur
    # pourrait designer une carte nue et l'effet vaudrait zero.
    def a_des_compteurs(effect: 'Effect', face: 'CardFace') -> bool:
        return face.CastTo(CanPlaceCounter).GetAllCounters() > 0

    def detonate(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()

        # Compter AVANT de defausser : une carte qui quitte le jeu perd ses
        # compteurs, et « X est le nombre de compteurs defausses ainsi ».
        valeur = sum(f.CastTo(CanPlaceCounter).GetAllCounters() for f in effect.targets)
        Faces.DiscardAll(effect.targets, effect)
        if valeur <= 0:
            return

        cibles: List['CardFace'] = []
        villain = Worlds.FindVillain(effect)
        if villain:
            cibles.append(villain)
        cibles += [x for x in Worlds.FindCardsOnField(effect, card_type=Minion,
                                                      engaged_with=initiator)
                   if not x.IsDefeated()]
        if cibles:
            this.DealDamage(cibles, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            detonate
        ).SetPlay().SetLabel('attack')
        .SetTarget(
            finder=CardFinder(card_type=Upgrade, check_effect_fn=a_des_compteurs),
            from_where=["YouControlCards"],
            range=(1, 1)
        ),
    ]
