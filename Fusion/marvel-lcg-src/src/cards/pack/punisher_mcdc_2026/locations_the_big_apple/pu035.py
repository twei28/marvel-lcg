from . import *

# Lower East Side (6) — LIEU (environnement LOCATION).
# Each character (including the villain for players here) in Lower East Side gains retaliate 1.
#
# Cartes de reference : up039 (Tonfa : `message.target.TemporaryGain(effect, would_atk_message, retaliate=+1)` sur `WhenCalculatingAttackDamage`,
# « retaliate 1 for this attack »), 64009 / sm 27067 (`GiveKeywordToInPlayWhenApplyThis(..., retaliate=1, get_new_value=fn, change_on_event=...)`),
# brique `Ville` (`Ville.Case`, message `AfterPlayerMovedInCity` ajoute le 22/10/2026 pour recalculer quand un joueur arrive/part).
# ⚠ « each character IN Lower East Side » : les personnages (identite, allies) des joueurs presents ET les sbires engages avec eux ; PAS ceux des
# joueurs qui sont ailleurs, meme dans la meme rangee. Le vilain n'est pas « dans » le lieu : il gagne retaliate 1 seulement CONTRE les joueurs ici
# (« the villain for players here »), donc par attaque, pas en continu.
# ⚠ `get_new_value` REMPLACE la valeur : rendre 0 hors du lieu.

def GetAbilities() -> Sequence['Ability']:

    def joueur_du_personnage(face: 'CardFace') -> 'Player|None':
        if Minion.IsType(face):
            return face.CastTo(Minion).engaged_player
        if Villain.IsType(face):
            return None
        return face.GetControlByPlayer()

    def retaliate_ici(effect: 'Effect', face: 'CardFace') -> int:
        joueur = joueur_du_personnage(face)
        return 1 if joueur is not None and Ville.Occupe(effect, joueur, effect.this) else 0

    def attaquant_ici(effect: 'Effect', message: 'Message.WhenCalculatingAttackDamage') -> bool:
        attaquant = message.would_atk_message.attacker
        joueur = joueur_du_personnage(attaquant) if attaquant is not None else None
        return Villain.IsType(message.target) and joueur is not None and Ville.Occupe(effect, joueur, effect.this)

    def riposte_du_vilain(effect: 'Effect', message: 'Message.WhenCalculatingAttackDamage') -> None:
        message.target.TemporaryGain(effect, message.would_atk_message, retaliate=+1)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Unit2, retaliate=1, get_new_value=retaliate_ici,
            change_on_event=OnEvent.TemplateTrigger(Message.AfterPlayerMovedInCity),
        ),
        Ability(AbilityType.ForcedInterrupt, Message.WhenCalculatingAttackDamage, [attaquant_ici], riposte_du_vilain),
    ]
