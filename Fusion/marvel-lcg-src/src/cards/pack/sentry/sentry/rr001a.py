from . import *

# * Sentry (face HEROS) : AERIAL. AVENGER. THW 1 / ATQ 2 / DEF 3, main 4, PV 16.
# Forced Response: At the end of your turn, place 1 balance counter on Duality Aspect.
# Golden Guardian — Once per phase, reduce the resource cost of the next event you play by X, where X is the number of balance counters on Duality Aspect.
#
# CARTES DE REFERENCE
#  - « At the end of your turn » : `so011` / Binary (`AbilityFactory.AfterPlayerTurnEnd(.., "You", op)`) ; type `ForcedResponse` comme le texte.
#  - « balance counter » : compteur maison declare dans `CardFace.COUNTER` (card_face.py) + `compteurs-fr.ts` ; pose par `Faces.PlaceCountersOn` (helper `PoserEquilibre`,
#    qui laisse The Watchtower detourner le compteur : `WhenCardWouldBePlacedCounter`).
#  - « reduce the resource cost of the next event you play » : `dz014` / `sentinel` : `AbilityFactory.WhenCalculateEffectCost(NonKeyword, op, conditions=[..])` + `message.UpdateCost(-X, effect)`.
#
# TEXTE CONTRE CODE
#  « At the end of YOUR turn » : fin du tour de ce joueur (heros seulement : l'alter-ego n'a pas cette capacite). « Forced » : obligatoire, aucun choix.
#  « ONCE PER PHASE » : marqueur `joueur.rr_gg_phase = world.phase_id`, pose quand l'evenement est JOUE (la condition de cout, evaluee plusieurs fois pour l'affichage, reste pure).
#  « the NEXT EVENT you play » : seul un evenement (jamais une amelioration) consomme la reduction ; X est lu au calcul du cout (compteurs sur Duality Aspect, pas « en jeu »).
#  X = 0 : aucune reduction et le marqueur n'est PAS pose (une phase sans compteur ne consomme pas Golden Guardian).
#  Chiffres : PV 16, main 4, THW 1, ATQ 2, DEF 3.


def GetAbilities() -> Sequence['Ability']:

    def un_equilibre(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        Unused(message)
        PoserEquilibre(effect, 1)

    def reduire_le_cout(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> None:
        x = EquilibreSurDualite(effect)
        if x > 0:
            message.UpdateCost(-x, effect)

    def golden_disponible(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        return (joueur is not None and message.is_play and message.GetToPlayer() is joueur
                and message.check_effect is not None and Event.IsType(message.check_effect.this)
                and getattr(joueur, "rr_gg_phase", None) != effect.world.phase_id)

    def noter_l_usage(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or EquilibreSurDualite(effect) <= 0:
            return
        joueur.rr_gg_phase = effect.world.phase_id
        joueur.rr_gg_evenement = message.played_face

    def un_evenement_par_ce_joueur(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        return (joueur is not None and message.GetToPlayer() is joueur
                and getattr(joueur, "rr_gg_phase", None) != effect.world.phase_id)

    return [
        AbilityFactory.AfterPlayerTurnEnd(
            AbilityType.ForcedResponse,
            "You",
            un_equilibre,
        ).SetName("Balance"),
        AbilityFactory.WhenCalculateEffectCost(
            AbilityType.NonKeyword,
            reduire_le_cout,
            conditions=[golden_disponible],
        ).SetName("Golden Guardian"),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Temp0,
            "You",
            CardFinder(card_type=Event),
            noter_l_usage,
            conditions=[un_evenement_par_ce_joueur],
        ),
    ]
