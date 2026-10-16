from cards.pack import *
from game.buff.buff import BuffCannotBeStunned

# ===========================================================================
# Pack BEBOP & ROCKSTEADY (scenario TMNT, Inkwire), prefixe `tk`. Module plat :
# `cards.pack.bebop_rocksteady.<card_id>` (modele : pack `spot`).
#
# Le scenario a DEUX vilains en jeu en meme temps (comme Sinister Six, mais
# les deux s'activent) ; chacun a deux faces ALERT / K.O. ; chacun porte un
# attachement permanent « Temper » (Hog Wild / Rhino Rage) a deux faces
# ROWDY / ENRAGED qui porte les compteurs « knucklehead ».
# card_id : voir tools/prefixes_fanmade.json (`tk`).
# ===========================================================================

COMPTEUR = 'knucklehead'
ALERTE = "ALERT"
KO = "K.O."
# Les deux familles d'attachement Temper : Hog Wild/Headfirst (Bebop) et
# Rhino Rage/Headstrong (Rocksteady).
FAMILLES = {"Bebop": "HOG", "Rocksteady": "RHINO"}


def NomDuVilain(villain: 'CardFace') -> str:
    """« Bebop » ou « Rocksteady » (par le nom, jamais par un homonyme sbire :
    on ne regarde que les VILAINS en jeu)."""
    for nom in FAMILLES:
        if villain.IsName(nom):
            return nom
    return ""


def VilainsEnJeu(effect: 'Effect') -> List['Villain']:
    """Bebop puis Rocksteady, ceux qui sont encore en jeu."""
    vilains = [v for v in Worlds.GetVillains(effect) if NomDuVilain(v)]
    return sorted(vilains, key=lambda v: 0 if NomDuVilain(v) == "Bebop" else 1)


def VilainNomme(effect: 'Effect', nom: str) -> 'Villain|None':
    for v in VilainsEnJeu(effect):
        if NomDuVilain(v) == nom:
            return v
    return None


def AutreVilain(effect: 'Effect', villain: 'CardFace') -> 'Villain|None':
    for v in VilainsEnJeu(effect):
        if v is not villain and v.card is not villain.card:
            return v
    return None


def EstKO(villain: 'CardFace') -> bool:
    return villain.HasTrait(KO)


def EstAlerte(villain: 'CardFace') -> bool:
    return villain.HasTrait(ALERTE)


def TemperDe(villain: 'CardFace') -> 'Attachment|None':
    """L'attachement Temper (Hog Wild / Headfirst ou Rhino Rage / Headstrong)
    accroche a ce vilain, quelle que soit sa face."""
    if villain is None:
        return None
    for att in villain.GetAttachedAttachments():
        if att.HasTrait("TEMPER"):
            return att
    return None


def TousLesTempers(effect: 'Effect') -> List['Attachment']:
    res = []
    for v in VilainsEnJeu(effect):
        t = TemperDe(v)
        if t is not None:
            res.append(t)
    return res


def Compteurs(temper: 'CardFace|None') -> int:
    return temper.GetCounters(COMPTEUR) if temper is not None else 0


def MettreKO(villain: 'CardFace', effect: 'Effect') -> bool:
    """Retourne le vilain sur sa face K.O. (sans effet s'il y est deja)."""
    if EstKO(villain):
        return False
    return villain.card.Flip(effect)


def MettreAlerte(villain: 'CardFace', effect: 'Effect') -> bool:
    """Retourne le vilain sur sa face ALERT (sans effet s'il y est deja)."""
    if EstAlerte(villain):
        return False
    return villain.card.Flip(effect)


def TemperSurSaFaceRowdy(temper: 'CardFace', effect: 'Effect') -> bool:
    """Retourne l'attachement Temper sur sa face ROWDY (sans effet s'il y est)."""
    if temper.HasTrait("ROWDY"):
        return False
    return temper.card.Flip(effect)


