from . import *

# * Binary (CAROL DANVERS) — ALLIE de campagne (Identity-Specific / Campaign, n° 227). Cout 3.
# THW 2 / ATK X*, 3 PV. AERIAL.
# Honorary.
# X is the number of [energy] resource in your hand.
#
# Cartes de reference :
#  - **`mw001a`** Madame Web (pack custom) : ATK/THW/DEF imprimes « X » sur la carte -> `desc.ATK = "0*"`
#    (0, pas « X », sinon le parseur natif plante : `can_attack.py:81`, `int(value)`) + capacite constante
#    `AbilityFactory.ThisGainKeyword(check_fn, attack=1, change_on_event=...)` qui remonte la stat au
#    nombre voulu. Meme montage ici : `check_fn` compte les cartes [energy] dans la main.
#  - **`galactic_storm/binary/gs001a`** Binary (meme auteur, meme texte « X is the number of [energy]
#    resources in your hand ») : `change_on_event=OnEvent.HandCards("EngagedPlayer")`, SEULE carte a tirer
#    une statistique de la main — sans cet evenement la valeur ne se recalcule qu'au prochain
#    `OnResetKeywords` (debut de partie/round), pas quand la main change en cours de cas. Trouve en
#    ecrivant le cas de test (gs227 restait a 2 apres avoir vide la main de ses [energy]).
#
# ⚠ Mots-pieges :
#  - « resource IN YOUR HAND » : des cartes de la MAIN du controleur (pas en jeu, pas le deck), chacune
#    portant une icone de ressource energie imprimee (`has_printed_res="Y"`) ;
#  - recalcul en continu : `change_on_event=OnEvent.HandCards("EngagedPlayer")`, sinon la stat reste figee
#    a la main de depart.


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
            change_on_event=OnEvent.HandCards("EngagedPlayer"),
        ).SetName("X"),
    ]
