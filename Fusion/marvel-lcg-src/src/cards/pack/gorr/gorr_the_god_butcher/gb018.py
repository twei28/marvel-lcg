from . import *

# Forgotten Gods — COMPLOT ANNEXE. Seuil 3 par joueur, icone de CRISE,
# 1 icone de boost + une etoile.
#
# Forced Response: When the villain phase ends, deal each player 1 indirect
#   damage.
# [star] Boost: Reveal this card.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Crisis` (mots-cles/crisis.md) : BASE AUTOMATIQUE, `desc.Crisis = "1"`.
#   Aucun script : le moteur applique tout seul l'interdiction de recuperer.
# - `Boost` etoile (mots-cles/boost.md) : `WhenCardBecomeBoost`.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « When the villain phase ends » : `WhenVillainPhaseEnd`
#   (turn_phase.py:271), employe par 18025 (Sibling Rivalry).
# - « [star] Boost: Reveal this card » : la carte de boost se revele au lieu
#   d'etre defaussee. C'est le meme detournement qu'an014 : une carte de boost
#   est rangee APRES la resolution de son effet, un `Reveal` immediat serait
#   ecrase. Le montage passe donc par `RegisterTemp` +
#   `WhenCardWouldDiscard`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « WHEN the villain phase ENDS » -> a la fin de la phase, une seule fois par
#   tour, quel que soit le nombre de joueurs.
# « deal EACH PLAYER 1 indirect damage » -> tous les joueurs, chacun 1.
# « [star] Boost: REVEAL this card » -> le complot annexe entre en jeu au lieu
#   de partir a la defausse : c'est une carte de boost qui s'installe.


def GetAbilities() -> Sequence['Ability']:

    def dieux_oublies(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this
        Unused(message)

        def frapper(joueur: 'Player') -> None:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, 1, effect)

        Players.ForEachPlayer(effect, frapper)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        if not joueur:
            return

        def reveler(effet_temp: 'Effect', message2: 'Message.WhenCardWouldDiscard') -> None:
            Unused(message2)
            this.Reveal(joueur, effet_temp)

        this.effect.RegisterTemp(
            AbilityFactory.WhenCardWouldDiscard(
                AbilityType.Temp0,
                "This",
                reveler,
            ),
        )

    return [
        AbilityFactory.WhenVillainPhaseEnd(
            AbilityType.ForcedResponse,
            dieux_oublies,
        ),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
