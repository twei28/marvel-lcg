from . import *

# Embody the Dragon — AMELIORATION, cout 0, [physical]. TECHNIQUE. x1 (Iron Fist 12/15).
# Temporary.
# Iron Fist gains retaliate X, where X is equal to the number of chi counters on this card.
# Hero Action: Move 1 chi counter from Iron Fist to this card.
#
# CARTES DE REFERENCE
#  - « gains <mot-cle> X, X dynamique » sur une AUTRE carte : `hc014` Battle for a Soul
#    (`GiveKeywordToInPlayWhenApplyThis(finder, ..., get_new_value=fn)`, RECETTES §3) ;
#    rafraichi quand un compteur change : `sm/sandman/27067` Sand Clone
#    (`change_on_event=OnEvent.Counter(..., 'sand')`).
#  - retaliate accorde a l'identite : `hood/24038`, `next_evol/40090` (`retaliate=2`).
#  - Hero Action sur une amelioration : `human_torch/ht006`.
#
# TEXTE CONTRE CODE
#  ⚠ « IRON FIST gains » : le NOM de la face heros, jamais Danny Rand (RECETTES §3 « NOM gets »
#    vs « YOU get ») : cible = la face `Hero` controlee par le joueur ; contre-cas en alter ego.
#  ⚠ « X = chi counters ON THIS CARD » : ceux de l'amelioration, pas ceux de l'identite.
#  ⚠ « MOVE 1 chi counter from Iron Fist to this card » : le compteur PART de l'identite et ARRIVE
#    ici (pas de duplication) ; pas de fleche : ce n'est pas un cout, mais sans compteur sur
#    l'identite l'action ne changerait rien, elle n'est donc pas offerte.
#  ⚠ Temporary : base automatique ; perdu tant que Danny Rand est face visible (64001b).


def GetAbilities() -> Sequence['Ability']:

    def chi_ici(effect: 'Effect', face: 'CardFace') -> int:
        Unused(face)
        return Chi(effect.this)

    def deplacer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        identite = IdentiteDuJoueur(effect)
        if identite is None or Chi(identite) < 1:
            return
        Faces.RemoveCountersOn([identite], 1, CHI, effect)
        Faces.PlaceCountersOn([this], 1, CHI, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Hero,
            control_by="You",
            retaliate=1,
            get_new_value=chi_ici,
            change_on_event=OnEvent.Counter("This", CHI),
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deplacer,
            conditions=[AuMoinsChi(1)],
        ),
    ]
