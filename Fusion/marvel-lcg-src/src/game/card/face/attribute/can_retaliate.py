from . import *

class HasRetaliate(HasAttribute):
    @override
    def __init__(self, paper: 'Paper') -> None:
        self.printed_retaliate = 0

        super().__init__(paper)

        self.RegisterAttribute("Retaliate", "printed_retaliate")
        self.RegisterInfoDict('retaliate')

    @override
    def OnResetKeywords(self, by_effect: 'Effect'):
        self.GainRetaliate(self.printed_retaliate, by_effect)
        return super().OnResetKeywords(by_effect)

    ################################################################################
    #
    @final
    def GainRetaliate(self, diff: int, by_effect: 'Effect'):
        self.GainKeyword(diff, 'Retaliate', by_effect)

    @final
    @property
    def retaliate(self) -> int:
        return self.GetKeyword('Retaliate')

class CanRetaliate(HasRetaliate):

    @staticmethod
    def AbiliteRiposte() -> 'Ability':
        """RR 1.8 p.38 : « Retaliate X » equivaut a « Forced Response : After this character
        is attacked, deal X damage to the attacker. » UNE capacite pour toute la partie, posee
        par `EventManager.RegisterPlayRule` SEULEMENT sous `v18_retaliate` : par carte, elle
        decalerait les identifiants d'effets (rejeu des sauvegardes d'avant) et casserait les
        faces creees sans carte (`TreatAsMinion`, mw026 Veranke)."""
        def riposte(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
            message.attacked.CastTo(CanRetaliate).ResolveRetaliate(message.would_atk_unit_message)

        def a_riposte(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
            cible = message.attacked
            return CanRetaliate.IsType(cible) and cible.IsInPlay() and cible.retaliate > 0

        return AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            None,
            None,
            riposte,
            conditions=[a_riposte]
        ).SetName("Retaliate").NoOutOfPlayLimit()

    @staticmethod
    def _JournaliserRiposte(riposteur: 'Any', attaquant: 'Any', valeur: int, resultat: 'Any') -> None:
        """Refonte de la phase du mechant (lot 5b) : la Riposte est accrochee au fait
        d'attaque qu'elle suit (meme attaquant, meme cible), pour son ecran a part.
        Journal d'affichage : sous garde, il ne peut rien interrompre."""
        try:
            world = riposteur.card.world
            subi = getattr(resultat, 'took_damage', valeur) if resultat is not None else 0
            riposte = {
                'degats': subi if isinstance(subi, int) else valeur,
                'restant': getattr(attaquant, 'health', None),
                'vaincu': bool(attaquant.IsDefeated() or not attaquant.IsInPlay()),
            }
            for fait in reversed(world.stat.faits_mechant):
                if fait.get('genre') == 'attaque' and fait.get('etat') in (None, 'resolu') \
                        and fait.get('auteur_id') == attaquant.card.object_id \
                        and fait.get('cible_id') == riposteur.card.object_id and 'riposte' not in fait:
                    fait['riposte'] = riposte
                    return
            # Riposte AVANT le journal (regles d'avant la 1.8) : le fait d'attaque la reprend.
            attente = world.stat.__dict__.setdefault('ripostes_en_attente', {})
            attente[(attaquant.card.object_id, riposteur.card.object_id)] = riposte
        except Exception:
            pass

    @final
    def ResolveRetaliate(self, atk_message: 'Message.WhenUnitWouldAttackUnit'):
        from game.effect.rule import Retaliate

        if self.retaliate > 0:
            attacker = atk_message.attacker
            if attacker and not attacker.IsDefeated():
                if not atk_message.IsRanged() and \
                    not self.IsDefeated() and \
                    not atk_message.IsIgnoreRetaliate():
                    resultat = attacker.TakeDamage(self, self.retaliate, Retaliate(self))
                    CanRetaliate._JournaliserRiposte(self, attacker, self.retaliate, resultat)
                    return resultat
                else:
                    ignore_message = Message.AfterIgnoreKeywordOnCard(attacker, [self], "Retaliate")
                    ignore_message.Send()
                    return None

