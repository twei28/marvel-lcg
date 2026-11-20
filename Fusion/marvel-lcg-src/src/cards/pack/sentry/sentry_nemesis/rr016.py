from . import *

# * Void : SBIRE (DARK SENTRY. ELITE.), SCH X☆ / ATQ X☆, PV 4 par joueur, boost 3, Toughness, Malevolent. Set « Sentry Nemesis ».
# Malevolent. (Each character you control and other enemies must target this card for their first attack each round.) Toughness.
# X is the number of balance counters on Duality Aspect. The Void cannot take less than X damage each round.
# ★ Forced Interrupt: When the Void would activate, if there are 3+ balance counters in play, resolve the "Special" ability of the topmost SPLIT card from the Sentry player's discard pile instead, if able.
#
# CARTES DE REFERENCE
#  - « SCH/ATK = X » variable : `ThisGainKeyword(fn, scheme=1, attack=1, change_on_event=OnEvent.Counter(CardFinder(name=..), 'balance'))` (`bg015`, `bw016`).
#  - « cannot take less than X damage » : `WhenUnitWouldTakeDamage(.., "This", op)` + `message.IncreaseDamage(n, effect)` (sender_damage.py:812).
#  - « When the Void would activate ... instead » : `AbilityFactory.WhenEnemyWouldActivate(NonKeywordStar, "This", op)` + `message.SetBeInstead(effect)` ; Special d'une autre carte : `carte.ResolveSpecialAbility(joueur, effect)`.
#  - Toughness : lu dans `desc` ; Malevolent : fiche `malevolent.md` (mot-cle maison, hors `desc`).
#
# TEXTE CONTRE CODE
#  « X » : compteurs sur DUALITY ASPECT seulement. « cannot take less than X damage EACH ROUND » : DECISION UTILISATEUR du 03/11 : CHAQUE ATTAQUE lui inflige au moins X (plancher par instance de degats,
#  applique quand elle en inflige au moins 1). « 3+ balance counters IN PLAY » : la somme de toutes les cartes (Duality Aspect + The Watchtower). « the TOPMOST SPLIT card » : la plus haute carte SPLIT de la
#  defausse du joueur Sentry. « INSTEAD » : l'activation est remplacee (ni manigance ni attaque) ; « if able » : sans carte SPLIT, le Void s'active normalement.
#  MALEVOLENT (fiche `malevolent.md`, page de regles A4 du 03/11) : tant que le Void est en jeu, la PREMIERE attaque de chaque personnage ami et de chaque AUTRE ennemi, a chaque round, est RE-CIBLEE sur le Void
#  (`WhenUnitWouldAttackUnit` + `message.ChangeTarget(void, effect)`, modele `ca019`) ; marqueur `attaquant.rr_void_ronde = world.round_id`. De plus un ennemi qui allait attaquer une IDENTITE alors que le Void est engage avec ce
#  joueur attaque le Void a la place (meme hors premiere attaque).
#  Chiffres : PV 4 par joueur, boost 3.


def GetAbilities() -> Sequence['Ability']:

    def x_courant(effect: 'Effect', faces: List['CardFace']) -> int:
        Unused(faces)
        return EquilibreSurDualite(effect)

    def plancher(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        x = EquilibreSurDualite(effect)
        subira = message.will_take_damage
        if x > 0 and 0 < subira < x:
            message.IncreaseDamage(x - subira, effect)

    def special_a_la_place(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        joueur = JoueurSentry(effect)
        if joueur is None:
            return
        cartes = CartesSplitDansLaDefausse(joueur)
        if not cartes:
            return
        message.SetBeInstead(effect)
        cartes[-1].ResolveSpecialAbility(joueur, effect)

    def malevolent(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        void = effect.this
        attaquant = message.trigger
        cible = message.target
        if attaquant is void or cible is void or not void.IsInPlay():
            return
        ronde = effect.world.round_id
        redirige = getattr(attaquant, "rr_void_ronde", None) != ronde
        if not redirige and Enemy.IsType(attaquant) and (Hero.IsType(cible) or AlterEgo.IsType(cible)):
            joueur_cible = cible.GetControlByOrOwner()
            redirige = Minion.IsType(void) and void.CastTo(Minion).engaged_player is joueur_cible
        attaquant.rr_void_ronde = ronde
        if redirige:
            message.ChangeTarget(void, effect)

    def trois_ou_plus(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        return EquilibreEnJeu(effect) >= 3

    return [
        AbilityFactory.ThisGainKeyword(
            x_courant,
            attack=1,
            scheme=1,
            change_on_event=OnEvent.Counter(CardFinder(name=NOM_DUALITE), NOM_EQUILIBRE),
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.NonKeyword,
            "This",
            plancher,
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            Unit2,
            Unit2,
            malevolent,
        ),
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.NonKeywordStar,  # ⚠ ForcedInterrupt resolvait le Special DEUX fois (soin de rr008 double) : NonKeywordStar, comme le ★ du texte imprime
            "This",
            special_a_la_place,
            conditions=[trois_ou_plus],
        ),
    ]
