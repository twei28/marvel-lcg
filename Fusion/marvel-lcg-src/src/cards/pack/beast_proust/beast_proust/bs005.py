from . import *

# Peter's Spider-Tracers : AMELIORATION (TECH), cout 3, [energy].
# This card enters play with 4 tracer counters on it. Reduce the cost of this card by 1 if you control an upgrade with the TECH trait.
# Resource: Remove 1 tracer counter from this card -> generate 1 [mental] resource for a TECH card. (Limit once per card.)
#
# CARTES DE REFERENCE
#  - `53006` Falcon's Flock : `CanGenerateResources(Resource, Resources(..), CardFinder2(<trait>)).SetCostFunc(CostFunc.Counter("This", 1, <pion>))` ; `16036` Particle Cannon : `ThisEnterPlayWithCounters`
#    (PAS la cle `Uses`, qui defausserait la carte au dernier pion : ce texte ne le dit pas).
#  - `nt005` : `ReduceCostToPlayThis(1, conditions=[..])`.
#  - ICONE de ressource : le « noeuds relies » du scan est la ressource [mental] (`desc.RES = B`), verifie contre bs008 Xavier's Cerebro (meme icone sur sa pastille, `RES = B`) et lj005 Kamala's Room.
#
# TEXTE CONTRE CODE
#  « enters play with 4 TRACER counters » : 4 pions `tracer`. « Resource » (pas « Hero Resource ») : `AbilityType.Resource`. « for a TECH CARD » : tout type de carte portant TECH (`CardFinder2("TECH")`). « Remove 1 tracer
#    counter FROM THIS CARD » : cout. « Limit once per CARD » : au plus une ressource de cette carte par carte payee (temoin dans les cas).
#  Chiffres : cout 3, 4 pions, 1 ressource.


def GetAbilities() -> Sequence['Ability']:

    def controle_une_amelioration_tech(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        return joueur is not None and bool(AmeliorationsTech(joueur))

    def reste_un_pion(effect: 'Effect', message: Any) -> bool:
        Unused(message)
        return effect.this.CastTo(Upgrade).GetCounters('tracer') > 0

    return [
        AbilityFactory.ReduceCostToPlayThis(1, conditions=[controle_une_amelioration_tech]),
        AbilityFactory.ThisEnterPlayWithCounters(4, 'tracer'),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B"),
            CardFinder2("TECH"),
            conditions=[reste_un_pion],
        ).SetCostFunc(CostFunc.Counter("This", 1, 'tracer')),
    ]
