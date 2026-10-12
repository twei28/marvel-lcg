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

