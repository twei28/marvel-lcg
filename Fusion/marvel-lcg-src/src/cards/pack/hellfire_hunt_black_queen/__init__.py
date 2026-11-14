from cards.pack import *
from cards.pack.hellfire_hunt.campaign import CampaignSetup
Unused(CampaignSetup)

# ===========================================================================
# Pack HELLFIRE HUNT - SCENARIO 3 « BLACK QUEEN » (campagne Hellfire Hunt, « MC Custom Content By: Dipsome »), 01/11/2026.
# Prefixe `hf` (tools/prefixes_fanmade.json), set 243. Module PLAT : `cards.pack.hellfire_hunt_black_queen.<card_id>`
# (modele : pack hellfire_hunt_white_queen). Tout helper appele par une carte vit ICI (NameError avale par le moteur sinon, lecon hk005).
#
# card_id : hf401-hf422 = scenario (numero du scan + 400 ; l'environnement recto-verso est hf407a / hf407b), hf361-hf366 = module DARKHOLD
# (numero du scan + 360, porte par CE pack). Le module Hellfire Conclave (hf311-hf318) est celui du pack hellfire_hunt_white_queen.
#
# LE SCENARIO EN UNE PHRASE : UN environnement recto-verso fait alterner la NUIT (« Under the Moonlight », hf407a) et le JOUR (« Beneath the Sun »,
# hf407b). Chaque face entre en jeu avec 3 compteurs « time » par joueur ; quand un personnage utilise un pouvoir de base ou qu'un ennemi
# s'active, la face visible perd un compteur ; sans compteur elle se RETOURNE et la face opposee « entre en jeu » avec ses 3 compteurs par joueur.
# Selene (le vilain, « Black Queen ») se soigne de la vie qu'elle vole. Le module Darkhold (mis de cote a la mise en place, sauf le
# Darkhold Dwarf) est melange au deck de rencontre par le stade 2A.
# ===========================================================================

NOM_SELENE = "Selene"
NOM_NUIT = "Under the Moonlight"
NOM_JOUR = "Beneath the Sun"
NOM_NUIT_ET_JOUR = (NOM_NUIT, NOM_JOUR)
NOM_ETERNAL_NIGHT = "Eternal Night"
NOM_DARKHOLD = "Darkhold"
NOM_DWARF = "Darkhold Dwarf"
NOM_BLACKHEART = "Blackheart"
NOM_MOON_GODDESS = "Immortal Moon Goddess"
ENSEMBLE_DARKHOLD = "Darkhold"
TRAIT_SORT = "SPELL OF DARKHOLD"
COMPTEUR_TEMPS = 'time'
COMPTEUR_SORT = 'darkspell'


# ----------------------------------------------------------------------------------------------------------------------------------
# Selene
# ----------------------------------------------------------------------------------------------------------------------------------
def Selene(effect: 'Effect') -> 'Villain|None':
    """Le VILAIN Selene en jeu (jamais l'allie campagne « Selene » de Enemy Of Enemy : `Worlds.GetVillains` ne rend que des vilains)."""
    for v in Worlds.GetVillains(effect):
        if v.IsName(NOM_SELENE):
            return v
    return None


def ChercheurSelene() -> 'CardFinder':
    return CardFinder(name=NOM_SELENE, card_type=Villain)


def DegatsNonExcedentairesSubis(message: 'Message.AfterUnitAttackEnd') -> int:
    """« the amount of non-excess damage characters the defending player controlled took from this attack » : la somme, sur chaque coup
    resolu de l'attaque, des degats subis par un personnage que le JOUEUR ATTAQUE controlait, moins l'exces (l'exces ne vit qu'a la
    defaite : `AfterUnitAttackUnit.excess_damage`, 0 sinon)."""
    joueur = message.GetAgainstPlayer()
    if joueur is None:
        return 0
    total = 0
    for m in message.atk_messages:
        pris = getattr(m, "taken_damage", 0)
        if pris <= 0:
            continue
        cible = getattr(m, "attacked", None)
        if cible is None or cible.GetControlByOrOwner() is not joueur:
            continue
        total += max(0, pris - getattr(m, "excess_damage", 0))
    return total


