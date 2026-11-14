from . import *

# Judgement Day — TRAITRISE (Accuser Corps). 2 icones de boost.
# When Revealed: Each ACCUSER CORPS enemy activates against you. If no enemy activated this way, search
#   the encounter deck and discard pile for a Kree Accuser and reveal it.
#
# Cartes de reference :
#  - « Each ACCUSER CORPS enemy activates against you » : `face.DoActivate(joueur, effect)`, modele
#    OFFICIEL 11051 Ancient Grudge, applique a chaque ennemi du trait trouve en jeu.
#  - « If no enemy activated this way, search ... and reveal it » : `Search.EncounterCard`, modele gs141a
#    (meme pack).
#
# ⚠ Mots-pieges : « EACH ACCUSER CORPS enemy » (tous, pas un seul choisi) ; « If NO enemy activated this
# way » = seulement si la liste etait VIDE au depart, pas si une activation echoue en cours de route.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        cibles = [f for f in Worlds.GetOnFieldCards(effect)
                  if Enemy.IsType(f) and f.IsInPlay() and f.HasTrait("ACCUSER CORPS")]
        if cibles:
            for cible in cibles:
                cible.CastTo(Enemy).DoActivate(joueur, effect)
        else:
            face = Search.EncounterCard(effect, joueur, include_discard_pile=True, name="Kree Accuser", card_type=Minion)
            if face is not None:
                face.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
