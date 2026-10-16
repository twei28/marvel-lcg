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
#  - « FIND Prey » : Prey est introuvable quand elle est DEJA en jeu (attachee
#    ailleurs) — lecture litterale « find = chercher hors du jeu », PROVISOIRE,
#    voir TODO-QUESTION ci-dessous ;
#  - si la cible a quitte le jeu (ennemi vaincu, manigance videe), rien a
#    attacher : Prey reste de cote ;
#  - le nom « Matagi » est celui de la capacite (italique imprime).
#
# TODO-QUESTION (ta001a, .planning/tmnt/alopex-questions.md, Q1) : Prey deja
# attachee a UNE AUTRE cible — « find » la deplace-t-elle ? Lecture retenue :
# NON (« find » = chercher parmi les cartes de cote ; Prey en jeu n'est pas
# « trouvable »).


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

        prey = PreyMiseDeCote(joueur)
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
