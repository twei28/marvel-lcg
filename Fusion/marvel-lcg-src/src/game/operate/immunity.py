from . import *

################################################################################
# BRIQUE COMMUNE (20/10/2026) : « ne peut pas etre affecte par les cartes
# joueur » (campagnes Punisher MC×DC et Galactic Storm). Recette :
# docs/reference/RECETTES-MOTEUR.md §15.2, fiche
# docs/reference/mots-cles/immunite-cartes-joueur.md.
#
# Textes servis :
# - Punisher p183 In the Crosshairs : « Attached character ... cannot be
#   affected by player cards. »
# - Galactic Storm p.14, trait HIDDEN : « players cannot affect the villain
#   with player cards. That includes attacking the villain with either heroes
#   or allies, dealing damage to the villain through overkill when a minion is
#   defeated with excess damage, placing a status card on the villain, and
#   attaching upgrades or other player cards to the villain. Players also
#   cannot discard tough status cards from the villain by performing an attack
#   with piercing or by any player card ability ... If a card ability has
#   multiple targets and one of them is the villain, players may only play
#   that card or initiate that ability if there is at least one other valid
#   target ... If ... only one target and that target is the villain, that
#   card cannot be played and the ability cannot be initiated. »
#
# Mecanique : une PROTECTION est un couple (source, s_applique_a). La source
# est la carte qui accorde l'immunite (l'attachement, ou le mechant lui-meme) ;
# elle ne protege que tant qu'elle est EN JEU sur cette face. `s_applique_a(face)`
# dit si une face donnee est protegee (le porteur de l'attachement, le mechant
# tant qu'il a le trait HIDDEN...). Les protections vivent sur le monde.
#
# Les points d'accroche du moteur (chacun commente « brique 2 ») :
#   - choix des cibles      selector.py        GetAllLegalTargets
#   - degats (exces compris) can_health.py     TakeDamageNoDeath
#   - poser un etat          can_status.py     GainStatus
#   - defausser un etat      can_status.py     LoseState (perforant compris)
#   - bonus/mots-cles        face_gain.py      Gain
#   - attacher une carte     asset.py / can_attach.py
#   - poser des compteurs    faces.py          PlaceCountersOn
#
# « Carte joueur » : l'effet est porte par une face `PlayerCard` (identite,
# allie, evenement, amelioration, soutien, ressource, manigance de joueur).
# Exception : la DEFENSE de base, qui designe l'attaquant comme cible
# (`SetTarget("Attacker")`) sans l'affecter. Defendre l'attaque d'un mechant
# protege reste donc possible.
#
class PlayerCardImmunity:

    class Protection:
        def __init__(self, source: 'CardFace', applies_to: Callable[['CardFace'], bool]) -> None:
            self.source = source
            self.applies_to = applies_to

        def IsActive(self) -> bool:
            source = self.source
            return source.card.face is source and source.IsInPlay()

    @staticmethod
    def _Registry(world: 'World') -> List['PlayerCardImmunity.Protection']:
        registre = getattr(world, 'protections_cartes_joueur', None)
        if registre is None:
            registre = []
            world.protections_cartes_joueur = registre
        return registre

    @staticmethod
    def Protect(source: 'CardFace', applies_to: Callable[['CardFace'], bool]) -> None:
        """Inscrit une protection (une seule par source : une seconde
        inscription de la meme face remplace la premiere)."""
        registre = PlayerCardImmunity._Registry(source.card.world)
        registre[:] = [p for p in registre if p.source is not source]
        registre.append(PlayerCardImmunity.Protection(source, applies_to))

    @staticmethod
    def IsPlayerCardEffect(effect: 'Effect|None') -> bool:
        from game.card.face.base import PlayerCard
        if effect is None:
            return False
        this = getattr(effect, 'this', None)
        if this is None or not PlayerCard.IsType(this):
            return False
        ability = getattr(effect, 'ability', None)
        if ability is not None and "DEF" in getattr(ability, 'func_names', ()):
            return False
        return True

    @staticmethod
    def IsProtected(face: 'CardFace|None') -> bool:
        """Cette face est-elle, en ce moment, insensible aux cartes joueur ?"""
        if face is None:
            return False
        registre = getattr(face.card.world, 'protections_cartes_joueur', None)
        if not registre:
            return False
        for protection in registre:
            if protection.IsActive() and protection.applies_to(face):
                return True
        return False

    @staticmethod
    def Refuses(face: 'CardFace|None', effect: 'Effect|None') -> bool:
        """Vrai si `effect` (venant d'une carte joueur) doit rester sans effet
        sur `face`. Rapide quand aucune protection n'existe (cas de toutes les
        parties ordinaires) : aucun message, aucun objet cree."""
        carte = getattr(face, 'card', None)
        if carte is None or effect is None:
            return False
        if not getattr(carte.world, 'protections_cartes_joueur', None):
            return False
        return PlayerCardImmunity.IsPlayerCardEffect(effect) and PlayerCardImmunity.IsProtected(face)
