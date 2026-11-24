from . import *

# America's Anger — EVENEMENT signature, custom « jakxin »
# Cout 1, [physical], traits SKILL + SUPERPOWER. Deux exemplaires physiques :
# ma009 et ma010, meme texte, meme code.
#
# Hero Action: Choose THW or ATK and ready your identity → apply all basic power
#   modifiers to the chosen power for your next basic thwart or attack this turn.
#
# ⚠ TEXTE CHANGE LE 17/11/2026 (version jakxin du 07/09/2026, image du Drive) :
# l'ancien texte disait « double all modifiers applied to the chosen power on its
# next use this turn ». LECTURE CHOISIE PAR L'UTILISATEUR le 17/11/2026 : « SOMME
# DES DEUX » : le pouvoir choisi recoit TOUS les modificateurs de base, ceux du
# CTR ET ceux de l'ATQ, additionnes, pour sa prochaine utilisation ce tour-ci.
# Comme le pouvoir choisi porte DEJA ses propres modificateurs, le supplement est
# le modificateur de l'AUTRE pouvoir : valeur finale = imprime + modif(CTR) + modif(ATQ).
# Ex. : Star Flight (+1 CTR) en jeu, on choisit ATQ -> la prochaine attaque de base
# vaut base + 1. Sans aucun modificateur sur l'autre pouvoir, le supplement est nul.
#
# ---------------------------------------------------------------------------
# ⚠ LA FLECHE EST UN COUT — ARBITRAGE EXPLICITE DE L'UTILISATEUR (30/08/2026)
#
# L'utilisateur a REFUSE une exception sur cette carte. Le cout est bien
# « choisir CTR ou ATQ ET REDRESSER TON IDENTITE », et la capacite ne part que
# si le cout est integralement payable.
#
# CONSEQUENCE ASSUMEE ET VOULUE : SI L'IDENTITE EST DEJA PRETE, LE COUT N'EST
# PAS PAYABLE ET LA CARTE EST INJOUABLE. Il faut s'etre incline d'abord
# (avoir attaque, contre ou defendu). Ce n'est PAS un defaut, ne pas
# « corriger », ne pas contourner.
#
# Rendu par `CostFunc.Ready("YourIdentity")` (cost_func.py:327-356), qui pose
# `canbe_ready=True` sur son selecteur : une identite deja prete n'est pas une
# cible legale, le moteur ne propose donc pas l'action (`CostFunc.Base
# .HasTargets`, cost_func.py:49). C'est la seule construction qui rend « cout
# impayable = rien ne se passe » sans le reecrire a la main.
#
# ECART TECHNIQUE, sans effet en jeu : la moitie « choose THW or ATK » du cout
# est resolue DANS LE CORPS (`player.ChooseAbilities` a deux branches) et non
# par une `CostFunc`. Un choix entre deux options toujours disponibles ne peut
# jamais echouer : le placer avant ou apres le paiement ne change aucune
# partie. Aucune `CostFunc` du moteur ne sait « choisir un mot ».
#
# ---------------------------------------------------------------------------
# « APPLY ALL BASIC POWER MODIFIERS TO THE CHOSEN POWER » (depuis le 17/11/2026)
#
# Les modificateurs se lisent `identite.thwart - identite.printed_thwart`
# (attributs officiels, can_thwart.py:17 et can_attack.py:42). Le pouvoir choisi
# a deja les siens ; la carte lui AJOUTE ceux de l'autre pouvoir :
#     supplement = modificateur(autre pouvoir)
# (ancienne lecture « doubler » : supplement = modificateur(pouvoir choisi)).
# Sans modificateur sur l'autre pouvoir, la carte ne fait RIEN. Un modificateur
# NEGATIF de l'autre pouvoir (Edges Syndrome : -1 a chaque pouvoir de base) est
# applique lui aussi : « ALL basic power modifiers », le signe n'est pas filtre.
#
# « ON ITS NEXT USE THIS TURN » -> une capacite TEMPORAIRE enregistree sur
# l'identite, `RegisterTemp(..., unregister_after_exec=True,
# until_turn_end=True)` (face_effect.py:97-124) : elle part a la PREMIERE
# utilisation du pouvoir choisi, et expire a la fin du tour si le pouvoir
# n'est pas utilise. Les deux bornes sont ecrites, pas une seule.
#
# Declencheur : `AbilityFactory.WhenUnitUseBasicPower(<type>, "You", fn,
# powers=[...])` (friend.py:339-370), puis `message.GainValue(n, effect)`
# (sender_unit.py:21-34), qui route vers `GainTHWForThisThwart` ou
# `GainATKForThisAttack` selon le pouvoir. C'est la brique exacte du moteur
# pour « cette utilisation-ci vaut N de plus ».


def GetAbilities() -> Sequence['Ability']:

    def _pouvoir(identite: 'CardFace', pouvoir: str) -> int:
        attribut = 'thwart' if pouvoir == "THW" else 'attack'
        courant = getattr(identite, attribut, 0)
        imprime = getattr(identite, 'printed_' + attribut, 0)
        return courant - imprime

    def americas_anger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        player = effect.GetInitiator()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is None:
            return

        def armer(pouvoir: str):
            autre = "ATK" if pouvoir == "THW" else "THW"

            def appliquer_les_deux(effect2: 'Effect',
                                   message2: 'Message.WhenUnitUseBasicPower') -> None:
                supplement = _pouvoir(identite, autre)
                if supplement != 0:
                    message2.GainValue(supplement, effect2)

            identite.effect.RegisterTemp(
                AbilityFactory.WhenUnitUseBasicPower(
                    AbilityType.Temp2,
                    "You",
                    appliquer_les_deux,
                    powers=[pouvoir],
                ),
                unregister_after_exec=True,
                until_turn_end=True,
            )

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Apply all basic power modifiers to your THW on its next use",
                lambda targets: armer("THW"),
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Apply all basic power modifiers to your ATK on its next use",
                lambda targets: armer("ATK"),
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            americas_anger,
        ).SetPlay()
        .SetCostFunc(CostFunc.Ready("YourIdentity")),
    ]
