from . import *

# Normal Again — OBLIGATION. Give to the Buffy Summers player. Uses (3 sanity counters). Victory 0. Boost 2.
# Forced Response: After you use a basic power, remove 1 sanity counter from here.
#
# CARTES DE REFERENCE
#  - `AfterUnitUseBasicPower(ForcedResponse, "You", op)` (14001a, tg001a) ; `Faces.RemoveCountersOn([this], 1, 'sanity', effect)` ;
#    `desc.Uses = "3,sanity"` (modele : obligation `thirst` du pack blade). Le compteur `sanity` a ete ajoute a l'enum `COUNTER`.
#  - `mv012` : `this.GetGaveToPlayer()` pour le joueur a qui l'obligation est donnee.
#
# TEXTE CONTRE CODE
#  « After YOU use a basic power » -> le joueur a qui elle est donnee, TOUT pouvoir de base (ATQ, CTR, DEF, REC) : `powers=None`.
#  Rien n'est imprime pour le dernier compteur : DECISION UTILISATEUR du 31/10/2026, l'obligation se DEFAUSSE a 0 compteur.


def GetAbilities() -> Sequence['Ability']:

    def mon_identite(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> bool:
        this = effect.this.CastTo(Obligation)
        joueur = this.GetGaveToPlayer() or this.GetControlByPlayer()
        return joueur is not None and message.trigger == joueur.GetIdentity()

    def normal_again(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.RemoveCountersOn([this], 1, 'sanity', effect)
        # Decision utilisateur du 31/10/2026 : a 0 compteur l'obligation se defausse.
        if this.GetCounters('sanity') <= 0:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.ForcedResponse,
            Identity,
            normal_again,
            conditions=[mon_identite],
        ),
    ]
