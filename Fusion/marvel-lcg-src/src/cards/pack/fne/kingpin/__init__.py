from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout, RetournerLAttachement
from game.card.face.attribute.can_boost import CanBoost

# Helpers du set Kingpin (Fear No Evil, 60159-60176), scenario final.
# Le vilain est une carte RECTO-VERSO (A1/A2 en standard, B1/B2 en expert) :
# face 1 intouchable (Stalwart, pas de degats, pas d'amelioration, manigance
# au lieu d'attaquer), face 2 atteignable (Steady, MARTIAL ARTIST). C'est
# Public Support (60163a) qui le retourne au debut d'une phase du mechant.
# Les nemesis des joueurs sont mises en jeu par le complot (60161a Setup,
# 60162a When Revealed) et par les traitrises (60175, 60176).

TRAIT_ARTS_MARTIAUX = "MARTIAL ARTIST"
TRAIT_UNDERLING = "UNDERLING"
GABARIT_ALLIE_BLACK_CAT = "fne_black_cat_ally"   # ATK 0** / THW 0** (2 degats consecutifs), Villainous, THIEF UNDERLING (pack "")


def TrouverKingpin(effect: 'Effect') -> 'Villain|None':
    """Le vilain Kingpin en jeu, quelle que soit sa face. `card_type=Villain`
    ecarte le SBIRE nemesis d'Echo, qui porte le meme nom."""
    return Worlds.FindCardOnField(effect, name="Kingpin", card_type=Villain)


def KingpinArtMartial(effect: 'Effect') -> bool:
    """« If Kingpin has the MARTIAL ARTIST trait » : la face 2 seulement."""
    k = TrouverKingpin(effect)
    return k is not None and k.HasTrait(TRAIT_ARTS_MARTIAUX)


def TrouverPublicSupport(effect: 'Effect') -> 'Environment|None':
    return Worlds.FindCardOnField(effect, name="Public Support", card_type=Environment)


def SbireNemesisEnJeu(joueur: 'Player', effect: 'Effect') -> 'Minion|None':
    """« Your nemesis minion », s'il est en jeu (marqueur `nemesis_of_player`
    pose a la mise en place, lu par `CardFinder(is_nemesis=joueur)`)."""
    return Worlds.FindCardOnField(effect, finder=CardFinder(card_type=Minion, is_nemesis=joueur))


def SbiresNemesisMisDeCote(joueur: 'Player') -> List['Minion']:
    """Le(s) sbire(s) nemesis encore dans la reserve nemesis du joueur."""
    return [f for f in joueur.set_aside_nemesis_sets.Get()
            if Minion.IsType(f) and f.IsNemesis(joueur)]


def CartesNemesisMisesDeCote(joueur: 'Player') -> List['CardFace']:
    """« your set-aside nemesis set » : ce qui reste dans la reserve."""
    return [f for f in joueur.set_aside_nemesis_sets.Get()
            if f.card.area is joueur.set_aside_nemesis_sets]


def TrouverEtRevelerUnderling(effect: 'Effect', joueur: 'Player') -> 'Minion|None':
    """« finds an UNDERLING minion that is not in play and reveals it » :
    Find (deck, defausse, mise de cote), jamais une carte deja en jeu."""
    return Find.FindAndReveal(
        effect, joueur,
        finder=CardFinder(card_type=Minion, trait=TRAIT_UNDERLING,
                          check_effect_fn=lambda e, f: not f.IsInPlay()),
    )