def JoueurQuiResout(effect: 'Effect') -> 'Player':
    """Le joueur qui resout la carte : l'initiateur s'il est joueur, sinon le
    joueur courant, sinon le premier joueur."""
    ini = effect.initiator
    if isinstance(ini, Player):
        return ini
    courant = effect.world.current_player
    if isinstance(courant, Player):
        return courant
    return Worlds.GetFirstPlayer(effect)


def JoueurResponsable(by_effect: 'Effect') -> 'Player':
    """« your » / « you » sur un effet de rencontre sans joueur designe (Special de
    Headfirst, resolu par la Reponse Forcee du vilain) : le joueur qui a inflige
    les degats si c'est un joueur, sinon le premier joueur.
    Tranche par l'utilisateur le 16/10/2026 (bebop-questions.md Q1) : cette lecture."""
    ini = by_effect.initiator
    if isinstance(ini, Player):
        return ini
    return Worlds.GetFirstPlayer(by_effect)


def ResoudreSpecialDuTemper(villain: 'CardFace', joueur: 'Player', effect: 'Effect') -> None:
    """« resolve the "Special" ability on the HOG / RHINO attachment »."""
    temper = TemperDe(villain)
    if temper is not None:
        temper.ResolveSpecialAbility(joueur, effect)


def CapacitesFaceAlerte(nom: str, n: int) -> List['Ability']:
    """Face ALERT de Bebop (n = menace posee) ou de Rocksteady (n = degats au
    premier joueur). Les deux : Interruption Forcee au debut de la phase du
    mechant + Reponse Forcee « apres avoir subi des degats ».
    Choix « A ou B » : fait par le PREMIER JOUEUR, une option impossible n'est
    pas proposee (Rules Reference : on ne peut choisir ce qu'on ne peut pas
    resoudre)."""
    def debut_de_phase(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(Villain)
        premier = Worlds.GetFirstPlayer(effect)
        temper = TemperDe(this)
        if nom == "Rocksteady":
            Faces.GiveStatus([this], "Tough", effect)

        def retirer(targets):
            Faces.RemoveCountersOn([temper], 1, COMPTEUR, effect)

        if nom == "Bebop":
            def autre(targets):
                this.PlaceThreatOnSchemes("MainScheme", n, effect)
        else:
            def autre(targets):
                this.DealDamage([premier.GetIdentity()], n, effect)

        premier.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 knucklehead counter", retirer,
                condition=Compteurs(temper) > 0),
            AbilityFactory.ForChoiceAbility(
                "Place %d threat on the main scheme" % n if nom == "Bebop"
                else "Deal %d damage to the first player" % n, autre),
        )

    def apres_degats(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Villain)
        ResoudreSpecialDuTemper(this, JoueurResponsable(message.by_effect), effect)

    return [
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, debut_de_phase),
        AbilityFactory.AfterUnitTookDamage(AbilityType.ForcedResponse, "This", apres_degats),
    ]


def CapacitesFaceKO(nom: str, n: int) -> List['Ability']:
    """Face K.O. : « When X activates, remove n knucklehead counter(s) from the
    attachment instead. If there are no knucklehead counters there, flip X to his
    ALERT side. » Lecture sequentielle : on retire d'abord, puis on teste (la
    FAQ : « once there are no more counters, the villain regains consciousness »)."""
    def activation(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        ActivationKO(effect.this.CastTo(Villain), n, effect, message)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt, "This", activation,
            conditions=[lambda effect, message: not EtourdiPrioritaire(effect.this)]),
    ]


def SurLeVilain(nom: str) -> 'CardFinder':
    return CardFinder(name=nom, card_type=Villain)


def TemperEnrage(effect: 'Effect', nom: str) -> bool:
    """Le Temper de ce vilain est-il sur sa face ENRAGED (Headfirst / Headstrong) ?"""
    t = TemperDe(VilainNomme(effect, nom))
    return t is not None and t.HasTrait("ENRAGED")


