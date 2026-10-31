from . import *

# Damaged Containment Suit — OBLIGATION de Vance Astro. Boost 2.
# Give to the Vance Astro player.
# Forced Interrupt: When you would take any amount of damage, take 1 additional damage.
# When Revealed: Find Containment Suit and tuck it here. If your remaining hit points were reduced to 0 or less this way,
#   set your hit point dial to 1 instead.
# Alter-Ego Action: Exhaust Vance Astro → add Containment Suit to your hand and remove this obligation from the game.
#
# CARTES DE REFERENCE
#  - `rg012` Caged Bird : la meme structure (chercher une carte nommee OU QU'ELLE SOIT, la glisser sous l'obligation, puis une
#    Alter-Ego Action qui l'en sort) ; `Search.SearchForCard(.., include_in_play=True)` + `this.PlaceCardHere(carte, False, effect)`.
#  - `dt094` Diversion Skill : `WhenUnitWouldTakeDamage(.., conditions=[identite du joueur])` + `message.IncreaseDamage(1, effect)`.
#  - `03008` Captain America's Helmet : `SetHealth(1, effect)` pour « set your hit point dial to 1 ».
#
# TEXTE CONTRE CODE
#  « Forced Interrupt: when YOU would take ANY amount of damage » -> TOUTE source (attaque, indirect, effet), identite du porteur
#    uniquement ; « take 1 ADDITIONAL damage » -> on AJOUTE 1 (`IncreaseDamage`), on ne remplace pas.
#  « Find Containment Suit » -> main, deck, defausse, zone du joueur ET jeu (comme rg012) : le costume peut etre PORTE.
#  « tuck it here » -> face cachee sous l'obligation (`PlaceCardHere(.., False, ..)`).
#  « if your remaining hit points were reduced to 0 or less THIS WAY » -> seulement si c'est le depart du costume (+2 PV) qui les
#    amene a 0 ou moins : on pose le cadran a 3 AVANT le depart (3 - 2 = 1) plutot que de laisser le moteur defaire l'identite.
#  « Alter-Ego Action: exhaust Vance Astro » -> `AlterEgoAction` + `Exhaust("YourIdentity")` ; le costume rejoint la MAIN (`ReturnToHand`),
#    PUIS l'obligation quitte le jeu (la retirer d'abord emporterait le costume avec elle : lecon rg012).
#  Chiffres : +1 degat, PV remis a 1, boost 2 (dans `desc`).

BONUS_PV_COSTUME = 2  # Containment Suit (mv004) : « You get +2 hit points »


def GetAbilities() -> Sequence['Ability']:

    def degat_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        message.IncreaseDamage(1, effect)

    def votre_identite(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Obligation)
        # ⚠ `GetGaveToPlayer()` (modele 60060) et NON `GetControlByPlayer()` : une obligation n'est pas « controlee » comme une amelioration,
        # elle est DONNEE a un joueur. Avec `GetControlByPlayer()` le filtre ne trouvait personne et le degat en plus ne partait jamais
        # (premiere version du cas : 3 degats au lieu de 4).
        joueur = this.GetGaveToPlayer() or this.GetControlByPlayer()
        return joueur is not None and message.trigger == joueur.GetIdentity()

    def damaged_containment_suit(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        costume = Search.SearchForCard(
            effect,
            joueur,
            include_player_hand_cards=True,
            include_player_deck=True,
            include_player_discard_pile=True,
            include_player_area=True,
            include_in_play=True,
            name=NOM_COSTUME,
        )
        if not costume:
            return
        # Le costume donne +2 PV tant qu'il est EN JEU : son depart fait baisser les PV restants de 2. S'ils tombaient a 0 ou
        # moins, le texte les remet a 1 : on pose 3 avant, le depart ramene a 1.
        if costume.IsInPlay() and identite is not None and identite.health - BONUS_PV_COSTUME <= 0:
            identite.SetHealth(BONUS_PV_COSTUME + 1, effect)
        this.PlaceCardHere(costume, False, effect)

    def retrouver_le_costume(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = effect.GetInitiator()
        cachees = list(this.GetPlacedCardArea().Get())
        if cachees and joueur is not None:
            Faces.ReturnToHand(cachees, joueur, effect)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            None,
            degat_en_plus,
            conditions=[votre_identite],
        ),
        AbilityFactory.WhenThisObligationRevealed(
            damaged_containment_suit,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            retrouver_le_costume,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
