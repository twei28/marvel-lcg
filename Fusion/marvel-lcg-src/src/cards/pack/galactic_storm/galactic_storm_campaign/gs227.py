from . import *

# * Binary (CAROL DANVERS) — ALLIE de campagne (Identity-Specific / Campaign, n° 227). Cout 3.
# THW 2 / ATK X*, 3 PV. AERIAL.
# Honorary.
# X is the number of [energy] resource in your hand.
#
# Carte de reference :
#  - **`mw001a`** Madame Web (pack custom) : ATK/THW/DEF imprimes « X » sur la carte -> `desc.ATK = "0*"`
#    (0, pas « X », sinon le parseur natif plante : `can_attack.py:81`, `int(value)`) + capacite constante
#    `AbilityFactory.ThisGainKeyword(check_fn, attack=1, change_on_event=...)` qui remonte la stat au
#    nombre voulu. Meme montage ici : `check_fn` compte les cartes [energy] dans la main.
#
# ⚠ Mots-pieges :
#  - « resource IN YOUR HAND » : des cartes de la MAIN du controleur (pas en jeu, pas le deck), chacune
#    portant une icone de ressource energie imprimee (`has_printed_res="Y"`) ;
#  - recalcul en continu : la main change a chaque tour, `change_on_event=OnEvent.NONE` suffit car
#    `ThisGainKeyword` est deja reevalue a chaque `OnResetKeywords` (modele mw001a, pas d'evenement
#    specifique necessaire pour une carte en main qui change par les moyens normaux du jeu).


def GetAbilities() -> Sequence['Ability']:

    def energie_en_main(effect: 'Effect', ui: List['CardFace']) -> int:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        cartes = joueur.hand_cards.FindCards(has_printed_res="Y")
        for carte in cartes:
            ui.append(carte)
        return len(cartes)

    return [
        AbilityFactory.ThisGainKeyword(
            energie_en_main,
            attack=1,
        ).SetName("X"),
    ]