def EtourdiPrioritaire(villain: 'CardFace') -> bool:
    """La carte Etourdi va REMPLACER cette activation : « Status cards always take
    priority » (FAQ de l'encart). Meme test que `status/stunned.py`
    (`trigger_has_this`) : un vilain STEADY n'est etourdi qu'a partir de 2 cartes."""
    unit = villain.card.face
    if unit.stunned <= 0:
        return False
    if unit.IsSteady() and unit.stunned < 2:
        return False
    return not unit.GetBuff(BuffCannotBeStunned)


def ActivationKO(this: 'Villain', n: int, effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
    """Activation d'un vilain K.O. : retirer n compteurs a la place, puis se
    reveiller s'il n'en reste plus. Partage entre la face K.O. et le
    declenchement de Headfirst / Headstrong."""
    message.SetBeInstead(effect)
    temper = TemperDe(this)
    reste = Compteurs(temper)
    if reste > 0:
        Faces.RemoveCountersOn([temper], min(n, reste), COMPTEUR, effect)
    if Compteurs(temper) == 0:
        MettreAlerte(this, effect)


def TempersEnrages(nom_cible: str) -> List['Ability']:
    """Headfirst / Headstrong : « When X would activate, if the other ENRAGED side
    is in play, flip Bebop and Rocksteady to their K.O. sides and flip both TEMPER
    attachments to their ROWDY sides. »"""
    autre = "Rocksteady" if nom_cible == "Bebop" else "Bebop"

    def declenche(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        for v in VilainsEnJeu(effect):
            MettreKO(v, effect)
        for t in TousLesTempers(effect):
            TemperSurSaFaceRowdy(t, effect)
        # L'activation qui a declenche le retournement est celle d'un vilain
        # desormais K.O. : tranche par l'utilisateur le 16/10/2026 (bebop-questions.md
        # Q2) : elle retire 1 jeton (2 en expert) au lieu d'attaquer.
        vilain = message.trigger.card.face.CastTo(Villain)   # la face COURANTE (K.O.)
        n = 2 if vilain.paper.card_id[:5] in ("tk002", "tk004") else 1
        ActivationKO(vilain, n, effect, message)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt, "AttachedEnemy", declenche,
            conditions=[lambda effect, message: TemperEnrage(effect, autre)
                        and not EtourdiPrioritaire(message.trigger)]),
    ]


def JoueurVainqueur(message: 'Message.WhenSchemeBeDefeated', effect: 'Effect') -> 'Player':
    """« you » d'un « When Defeated » : le joueur qui a vaincu la manigance."""
    j = getattr(message, "defeating_player", None)
    return j if j is not None else Worlds.GetFirstPlayer(effect)


def PoserCompteursSurTemper(nom: str, n: int, effect: 'Effect') -> None:
    """« Place n knucklehead counter(s) on the HOG / RHINO attachment »."""
    temper = TemperDe(VilainNomme(effect, nom))
    if temper is not None:
        Faces.PlaceCountersOn([temper], n, COMPTEUR, effect)


def Dodgy() -> 'Ability':
    """Mot-cle maison DODGY (insert Bebop & Rocksteady) : « When a character
    thwarts this side scheme, they may use their DEF instead of their THW. »
    Cousin d'`Assault` (has_assault.py), mais FACULTATIF : le joueur choisit, et
    Dodgy n'oblige pas a se servir de la DEF. Seule la manigance annexe qui le
    porte l'offre ; fiche : docs/reference/mots-cles/dodgy.md."""
    def utiliser_la_defense(effect: 'Effect', message: 'Message.WhenSchemeBeingThwart') -> None:
        unit = message.trigger
        if not HasDefense.IsType(unit):
            return
        thw = unit.thwart if HasThwart.IsType(unit) else 0
        diff = unit.defense - thw
        if diff <= 0:
            return                       # rien a gagner : on ne pose pas la question
        joueur = unit.GetControlByPlayer()
        if joueur is None:
            return
        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Use DEF instead of THW",
                lambda targets: message.GainThwartForThisThwart(diff, effect)),
        )

    return AbilityFactory.WhenUnitThwartScheme(
        AbilityType.Rule, None, utiliser_la_defense,
        which_card_be_thwart="This", is_basic_thwart=True)


