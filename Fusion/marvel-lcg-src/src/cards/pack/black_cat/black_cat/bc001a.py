from . import *

# * Black Cat (face heros) — HERO FOR HIRE. THIEF.
#   PV 9, CTR 2, ATQ 1, DEF 2, main 5.
# If there are more than 3 tucked cards here, discard all but 3 of those cards.
# Tychokinesis — Interrupt: When icons ([star] and [boost]) on an encounter
#   card would be counted, count the icons on a card tucked here instead.
#   Then, discard it.
#
# ⚠ ATQ 1 EST LA PLUS FAIBLE DU DEPOT POUR UN HEROS. Black Cat ne frappe pas :
# elle transforme des icones de bonus en degats, en menace retiree et en
# prevention, par ses cartes signature. Tychokinesis est le pivot : elle
# REMPLACE le hasard du deck de rencontre par une carte que la joueuse a
# choisie et rangee d'avance.
#
# CARTES DE REFERENCE
#  - `15001a` * Scarlet Witch, « Chaos Control » : MOT POUR MOT le meme
#    montage — `WhenBoostIconsWouldBeCount`, `SetBeInstead`, `SetBoostIcon`.
#    Seule la provenance de la carte change : le dessus du deck chez elle, la
#    PILE ici.
#  - `48021` * Gambit : l'autre carte du depot qui lit les icones d'une carte
#    glissee sous une autre.
#
# TEXTE CONTRE CODE
#  ⚠ « count the icons ([star] AND [boost]) » -> LES DEUX SORTES, donc
#    `IconesEtEtoiles` (`CountTotalBoostStarAndBoost`). `CountTotalBoostIcons`
#    ignore l'etoile (faces_counter.py:142) : piege paye la veille sur
#    `sn014`, et imprime ici sur CINQ cartes du set.
#  ⚠ « on an ENCOUNTER CARD » -> une carte de rencontre. Une carte JOUEUR
#    distribuee comme carte de bonus ne declenche pas.
#  ⚠ « count the icons on a card tucked here INSTEAD » -> c'est le mot
#    « instead » du moteur, `SetBeInstead`, suivi de `SetBoostIcon` qui impose
#    la valeur. Sans `SetBeInstead`, `CountBoostIconsInternal` rendrait la
#    valeur imprimee de la carte d'origine.
#  ⚠ ON COMPTE AVANT DE DEFAUSSER, et c'est l'inverse de `15001a`. La raison
#    est dans le moteur : `CountBoostIconsInternal` (has_boost_icon.py:33)
#    court-circuite tout et rend `printed_boost` tant que la carte est dans
#    une zone `is_place_card_area` — mais une fois DEFAUSSEE elle repasse par
#    le chemin normal, qui envoie un message et peut donner autre chose.
#    Scarlet Witch defausse d'abord parce que sa carte vient du DECK ; ici la
#    carte est glissee, on la lit donc a sa place.
#  « a card tucked here » -> LA JOUEUSE CHOISIT laquelle. Les cartes glissees
#    ne sont pas interchangeables, c'est tout l'interet de la pile.
#  ⚠ « HERE » : la zone est portee par la CARTE, pas par la face
#    (card_face.py:1017). La pile est la meme des deux cotes de l'identite.
#  ⚠ AUCUNE LIMITE IMPRIMEE. Ni « once per phase » (comme `15001a`), ni
#    « once per round ». On n'en ajoute pas.
#  ⚠ Le plafond de 3 n'est PAS un plafond de pose : voir `RegleDesTroisCartes`
#    dans le `__init__.py` du set.


def GetAbilities() -> Sequence['Ability']:

    def carte_de_rencontre(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> bool:
        Unused(effect)
        return EncounterNonVillainCard.IsType(message.trigger)

    def tychokinesis(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        pile = CartesGlissees(effect, joueur)
        if not pile:
            return

        choisie = joueur.AskChooseFaces(
            pile, (1, 1), effect,
            prompt="Count the icons on this tucked card instead")
        if not choisie:
            return

        # ⚠ On compte TANT QUE LA CARTE EST GLISSEE (voir l'encadre en tete).
        valeur = IconesEtEtoiles(list(choisie))

        message.SetBeInstead(effect)
        message.SetBoostIcon(valeur, effect)

        # « Then, discard it. »
        Faces.DiscardAll(list(choisie), effect)

    return [
        RegleDesTroisCartes(),
        AbilityFactory.WhenBoostIconsWouldBeCount(
            AbilityType.Interrupt,
            tychokinesis,
            conditions=[carte_de_rencontre, PileNonVide],
        ).SetName("Tychokinesis"),
    ]
