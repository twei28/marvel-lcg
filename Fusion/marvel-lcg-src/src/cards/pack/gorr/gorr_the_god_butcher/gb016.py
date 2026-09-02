from . import *

# Brutal Cunning — TRAITRISE (×2). Peril. 2 icones de boost.
#
# Peril.
# When Revealed: Choose one:
# • Discard cards from the top of the encounter deck until you discard a
#   NECROVERSE attachment. Reveal that card.
# • Shuffle the bottommost NECROVERSE attachment in the encounter discard pile
#   into the encounter deck. This card gains surge.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - `Peril` (mots-cles/peril.md) : BASE AUTOMATIQUE, `desc.Peril = "1"`. Le
#   moteur injecte tout seul la condition qui empeche les autres joueurs
#   d'intervenir (ability.py:275-284). Aucun script.
# - `Surge` conditionnel (mots-cles/surge.md) : « this card GAINS surge » n'est
#   PAS la base automatique `desc.Surge` — c'est le helper `ThisCardGainSurge`
#   du `cards/pack/__init__.py`, modele ag014.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Discard cards from the top of the encounter deck until ... Reveal that
#   card » : 04113b (The Mad Doctor) pour `DiscardEncounterCardsUntil`, et
#   sp019 pour la revelation qui suit.
# - « the BOTTOMMOST card ... in the encounter discard pile » : la pile de
#   defausse est un `Deck`, `Get(True)` rend ses cartes du dessus vers le
#   dessous ; le « bottommost » est donc le DERNIER de la liste.
# - Choix impose entre deux branches : `ChooseAbilities`, comme gb015.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « a NECROVERSE ATTACHMENT » -> trait ET type : un sbire NECROVERSE ne compte
#   pas, un attachement sans le trait non plus.
# « REVEAL that card » -> la carte trouvee est revelee, donc elle s'attache et
#   resout son texte : c'est la branche qui AIDE le vilain.
# « the BOTTOMMOST ... in the encounter DISCARD PILE » -> on ne fouille pas le
#   deck : la carte revient d'entre les mortes.
# « THIS card gains surge » -> la traitrise elle-meme, pas la carte remelangee.
# ⚠ Les deux branches restent proposees meme si elles ne peuvent rien faire :
#   le texte n'impose aucune condition. Une branche sans cible ne fait rien,
#   et la seconde donne quand meme surge.


def GetAbilities() -> Sequence['Ability']:

    def attachement_necroverse() -> 'CardFinder':
        return CardFinder(trait="NECROVERSE", card_type=Attachment)

    def ruse_brutale(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        joueur = message.GetToPlayer()
        if not joueur:
            return

        def fouiller(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            trouve = Worlds.DiscardEncounterCardsUntil(
                effect,
                trait="NECROVERSE",
                card_type=Attachment,
            )
            if trouve is not None:
                trouve.Reveal(joueur, effect)

        def repecher(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            defausse = Worlds.GetEncounterDiscardPile(effect)
            candidats = attachement_necroverse().Checks(defausse.Get(True))
            if candidats:
                # « bottommost » : le dessous de la pile, donc le dernier de la
                # liste rendue du dessus vers le dessous.
                Faces.ShuffleAllTo([candidats[-1]], 'EncounterDeck', effect)
            ThisCardGainSurge(effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard from the encounter deck until a NECROVERSE attachment, reveal it",
                fouiller),
            AbilityFactory.ForChoiceAbility(
                "Shuffle the bottommost NECROVERSE attachment from the discard pile back in",
                repecher),
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            ruse_brutale,
        ),
    ]
