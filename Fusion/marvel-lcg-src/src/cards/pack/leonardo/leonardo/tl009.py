from . import *

# Taicho — AMELIORATION signature, x1. TITLE. Cout 1, [energy].
# Hero Action: Exhaust a [[KATANA]] upgrade you control -> ready this card.
# Hero Response: After an ally takes consequential damage ([consequential]),
#   exhaust this card -> ready that ally.
#
# Cartes de reference :
#  - `drax/19012` Martyr: Phyla-Vell : `AfterAllyTakeConsequentialDamage(
#    Response, ..., op)` ; le message porte `trigger` = l'allie ;
#  - `27018` / `27043` : `CostFunc.Exhaust(trait=..., from_where=[...])` ;
#  - `ho009` : une Hero Action payee par l'inclinaison d'une AUTRE carte.
#
# Mots-pieges :
#  - « Exhaust a [[KATANA]] upgrade you control » : cout sur UN katana, la carte
#    elle-meme n'est PAS inclinee par ce cout ;
#  - « ready THIS card » : sans condition, l'action se proposerait carte deja
#    prete ; on ajoute `conditions=[...IsExhaust()]` pour eviter la boucle
#    (lecon Underling) ;
#  - « an ALLY » : tout allie en jeu (pas seulement les siens), `Ally` nu ;
#  - « takes consequential damage » : seulement si des degats consecutifs ont
#    ete REELLEMENT subis (Tough les empeche, cf. 19012) ;
#  - « exhaust THIS card -> ready THAT ally » : cout = inclinaison de la
#    carte ; l'allie cible est `message.trigger`, et on verifie qu'il est
#    toujours en jeu (il a pu etre vaincu par ces degats).


def GetAbilities() -> Sequence['Ability']:

    def reprendre(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        Faces.ReadyAll([this], effect)

    def redresser_allie(effect: 'Effect', message: 'Message.AfterAllyTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        allie = message.trigger
        if allie is not None and allie.IsInPlay():
            Faces.ReadyAll([allie], effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reprendre,
            conditions=[lambda effect, message: effect.this.IsExhaust()],
        ).SetCostFunc(CostFunc.Exhaust(card_type=Upgrade, trait="KATANA",
                                       from_where=["YouControlCards"])),
        AbilityFactory.AfterAllyTakeConsequentialDamage(
            AbilityType.HeroResponse,
            Ally,
            redresser_allie,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
