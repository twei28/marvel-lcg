from . import *

# * Spider-Man Noir (face heros) — WEB-WARRIOR.
#   PV 10, CTR 0, ATQ 0, DEF 3, main 5.
# [star] Spider-Man Noir gets +X ATK and THW where X is equal to the number of
#   cards tucked under him.
# Spider-Sense — Response: After you resolve a treachery, tuck that card here
#   (to a maximum of 3).
#
# ⚠ ATQ 0 ET CTR 0 IMPRIMES. Sans carte glissee, ce heros ne frappe ni ne
# contre : la pile n'est pas un bonus, c'est son moteur entier. DEF 3 en
# revanche est fixe — les etoiles sont imprimees sur CTR et ATQ seulement,
# verifie au scan.
#
# CARTE DE REFERENCE
#  - ⚠ `31015` * Spider-Man Noir (pack spdr) : L'ALLIE OFFICIEL DU MEME NOM,
#    et il porte MOT POUR MOT la meme mecanique — `ThisGainKeyword` sur la
#    taille de la pile avec `attack=1, thwart=1`, plus
#    `AfterYouResolveTreachery` qui glisse la traitrise, plafond 3 compris.
#    La carte fan est une version HEROS de cet allie. C'est aussi l'homonyme
#    qui interdit tout `CardFinder(name=...)` dans ce pack (voir le
#    `__init__.py` du set).
#  - `52001a` * Silk : l'autre carte du depot qui glisse une traitrise
#    resolue, et l'endroit ou `.SetTarget("Trigger")` est employe.
#  - `58001a` * Wonder Man : le meme bonus dynamique porte par une IDENTITE,
#    et le CORRECTIF qui va avec — `get_new_value` passe par
#    `asset_helper.check_fn`, qui fait `CastTo(CanAttach)` : pose sur une
#    identite, cela leve « AssertionError: face_type=CanAttach » et rend la
#    creation de partie IMPOSSIBLE. `ThisGainKeyword` est la fabrique prevue
#    pour un bonus dynamique porte par la carte elle-meme.
#
# TEXTE CONTRE CODE
#  « +X ATK AND THW » -> LES DEUX, donc `attack=1, thwart=1` sur le meme
#    `ThisGainKeyword` : la valeur rendue par la fonction est multipliee par
#    chacun. Pas deux capacites.
#  « the number of cards TUCKED UNDER HIM » -> `GetPlacedCardArea().GetSize()`,
#    recalcule a chaque mouvement de la pile par
#    `OnEvent.PlacedCard("Here")`. ⚠ « Here » et non « Identity » : le
#    litteral « Identity » est un `# Hack` du moteur (on_event.py:419) qui
#    rend True pour N'IMPORTE QUEL tuck, ou qu'il soit. Wonder Man devait s'en
#    servir parce que sa pile est sur un SOUTIEN ; ici la pile est sur la
#    carte qui porte la capacite, donc « Here » teste vraiment la bonne zone.
#  ⚠ AUCUN PLAFOND SUR LE BONUS. Le « (to a maximum of 3) » borne la POSE de
#    cartes, pas le compte : le texte du [star] ne dit pas « to a maximum of
#    +3 ». En pratique les deux coincident, puisque rien ne peut faire monter
#    la pile au-dela de 3 — mais on code ce qui est ecrit, et le plafond vit
#    donc dans `GlisserSousIdentite`, pas ici.
#  « After you RESOLVE a treachery » -> la traitrise est resolue, donc en
#    DEFAUSSE DE RENCONTRE quand la Reponse part. `52001a` filtre d'ailleurs
#    explicitement sur `is_encounter_discard_pile` ; `31015`, lui, ne le fait
#    pas. On suit `31015`, la carte jumelle : le moteur donne la carte sur
#    `message.trigger` et la deplacer depuis la defausse est licite.
#  « tuck that card HERE » -> CETTE carte, pas une au choix. Mot-piege
#    « that » (`wd022`).


def GetAbilities() -> Sequence['Ability']:

    def taille_de_la_pile(effect: 'Effect', ui: List['CardFace']) -> int:
        pile = list(effect.this.GetPlacedCardArea().Get())
        ui.extend(pile)
        return len(pile)

    def sens_daraignee(effect: 'Effect', message: 'Message.AfterCardRevealed') -> None:
        this = effect.this.CastTo(Hero)

        # `effect.targets` vaut la traitrise, via `.SetTarget("Trigger")`.
        # On repasse quand meme par le helper du set : lui seul applique le
        # plafond imprime, et il rend ce qui a REELLEMENT ete glisse.
        GlisserSousIdentite(effect, list(effect.targets), JoueurDeCetteCarte(effect))
        Unused(this, message)

    def la_pile_nest_pas_pleine(effect: 'Effect', message: 'Message.AfterCardRevealed') -> bool:
        Unused(message)
        return effect.this.GetPlacedCardArea().GetSize() < PLAFOND_PILE

    return [
        AbilityFactory.ThisGainKeyword(
            taille_de_la_pile,
            attack=1,
            thwart=1,
            change_on_event=OnEvent.PlacedCard("Here"),
        ),
        AbilityFactory.AfterYouResolveTreachery(
            AbilityType.Response,
            sens_daraignee,
            conditions=[la_pile_nest_pas_pleine],
        ).SetTarget("Trigger")
        .SetName("Spider-Sense"),
    ]