def VolDeVie() -> 'Ability':
    """Selene I, II, III : « Forced Response : After Selene attacks, heal damage from her equal to the amount of non-excess damage characters
    the defending player controlled took from this attack. » Cartes de reference : 01113-type `AfterUnitAttackEnd("This")` pour le declencheur ;
    soin = `HealHealth(n, effect)` (can_health.py)."""
    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Villain)
        n = DegatsNonExcedentairesSubis(message)
        if n > 0:
            this.HealHealth(n, effect)

    return AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "This", apres_attaque)


# ----------------------------------------------------------------------------------------------------------------------------------
# L'environnement jour / nuit
# ----------------------------------------------------------------------------------------------------------------------------------
def Temps(effect: 'Effect') -> 'Environment|None':
    """L'environnement recto-verso en jeu (face visible : Under the Moonlight ou Beneath the Sun), ou None."""
    for face in Worlds.FindCardsOnField(effect, card_type=Environment):
        if face.IsName(NOM_NUIT) or face.IsName(NOM_JOUR):
            return face
    return None


def EstLaNuit(effect: 'Effect') -> bool:
    env = Temps(effect)
    return env is not None and env.IsName(NOM_NUIT)


def EstLeJour(effect: 'Effect') -> bool:
    env = Temps(effect)
    return env is not None and env.IsName(NOM_JOUR)


def RetirerDuTemps(effect: 'Effect', env: 'CardFace|None', n: int) -> int:
    """« remove N time counter(s) from <environnement> » : rend le nombre de compteurs reellement retires (0 si Eternal Night, hf421, l'a
    empeche : c'est SA capacite `WhenCardWouldRemovedCounter`, pas un test ici)."""
    if env is None or n <= 0:
        return 0
    avant = env.GetCounters(COMPTEUR_TEMPS)
    if avant <= 0:
        return 0
    Faces.RemoveCountersOn([env], min(n, avant), COMPTEUR_TEMPS, effect)
    return avant - env.GetCounters(COMPTEUR_TEMPS) if env.IsInPlay() else min(n, avant)


def PoserDuTemps(effect: 'Effect', env: 'CardFace', n: int) -> None:
    Faces.PlaceCountersOn([env], n, COMPTEUR_TEMPS, effect)


def CompteursDepart(effect: 'Effect') -> int:
    """« enters play with 3[per_hero] time counters »."""
    return 3 * Worlds.GetPlayerNumIcon(effect)


def RemplirLeTemps(effect: 'Effect') -> None:
    """La face qui vient d'entrer en jeu (par la mise en place OU par un retournement) porte EXACTEMENT 3 compteurs par joueur : les restes de la
    face precedente (retournee de force par Eternal Night, par exemple) ne la suivent pas. Voir QUESTIONS.md n°1.
    ⚠ On AJUSTE par la difference, on ne vide jamais la carte : retirer le dernier compteur declenche « If there are no time counters here,
    flip this card » et le retournement rappellerait cette fonction a l'infini (RecursionError mesuree le 01/11/2026)."""
    env = effect.this
    voulu = CompteursDepart(effect)
    reste = env.GetCounters(COMPTEUR_TEMPS)
    if reste < voulu:
        PoserDuTemps(effect, env, voulu - reste)
    elif reste > voulu:
        Faces.RemoveCountersOn([env], reste - voulu, COMPTEUR_TEMPS, effect)


