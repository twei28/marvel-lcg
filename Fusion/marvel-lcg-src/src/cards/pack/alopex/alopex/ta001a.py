from . import *

# * Alopex (face heros) — FOX. NINJA. VIGILANTE.
# CTR 1 / ATQ 2 / DEF 3 — HS 5 / PV 9
# Matagi — Forced Response: After you attack an enemy or thwart a scheme, find
#   Prey and attach it to that enemy or scheme.
#
# Cartes de reference :
#  - « after you attack OR thwart » : `ironheart/29015` Falcon,
#    `AbilityFactory.AfterUnitAttackOrThwart(type, "This", op)` (messages
#    `AfterUnitAttackEnd` / `AfterUnitThwartEnd`) ;
#  - « find X and attach it to » : `SetupCards.AttachTo` (setup_cards.py) /
#    `Upgrade.AttachTo2(face, effect)` ; ici la source est la reserve du joueur
#    (`set_aside_deck`), pas le deck rencontre.
#
# Mots-pieges :
#  - « Forced RESPONSE » : AbilityType.ForcedResponse, obligatoire ;
#  - « attack AN ENEMY » : la (ou les) cible(s) de l'attaque ; « thwart A
#    SCHEME » : la manigance contree. « THAT enemy or scheme » = la meme cible ;
#  - « FIND Prey » : DECISION UTILISATEUR (16/10/2026, Q1) : regle officielle « find »
#    = chercher dans chaque zone ou la carte peut se trouver (cartes de cote, zone
#    de jeu...). Prey deja attachee ailleurs est trouvee et DEPLACEE ;
#  - si la cible a quitte le jeu (ennemi vaincu, manigance videe), rien a
#    attacher : Prey reste de cote ;
#  - le nom « Matagi » est celui de la capacite (italique imprime).
#


def GetAbilities() -> Sequence['Ability']:

    def matagi(effect: 'Effect', message: 'Message.AfterUnitAttackEnd|Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        if isinstance(message, Message.AfterUnitAttackEnd):
            cibles = [f for f in message.attacked_targets if Enemy.IsType(f)]
        else:
            cibles = [f for f in message.schemes if Scheme2.IsType(f)]
        # « THAT enemy or scheme » : la cible de CETTE attaque / CE contre.
        cibles = [f for f in cibles if f.IsInPlay()]
        if not cibles:
            return

        # DECISION UTILISATEUR (16/10/2026, Q1) : regle officielle « find » = chercher dans
        # CHAQUE zone ou la carte peut se trouver (cartes de cote, zone de jeu...). Prey deja
        # attachee a une autre cible est donc TROUVEE et deplacee sur la nouvelle cible.
        prey = PreyMiseDeCote(joueur) or PreyEnJeu(effect, joueur)
        if prey is None:
            return
        prey.CastTo(Upgrade).AttachTo2(cibles[0], effect)

    return [
        AbilityFactory.AfterUnitAttackOrThwart(
            AbilityType.ForcedResponse,
            "This",
            matagi,
        ).SetName("Matagi"),
    ]
