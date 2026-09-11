from . import *
# * Outer Demons — AMELIORATION, cout 2, [wild]. CONDITION. INFERNAL.
# Hellcat gains villainous.
# Interrupt: When a boost card given to Hellcat is turned faceup, cancel its
#   "Boost" ability. Then, heal 1 damage from Hellcat.
# Forced Response: After you change form, discard this card.
#
# ⚠ UN HEROS QUI RECOIT DES CARTES BOOST. Voie ouverte le 01/09/2026 par dd001a
#   Doctor Doom (« you gain villainous ») : `Hero` herite de `HasVillainous`,
#   donc de `CanBoost`, et `can_attack.py:264` distribue une carte boost a
#   l'attaque de base de toute face villainous ; `ResolveBoostCards` la
#   retourne face visible (message `WhenBoostCardTurnedFaceUp`) et ajoute ses
#   icones a l'ATQ. Ici l'accord est CONTINU, porte par l'amelioration :
#   `GiveKeywordToAttached(..., villainous=1)`, parametre ajoute a la fabrique
#   le 11/09/2026 (`Gain` l'acceptait deja).
# ⚠ Attaque SEULEMENT : le moteur ne distribue pas de boost au contre de base
#   (can_thwart.py n'a pas l'equivalent de can_attack.py:264). Ecart assume,
#   identique a Doom, note dans le gabarit.
# ⚠ `canbe_cancel=None` et non "Ability" : le soin doit partir meme si la
#   carte boost n'a pas d'effet [star] ; « cancel » est alors sans objet.
# Modeles : dd001a (villainous), 10009 Boundless Rage (Forced Response apres
# changement de forme -> defausse), fabrique `WhenBoostCardTurnedFaceUp`
# (boost.py:239) avec `boost_for_card`.

def GetAbilities() -> Sequence['Ability']:

    def outer_demons(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Upgrade)
        message.CancelBoostAbility(effect)
        joueur = effect.GetInitiator()
        heroine = joueur.GetHero() if joueur else None
        if heroine is not None:
            this.HealthUnits([heroine], 1, effect)

    def discard_after_change_form(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        Faces.DiscardAll([this], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name=HELLCAT), villainous=1),
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Interrupt,
            None,
            outer_demons,
            boost_for_card=CardFinder(name=HELLCAT),
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.ForcedResponse,
            "You",
            discard_after_change_form,
        ),
    ]
