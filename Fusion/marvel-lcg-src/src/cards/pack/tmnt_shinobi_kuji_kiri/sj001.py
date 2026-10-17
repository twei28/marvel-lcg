from . import *

# Foresight (sj001), Kuji-Kiri, evenement SPELL (Inkwire, TMNT Shinobi).
# Hero Action: Look at the top card of the encounter deck. You may reveal that card to draw 3 cards.
#
# Mots-cles : aucun mot-cle imprime (Spell = trait).
# Carte de reference : `agent_13/ag004` Infiltrate (`LookAtDeck("EncounterDeck", 1, ...)` puis `MayChooseOneAbility`
# pour l'option facultative) et `aos/50023` Melinda May (regarder le dessus du deck rencontre). Reveler la carte
# regardee : `Worlds.RevealEncounterDeckTopCard` (c'est elle, le dessus du deck).
#
# TEXTE CONTRE CODE
#  ⚠ « You MAY reveal » : facultatif (`MayChooseOneAbility`) ; sans reponse, rien n'est revele ni pioche.
#  ⚠ « reveal that card TO draw 3 cards » : la revelation est la condition, la pioche vient apres (meme si
#    la carte revelee est annulee ou fait surge : elle a ete revelee).
#  ⚠ Homonymes officiels (autres cartes) : mw009 Foresight (Madame Web, interruption) et vp008 Foresight
#    (Venompool, amelioration). Texte et type differents : aucune confusion possible.


def GetAbilities() -> Sequence['Ability']:

    def foresight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        faces = joueur.LookAtDeck("EncounterDeck", 1, effect)
        if not faces:
            return

        def reveler(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            Worlds.RevealEncounterDeckTopCard(joueur, effect)
            joueur.DrawUp(3, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Reveal that card to draw 3 cards",
                reveler,
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            foresight,
        ).SetPlay(),
    ]
