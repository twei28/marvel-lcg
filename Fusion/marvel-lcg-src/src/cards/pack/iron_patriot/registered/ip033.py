from . import *

# * The Hood — SBIRE du deck REGISTERED (20/20). 4 PV, ATQ 2, MNG 3, boost 4.
# CRIMINAL. ELITE.
# Steady. Surge.
# [star] Forced Interrupt: When The Hood attacks, give him 1 boost card for
#   this activation.
# Demonic Crimes — Special: Discard the top card of the REGISTERED deck. For
#   each boost icon discarded this way, choose to deal 1 damage to an enemy or
#   remove 1 threat from a scheme.
#
# ⚠ LA DERNIERE CARTE DU DECK EN BRULE UNE AUTRE. Le « Special » se paie en
# cartes du deck REGISTERED : plus on l'utilise, moins il reste de monde a
# recruter. C'est la seule carte du pack qui fait ce troc.
#
# CARTES DE REFERENCE
#  - `01113` * Klaw : `message.GiveAdditionalBoostCardForThisActivation(1,
#    effect)` sur `WhenUnitWouldAttack(ForcedInterrupt, "This", ...)`.
#  - `bc006` Lucky Hit : compter les icones d'une carte qu'on vient de
#    defausser.
#
# TEXTE CONTRE CODE
#  ⚠ « give HIM 1 boost card » : une carte de boost en plus pour SON attaque,
#    pas pour celle du vilain. Cette ligne ne vaut donc que tant que The Hood
#    est un SBIRE — un allie ne recoit pas de cartes de boost. Elle est portee
#    quand meme apres la conversion (voir `RecruterCommeAllieRegistered`) : la
#    fenetre existe, elle ne se declenche simplement jamais.
#  ⚠ « the top card of the REGISTERED deck » : le deck additionnel, pas celui
#    du joueur ni celui de rencontre.
#  ⚠ « For each boost ICON discarded this way » : les icones CHIFFREES, lues
#    APRES la defausse par `IconesDeBoostDe` — donc en voyant les
#    modificateurs, `ip008` compris. L'etoile de boost n'en fait pas partie.
#  ⚠ « CHOOSE to deal 1 damage OR remove 1 threat » : le choix se fait ICONE
#    PAR ICONE, pas une fois pour toutes. Trois icones peuvent donner deux
#    degats et un contre.
#  ⚠ Deck REGISTERED vide : rien ne se passe.
#  ⚠ Steady et Surge sont des BASES NATIVES de sbire.


def GetAbilities() -> Sequence['Ability']:

    def carte_de_boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    def crimes_demoniaques(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        deck = DeckRegistered(joueur)
        if deck.GetSize() == 0:
            return
        defaussees = deck.DiscardCardsInternal(1, effect, continue_after_shuffle=False)
        icones = sum(IconesDeBoostDe(f) for f in defaussees)

        for _ in range(icones):
            def frapper(cibles: Sequence['CardFace']) -> None:
                this.DealDamage([c for c in cibles if c is not None], 1, effect)

            def contrer(cibles: Sequence['CardFace']) -> None:
                this.RemoveThreatFromSchemes([c for c in cibles if c is not None], 1, effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 1 damage to an enemy",
                    frapper,
                ).SetTarget(Enemy),
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 threat from a scheme",
                    contrer,
                ).SetTarget(Scheme2),
            )

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            carte_de_boost_en_plus,
        ),
        SpecialRegistered("Demonic Crimes", crimes_demoniaques),
    ]