def CapacitesDeKingpin1() -> Sequence['Ability']:
    """Face 1 (A1 / B1). Stalwart : base desc.
    « Kingpin cannot be dealt damage or have upgrades attached » :
    UnitCannotTakeDamage (sd022, rend une LISTE) + UnitCannotHaveUpgradeAttached
    (46003, liste aussi).
    « [star] Forced Interrupt: When Kingpin would attack you, he schemes
    instead » : WhenUnitWouldAttack + message.DoSchemeInstead (51019
    Invisibility Gear, ag005)."""
    def manigance(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DoSchemeInstead(effect)

    moi = CardFinder(name="Kingpin", card_type=Villain)
    return [
        *AbilityFactory.UnitCannotTakeDamage(moi),
        *AbilityFactory.UnitCannotHaveUpgradeAttached(moi),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", manigance),
    ]


def CapacitesDeKingpin2(*, overkill: bool) -> Sequence['Ability']:
    """Face 2 (A2 / B2). Steady : base desc.
    « [star] Forced Interrupt: When Kingpin activates against you, if you are
    not engaged with a minion, give Kingpin 1 additional boost card for this
    activation [B2 : and this activation gains overkill if it is an attack] » :
    modele 60093 Maggia Underboss (WhenUnitWouldAttack + WhenUnitWouldScheme,
    GiveAdditionalBoostCardForThisActivation, condition dans `conditions`)."""
    def sans_sbire(effect: 'Effect', message: 'Message.WhenUnitWouldAttack|Message.WhenUnitWouldScheme') -> bool:
        joueur = message.GetAgainstPlayer()
        return joueur is not None and joueur.engaged_minions.GetSize() == 0

    def boost_en_plus(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)

    def boost_et_overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
        if overkill:
            message.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", boost_et_overkill, conditions=[sans_sbire]),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", boost_en_plus, conditions=[sans_sbire]),
    ]


def ReponseForceeSoutien() -> 'Ability':
    """Public Support (les deux faces) : « Forced Response: After a minion is
    defeated, place 1 support counter here » (60094 Consolidate Power)."""
    def sbire_vaincu(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        Faces.PlaceCountersOn([effect.this], 1, 'support', effect)

    return AbilityFactory.AfterUnitBeDefeated(AbilityType.ForcedResponse, Minion, sbire_vaincu)


def AttacheAKingpin() -> 'Ability':
    """« Attach to Kingpin » (When Revealed des PERSONA / WEAPON)."""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Kingpin", card_type=Villain))


def CapacitesDUnePersona(trait_evenement: str, nom_action: str,
                         a_la_revelation: Callable[['Effect', 'Player', 'Villain'], None],
                         action: Callable[['Effect', 'Player', 'Villain'], None],
                         ) -> Sequence['Ability']:
    """James Wesley / Vanessa Fisk : +1 SCH (desc SCH+).
    When Revealed: Attach to Kingpin [+ effet].
    Hero Action: Discard a <TRAIT> event from your hand -> discard this.
      Kingpin <schemes | attacks you>.
    [star] Boost: Attach this card to Kingpin.
    Modeles : 60117 (AttachToFaceWhenPutIntoPlay(Villain)), 45014
    (CostFunc.Discard("YourHandCards")), 21170 (WhenThisBoostAttachTo)."""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        kingpin = TrouverKingpin(effect)
        if kingpin is not None:
            a_la_revelation(effect, message.GetToPlayer(), kingpin)

    def agir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        joueur = effect.GetInitiator()
        kingpin = TrouverKingpin(effect)
        Faces.DiscardAll([this], effect)
        if kingpin is not None:
            action(effect, joueur, kingpin)

    return [
        AttacheAKingpin(),
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, agir)
            .SetName(nom_action)
            .SetCostFunc(CostFunc.Discard("YourHandCards", trait=trait_evenement, card_type=Event)),
        AbilityFactory.WhenThisBoostAttachTo(CardFinder(name="Kingpin", card_type=Villain)),
    ]


def ConvertirBlackCatEnAlliee(sbire: 'Minion', joueur: 'Player', effect: 'Effect') -> bool:
    """« take control of Black Cat as an ally » (an ally that takes 2
    consequential damage after she attacks or thwarts) : Faces.TreatAsAlly
    (faces.py:340, modele iron_patriot), gabarit fne_black_cat_ally (pack "",
    ajoute le 18/09/2026 : ATK 0** / THW 0**, Villainous 1, THIEF UNDERLING).
    TreatAsAlly recopie nom, image, ATK et SCH->THW ; les 2 degats consecutifs
    viennent des deux etoiles du gabarit ; Villainous est garde (FAQ du livret,
    `Ally` herite de HasVillainous depuis le 18/09/2026)."""
    return Faces.TreatAsAlly(sbire, GABARIT_ALLIE_BLACK_CAT, joueur, effect)
