from . import *

# * Tony's Workshop — soutien signature, x1 (n/15 = 9).
# LOCATION. Cout 1, ressource [physical].
# Alter-Ego Action: Exhaust Tony's Workshop -> heal 1 damage from Tony Stark
#   and place 1 reactor counter on him.
#
# Cartes de reference :
#  - `aa003` * Ebony pour le squelette « soutien + Alter-Ego Action payee par
#    `CostFunc.Exhaust("This")` » ;
#  - `38007` Energy Transfer / `hk011` pour `HealthUnits` ;
#  - `im001a` du meme pack pour `Faces.PlaceCountersOn`.
#
# ⚠ PAS DE `CanPlayThisSupportCard()`. Releve du 03/09/2026 sur tout le
# depot : **212 soutiens sur 257 ne l'appellent pas**, et la mesure faite le
# meme jour sur ls002 a montre qu'un ALLIE entre en jeu sans l'equivalent —
# la fabrique ne sert qu'aux cartes jouees hors de leur tour ou sous
# condition. Le cas de test de cette carte le verifiera.

# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « heal 1 damage from **Tony Stark** ... and place 1 reactor counter on
#    **him** » : les deux visent la MEME carte, l'identite. On passe par
#    `GetIdentity()`, pas par un `CardFinder(name="Tony Stark")` — `si016`
#    * Tony Stark A.I. est un sbire nemesis qui porte presque ce nom, et
#    l'alter-ego OFFICIEL `01029b` le porte exactement.
#  - `Alter-Ego Action` : rien en forme de heros. C'est la seule source de
#    compteur accessible en forme civile, et elle soigne en meme temps — sur
#    un heros a 10 PV, c'est la carte de temporisation du pack.
#  - « Exhaust ... -> » : cout, donc une fois par round.
#  - ⚠ Cette carte est nommee par l'obligation `im014`, qui exige de
#    l'incliner pour la branche indolore : les deux se lisent ensemble.


def GetAbilities() -> Sequence['Ability']:

    def tonys_workshop(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        this.HealthUnits([identite], 1, effect)
        Faces.PlaceCountersOn([identite], 1, 'reactor', effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            tonys_workshop,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
