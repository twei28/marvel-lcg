from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_fn(effect: 'Effect', last_value: int):
        identity = effect.GetInitiator().GetIdentity()
        n = identity.tough if identity else 0
        return min(n, 4)
    def process_fn(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Ally).GainThwart(diff, effect)
    return [
        AbilityFactory.WhileValid(
            # CORRECTIF (10/10/2026, rapport n75) : le bonus ne se recalculait
            # qu'a l'entree ou la sortie d'un allie. Il suit maintenant chaque
            # Tenace pose sur l'identite ou defausse d'elle (modele d'ecoute :
            # 29030 Lucia von Bardas, `OnEvent.Status`).
            [OnEvent.CardInPlay(Ally), OnEvent.Status("YourIdentity", 'Tough')],
            lambda effect, message: True,
            check_fn,
            process_fn,
        ),
    ]
