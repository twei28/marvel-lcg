from . import *

# * Mimic-27 — sbire nemesis d'Okoye, WAKANDA
# X is equal to your ATK (X is equal to 0 instead if you are in alter-ego
#   form).
# Forced Interrupt: When Mimic-27 attacks, you must choose an ally to defend
#   against her attack, if able.
# Forced Response: After Mimic-27 attacks and defeats a character, she
#   attacks again. (Limit once per round.)
#
# "X = your ATK, 0 en alter-ego" : contrairement a kb017 (Madame Masque, qui
# doit lire `printed_attack` de la face Heros MEME quand elle n'est pas
# affichee), ici la regle imprimee zero deja X en alter-ego -- pas besoin du
# contournement `printed_attack` : `identite.attack` (stat CALCULEE) est
# fiable puisqu'elle n'est lue QUE quand la face Heros est active. Modele du
# crochet `ThisSetKeyword` : kb017.
#
# "must choose an ally to defend... if able" : modele twc/bulldozer/07051.py
# (Ramming Speed), `message.MustDefendWithAlly(effect)`.
#
# "attacks again" apres avoir defait un personnage : `message.atk_messages`
# (AfterUnitAttackEnd, sender_damage.py:558-568) porte `has_defeated_target`
# sur chaque sous-message (deja lu par friend.py:260-269 pour un autre
# declencheur). Re-attaque : `this.CastTo(Enemy).BasicAttack([cible], effect)`
# contre l'identite du joueur engage, modele cw/dangerous_recruits/56087.py
# (Venom, `this.CastTo(Enemy).BasicAttack([leader], effect)`).


def GetAbilities() -> Sequence['Ability']:

    def mimic_27_atk(effect: 'Effect', ui: List['CardFace']) -> Tuple[int, bool]:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        if joueur is None:
            return 0, False
        identite = joueur.GetIdentity()
        ui.append(identite)
        # CORRECTIF (empiriquement trouve via test_capacites, cas ok022 --
        # 'Hero' object has no attribute 'IsAlterEgo' : IsAlterEgo/IsHero sont
        # des methodes du JOUEUR (player.py:236/246), pas de la face identite.
        valeur = 0 if joueur.IsAlterEgo() else identite.attack
        return valeur, valeur != this.attack

    def doit_defendre(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.MustDefendWithAlly(effect)

    def attaque_a_nouveau(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)

        a_defait = any(getattr(m, 'has_defeated_target', False) for m in message.atk_messages)
        if not a_defait:
            return

        joueur = this.GetEngagedPlayer()
        if joueur is None:
            return
        this.CastTo(Enemy).BasicAttack([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.ThisSetKeyword(
            mimic_27_atk,
            attack=1,
            change_on_event=OnEvent.CardKeyword("Character"),
        ),
        AbilityFactory.WhenUnitAttackYou(
            AbilityType.ForcedInterrupt,
            "This",
            doit_defendre,
        ),
        AbilityFactory.AfterUnitAttackEnd(
            AbilityType.ForcedResponse,
            "This",
            attaque_a_nouveau,
        ).LimitOncePerRound(),
    ]
