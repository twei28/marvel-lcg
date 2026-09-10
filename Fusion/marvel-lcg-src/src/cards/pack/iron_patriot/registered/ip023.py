from . import *

# * Bullseye — SBIRE du deck REGISTERED (10/20). 4 PV, ATQ 2, MNG 2, boost 3.
# ASSASSIN. AVENGER. ELITE.
# Quickstrike.
# [star] When Bullseye makes a basic attack against a unique character
#   ([unique]), he gets +1 ATK. Bullseye's attacks gain ranged.
# Kill Order — Special: Choose a minion -> discard the top card of the
#   encounter deck. If that card has a star icon ([star]) in the boost area,
#   defeat that minion.
#
# ⚠ L'ETOILE [star] EN TETE DE LIGNE N'EST PAS UNE MECANIQUE : c'est la puce
# d'affichage des capacites de carte-rencontre, exactement comme sur `01130`
# * Whirlwind ou `01129` * Radioactive Man, dont les modules la traitent comme
# du decor. Tout le pack l'emploie ainsi. Elle ne doit pas etre confondue avec
# l'etoile DE BOOST citee plus bas, qui, elle, se mesure (`face.boost_star`).
#
# CARTES DE REFERENCE
#  - `50099` * Rapido / `04027` * Crossfire :
#    `AbilityFactory.UnitAttackGainKeyword("This", ranged=True)`.
#  - `dt069` Incentivized : `GainForThisActive(effect, message, attack=N)` sur
#    `WhenUnitWouldAttackUnit` — le bonus ne dure QUE cette attaque.
#  - `bc006` Lucky Hit : `Worlds.DiscardEncounterTopCard(effect)`, qui rend la
#    carte defaussee, et le comptage de son etoile.
#
# TEXTE CONTRE CODE
#  ⚠ « makes a BASIC ATTACK » : l'attaque de base seulement,
#    `is_basic_attack=True`. Un degat inflige par une capacite ne compte pas.
#  ⚠ « against a UNIQUE character ([unique]) » : la cible porte le point
#    d'exclamation d'unicite. `CardFinder(is_unique=True)`.
#  ⚠ « Choose a minion -> » : PAS DE COUT, la fleche separe ici la cible de
#    l'effet. On la traite en cible (`SetTarget`), et la carte ne fait rien
#    s'il n'y a aucun sbire.
#  ⚠⚠ « If that card has a STAR ICON in the BOOST AREA » : l'etoile de boost,
#    `face.boost_star` (has_boost_icon.py:50), et NON les icones chiffrees.
#    La distinction est le sujet meme de la phrase.
#  ⚠ Le sbire choisi peut etre Bullseye lui-meme s'il est encore sbire : rien
#    ne l'interdit, et l'insert vend cette carte comme un assassin.
#  ⚠⚠ PAS DE `.SetTarget()` SUR CETTE CARTE. Le moteur l'interdit aux ENNEMIS :
#    `Ability.Initialize` leve `assert self.selectors == []` des que la face
#    est un `Enemy` (ability.py:168), et les cartes du deck REGISTERED sont
#    chargees comme des SBIRES. La cible se demande donc DANS l'operation, par
#    `joueur.AskChooseFaces`. Mesure du 09/09/2026, sur `ip021`.


def GetAbilities() -> Sequence['Ability']:

    def oeil_de_taureau(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        this.CastTo(Unit2).GainForThisActive(effect, message, attack=1)

    def ordre_de_tuer(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        Unused(message)
        joueur = effect.GetInitiator()
        sbires = Worlds.GetOnFieldMinions(effect)
        if joueur is None or not sbires:
            return
        cibles = joueur.AskChooseFaces(sbires, (1, 1), effect,
                                       prompt="Choose a minion")
        if not cibles:
            return
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is None:
            return
        if face.boost_star > 0:
            Faces.DefeatUnits(cibles, this, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            ranged=True,
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            "This",
            CardFinder(is_unique=True),
            oeil_de_taureau,
            is_basic_attack=True,
        ),
        SpecialRegistered("Kill Order", ordre_de_tuer),
    ]
