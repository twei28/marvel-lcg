from . import *

# Foreboding Influence — EVENEMENT, cout 2, RES [mental]. TACTIC. x2.
# Alter-Ego Action: Shuffle 2 cards from the REGISTERED discard pile into the
#   REGISTERED deck.
# Hero Response: After you attack a minion, spend resources equal to the number
#   of boost icons on that card to take control of that minion and treat it as
#   an REGISTERED ally.
#
# ⚠⚠ DEUX CAPACITES DE JEU, comme `ip010`. Declaree dans la liste d'exceptions
# du moteur avant l'ecriture de ce module.
#
# ⚠ « an REGISTERED ally » : coquille de l'auteur pour « a REGISTERED ally ».
# Reproduite dans `cards.json`, c'est ce qui est imprime.
#
# CARTES DE REFERENCE
#  - `ip002a` Registration Act : le recrutement, par
#    `RecruterCommeAllieRegistered`. Ici il ne part PAS du deck mais d'un sbire
#    DEJA EN JEU qu'on vient d'attaquer — le sens est inverse, la primitive la
#    meme.
#  - `28014` One by One : la Reponse « after you attack ».
#
# TEXTE CONTRE CODE
#  ⚠ « After you ATTACK a minion » et non « defeat » : le sbire doit SURVIVRE
#    pour etre recrute. Attaquer trop fort, c'est perdre la recrue — la carte
#    recompense la retenue.
#  ⚠ Le prix reste les ICONES DE BOOST du sbire, comme partout dans ce pack.
#  ⚠ « Shuffle 2 CARDS » : deux exactement, ou tout ce qui reste si la defausse
#    en contient moins. Une defausse vide ne rend pas la carte injouable — sa
#    seconde moitie existe.

#  ⚠⚠ `attacker="You"` NE MARCHE PAS. `Condition.CheckWhichCard` connait
#    « This », « YourHero », « YouControlCharacter »... mais PAS « You » tout
#    court : la fonction tombe sur `assert not isinstance(check_rule,
#    Sequence)` (card_type.py:247) — une chaine EST une Sequence — et la
#    condition explose en silence sous le harnais. Mesure du 09/09/2026. On
#    ecrit donc « YourHero », qui existe et qui dit la meme chose ici : c'est
#    le HEROS qui attaque.


def GetAbilities() -> Sequence['Ability']:

    def remelanger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        defausse = DefausseRegistered(joueur)
        cartes = [c for c in defausse.Get(True) if c is not None][:2]
        if cartes:
            Faces.ShuffleAllTo(cartes, DeckRegistered(joueur), effect)

    def retourner_le_sbire(effect: 'Effect', message: 'Message.AfterUnitBeAttacked') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        # ⚠ `message.attacked`, PAS `message.trigger` : sur
        # `Message.AfterUnitAttackUnit`, le `trigger` est L'ATTAQUANT (le
        # heros) et la cible est `attacked` (modele `01118` * Sonic
        # Converter). Se tromper ici, c'est tenter de recruter son propre
        # heros.
        sbire = message.attacked
        if joueur is None or sbire is None or not sbire.IsInPlay():
            return

        def recruter(cibles: Sequence['CardFace']) -> None:
            Unused(cibles)
            RecruterCommeAllieRegistered(sbire, joueur, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take control of that minion as a REGISTERED ally",
                recruter,
            ).SetHasNoTargetEffect()
            .SetCostFunc(CostFunc.Spend(Cost(str(IconesDeBoostDe(sbire))))),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            remelanger,
        ).SetPlay(),
        AbilityFactory.AfterUnitBeAttacked(
            AbilityType.HeroResponse,
            Minion,
            retourner_le_sbire,
            attacker="YourHero",
        ).SetPlay(),
    ]
