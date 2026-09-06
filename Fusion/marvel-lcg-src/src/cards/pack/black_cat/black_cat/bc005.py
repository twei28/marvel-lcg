from . import *

# Cat Burglary — EVENEMENT, cout 2, [mental]. SKILL. THWART. x2.
# Hero Action (thwart): Look at the top 3 cards of the encounter deck and
#   discard 1. Remove 1 threat from a scheme plus 1 additional threat for each
#   icon ([star] and [boost]) in that card's boost area. Tuck it under
#   Black Cat.
#
# ⚠ HOMONYME INTERNE AU PACK : « Cat Burglary » est AUSSI le libelle de la
# capacite de `bc001b` Felicia Hardy. Le texte francais s'ecrit sur le
# `card_id`.
#
# CARTES DE REFERENCE
#  - `48021` * Gambit : `LookAtDeck("EncounterDeck", 3, effect)` puis
#    `AskChooseFace`, exactement les trois cartes d'ici.
#  - `42006` Natural Flight : « Hero Action (thwart): Remove N threat from a
#    scheme » -> `SetPlay().SetLabel('thwart').SetTarget(Scheme2)`.
#
# TEXTE CONTRE CODE
#  ⚠ PAS DE FLECHE. Tout est effet : regarder, defausser, retirer, glisser.
#    Rien n'est un cout, la carte est donc jouable meme si le deck de
#    rencontre est vide — elle retire alors 1 menace et ne glisse rien.
#    Difference imprimee avec `bc008` et `bc009`, qui ont une fleche.
#  ⚠ « discard 1 » PUIS « TUCK IT » -> la MEME carte. Mot-piege « it »
#    (`wd022`) : on garde la reference exacte, on ne repeche pas « une carte »
#    de la defausse.
#  ⚠ « 1 threat PLUS 1 additional for each icon » -> 1 est un PLANCHER. Une
#    carte a 2 icones retire 3 menaces, pas 2.
#  ⚠ « each icon ([star] AND [boost]) » -> `IconesEtEtoiles`.
#  ⚠ ON COMPTE AVANT DE DEFAUSSER : une carte encore dans le deck rend sa
#    valeur imprimee (`CountBoostIconsInternal`, has_boost_icon.py:41), une
#    carte defaussee repasse par le chemin normal. Meme precaution que
#    `bc001a`.
#  « the top 3 cards » -> `LookAtDeck` ne deplace rien : les deux cartes non
#    choisies restent sur le deck, dans leur ordre.


def GetAbilities() -> Sequence['Ability']:

    def cambriolage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        vues = joueur.LookAtDeck("EncounterDeck", 3, effect)
        choisie = joueur.AskChooseFace(list(vues), effect) if vues else None

        # ⚠ Compter AVANT de defausser.
        bonus = IconesEtEtoiles([choisie]) if choisie is not None else 0
        if choisie is not None:
            Faces.DiscardAll([choisie], effect)

        this.RemoveThreatFromSchemes(effect.targets, 1 + bonus, effect)

        # « Tuck IT under Black Cat » : la carte defaussee, pas une autre.
        if choisie is not None:
            GlisserSousIdentite(effect, [choisie], joueur)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cambriolage,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
