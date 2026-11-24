from cards.pack import *

# ===========================================================================
# Pack HELLFIRE HUNT - SCENARIO 1 « WHITE QUEEN » (campagne Hellfire Hunt, « MC Custom Content By: Dipsome »), 26/10/2026.
# Prefixe `hf` (tools/prefixes_fanmade.json), set 240. Module PLAT : `cards.pack.hellfire_hunt_white_queen.<card_id>`
# (modele : pack bebop_rocksteady). Tout helper appele par une carte vit ICI (NameError avale par le moteur sinon, lecon hk005).
#
# card_id : hf101-hf125 = scenario (numero du scan + 100), hf301-hf308 = module Perfection, hf311-hf318 = Hellfire Conclave,
# hf321-hf325 = Psionic Delusion. hf001-hf099 = fondations de campagne (autre agent, pack a part).
#
# LE SCENARIO EN UNE PHRASE : White Queen est UN vilain a deux faces (A = PSIONIC, B = DIAMOND) qui change de forme sans etre
# « vaincue » : ses PV, ses degats et ses attachements ne bougent pas (livret p. 8, « Two-sided villain »). Quand un STADE est vaincu,
# le stade suivant est revele DANS LA MEME FORME : le moteur choisit la face qui partage le plus de traits avec l'ancienne
# (`scenario.AdvanceVillainStage`, `GetShareTraitNum`), ce que mesure le cas `[hf] hf101 ... meme forme`.
# ===========================================================================

NOM_WQ = "White Queen"
PSIONIQUE = "PSIONIC"
DIAMANT = "DIAMOND"
ILLUSION = "ILLUSION"


def VilainWQ(effect: 'Effect') -> 'Villain|None':
    """Le VILAIN White Queen en jeu (jamais un sbire homonyme du module Perfection)."""
    for v in Worlds.GetVillains(effect):
        if v.IsName(NOM_WQ):
            return v
    return None


def EstPsionique(face: 'CardFace|None') -> bool:
    return face is not None and face.HasTrait(PSIONIQUE)


def EstDiamant(face: 'CardFace|None') -> bool:
    return face is not None and face.HasTrait(DIAMANT)


def RetournerWQ(effect: 'Effect', villain: 'Villain|None'=None) -> bool:
    """« Flip White Queen » : retourne la CARTE du vilain. Ses PV, ses degats, ses statuts et ses attachements restent (un
    retournement n'est pas une defaite). Sans effet si le vilain n'est plus en jeu."""
    villain = villain or VilainWQ(effect)
    if villain is None or not villain.IsInPlay():
        return False
    return villain.card.Flip(effect)


def NombreDeCartesAvecTrait(effect: 'Effect', trait: str) -> int:
    """Le nombre de cartes en jeu portant ce trait (modele 06027 : `Worlds.FindCardSizeOnField`)."""
    return Worlds.FindCardSizeOnField(effect, trait=trait)


def NombreDIllusions(effect: 'Effect') -> int:
    """« the number of [[Illusion]] cards in play »."""
    return NombreDeCartesAvecTrait(effect, ILLUSION)


def DefausserEtCompterIcones(effect: 'Effect', nombre: int=1) -> int:
    """Defausse le dessus du deck de rencontre et rend le nombre d'icones de boost des cartes defaussees."""
    faces = Worlds.DiscardEncounterCards(nombre, effect)
    return FacesCounter.CountTotalBoostIcons(faces)


def ReponseForceeFormeA() -> 'Ability':
    """Formes A (PSIONIC) des trois stades : « After White Queen attacks you, discard the top card of the encounter deck. If that card
    has the ILLUSION trait, reveal it. Flip White Queen (whether that card had the ILLUSION trait or not). »"""
    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Villain)
        joueur = message.GetAgainstPlayer()
        face = Worlds.DiscardEncounterTopCard(effect)
        if face is not None and face.HasTrait(ILLUSION) and joueur is not None:
            face.Reveal(joueur, effect)
        RetournerWQ(effect, this)

    return AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "This", apres_attaque)


def ReponseForceeFormeB() -> 'Ability':
    """Formes B (DIAMOND) : « After White Queen schemes, flip this card. »"""
    def apres_complot(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        RetournerWQ(effect, effect.this.CastTo(Villain))

    return AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_complot)


def InterruptionForceeFormeB() -> 'Ability':
    """Formes B : « When White Queen would take any amount of damage from an attack, discard the top card of the encounter deck.
    Reduce damage from that attack by the number of boost icons discarded this way. »"""
    def avant_degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        icones = DefausserEtCompterIcones(effect)
        if icones > 0:
            message.PreventDamage(icones, effect)

    return AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", avant_degats, is_from_attack=True)


