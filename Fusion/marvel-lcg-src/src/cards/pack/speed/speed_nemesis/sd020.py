from . import *

# Inspirational Art — ATTACHEMENT nemesis, custom « CptScorp »
# 3 icones de bonus, trait ART.
# Attach to the villain.
# Forced Interrupt: When a boost card is turned faceup during a villain
#   activation, each boost card gets +1 boost icons ([boost]).
# Hero Action: Spend [energy][physical] resources -> discard this card.
#
# Structure modele : `01100` Enhanced Ivory Horn et `04072` Laser Rifle, meme
# triplet « attacher + capacite passive + Hero Action de defausse a cout de
# ressources ».
#
# ---------------------------------------------------------------------------
# « ATTACH TO THE VILLAIN » -> `AbilityFactory.AttachToFaceWhenPutIntoPlay(
# Villain)`, exactement 04072 Laser Rifle.
#
# ---------------------------------------------------------------------------
# LE FORCED INTERRUPT -> `AbilityFactory.WhenBoostCardTurnedFaceUp(
# AbilityType.ForcedInterrupt, None, ..., boost_for_card=Villain)`
# (factory/boost.py:241). Modele de la fabrique : `08004` Attacrobatics
# (Black Widow), qui annule les icones a la meme fenetre.
#
# - C'est LA fenetre imprimee, « when a boost card is TURNED FACEUP ».
#   `CanBoost.ResolveBoostCards` (can_boost.py:38-76) deroule :
#   (a) `WhenBoostCardWouldTurnedFaceUp`, puis le DEPLACEMENT de la carte vers
#   la zone de bonus, puis `WhenBoostCardTurnedFaceUp`, puis
#   `WhenCardBecomeBoost`, et enfin (c) le comptage par
#   `face.CountBoostIconsInternal()`.
#
# ⚠ NE PAS S'ACCROCHER A `WhenBoostCardWouldTurnedFaceUp` (le message « would »).
#   Essaye d'abord, il est ANNULE par le deplacement qui le suit : entrer dans
#   une nouvelle zone declenche `OnResetKeywords`, qui remet le compteur
#   `Boost` a sa valeur imprimee et efface le +1. Le journal du cas de test le
#   montrait noir sur blanc, deux lignes de suite : « Stampede gains 1 boost
#   icons » puis « moved to boosting area », et l'attaque ne comptait qu'une
#   icone (30/08/2026). Le message « turned faceup », lui, est envoye APRES le
#   deplacement : le +1 survit jusqu'au comptage.
#
# - `boost_for_card=Villain` rend « DURING A VILLAIN ACTIVATION » : la
#   condition porte sur `message.would_message.trigger`, c'est-a-dire l'ennemi
#   qui active. L'activation d'un sbire ne declenche donc rien.
#
# - « EACH boost card gets +1 » : la fabrique se declenche UNE FOIS PAR CARTE
#   DE BONUS retournee, et on ajoute l'icone a `message.trigger`, la carte en
#   cours. Toutes les cartes de bonus de l'activation y passent donc, une par
#   une — ce qui est exactement « chacune ».
#
# - `GainBoostIcons(1, ...)` (has_boost_icon.py:62) est la seule voie du depot
#   pour ajouter une icone a une carte precise. Elle est sans risque de
#   remanence : la carte de bonus est defaussee a l'etape (d) de la meme
#   boucle, et `OnResetKeywords` (has_boost_icon.py:17) remet le compte a la
#   valeur imprimee si elle revient un jour en jeu.
#
# - Garde `HasBoostIcon.IsType` : une carte JOUEUR distribuee en carte de bonus
#   n'a pas d'icone de bonus, on ne lui en ajoute pas.
#
# ---------------------------------------------------------------------------
# LA HERO ACTION -> `AbilityFactory.PlayerActionToDiscardThis(AbilityType
# .HeroAction).SetCost(Cost("YR"))`, la forme exacte de 01100 et 04072.
#
# Le cout est **1 energie + 1 physique**, releve par DECOUPE D'IMAGE du coin
# de texte (`/tmp/claude-1000/speed_work/art_cout.png`), jamais a vue — lecon
# Lockjaw. `Cost("YR")` est le litteral du moteur pour ce couple
# (element/cost.py:38-42).
#
# ---------------------------------------------------------------------------
# ⚠ COLLISION AVEC sd018 The Real Question — TRANCHEE ICI.
#
# sd018 donne PERMANENT a tous les attachements tant qu'elle est en jeu. Or une
# carte Permanente ne peut pas quitter le jeu : `HasPermanent
# .OnWhenCardLeavePlay` (has_permanent.py:16-35) bloque la sortie, et
# `CardFace.DiscardInternal` (card_face.py:473-483) contient meme un
# `assert controller.is_eliminated` sur ce chemin — une partie a deja PLANTE
# sur ce piege dans ce projet.
#
# On rend donc la Hero Action INDISPONIBLE (condition de declenchement) tant
# que The Real Question est en jeu, au lieu de la laisser partir et echouer.
# C'est l'intention lisible de l'auteur : battre la manigance d'abord, puis
# nettoyer les attachements. Le joueur voit une action grisee, pas un plantage.
#
# La recherche est bornee par TYPE ET PAR NOM (`CardFinder(name=...,
# card_type=EncounterSideScheme)`) : « The Real Question » est un nom unique du
# catalogue, mais on ne prend pas le risque d'un homonyme futur.


def GetAbilities() -> Sequence['Ability']:

    def the_real_question_en_jeu(effect: 'Effect') -> bool:
        return Worlds.GetOnFieldSchemes(
            effect,
            CardFinder(name="The Real Question", card_type=EncounterSideScheme),
        ) != []

    def peut_se_defausser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return not the_real_question_en_jeu(effect)

    def inspirational_art(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)

        carte_de_bonus = message.trigger
        if HasBoostIcon.IsType(carte_de_bonus):
            carte_de_bonus.GainBoostIcons(1, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain,
        ),
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.ForcedInterrupt,
            None,
            inspirational_art,
            boost_for_card=Villain,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
            conditions=[peut_se_defausser],
        ).SetCost(Cost("YR")),
    ]
