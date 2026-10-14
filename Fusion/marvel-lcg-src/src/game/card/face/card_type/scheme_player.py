from core import *
from game.card.face import *
from game.ability import *
from game.ability.factory import *
from game.message import *

@final
# ⚠ CORRECTIF DU 09/09/2026 — `HasPermanent` ET `HasSetup` AJOUTES.
# Une manigance-joueur PEUT etre permanente et se mettre en place : `ip002a`
# Registration Act (pack iron_patriot, Neptune) imprime « Permanent. Setup. »
# et demarre la partie EN JEU. Sans ces deux attributs, les cles `desc` du
# meme nom font tomber le montage du deck sur un `KeyError: 'Permanent'` —
# attrape par `verifier_tous_les_decks.py`, qui existe pour ca.
# `EncounterSideScheme` les portait deja (scheme_side.py) : la manigance de
# JOUEUR etait la seule des deux a en etre privee, sans raison apparente.
class PlayerSideScheme(SchemeSide2, CanCrisis, HasAmplify, HasVictory, HasPermanent, HasSetup, ClassCard, FinalType):

    @override
    def GetAbilities(self) -> List['Ability']:
        abilities: List['Ability'] = []
        if not self.ability.Find(func_name="Play"):
            abilities.append(
                AbilityFactory.CanPlayThisSchemeCard()
            )
        return abilities + super().GetAbilities()

    @override
    def OnAfterCardEnterPlay(self, message: 'Message.AfterCardEnterPlay') -> None:
        world = self.card.world
        from game.player import Player
        initiateur = getattr(message.by_effect, "initiator", None)
        joueur = initiateur if isinstance(initiateur, Player) and initiateur.IsHero() else None
        world.limit_player_side_scheme.CheckLimit(joueur)
        return super().OnAfterCardEnterPlay(message)