def MenaceSurLeComplotPrincipal(effect: 'Effect', valeur: int) -> None:
    """« place N threat on the main scheme »."""
    effect.this.PlaceThreatOnSchemes("MainScheme", valeur, effect)


def ChercherEtReveler(effect: 'Effect', nom: str, *, mis_de_cote: bool=False) -> 'CardFace|None':
    """« The first player searches the encounter deck and discard pile (and set-aside area) for X and reveals it. (Shuffle.) »
    Le melange est fait par `Search` lui-meme (modele 01180 Legions of Hydra)."""
    joueur = Worlds.GetFirstPlayer(effect)
    face = Search.EncounterCard(effect, "FirstPlayer", include_discard_pile=True, include_set_aside=mis_de_cote, name=nom)
    if face is not None:
        face.Reveal(joueur, effect)
    return face


COMPTEUR_ILLUSION = 'illusion'


def ChercheurWQ() -> 'CardFinder':
    return CardFinder(name=NOM_WQ, card_type=Villain)


def ExemplaireIllusionAttache(ability_type: 'AbilityType'=None) -> None:
    return None


def PoserUnCompteurSiPsionique() -> 'Ability':
    """« When Revealed : If the villain or a minion engaged with you has the PSIONIC trait, place 1 additional illusion counter here. »
    (modules Perfection hf303-hf306 ; modele de lecture : 41029 Telekinetic Dragon pour le joueur qui recoit la carte)."""
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        candidats = list(Worlds.GetVillains(effect)) + list(joueur.GetEngagedMinions())
        if any(f.HasTrait(PSIONIQUE) for f in candidats):
            Faces.PlaceCountersOn([this], 1, COMPTEUR_ILLUSION, effect)

    return AbilityFactory.WhenThisRevealed(None, revelee)


def RetirerUnCompteurIllusion(effect: 'Effect') -> None:
    """« remove 1 illusion counter from here » : le dernier retire fait quitter la carte (mot-cle Uses, natif)."""
    Faces.RemoveCountersOn([effect.this], 1, COMPTEUR_ILLUSION, effect)


def SbireWQEntreEnJeu() -> 'Ability':
    """Perfection hf301 / hf302 : « Forced Interrupt : When a White Queen minion attempts to enter play, give the engaged player a facedown
    encounter card and discard this card. » Le sbire n'entre JAMAIS en jeu tant que le VILAIN White Queen y est (scenario 1 ; livret p. 8) ; correctif du
    01/11/2026 : l'Interruption ne part que dans ce cas (scenario 4 Torn : le vilain est Emma Frost). Modele : 22028 Gamora
    (`WhenCardWouldEnterPlay` Forced Interrupt « This »)."""
    def entre_en_jeu(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        # CORRECTIF (01/11/2026, scenario Torn, `hellfire_hunt_torn`) : la carte est UNIQUE (« * White Queen ») ; elle ne peut pas entrer en jeu pendant que le VILAIN
        # White Queen y est (scenario 1). Au scenario 4 (Torn) le vilain est Emma Frost : les sbires White Queen du module Perfection y entrent NORMALEMENT (hf510
        # Hellfire Assault : « if it is White Queen, Emma Frost attacks the player »). Sans cette garde l'Interruption defaussait ces sbires partout.
        if VilainWQ(effect) is None:
            return
        ini = message.by_effect.initiator
        joueur = ini if Player.IsType(ini) else Worlds.GetFirstPlayer(effect)
        # La carte va a la DEFAUSSE rencontre au lieu d'entrer en jeu (`ChangeToArea`, modele 25002 / gmw collector).
        message.ChangeToArea(Worlds.GetEncounterDiscardPile(effect), effect)
        joueur.DealEncounterCards(1, effect)

    return AbilityFactory.WhenCardWouldEnterPlay(AbilityType.ForcedInterrupt, "This", entre_en_jeu)


def Soigner_Interdit() -> 'Ability':
    """« Attached character cannot be healed. » : un soin du personnage porteur est REMPLACE par rien (modele 90129 Wounded Civilians :
    `Ability(Interrupt, Message.WhenUnitHealHealth, ...)` + `SetBeInstead`)."""
    def pas_de_soin(effect: 'Effect', message: 'Message.WhenUnitHealHealth') -> None:
        message.SetBeInstead(effect)

    def porteur(effect: 'Effect', message: 'Message.WhenUnitHealHealth') -> bool:
        hote = getattr(effect.this, "bind_face", None)
        return hote is not None and message.trigger.card == hote.card

    return Ability(AbilityType.NonKeyword, Message.WhenUnitHealHealth, [porteur], pas_de_soin)
