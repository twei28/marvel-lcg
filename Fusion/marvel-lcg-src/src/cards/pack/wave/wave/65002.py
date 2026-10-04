from . import *

# * Sea Hunter
#
# Response: After Sea Hunter attacks or thwarts, flip a faceup card in your
# Rising Tide area and pay the printed cost of an event in your discard pile
# -> play that event as though it were in your hand.
#
# ⚠ LA CARTE LA PLUS RISQUEE DU PACK, ET C'EST DIT ICI PLUTOT QUE CACHE. Le
# cout est DOUBLE et DYNAMIQUE (retourner une carte de Rising Tide ET payer un
# montant qui depend de l'evenement choisi), sans precedent exact trouve
# ailleurs dans le depot. Implementation : le joueur CHOISIT D'ABORD
# l'evenement de sa defausse (aucun cout encore engage), PUIS retourne la
# carte de Rising Tide, PUIS `PlayCardsLikeInTurn` paye le cout imprime -- qui
# verifie lui-meme la solvabilite avant de rien engager (meme garde que le
# correctif du paiement atomique, `EffectChecker.check_pay`). Si le joueur
# choisit de ne rien jouer (`forced=False`), rien n'est retourne ni depense.
# NON VERIFIE EN PARTIE REELLE : voir la gate du gabarit PROCESSUS-CARTE.

def GetAbilities() -> Sequence['Ability']:

    def sea_hunter(effect: 'Effect', message: 'Message.AfterUnitAttackEnd|Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        if not isinstance(joueur, Player):
            return

        # Rien a proposer sans carte face visible a retourner.
        if not CartesDansRisingTide(joueur, face_visible=True):
            return

        evenements = [f for f in joueur.discard_pile.GetAll(False)
                      if Event.IsType(f) and f.CanPlayBy(joueur)]
        if not evenements:
            return

        choisi = joueur.AskChooseFace(
            evenements, effect, peek=True, forced=False,
            prompt="Play from your discard pile",
        )
        if choisi is None:
            return

        RetournerUneCarteRisingTide(
            effect, joueur, face_visible=True, forced=True,
            prompt="Flip to play a discarded event",
        )
        joueur.PlayCardsLikeInTurn([choisi], effect, forced=True)

    return [
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.Response, "This", sea_hunter,
        ).SetName("Sea Hunter"),
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.Response, "This", sea_hunter,
        ).SetName("Sea Hunter"),
    ]
