from . import *

# Yaka Arrow — amelioration signature, x1 (n/15 = 15). TECH. WEAPON.
# Cout 1, ressource [energy]. LA CARTE AUTOUR DE LAQUELLE TOUT LE PACK TOURNE.
# Yaka Arrow cannot be attached to cards unless it is in play. While it is
#   attached to Yondu, he gets +1 THW and +1 ATK.
# Forced Interrupt: When attached enemy would be defeated, attach Yaka Arrow to
#   an enemy, to your identity, or add it to your hand.
#
# Cartes de reference :
#  - **`40122a`** * Juggernaut's Helmet et `nt016` Cosmic Ax (pack
#    night_thrasher) : une amelioration/attachement qui vit sur un ENNEMI et
#    change d'hote. `AttachTo2` (can_attach.py:49) est le seul chemin.
#  - `50144` / `ho012` pour `GiveKeywordToAttached(CardFinder(name="Yondu"),
#    thwart=1, attack=1)` : le bonus ne vaut QUE tant qu'elle est sur lui, et
#    `GiveKeywordToAttached` est precisement « tant que je suis attachee a ».
#  - `WhenUnitWouldBeDefeated` (do_attack / defeated.py) pour la fenetre
#    « would be defeated », modele `ag013` Hallucination et `al013`.
#  - `08013` Stealth Strike pour le choix a trois branches dans l'operation.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « cannot be attached to cards **unless it is in play** » : une fleche en
#    MAIN ou en DEFAUSSE n'est pas deplaçable. C'est ce que le helper
#    `LaFleche` rend en ne balayant que le terrain, et c'est ce qui separe
#    « deplacer » (gratuit, neuf cartes le font) de « convoquer » (le mot-cle
#    maison `summon`, qui la ramene en main).
#  - « While it is attached to **YONDU** » : un NOM PROPRE, la seule face
#    HEROS — l'alter-ego s'appelle Yondu Udonta et n'a ni CTR ni ATQ.
#    `CardFinder(name="Yondu")`, jamais `"You"` (piege an002).
#  - « When attached **enemy** would be defeated » : uniquement quand elle est
#    sur un ENNEMI. Plantee sur l'identite, elle ne bouge pas quand le heros
#    tombe.
#  - « **would be** defeated » : AVANT la defaite, sans quoi la fleche
#    partirait a la defausse avec son hote. C'est une `Forced Interrupt`, donc
#    obligatoire — mais le CHOIX de la destination, lui, appartient au joueur.
#  - Trois destinations, jamais deux : un ennemi, l'identite, ou LA MAIN. La
#    troisieme est celle qu'on oublie, et c'est la seule qui sorte la fleche
#    du terrain.
#  - ⚠ Deplacer la fleche declenche `yd001a` D'ast Whistlin' DEUX fois : un
#    degat a l'hote quitte, un degat au nouvel hote. Ne rien coder pour ca
#    ici, c'est le heros qui ecoute les messages d'`AttachTo2`.


def GetAbilities() -> Sequence['Ability']:

    def redeployer(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()

        # « attach ... to AN ENEMY » : jamais celui qui est en train de tomber.
        autres = [e for e in EnnemisEnJeu(effect) if e is not Hote(this)]

        def vers_un_ennemi(cibles: Sequence['CardFace']) -> None:
            AttacherLaFleche(effect, cibles[0] if cibles else None)

        def vers_l_identite(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            AttacherLaFleche(effect, identite)

        def vers_la_main(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            RappelerLaFlecheEnMain(effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Attach Yaka Arrow to an enemy",
                vers_un_ennemi,
                condition=bool(autres),
            ).SetTarget(Enemy),
            AbilityFactory.ForChoiceAbility(
                "Attach Yaka Arrow to your identity",
                vers_l_identite,
                condition=identite is not None,
            ),
            AbilityFactory.ForChoiceAbility(
                "Add Yaka Arrow to your hand",
                vers_la_main,
            ),
        )

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Enemy),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS),
            thwart=1,
            attack=1,
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "AttachedEnemy",
            redeployer,
        ),
    ]
