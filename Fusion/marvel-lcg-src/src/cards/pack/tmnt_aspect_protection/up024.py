from . import *

# * Nobody (Angel Bridge) — ALLIE 3 [mental], aspect Protection (TMNT Heroes, Inkwire). NINJA. VIGILANTE.
# THW 2 (2), ATK 2 (1), PV 3.
# Response: After Nobody enters play, place a tough or cloaked status card on them.
#
# NOUVELLE. MOTS-CLES : carte d'etat Tough (toughness.md, statut) et Cloaked (cloaked.md) ; fiches lues.
# ⚠ Homonyme de `ta002` « Nobody / Angel Bridges » (allie de heros d'Alopex) : meme titre unique, les deux
# ne coexistent pas (regle d'unicite sur le titre) : question ouverte, voir aspects-protection-questions.md.
#
# CARTES DE REFERENCE
#  - `56041` Patriot : `Faces.GiveStatus([this], "Tough", effect)` sur soi.
#  - `td005` Improvised Tactics : « Cloak » = `Faces.GiveStatus([...], "Cloaked", effect)`.
#  - `tl005` / `tl006` : un choix entre options imprimees = `joueur.ChooseAbilities(effect,
#    ForChoiceAbility(...), ForChoiceAbility(...))`.
#
# TEXTE CONTRE CODE
#  ⚠ « a tough OR cloaked » : UN seul des deux, au choix du joueur.
#  ⚠ « on THEM » : sur Nobody (la carte elle-meme).
#  ⚠ « Response » optionnelle : le joueur peut ne pas la declencher (fenetre du moteur).


def GetAbilities() -> Sequence['Ability']:

    def nobody(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None or not this.IsInPlay():
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place a tough status card on Nobody",
                lambda cibles: Faces.GiveStatus([this], "Tough", effect)),
            AbilityFactory.ForChoiceAbility(
                "Place a cloaked status card on Nobody",
                lambda cibles: Faces.GiveStatus([this], "Cloaked", effect)),
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            nobody,
        ),
    ]
