from . import *

# Predatory Instincts — AMELIORATION, cout 2, [mental]. SUPERPOWER.
# Blade gets +1 DEF.
# Hero Response: After an enemy enters play, exhaust Predatory Instincts ->
#   search your deck and discard pile for a copy of Vampire Bite and add it to
#   your hand.
#
# CARTES DE REFERENCE
#  - `aa008` : `GiveKeywordToInPlayWhenApplyThis(..., defense=1)` sur "You".
#  - `ar007` God of War : `AfterCardEnterPlay(HeroResponse, <type>, op)`, ici
#    `Enemy` (vilain compris : un second vilain qui entre en jeu compte).
#  - `an001b` : `Search.PlayerCard(..., include_discard_pile=True, name=...)`
#    + `GainCard`.
#
# TEXTE CONTRE CODE
#  ⚠ « a copy of VAMPIRE BITE » -> recherche par NOM, sans homonyme au depot.
#  ⚠ « After an ENEMY enters play » -> sbire OU vilain ; un sbire convoque par
#    On the Hunt (bl004) declenche la Response.
#  ⚠ Aucune limite imprimee : la carte s'incline, c'est sa limite.


def GetAbilities() -> Sequence['Ability']:

    def flairer(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_VAMPIRE_BITE,
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            defense=1,
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            Enemy,
            flairer,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
