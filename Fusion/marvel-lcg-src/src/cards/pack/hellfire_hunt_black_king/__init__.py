from cards.pack import *

# ===========================================================================
# Pack HELLFIRE HUNT - SCENARIO 2 « BLACK KING » (campagne Hellfire Hunt, « MC Custom Content By: Dipsome »), 01/11/2026.
# Prefixe `hf` (tools/prefixes_fanmade.json), set 242. Module PLAT : `cards.pack.hellfire_hunt_black_king.<card_id>`
# (modele : le pack hellfire_hunt_white_queen). Tout helper appele par une carte vit ICI (NameError avale par le moteur sinon, lecon hk005).
#
# card_id : hf201-hf227 = scenario (numero du scan + 200), hf331-hf338 = module « Sebastian Shaw » (que CE pack porte seul ; le scenario Torn le
# reutilise par son nom d'encounter set `hf_sebastian_shaw`).
#
# LE SCENARIO EN UNE PHRASE : Sebastian Shaw (« Absorb ») stocke l'energie des coups recus sous forme de compteurs `energy` ; en attaquant il en
# depense jusqu'a 3 pour +1 ATK chacun ; le Black King (attachement permanent) convertit ces compteurs en MENACE ; les mutants CAPTIFS sont
# caches sous la manigance annexe « Captured by Hellfire! », qui fait avancer le complot (2A) quand le dernier est libere.
# ===========================================================================

NOM_SHAW = "Sebastian Shaw"
ENERGIE = 'energy'
CAPTIF = "CAPTIVE"
CLE_TACTIQUE = 'king_tactic'      # compteur de round (`world.stat.AddRoundCounter`) : instances de la Tactique du Roi sur la face B


def ShawVilain(effect: 'Effect') -> 'Villain|None':
    """Le VILAIN Sebastian Shaw en jeu (jamais le sbire homonyme du module : `Villain` seulement)."""
    for v in Worlds.GetVillains(effect):
        if v.IsName(NOM_SHAW):
            return v
    return None


def Energie(face: 'CardFace|None') -> int:
    """Nombre de compteurs d'energie sur cette carte."""
    return face.GetCounters(ENERGIE) if face is not None else 0


def PlacerEnergie(effect: 'Effect', nombre: int) -> int:
    """« place N energy counters on Sebastian Shaw » : sans effet si le vilain n'est pas en jeu. Rend le nombre pose."""
    shaw = ShawVilain(effect)
    if shaw is None or nombre <= 0:
        return 0
    return Faces.PlaceCountersOn([shaw], nombre, ENERGIE, effect) or 0


def MenaceSurLeComplotPrincipal(effect: 'Effect', valeur: int) -> None:
    """« place N threat on the main scheme »."""
    if valeur > 0:
        effect.this.PlaceThreatOnSchemes("MainScheme", valeur, effect)


def ChercherEtReveler(effect: 'Effect', nom: str, *, mis_de_cote: bool=False) -> 'CardFace|None':
    """Cherche une carte de rencontre par son nom (deck, defausse, zone mise de cote) et la revele ; melange fait par `Search`."""
    joueur = Worlds.GetFirstPlayer(effect)
    face = Search.EncounterCard(effect, "FirstPlayer", include_discard_pile=True, include_set_aside=mis_de_cote, name=nom)
    if face is not None:
        face.Reveal(joueur, effect)
    return face


