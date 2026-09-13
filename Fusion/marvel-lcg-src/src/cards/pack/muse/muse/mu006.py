from . import *

# Obsession — TRAITRISE, boost ETOILE. Deux exemplaires dans le set.
# When Revealed: Muse activates against you. If he is not in play, find Muse
#   and put him into play engaged with you.
# [star] Boost: This card gets +X boost icons, where X is the number of cards
#   in your hand with your identity's picture.
#
# CARTES DE REFERENCE
#  - `11051` Ancient Grudge : MOT POUR MOT la meme structure — « X activates
#    against you ; if X is not in play, search the encounter deck and discard
#    pile for X and put it into play ». `DoActivate` puis `Search.EncounterCard`
#    + `PutIntoPlay(joueur, effect)`.
#  - `sm016` Power Surge : le boost etoile variable, `this.GainBoostIcons(n,
#    effect)` dans un `WhenCardBecomeBoost`.
#
# ⚠ « YOUR hand » SUR UNE CAPACITE BOOST = LE JOUEUR QUI DEFEND, et le moteur
# le dit lui-meme (sender_card.py:688 : « Any constant or boost abilities that
# refer to "you" refer to the defending player »). Une carte de rencontre n'a
# pas de controleur joueur : passer par le proprietaire rendrait None ou le
# mauvais joueur. Lecon deja payee sur `sm016`.
#
# TEXTE CONTRE CODE
#  ⚠ « ACTIVATES against you » d'abord, « si pas en jeu » ENSUITE : l'ordre
#    imprime est trompeur. On cherche Muse, on le pose s'il manque, PUIS il
#    s'active — sinon la premiere phrase ne peut pas s'appliquer.
#  ⚠ « find Muse » sans dire ou : le deck de rencontre ET sa defausse, comme
#    `11051`. Muse peut donc revenir apres avoir ete vaincu.
#  ⚠ « put him into play ENGAGED WITH YOU » : `PutIntoPlay(joueur, effect)`
#    engage le sbire avec ce joueur, c'est le comportement du moteur.
#  ⚠ Boost ETOILE : aucune valeur `Boost` dans `desc` (verifie contre `01144a`),
#    une capacite `WhenCardBecomeBoost` a la place.
#  ⚠ X peut valoir ZERO : une main sans carte signature n'ajoute rien, et la
#    carte ne fait alors aucun boost. C'est bien ce que dit le texte.


def GetAbilities() -> Sequence['Ability']:

    def obsession(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        muse = TrouverMuse(effect)
        if muse is None:
            trouve = Search.EncounterCard(
                effect,
                joueur,
                include_discard_pile=True,
                name=NOM_MUSE,
                card_type=Minion,
            )
            if trouve is None:
                return
            trouve.PutIntoPlay(joueur, effect)
            muse = TrouverMuse(effect)

        if muse is not None:
            muse.CastTo(Enemy).DoActivate(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)

        joueur = message.GetToPlayer()
        if joueur is None:
            return
        combien = len(CartesSignatureDe(
            [c for c in joueur.hand_cards.Get() if c is not None]))
        if combien > 0:
            this.GainBoostIcons(combien, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            obsession,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
    ]
