from . import *

# * Registration Act — MANIGANCE-JOUEUR, cout 0, RES [mental], 4 menaces PAR
# JOUEUR. Permanent. Setup.
# This scheme does not count against the player side scheme limit.
# Enlistment — Action: Reveal the top card of the REGISTERED deck and put it
#   into play engaged with you. At the end of the round, you may spend
#   resources equal to the number of boost icons on that card to take control
#   of that minion and treat it as a REGISTERED ally.
# Minions with the REGISTERED trait are treated as REGISTERED allies. They take
#   1 consequential damage after they attack or thwart, and their THW is equal
#   to their printed SCH.
# When Defeated: Flip this card.
#
# ⚠⚠ C'EST LA CARTE QUI PORTE LE SYSTEME. Son verso `ip002b` Dark Reign fait la
# meme chose SANS attendre la fin du round : contrer cette manigance, c'est
# accelerer tout le pack.
#
# CARTES DE REFERENCE
#  - `09001b` Stephen Strange : le deck additionnel, sa defausse, et la
#    redirection. Monte par `ip001b`, pas ici.
#  - `Faces.TreatAsAlly` (faces.py:340) : la conversion sbire -> allie. Elle
#    RECOPIE DEJA `printed_scheme` dans `printed_thwart`, ce qui EST la phrase
#    « their THW is equal to their printed SCH ». Rien a coder pour elle.
#  - `RunAt.RoundEnd` (run_at.py:21) : « At the end of the round ».
#
# TEXTE CONTRE CODE
#  ⚠ « Permanent. Setup. » sont des BASES NATIVES, lues dans `desc`. Elles ont
#    exige un CORRECTIF MOTEUR le 09/09/2026 : `PlayerSideScheme` n'heritait ni
#    de `HasPermanent` ni de `HasSetup`, alors que `EncounterSideScheme` les
#    portait deja. Sans lui, le montage du deck tombait sur un
#    `KeyError: 'Permanent'`. Rien a coder ici non plus.
#  ⚠⚠ « does not count against the player side scheme limit » N'EST PAS UNE
#    REGLE D'EDITEUR, contrairement a ce que cette note disait d'abord. Le
#    moniteur `world/limit_monitor/player_side_scheme_limit.py` compte les
#    manigances de joueur EN JEU et fait defausser les excedentaires : sans
#    l'exemption, Registration Act mangeait l'unique place disponible et
#    TOUTE autre manigance de joueur — `ip003` Absolute Power la premiere —
#    etait defaussee a la seconde ou elle entrait en jeu. Mesure du
#    09/09/2026 : « ip003 entered play » puis « ip003 was discarded » dans le
#    meme souffle.
#    Le moteur prevoit le drapeau `not_count_player_side_scheme_limit`
#    (limit_monitor:35) ; on le pose A L'ENTREE EN JEU.
#    ⚠ PAS sur `WhenCardSetup`, contrairement a `61007` Piecing It All
#    Together : cette carte-la se JOUE, celle-ci est posee par la BASE NATIVE
#    `desc.Setup`, et la trace du 09/09/2026 le montre — Registration Act entre
#    en jeu au montage du scenario (ligne 26), bien avant la phase « Capacites
#    de mise en place des personnages » (ligne 40), qui reste vide. La fenetre
#    de setup ne lui est jamais offerte.
#    ⚠ On le pose sur LES DEUX FACES : `ip002b` Dark Reign porte la meme
#    phrase, et c'est la face EN JEU que le moniteur lit.
#  ⚠ « the number of BOOST ICONS on that card » et non son cout : c'est tout
#    l'interet de `ip008` Director of Security, qui retire une icone. D'ou
#    `IconesDeBoostDe`, qui passe par `CountBoostIconsInternal` et voit donc
#    les modificateurs.
#  ⚠ « YOU MAY spend » : optionnel. Refuser laisse le sbire ENGAGE AVEC VOUS,
#    ce qui est le prix a payer — l'insert insiste sur ce point.
#  ⚠⚠ « When Defeated: Flip this card. » -> le verso Dark Reign, ET IL DOIT
#    REVENIR EN JEU. `this.FlipTo(effect)` seul ne suffit pas : une manigance
#    vaincue a DEJA quitte le terrain quand la fenetre « When Defeated »
#    s'ouvre, et retourner une carte hors jeu ne la ramene pas. Mesure du
#    09/09/2026 : le journal montre « Registration Act was defeated » puis
#    plus rien, et le harnais ne trouvait Dark Reign nulle part.
#    Le modele est `40190a` * Assemble the Team (campagne NeXt Evolution) :
#    `this.card.Flip(effect)` puis `face.Reveal(joueur, effect)` — c'est la
#    revelation qui remet la nouvelle face en jeu.


def GetAbilities() -> Sequence['Ability']:

    def hors_limite(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Unused(message)
        for face in effect.this.card.printed_faces:
            face.not_count_player_side_scheme_limit = True

    def enrolement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        RevelerEtProposerLeRecrutement(joueur, effect, a_la_fin_du_round=True)

    def basculer(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(message)
        joueur = JoueurQuiControle(this)
        this.card.Flip(effect)
        verso = this.card.face
        if verso is not None and not verso.IsInPlay():
            verso.Reveal(joueur, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Temp0,
            "This",
            hors_limite,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            enrolement,
        ).SetName("Enlistment"),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            basculer,
        ).NoOutOfPlayLimit(),
    ]
