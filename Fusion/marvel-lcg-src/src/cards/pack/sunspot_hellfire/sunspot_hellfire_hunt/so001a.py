from . import *

# * Sunspot (face HEROS) — X-FORCE. PV 10, THW 0, ATK 0, DEF 0, main 5.
# Solar Rechanneling — Interrupt: When you use one of Sunspot's basic powers (THW, ATK, or DEF), remove X solar counters
#   from Sunspot -> Sunspot gets +X to that chosen power for this use. If you removed at least half of the counters,
#   ready Sunspot.
# Forced Response: At the end of each phase, if Sunspot has no solar counters, exhaust Sunspot and flip him into his
#   alter-ego form.
#
# CARTES DE REFERENCE
#  - `14002` Scarlet Witch / `27047` Dum Dum Dugan : `WhenUnitUseBasicPower(Interrupt, "This", op)` + `message.GainValue(n, effect)`
#    (le bonus vaut pour LE pouvoir utilise, ATK, THW ou DEF : « that chosen power »).
#  - `sw006`/`sw007` (Spider-Woman) : X choisi par le joueur, depense depuis l'identite (helpers du set).
#  - `14001a` Quicksilver : `Faces.ReadyAll(effect.targets, effect)` avec `.SetTarget("YourHero")`.
#  - `35002`-like / `wn001a` : `joueur.GetIdentity().ChangeToOtherIdentityForm(effect)` (Split Personality 01025).
#
# TEXTE CONTRE CODE
#  ⚠ « at least HALF of the counters » : la moitie du STOCK AVANT le retrait (retire * 2 >= stock) ; on ne relit pas le stock apres.
#  ⚠ X = 0 ne fait rien (rien de retire, pas de redressement).
#  ⚠ « At the end of EACH phase » : phase des joueurs ET phase du mechant (`AfterPhaseEnd(.., None, ..)`).
#  ⚠ Le Forced Response n'existe que face HEROS : sous forme d'alter ego le heros n'est pas la face visible.


def GetAbilities() -> Sequence['Ability']:

    def solar_rechanneling(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        Unused(message)
        joueur = JoueurQuiControle(effect)
        if joueur is None:
            return
        stock = SolairesDe(joueur)
        if stock <= 0:
            return
        retire = RetirerSolaires(joueur, DemanderCombien(joueur, effect), effect)
        if retire <= 0:
            return
        message.GainValue(retire, effect)
        if retire * 2 >= stock:
            Faces.ReadyAll(effect.targets, effect)

    def reflux(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        Unused(message)
        joueur = JoueurQuiControle(effect)
        if joueur is None or SolairesDe(joueur) > 0:
            return
        Faces.ExhaustAll([effect.this], effect)
        joueur.GetIdentity().ChangeToOtherIdentityForm(effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            solar_rechanneling,
        ).SetTarget("YourHero")
        .SetName("Solar Rechanneling"),
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            None,
            reflux,
        ),
    ]
