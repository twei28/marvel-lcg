from . import *
# * Wasp (forme minuscule) — « Bumble Bee » : Response, apres le passage a cette forme, desoriente un sbire ;
# on PEUT payer [mental][mental] pour desorienter le vilain A LA PLACE.
def GetAbilities() -> Sequence['Ability']:
    def bumble_bee(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
        joueur = effect.GetInitiator()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Confuse a minion",
                lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget(Minion, canbe_confused=True),
            AbilityFactory.ForChoiceAbilityWithCost(
                Cost("BB"),
                "Confuse the villain instead",
                lambda cibles, res: Faces.GiveStatus(cibles, "Confused", effect),
                # La branche payante n'est OFFERTE que si le cout est couvrable : sinon le paiement echoue et le moteur
                # annule TOUT le changement de forme (UndoRequest, vu au harnais).
                conditions=[lambda e, m: PeutCouvrirLeCout(joueur, effect, Cost("BB"))],
            ).SetTarget(Villain, canbe_confused=True),
        )
    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            bumble_bee,
            to_this_form=True,
        ).SetName("Bumble Bee"),
    ]
