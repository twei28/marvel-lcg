from . import *

# Inside Galactus. ENVIRONNEMENT. COSMIC. LOCATION.
# Residual Cosmic Power. The villain gets +1 ATK.
# Digestive Juices — Forced Response: At the end of the villain phase, deal 2 indirect damage to each player.
#
# Cartes de reference :
#  - « The villain gets +1 ATK » (dynamique : le mechant avec le jeton actif, Coeur OU Metazombie, change en
#    cours de partie) : `AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(check_face_fn=...), attack=1)`,
#    modele sk096 Tarnax VII (« Each SKRULL minion gets +1 ATK »), mais filtre sur « est le mechant actif »
#    (`Villains.Active`) plutot que sur un trait.
#  - « Digestive Juices » : `AbilityFactory.WhenVillainPhaseEnd` + `Players.ForEachPlayer` +
#    `identite.TakeIndirectDamage`, modele cr016 Shi'ar Battle Cruiser (Corsair).
#
# ⚠ Mots-pieges : « the villain », pas « Metazombies » — l'environnement ne buffe que CELUI avec le jeton actif
# (Coeur compris), jamais tous les Metazombies a la fois.


def _est_le_mechant_actif(face: 'CardFace') -> bool:
    from game.effect.rule import GameRule
    from game.card.face.base import Villain
    if not Villain.IsType(face):
        return False
    actif = Worlds.FindVillain(GameRule(face))
    return actif is not None and face.card is actif.card


def GetAbilities() -> Sequence['Ability']:

    def digestive_juices(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        Unused(message)
        this = effect.this

        def frapper(joueur: 'Player') -> None:
            identite = joueur.GetIdentity()
            if identite is not None:
                identite.TakeIndirectDamage(this, 2, effect)

        Players.ForEachPlayer(effect, frapper)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(check_face_fn=_est_le_mechant_actif),
            attack=1,
            # Le bonus ne se recalcule PAS tout seul quand le jeton actif change de carte (rien
            # dans `change_on_event` par defaut pour un `check_face_fn` sans trait) : sans cette ligne,
            # Rhino restait bonifie meme apres que le jeton soit passe a hg001 (mesure le 27/10/2026).
            # Le jeton est un COMPTEUR nomme 'active' (`villain.py:SetActive`, `Faces.PlaceCountersOn`/
            # `RemoveCountersOn`) : `OnEvent.Counter` est le crochet natif pour ca.
            change_on_event=OnEvent.Counter(CardFinder(card_type=Villain), 'active'),
        ),
        AbilityFactory.WhenVillainPhaseEnd(AbilityType.ForcedResponse, digestive_juices),
    ]
