from . import *

# * Yautja Trophy Room — SOUTIEN, cout 2, [mental]. LOCATION.
# Response: After you defeat a minion, place 1 skull counter here.
# Resource: Exhaust Yautja Trophy Room and remove X skull counters from it → generate X [wild] resources.
#
# Cartes de reference :
#  - `an001a` / `vp001a` : `AfterUnitDefeatedUnit(Response, "You", Minion, op)` ; `Faces.PlaceCountersOn([this], 1, 'skull', effect)`
#    (compteur `skull` ajoute a l'enum `COUNTER`, card_face.py, 25/10/2026).
#  - `sm011` Spinnerets (« Remove X web counters → generate X [wild] ») : « retire 1 pion → 1 ressource, autant de fois que de
#    pions », equivalent en jeu (les ressources s'additionnent sur le meme paiement), `SetToAvailableTimesFn` ;
#    `ze011` Mount Olympus : `CostFunc.Custom` pour un cout arbitraire ; `conditions=[...]` OBLIGATOIRE sur `CanGenerateResources`.
#
# ⚠ Mots-pieges :
#  - « EXHAUST ... and remove X counters » : l'inclinaison n'est payee QU'UNE FOIS par paiement, X pions sont retires pour X
#    ressources. Montage : chaque utilisation retire 1 pion ; la premiere incline la carte, les suivantes (meme paiement) la
#    trouvent deja inclinee PAR CE PAIEMENT (marque `_pd_paiement` posee sur l'effet paye, lue par la condition de disponibilite).
#    Une carte inclinee par autre chose reste inutilisable.
#  - « After YOU defeat a minion » : Predator lui-meme, un SBIRE (Minion), pas un allie.
#  - « a Resource: » sans « Hero » : utilisable aux deux formes ; ressource wild (`Resources("G")`).
#  - UNE SEULE `CanGenerateResources` par carte (assert du moteur).


def GetAbilities() -> Sequence['Ability']:

    def trophee(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)
        Faces.PlaceCountersOn([this], 1, 'skull', effect)

    def disponible(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        this = effect.this.CastTo(Support)
        if this.GetCounters('skull') < 1:
            return False
        return this.IsReady() or getattr(this, "_pd_paiement", None) is message.paying_for_effect

    def payer(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(targets)
        this = effect.this.CastTo(Support)
        if this.GetCounters('skull') < 1:
            return False
        if this.IsReady():
            if not Faces.ExhaustAll([this], effect):
                return False
        Faces.RemoveCountersOn([this], 1, 'skull', effect)
        return True

    def marquer_le_paiement(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        effect.this._pd_paiement = message.for_effect  # type: ignore

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Minion,
            trophee,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            conditions=[disponible],
            ex_operation=marquer_le_paiement,
        ).SetCostFunc(CostFunc.Custom(None, payer))
        .SetToAvailableTimesFn(lambda effect, message: effect.this.GetCounters('skull')),
    ]
