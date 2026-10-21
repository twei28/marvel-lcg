from ..commun import *
from cards.pack.fne import PeutCouvrirLeCout

# Set CAPOS (pack MC×DC 2026, scenario 1 « The Big Apple ») : les 8 vilains de rangee, face A (standard) / face B (expert).
# Chaque CAPO n'a qu'une capacite ; les fabriques ci-dessous servent aux deux faces (le chiffre ou le mot qui change est un parametre).
#
# Cartes de reference communes :
#  - toafk/kang/__init__.py (Kang I : `WhenUnitAttackYou(ForcedInterrupt, "This", ...)` + `ChooseAbilities` de deux branches, « +2 ATK for
#    this attack » = `GainForThisActive(effect, message, attack=2)`, menace = `PlaceThreatOnSchemes(MainScheme, can_place_threat=True)`),
#  - jigsaw/jigsaw_commun.py (`AfterUnitAttackUnit(ForcedResponse, "This", "You", ...)`),
#  - commun.py (`AuChoixDuJoueur` : « a character you control » choisi par le JOUEUR).
# ⚠ « you » d'un vilain = le joueur que le CAPO attaque. Un CAPO n'attaque que les joueurs de sa rangee (Never Sleeps).


def JoueurVise(message: 'Message2') -> 'Player|None':
    """Le joueur contre qui le CAPO attaque (message d'attaque annoncee ou deja resolue)."""
    joueur = getattr(message, "against_player", None)
    if joueur is not None:
        return joueur
    try:
        return message.GetToPlayer()
    except Exception:
        return None


def Nefaria() -> 'List[Ability]':
    """★ Count Nefaria's attacks gain overkill and ranged."""
    return [AbilityFactory.UnitAttackGainKeyword("This", overkill=True, ranged=True)]


def CrimeMaster() -> 'List[Ability]':
    """★ Crime-Master gets +1 ATK for each minion engaged with you (to a maximum of +2 ATK)."""

    def plus_atk(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = JoueurVise(message)
        if joueur is None:
            return
        n = min(2, len(joueur.GetEngagedMinions()))
        if n > 0:
            effect.this.CastTo(EncounterVillain).GainForThisActive(effect, message, attack=n)

    return [AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", plus_atk)]


def Ringmaster() -> 'List[Ability]':
    """Forced Response : After Ringmaster attacks you, choose : spend a [mental] resource / confuse a character you control."""

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        joueur = JoueurVise(message)
        if joueur is None:
            return

        def payable(effet_choix: 'Effect', message_choix: 'Message.WhenPlayerChooseAbility') -> bool:
            return PeutCouvrirLeCout(joueur, effet_choix, Cost("B"))

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(Cost("B"), "Spend a [mental] resource", lambda cibles, res: None, conditions=[payable]),
            AbilityFactory.ForChoiceAbility(
                "Confuse a character you control",
                lambda cibles: Faces.GiveStatus(cibles, "Confused", effect),
            ).SetTarget("YouControlUnit", canbe_confused=True),
        )

    return [AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", "You", apres_attaque)]


def LadyYulan(soin: int, cartes: int) -> 'List[Ability]':
    """★ Forced Response : After Lady Yulan attacks, choose : heal `soin` damage from her / discard the top `cartes` cards of your deck."""

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(EncounterVillain)
        joueur = JoueurVise(message)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Heal %d damage from Lady Yulan" % soin, lambda cibles: this.HealHealth(soin, effect)),
            AbilityFactory.ForChoiceAbility("Discard the top %d cards of your deck" % cartes, lambda cibles: joueur.DiscardDeckTopCards(cartes, effect)),
        )

    return [AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", "You", apres_attaque)]


def MisterNegative(overkill: bool) -> 'List[Ability]':
    """★ Forced Interrupt : When Mister Negative attacks, choose : give him 1 additional boost card for this attack [expert : and this attack
    gains overkill] / after this attack, stun a character you control."""

    def avant_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = JoueurVise(message)
        if joueur is None:
            return

        def carte_de_plus(cibles: Sequence['CardFace']) -> None:
            message.GiveAdditionalBoostCardForThisActivation(1, effect)
            if overkill:
                message.GainOverKill(effect)

        def etourdir_apres(cibles: Sequence['CardFace']) -> None:
            RunAt.AfterEnemyActivationEnd(
                effect, message,
                lambda: AuChoixDuJoueur(effect, joueur, lambda c: Faces.GiveStatus(c, "Stunned", effect), canbe_stunned=True),
            )

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Give him 1 additional boost card for this attack" + (". This attack gains overkill" if overkill else ""), carte_de_plus),
            AbilityFactory.ForChoiceAbility("After this attack, stun a character you control", etourdir_apres),
        )

    return [AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", avant_attaque)]


def TheRose() -> 'List[Ability]':
    """★ Forced Interrupt : When The Rose attacks, choose : place 2 threat on the main scheme / she gets +2 ATK for this attack."""

    def avant_attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(EncounterVillain)
        joueur = JoueurVise(message)
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Place 2 threat on the main scheme",
                lambda cibles: this.PlaceThreatOnSchemes(cibles, 2, effect),
            ).SetTarget(MainScheme, can_place_threat=True),
            AbilityFactory.ForChoiceAbility(
                "The Rose gets +2 ATK for this attack",
                lambda cibles: this.GainForThisActive(effect, message, attack=2),
            ).SetTarget([this]),
        )

    return [AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", avant_attaque)]


def Nightshade() -> 'List[Ability]':
    """★ Forced Response : After Nightshade attacks you, take 1 indirect damage for each ally you control."""

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(EncounterVillain)
        joueur = JoueurVise(message)
        if joueur is None:
            return
        n = len([c for c in joueur.GetControlCharacters() if Ally.IsType(c)])
        if n > 0:
            joueur.GetIdentity().TakeIndirectDamage(this, n, effect)

    return [AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", "You", apres_attaque)]


def Diamondback() -> 'List[Ability]':
    """Forced Response : After Diamondback takes at least 3 damage from an attack, give him a facedown boost card."""

    def apres_degats(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveFacedownBoostCards([effect.this], 1, effect)

    return [AbilityFactory.AfterUnitAttackUnit(
        AbilityType.ForcedResponse, None, "This", apres_degats, target_took_damage=True, dealt_more_than_damage=3)]
