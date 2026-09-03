from . import *

# Tactical Overview — evenement signature, x2 (n/15 = 3 et 4).
# SUPERPOWER. THWART. Cout 2, ressource [mental].
# Hero Action (thwart): Remove 3 threat from a scheme. You may remove 1
#   reactor counter from Iron Man to remove 3 additional threat from that
#   scheme. If Iron Man has the AERIAL trait, you may divide threat removed
#   from among schemes as you choose.
#
# LA JUMELLE EXACTE DE `im002`, cote menee : meme cout, meme structure a trois
# etages (base / compteur / AERIAL), meme mot « that ». Seuls changent la
# ressource imprimee, le libelle et la cible.
#
# Cartes de reference :
#  - `hk003` / `an004` pour `RemoveThreatFromSchemes` ;
#  - `im002` du meme pack pour le squelette ;
#  - `RetirerUnReacteur` (helper du set).
#
# ⚠ LA REPARTITION DE LA MENACE N'A PAS D'API, contrairement aux degats.
# `player.AssignDamage` existe (27071 Sand Storm) ; il n'y a **aucun
# `AssignThreat`**. `RemoveThreatFromSchemesTotal` (card_face.py:734) ne fait
# PAS ce qu'on croit : il retire 1 menace a chacune des N premieres
# manigances, ce qui n'est pas « repartir N menaces librement ». On rend donc
# la repartition libre en posant la question UNE FOIS PAR POINT : le joueur
# choisit une manigance, on lui en retire 1, N fois. En solo avec une seule
# manigance c'est identique ; a plusieurs manigances, c'est la lettre du
# texte.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **You MAY** remove 1 reactor counter » : facultatif ET cout. Les 3
#    menaces supplementaires ne tombent que si le compteur est parti.
#  - « from **that** scheme » : la MEME manigance, pas un second choix.
#  - « **If** Iron Man has the AERIAL trait » : lu a la resolution.
#  - Le libelle `(thwart)` alimente Desoriente.


def GetAbilities() -> Sequence['Ability']:

    def tactical_overview(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return

        menaces = 3

        if CompteursReacteur(identite) >= 1:
            choix = joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 reactor counter to remove 3 additional threat",
                    lambda cibles: None,
                ),
            )
            if choix is not None and RetirerUnReacteur(identite, effect):
                menaces += 3

        if identite.HasTrait("AERIAL"):
            # Repartition libre : une question par point retire.
            for _ in range(menaces):
                joueur.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Remove 1 threat from a scheme",
                        lambda cibles: this.RemoveThreatFromSchemes(cibles, 1, effect),
                    ).SetTarget(Scheme2, has_threat=True),
                )
            return

        this.RemoveThreatFromSchemes(effect.targets, menaces, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tactical_overview,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
