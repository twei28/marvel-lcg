from . import *

# * Binary — face HEROS (1A). PV 12, CTR 2, ATQ X, DEF 2, main 5.
# AERIAL. STARJAMMER.
# X is the number of [energy] resources in your hand (to a maximum of 5).
# Burnout — Forced Response: After your turn ends, discard each [energy]
#   resource from your hand.
#
# Cartes de reference :
#  - **`mw001a`** * Madame Web : statistique imprimee « X », declaree a 0 dans
#    cards.json et remontee par `ThisGainKeyword(fn, attack=1,
#    change_on_event=...)`, plafonnee (« to a maximum of 3 »).
#  - **`sm/personal_nightmare/27154`** Evil Doppelganger : la SEULE carte du
#    depot qui tire une statistique de la MAIN (`change_on_event=
#    OnEvent.HandCards("EngagedPlayer")`).
#  - **`wolv/35030`** Death Factor : « Forced Response: After your turn ends »
#    = `AfterPlayerTurnEnd(ForcedResponse, "You", op)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « X is the number of [energy] RESOURCES » : des icones (Energy Torrent
#    vaut 2), lues en main APRES Energy Conversion ; le wild ne compte pas
#    (question Q3). Helper unique `EnergieEnMain` (binary/__init__.py).
#  - « to a MAXIMUM of 5 » : `min(5, ...)`.
#  - « After YOUR turn ends » : `"You"`, pas chaque joueur.
#  - « discard EACH [energy] resource » : chaque CARTE portant au moins une
#    icone [energy] ; avec Energy Conversion en jeu, toute carte a ressource de
#    la main est [energy] et part (lecture litterale, notee au gabarit).
#  - Les deux capacites sont imprimees sur la face HEROS : Carol Danvers (1B)
#    n'a ni ATQ X ni Burnout (contre-cas en alter ego).


def GetAbilities() -> Sequence['Ability']:

    def x_energie(effect: 'Effect', ui: List['CardFace']) -> int:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return 0
        cartes = [f for f in joueur.hand_cards.Get() if EnergieDeLaCarte(f) > 0]
        ui.extend(cartes)
        return min(5, EnergieEnMain(joueur))

    def burnout(effect: 'Effect', message: 'Message.AfterPlayerTurnEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        cartes = CartesEnergieEnMain(joueur)
        if cartes:
            Faces.DiscardAll(cartes, effect)

    return [
        AbilityFactory.ThisGainKeyword(
            x_energie,
            attack=1,
            change_on_event=RecalculEnergie(),
        ).SetName("X"),
        AbilityFactory.AfterPlayerTurnEnd(
            AbilityType.ForcedResponse,
            "You",
            burnout,
        ).SetName("Burnout"),
    ]