def AbilitesDuTemps(nuit: bool) -> 'List[Ability]':
    """Les abilites des DEUX faces de l'environnement jour / nuit (hf407a nuit, hf407b jour)."""
    def entree_en_jeu(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        RemplirLeTemps(effect)

    def apres_retournement(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        RemplirLeTemps(effect)

    def plus_de_temps(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        effect.this.card.Flip(effect)

    def pouvoir_de_base(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        RetirerDuTemps(effect, effect.this, 1)

    def activation_ennemie(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        RetirerDuTemps(effect, effect.this, 1)

    abilites = [
        AbilityFactory.AfterCardEnterPlay(AbilityType.NonKeyword, "This", entree_en_jeu),
        AbilityFactory.AfterCardFlipToThisSide(AbilityType.NonKeyword, apres_retournement),
        AbilityFactory.IfThereIsNoCounterHere(COMPTEUR_TEMPS, plus_de_temps),
        # « After a character uses a basic power » : un personnage AMI (identite ou allie) qui attaque, contre, defend ou recupere ;
        # les ennemis relevent de la seconde moitie de la phrase (« or an enemy activates »). Voir QUESTIONS.md n°2.
        AbilityFactory.AfterUnitUseBasicPower(AbilityType.ForcedResponse, Friend, pouvoir_de_base, powers=["ATK", "THW", "DEF", "REC"]),
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, Enemy, activation_ennemie),
    ]
    if nuit:
        def boost_en_plus(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> None:
            message.GiveAdditionalBoostCardForThisActivation(1, effect)

        def selene_s_active(effect: 'Effect', message: 'Message.WhenEnemyActivateAgainstYou') -> bool:
            return Villain.IsType(message.trigger) and message.trigger.IsName(NOM_SELENE)

        abilites.append(Ability(AbilityType.ForcedInterrupt, Message.WhenEnemyActivateAgainstYou, [selene_s_active], boost_en_plus))
    else:
        abilites += AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Identity, attack=1, thwart=1, defense=1, recover=1)
    return abilites


# ----------------------------------------------------------------------------------------------------------------------------------
# Darkhold et ses sorts
# ----------------------------------------------------------------------------------------------------------------------------------
def Darkhold(effect: 'Effect') -> 'Attachment|None':
    """Le Darkhold EN JEU (attachement), ou None."""
    for face in Worlds.FindCardsOnField(effect, name=NOM_DARKHOLD, card_type=Attachment):
        return face
    return None


def DarkholdSurLeVilain(effect: 'Effect') -> 'Attachment|None':
    """« If Darkhold is attached to the villain » : le Darkhold en jeu, attache a un vilain."""
    d = Darkhold(effect)
    if d is not None and Villain.IsType(d.bind_face):
        return d
    return None


def TrouverEtReveler(effect: 'Effect', nom: str, joueur: 'Player|None'=None) -> 'CardFace|None':
    """« find <nom> and reveal it » : deck de rencontre, defausse et zone mise de cote (« find », Rules Reference 1.8 p.19). Le melange est
    fait par `Search` (modele hf105a / hf106a du pack White Queen)."""
    joueur = joueur or Worlds.GetFirstPlayer(effect)
    face = Search.EncounterCard(effect, "FirstPlayer", include_discard_pile=True, include_set_aside=True, name=nom)
    if face is not None:
        face.Reveal(joueur, effect)
    return face


def ResolutionDeSort(sort_si_darkhold: 'Callable[[Effect, Player], None]') -> 'Ability':
    """Les quatre sorts « Spell of Darkhold » (hf363-hf366) : « When Revealed : If Darkhold is attached to the villain, <effet>, remove 1
    darkspell counter from Darkhold. Otherwise, find Darkhold and reveal it. » (hf363 : l'effet est un ATTACHEMENT a un allie.)"""
    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        livre = DarkholdSurLeVilain(effect)
        if livre is None:
            TrouverEtReveler(effect, NOM_DARKHOLD, joueur)
            return
        sort_si_darkhold(effect, joueur)
        # Le sort peut avoir change le livre (jamais en pratique) : on relit pour ne pas retirer sur une carte qui a quitte le jeu.
        if livre.IsInPlay():
            Faces.RemoveCountersOn([livre], 1, COMPTEUR_SORT, effect)

    return AbilityFactory.WhenThisRevealed(None, revele)


def CoutTempsDuJour() -> 'CostFunc.Counter':
    """« remove 1 time counter from Beneath the Sun » en COUT (hf413-hf418) : il faut que le JOUR soit la face visible et qu'il lui reste un compteur."""
    return CostFunc.Counter(CardFinder(name=NOM_JOUR, card_type=Environment), 1, COMPTEUR_TEMPS)


def MenaceSurLeComplotPrincipal(effect: 'Effect', valeur: int) -> None:
    """« place N threat on the main scheme »."""
    effect.this.PlaceThreatOnSchemes("MainScheme", valeur, effect)
