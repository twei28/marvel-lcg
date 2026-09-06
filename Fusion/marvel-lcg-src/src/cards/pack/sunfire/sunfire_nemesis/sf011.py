from . import *

# Hand Ambush — COMPLOT ANNEXE nemesis (N 1/5). 2 icones de boost.
#   Menace de depart 2[per_hero]. Icone AMPLIFY.
# The Hand were lying in wait for us!
# Forced Interrupt: When an enemy enters play, give it a facedown boost card.
# Forced Response: After a HAND minion is defeated, place it on top of the
#   encounter deck.
#
# MOT-CLE : AMPLIFY — fiche `docs/reference/mots-cles/amplify.md`. BASE
# AUTOMATIQUE, `desc.Amplify = "1"`, AUCUN SCRIPT.
# ⚠ L'icone a ete identifiee PAR COMPARAISON D'IMAGE avec `16054` Vendetta,
# carte officielle dont le `desc` declare `"Amplify": "1"` : les deux dessins
# sont SUPERPOSABLES. Jamais nommee a vue — c'est un « + » accole a une forme
# a trois branches, a ne pas confondre avec le « + » sur carte inclinee
# (hazard, `01107`) ni avec celui sur maison soulignee (acceleration,
# `01109`), les deux ayant ete compares cote a cote. Lecon Lockjaw.
#
# ⚠ LA CARTE QUI REND LA MAIN INTARISSABLE : ses deux moities se repondent.
# Chaque ennemi qui arrive recoit une carte de bonus de plus, et chaque sbire
# HAND vaincu RETOURNE SUR LE DECK — il reviendra. C'est le piege du set.
#
# CARTES DE REFERENCE
#  - `02035` Intimidation : `Faces.GiveFacedownBoostCards([<ennemis>], 1, ...)`.
#  - `AfterUnitBeDefeated` : « after a minion is defeated ».
#
# TEXTE CONTRE CODE
#  ⚠ « When AN ENEMY enters play » -> TOUS les ennemis, vilain compris, et pas
#    seulement les sbires de la Main. Le texte ne restreint pas.
#  ⚠ « FORCED INTERRUPT » : la carte de bonus est donnee AVANT que l'ennemi ne
#    soit vraiment la, ce qui la rend disponible des sa premiere activation.
#  ⚠ « After a [[HAND]] MINION is defeated » -> le TRAIT, pas le nom : `sf012`
#    Silver Samurai et `sf013` Hand Ninja le portent tous les deux, et un
#    futur sbire HAND en profiterait aussi.
#  ⚠ « place it ON TOP OF the encounter deck » -> sur le DESSUS, pas melange.
#    Le sbire revient donc au prochain tour du mechant. `Faces.MoveAllToDeck`
#    avec `"Top"` est la seule voie qui garantit la position.


def GetAbilities() -> Sequence['Ability']:

    def carte_de_bonus_en_plus(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        ennemi = message.trigger
        if ennemi is not None and Enemy.IsType(ennemi):
            Faces.GiveFacedownBoostCards([ennemi], 1, effect)

    def sbire_de_la_main(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> bool:
        Unused(effect)
        sbire = message.trigger
        return sbire is not None and sbire.HasTrait(TRAIT_MAIN)

    def remettre_sur_le_deck(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        sbire = message.trigger
        if sbire is None:
            return
        deck = Worlds.GetEncounterDeck(effect)
        if deck is not None:
            Faces.MoveAllToDeck([sbire], deck, "Top", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedInterrupt,
            Enemy,
            carte_de_bonus_en_plus,
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Minion,
            remettre_sur_le_deck,
            conditions=[sbire_de_la_main],
        ),
    ]
