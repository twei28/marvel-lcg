from . import *

# * Rick Jones — ALLIE de scenario (Kree Sentry), sans cout. CIVILIAN. PV 5, CTR 1, ATQ 2 (2 degats consecutifs).
# The first player controls Rick Jones. He does not count against your ally limit.
# Forced Interrupt: When Kree Sentry attacks you, it attacks Rick Jones instead.
# If Rick Jones leaves play, the players lose the game.
#
# Cartes de reference :
#  - « does not count against your ally limit » : `ThisNotCountAllyLimit()`, modele OFFICIEL 50091 Rescued Captive
#    (repris tel quel par gs121 Lilandra).
#  - « When X attacks you, it attacks <allie> instead » : `WhenUnitWouldAttack(ForcedInterrupt)` +
#    `message.ReplaceTarget(allie)`, modele OFFICIEL 50089b Extract Captives (repris par gs114 Deathbird).
#  - « The first player controls Rick Jones » : mis en jeu par 1A (gs079a) sous le controle du PREMIER joueur
#    (`PutIntoPlay(.., under_control=True)`) ; aucune capacite a coder.
#  - « If Rick Jones leaves play, the players lose the game » : `AfterCardLeavePlay("This")` (porte NoOutOfPlayLimit),
#    `Worlds.SetGameOver(False)`, modele gs121 Lilandra (mais ICI tout depart compte, pas seulement le retrait de la partie).
#
# ⚠ Mots-pieges : « attacks YOU » = le joueur que Rick Jones sert (son controleur) : l'attaque contre un AUTRE joueur
# n'est pas detournee ; « INSTEAD » : l'attaque change de cible, elle n'est pas doublee ; l'attaque detournee vers un
# allie n'est pas dirigee contre le joueur (livret p.4 : « attacks you » ne part pas, le « vous » des Boost reste le
# controleur de l'allie) -> `property.not_against_player` / `boost_player` comme `Enemy.AttackCharacter`, decision
# de l'utilisateur du 20/10/2026 (`ally_attack_is_against_player=False` dans Galactic Storm) ; « leaves play » =
# TOUT depart (vaincu, defausse, retire).


def GetAbilities() -> Sequence['Ability']:

    def controleur_de_rick(effect: 'Effect') -> 'Player|None':
        joueur = effect.this.GetControlBy()
        return joueur if joueur is not None and joueur.IsPlayer() else None

    def sentry_vous_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        joueur = controleur_de_rick(effect)
        if joueur is None or not effect.this.IsInPlay():
            return False
        if message.against_player is not joueur:
            return False
        return joueur.GetIdentity() in message.attacked_targets

    def detourner(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = controleur_de_rick(effect)
        message.ReplaceTarget(effect.this)
        # Livret p.4 : une attaque dirigee contre un allie n'est pas une attaque « contre vous ».
        message.property.boost_player = joueur
        message.property.not_against_player = True
        message.property.against_player = None

    def depart(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        Unused(message)
        if not effect.world.is_game_over:
            Worlds.SetGameOver(False, effect)

    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name=SENTRY, card_type=Villain),
            detourner,
            conditions=[sentry_vous_attaque],
        ),
        AbilityFactory.AfterCardLeavePlay(AbilityType.NonKeywordBold, "This", depart),
    ]