# ----------------------------------------------------------------------------------------------------------------------------
# Absorb / attaque de Shaw (hf201-hf203)
# ----------------------------------------------------------------------------------------------------------------------------
def AbilitesDeShaw(energie_en_plus: int=0) -> 'List[Ability]':
    """Les deux capacites imprimees sur Shaw (I), (II) et (III) :
    [star] Forced Interrupt : When Sebastian Shaw attacks, remove all energy counters here to a maximum of 3. For each energy counter removed in
    this way, he gets +1 ATK for this activation.
    Absorb - Forced Response : After Sebastian Shaw takes damage from an attack, place energy counters on him equal to the damage taken.
    (III) : « Place 1 additional energy counter here. » : `energie_en_plus`."""
    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        shaw = effect.this.CastTo(Villain)
        retirer = min(3, Energie(shaw))
        if retirer > 0:
            retires = Faces.RemoveCountersOn([shaw], retirer, ENERGIE, effect) or 0
            if retires > 0:
                message.GainATKForThisAttack(retires, effect)

    def absorption(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        shaw = effect.this.CastTo(Villain)
        Faces.PlaceCountersOn([shaw], message.took_damage + energie_en_plus, ENERGIE, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", attaque),
        AbilityFactory.AfterUnitTookDamage(AbilityType.ForcedResponse, "This", absorption, is_from_attack=True),
    ]


# ----------------------------------------------------------------------------------------------------------------------------
# Black King (hf207a / hf207b) : « King's Tactic »
# ----------------------------------------------------------------------------------------------------------------------------
def SurShaw() -> 'CardFinder':
    return CardFinder(name=NOM_SHAW, card_type=Villain)


def TactiqueDuRoi(limitee: bool) -> 'Ability':
    """King's Tactic - Forced Interrupt : When Sebastian Shaw's « Absorb » ability triggers while there is an energy counter on him, remove each
    energy counter from him, place that much threat on the main scheme. [face B : (Max 1[per player] times per round.)]
    L'Absorb de Shaw est une Reponse forcee « apres des degats d'attaque » ; la Tactique est une INTERRUPTION forcee sur le MEME message : le moteur
    resout les interruptions forcees avant les reponses forcees (`TimingPriority`), donc les compteurs deja la sont retires AVANT que l'Absorb n'en
    pose de nouveaux (ce que mesure le cas `[hf] hf207a ... avant l'Absorb`).
    FAQ du livret (p. 22) : la limite compte les instances de la face B seulement ; au-dela, la Tactique ne part pas et les compteurs s'empilent."""
    def sous_la_limite(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        if not limitee:
            return True
        return effect.world.stat.GetRoundCounter(Worlds.GetFirstPlayer(effect), CLE_TACTIQUE) < Worlds.GetPlayerNum(effect)

    def tactique(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        shaw = message.trigger
        retires = Faces.RemoveCountersOn([shaw], "All", ENERGIE, effect) or 0
        if limitee:
            effect.world.stat.AddRoundCounter(Worlds.GetFirstPlayer(effect), CLE_TACTIQUE)
        MenaceSurLeComplotPrincipal(effect, retires)

    return AbilityFactory.AfterUnitTookDamage(
        AbilityType.ForcedInterrupt, "AttachedEnemy", tactique, is_from_attack=True,
        conditions=[lambda effect, message: Energie(message.trigger) > 0, sous_la_limite])


# ----------------------------------------------------------------------------------------------------------------------------
# Mise en place du scenario (hf204a) et alliés CAPTIVE (hf208-hf211)
# ----------------------------------------------------------------------------------------------------------------------------
CAPTIFS = ['hf208', 'hf209', 'hf210', 'hf211']     # Dust, Mercury, Surge, Prodigy (scans 8 a 11 + 200)
CLE_RECRUTES = 'Recruited Allies'


def CaptifsDejaRecrutes(effect: 'Effect') -> List[str]:
    """Les captifs que le carnet de la campagne note deja « Recruited » (ils sont alors dans le deck Recruited Mutants, pas mis de cote)."""
    return [i for i in CampaignLog.GetListInternal(CLE_RECRUTES, effect) if i in CAPTIFS]


def MiseEnPlaceDuScenario(effect: 'Effect') -> None:
    """Setup de 1A : « Remove each minion named Sebastian Shaw from the game. Set each CAPTIVE ally aside. Reveal the Captured by Hellfire! side
    scheme. Attach Black King to Sebastian Shaw. » Dans cet ordre : les captifs doivent etre de cote AVANT que Captured by Hellfire! les cache."""
    sbires = [f for f in Worlds.GetEncounterDeckCards(effect) if Minion.IsType(f) and f.IsName(NOM_SHAW)]
    if sbires:
        Faces.RemoveAllFromGame(sbires, effect)

    deja = CaptifsDejaRecrutes(effect)
    for card_id in CAPTIFS:
        if card_id not in deja:
            CardFactory.GenerateCard(card_id, effect.world.aside_deck, effect.world)

    ChercherEtReveler(effect, "Captured by Hellfire!")

    for roi in Worlds.GetSetAsideAreaCards(effect, CardFinder(name="Black King")):
        roi.PutIntoPlay(Worlds.GetFirstPlayer(effect), effect)
        break


def CaptifRecrute() -> 'Ability':
    """« These allies can be used for the rest of the campaign as have the RECRUITED trait » (livret p. 10) : un captif que le carnet note
    « Recruited » porte le trait RECRUITED (Xavier's Institute envoie alors sa defausse dans la defausse Recruited Mutants). Dans le scenario
    ou il est libere il ne le porte PAS encore : le carnet ne le note qu'a la victoire."""
    def note(effect: 'Effect', ui: List['CardFace']) -> int:
        return 1 if effect.this.paper.card_id in CampaignLog.GetListInternal(CLE_RECRUTES, effect) else 0

    return AbilityFactory.ThisGainKeyword(note, trait="RECRUITED")


def BlackKing(effect: 'Effect') -> 'CardFace|None':
    """L'attachement Black King (face A ou B) porte par Sebastian Shaw."""
    shaw = ShawVilain(effect)
    if shaw is None:
        return None
    for face in shaw.GetAttachedAttachments():
        if face.paper.card_id in ('hf207a', 'hf207b'):
            return face
    return None


def BoostDonnerLeSbire(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
    """Ebon Knight, [star] Boost : « After this activation, deal Ebon Knight to you as a facedown encounter card. »"""
    this = effect.this
    joueur = message.GetToPlayer()

    def apres_l_activation() -> None:
        joueur.DealEncounterCard(this, effect)

    message.AfterThisActivation(effect, apres_l_activation)


# ----------------------------------------------------------------------------------------------------------------------------
# Module « Sebastian Shaw » (hf331-hf338) : les attachements SUPERPOWER « mis de cote » apres usage
# ----------------------------------------------------------------------------------------------------------------------------
SET_SHAW = "Sebastian Shaw"


def AttachementsDeShawMisDeCote(effect: 'Effect') -> 'List[CardFace]':
    """Les attachements du module (Energy Absorption, Energy Counterattack) qui attendent dans la zone mise de cote."""
    return [f for f in Worlds.GetSetAsideAreaCards(effect) if Attachment.IsType(f) and f.paper.set_name == SET_SHAW]


def AttacherAShawOuAuVilain() -> 'Ability':
    """« Max 1 per character. Attach to Sebastian Shaw. Otherwise, attach to the villain. »
    Modele : 04119 (`without_another_copy`). ⚠ `otherwise_attach_to=` du moteur n'applique PAS « Max 1 » (le 2e exemplaire s'attachait quand meme au
    vilain, cas `hf333`) : la branche « sinon » est donc ecrite ici (`if_cannot_operation`), avec la meme verification de copie. Aucun hote
    possible : la carte est defaussee."""
    def sinon(effect: 'Effect', joueur: 'Player') -> None:
        this = effect.this.CastTo(Attachment)
        for villain in Worlds.GetVillains(effect):
            if villain.GetInventoryDeck().FindCard(name=this.name, card_type=Attachment) is None:
                this.AttachTo2(villain, effect)
                return
        Faces.DiscardAll([this], effect)

    return AbilityFactory.AttachToFaceWhenPutIntoPlay(
        CardFinder(name=NOM_SHAW), without_another_copy=True, if_cannot_operation=sinon)
