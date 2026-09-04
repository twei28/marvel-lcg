from . import *

# Whistle While You Work — evenement signature, x2 (n/15 = 3 et 4). TACTIC.
# Cout 1, ressources [mental] ET [wild] (deux icones imprimees).
# Hero Action: Attach the Yaka Arrow upgrade to Yondu -> ready Yondu and the
#   Tahlei upgrade. If the Yaka Arrow upgrade is not in play, summon it and
#   add it to your hand instead.
#
# Cartes de reference :
#  - `AttacherLaFleche` et `Convoquer` (helpers du set).
#  - `an001a` / `31009` / `ok014` pour `Faces.ReadyAll(faces, effect)`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **-> ready** » : la fleche posee sur Yondu est le COUT, le
#    redressement est l'effet. Mais le cout n'est payable que si la fleche est
#    EN JEU — d'ou la seconde phrase, qui n'est pas une branche annexe mais le
#    repli obligatoire.
#  - « **instead** » : les deux moities s'EXCLUENT. Fleche en jeu, on la pose
#    et on redresse ; fleche absente, on la convoque en main et on ne redresse
#    RIEN. Coder les deux a la suite doublerait la carte.
#  - « ready **Yondu AND the Tahlei upgrade** » : les deux, et Tahlei peut ne
#    pas etre en jeu — le redressement porte alors sur le seul heros.
#    `Faces.ReadyAll` fait deja le tri.
#  - « attach ... **to Yondu** » : un NOM PROPRE, la face HEROS. Poser la
#    fleche sur l'identite declenche le SOIN de `yd001a`, pas un degat.
#  - « summon ... **and add it to your hand** » : en MAIN, pas en jeu.
#  - Aucun libelle : ce n'est ni une attaque ni une menee.
#  - DEUX icones de ressource imprimees, [mental] et [wild] : `RES: "BG"`,
#    croisees avec `yd011` Tahlei (deux [mental]) et `yd007` Jackpot! (un
#    [wild]) du meme pack (leçon Lockjaw).


def GetAbilities() -> Sequence['Ability']:

    def whistle_while_you_work(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        # « If the Yaka Arrow upgrade is NOT in play, ... INSTEAD » : les deux
        # moities s'excluent, et c'est la presence sur le TERRAIN qui tranche.
        if LaFleche(effect) is None:
            Convoquer(effect, NOM_FLECHE)
            return

        heros = joueur.GetIdentity()
        if not AttacherLaFleche(effect, heros):
            return

        a_redresser = [f for f in (heros, LaTahlei(effect)) if f is not None]
        Faces.ReadyAll(a_redresser, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            whistle_while_you_work,
        ).SetPlay(),
    ]
