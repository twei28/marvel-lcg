from . import *

# Raising Block — EVENEMENT 0 [physical], Taijutsu (TMNT Shinobi, Inkwire). DEFENSE.
# Hero Interrupt (defense): When you would take any amount of damage from an attack, prevent 3 of that damage.
# Hero Response: After you spend this card to pay for a DEFENSE event, draw 1 card.
#
# Mots-cles : aucun (Shinobi / Taijutsu = classe, fiche shinobi.md lue).
#
# Cartes de reference :
#  - « prevent 3 of that damage » (un Interrupt de defense) : `05005` Wiggle Room (`WhenUnitWouldTakeDamage(
#    HeroInterrupt, "You", op).SetPlay().SetLabel('defense')` + `message.PreventDamage(3, effect)`), avec le filtre
#    `is_from_attack=True` de `donatello/td003` Bo Tobu pour « from an attack » ;
#  - « After you spend this card to pay for a <filtre> event » : `42008` Avian Anatomy
#    (`AfterYouSpendThisCard(Response, op, to_pay_card=CardFinder2("AERIAL", Event))`) ; `32018` Defensive Energy
#    pour « when you spend » (la meme carte-ressource, cote Interruption).
# TEXTE CONTRE CODE
#  ⚠ « any amount of damage FROM AN ATTACK » -> `is_from_attack=True` (pas les degats de carte ni de traitrise).
#  ⚠ « prevent 3 OF THAT damage » : au plus 3, pas tout.
#  ⚠ « After you spend THIS card to pay for a DEFENSE event » : une AUTRE carte, trait DEFENSE, de type evenement ;
#    la Reponse est portee par la carte depensee, pas par la carte payee.
#  ⚠ « Hero » Interrupt / Response : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def raising_block(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        message.PreventDamage(3, effect)

    def piocher(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is not None:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            raising_block,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            piocher,
            to_pay_card=CardFinder2("DEFENSE", Event),
        ),
    ]
