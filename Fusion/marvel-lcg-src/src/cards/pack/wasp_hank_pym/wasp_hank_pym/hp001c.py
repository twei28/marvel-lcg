from . import *
# * Wasp (forme geante) — « Man-Mountain » : apres le passage a cette forme, etourdit un sbire ;
# on PEUT payer [physical][physical] pour etourdir le vilain A LA PLACE.
def GetAbilities() -> Sequence['Ability']:
    def man_mountain(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun a minion",
                lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect),
            ).SetTarget(Minion, canbe_stunned=True),
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("RR"),
                "Stun the villain instead",
                lambda cibles, res: Faces.GiveStatus(cibles, "Stunned", effect),
                # La branche payante n'est OFFERTE que si le cout est couvrable : sinon le paiement echoue et le moteur
                # annule TOUT le changement de forme (UndoRequest, vu au harnais).
                conditions=[lambda e, m: PeutCouvrirLeCout(joueur, effect, Cost("RR"))],
            ).SetTarget(Villain, canbe_stunned=True),
        )
    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            man_mountain,
            to_this_form=True,
        ).SetName("Man-Mountain"),
    ]