def AttachSiAlerte(nom: str) -> 'Ability':
    """« Attach to Bebop if he is ALERT. Otherwise, this card gains surge. »"""
    return AbilityFactory.AttachToFaceWhenPutIntoPlay(
        CardFinder(name=nom, card_type=Villain, trait=ALERTE),
        if_cannot_gain_surge=True)


def DefausseSiLeVilainDevientKO(nom: str) -> 'Ability':
    """« Forced Response: After X flips to his K.O. side, discard this card. »"""
    def op(effect: 'Effect', message: 'Message.AfterCardFlip') -> None:
        Faces.DiscardAll([effect.this], effect)
    return Ability(
        AbilityType.ForcedResponse, Message.AfterCardFlip,
        [lambda effect, message:
            Villain.IsType(message.to_face) and NomDuVilain(message.to_face) == nom
            and message.to_face.HasTrait(KO)],
        op)


def Accessoire(nom: str, famille: str, *, steady: bool=False, compteur_a_la_revelation: bool=False,
               piercing: bool=False, overkill: bool=False) -> List['Ability']:
    """Shutter Shades / Aviator Cap / Roberta / Juniper : attachement a un vilain ALERT,
    discarde quand il passe K.O."""
    ab = [AttachSiAlerte(nom), DefausseSiLeVilainDevientKO(nom)]
    if steady:
        ab += AbilityFactory.GiveKeywordToAttached(Villain, steady=1)
    if compteur_a_la_revelation:
        def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
            PoserCompteursSurTemper(nom, 1, effect)
        ab.append(AbilityFactory.WhenThisRevealed(None, revele))
    if piercing or overkill:
        ab.append(AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name=nom, card_type=Villain), piercing=piercing, overkill=overkill))
    return ab


def BoostReveleCetteCarte() -> 'Ability':
    """« [star] Boost: Reveal this card. »"""
    return AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard)


def BumblingBuffoons() -> List['Ability']:
    """tk013-tk015 : Dodgy ; « When Defeated: Choose an enemy. That enemy attacks you.
    You may deal damage from this attack to another enemy of your choice instead. »
    « You » = le joueur qui a vaincu la manigance."""
    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = JoueurVainqueur(message, effect)
        ennemis = Worlds.GetOnFieldEnemies(effect)
        if not ennemis:
            return
        attaquant = joueur.AskChooseFace(ennemis, effect, prompt="Choose an enemy")
        if attaquant is None:
            return

        def sur_l_attaque(atk: 'Message.WhenUnitWouldAttack') -> None:
            autres = [e for e in Worlds.GetOnFieldEnemies(effect) if e is not attaquant]

            def redirige(e2: 'Effect', m2: 'Message.WhenUnitWouldTakeDamage') -> None:
                if not autres:
                    return
                def vers_un_autre(targets):
                    cible = joueur.AskChooseFace(autres, e2, prompt="Choose another enemy")
                    if cible is None:
                        return
                    m2.SetBeInstead(e2)
                    attaquant.DealDamage([cible], m2.property.damage, e2)
                joueur.MayChooseOneAbility(
                    e2, AbilityFactory.ForChoiceAbility(
                        "Deal this attack's damage to another enemy", vers_un_autre))

            effect.this.effect.RegisterTemp(
                AbilityFactory.WhenUnitWouldTakeDamage(
                    AbilityType.Temp0, joueur.GetIdentity(), redirige, is_from_attack=atk),
                unregister_after_exec=True, until_event_end=atk)

        attaquant.CastTo(Enemy).DoAttackYou(joueur, effect, operation=sur_l_attaque)

    return [
        Dodgy(),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
        BoostReveleCetteCarte(),
    ]


def LieuxAmis(effect: 'Effect') -> List['CardFace']:
    """Les cartes LOCATION en jeu cote joueurs (« a friendly LOCATION »)."""
    res = []
    for joueur in Worlds.GetPlayers(effect):
        res += [f for f in joueur.supports.Get() if f.HasTrait("LOCATION")]
    return res
