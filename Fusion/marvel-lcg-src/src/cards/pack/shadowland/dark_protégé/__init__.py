from cards.pack.shadowland import *
from cards.pack.fne import PeutCouvrirLeCout

# ===========================================================================
# Set DARK PROTEGE (Shadowland, sl012a/b a sl027) : les six vilains tires au hasard par sl001a et leurs cartes liees.
# Le recto (A) et le verso (B) d'un vilain portent le MEME texte (le verso ajoute Steady + Toughness, lus dans `desc`, et White Tiger perd son +1 ATK) : chaque vilain est
# donc construit UNE fois ici, et `sl01Na.py` / `sl01Nb.py` l'appellent. L'etoile avant « Forced ... » est un marqueur (convention Skrull Menace / Rainy) : reponse obligatoire ordinaire.
# ===========================================================================


def JoueurVise(message: 'Message.WhenUnitWouldAttack') -> 'Player|None':
    """« When X attacks you » : le joueur dont l'IDENTITE est visee (une attaque deja dirigee vers un allie ne compte pas)."""
    joueur = message.against_player
    if joueur is None or joueur.GetIdentity() not in message.attacked_targets:
        return None
    return joueur


def JoueurDe(face: 'CardFace') -> 'Player|None':
    """Le joueur qui controle ce personnage (identite ou allie), None pour un ennemi."""
    joueur = face.GetControlBy()
    return joueur if joueur is not None and Player.IsType(joueur) else None


def LimiteParJoueurEtParRound(effect: 'Effect', joueur: 'Player', cle: str, *, consommer: bool) -> bool:
    """« (Limit once per round per player.) » sur un declencheur dont le message n'a pas de joueur cible : `LimitOncePerRoundPerPlayer` plante (assert
    `TriggerNonePlayerMessage`). Meme registre que hunting_season/trap (`LimiteParJoueurEtParRound`), mais PROPRE a ce set : la cle nomme le vilain,
    donc les deux faces (A et B) partagent la meme limite. Vrai tant qu'elle n'est pas atteinte ; `consommer` compte l'usage."""
    monde = effect.world
    registre = getattr(monde, "_limites_sl", None)
    if registre is None:
        registre = {}
        setattr(monde, "_limites_sl", registre)
    index = (cle, Worlds.GetPlayers(effect).index(joueur), monde.round_id)
    if index in registre:
        return False
    if consommer:
        registre[index] = 1
    return True


def CoutImprimeImpair(face: 'CardFace') -> bool:
    """« that card's printed cost is an odd number » : le cout IMPRIME (pas le cout paye). Une carte sans cout imprime n'est ni paire ni impaire : faux."""
    return HasCost.IsType(face) and face.has_printed_cost and face.printed_cost.val % 2 == 1


################################################################################
# VILAINS
################################################################################
def CapacitesArchpriestess() -> Sequence['Ability']:
    """[star] Forced Response : After Archpriestess attacks you, give a minion a tough status card. If no tough status card was placed this way, discard the top 3 cards of the
    encounter deck, then deal 1 minion discarded this way to yourself as a facedown encounter card.
    Cartes de reference : skrull_menace/skrull_elite_war_skrull/sk245 (`AfterUnitAttackYou`), sk151 Metallic Skin (`Faces.GiveStatus(.., "Tough")`), skrull_pantheon/sk171a (defausser du
    deck rencontre PUIS distribuer une carte defaussee : `Worlds.DiscardEncounterCards` + `DealEncounterCard`).
    ⚠ « a minion » : n'importe quel sbire en jeu, choisi par le joueur attaque, MEME s'il a deja un Tough (rien n'est alors pose : `GiveStatus` rend 0 et « if no tough status
    card was placed » joue) ; « deal 1 minion discarded this way » : le joueur choisit parmi les SBIRES defausses (pas les autres cartes) ; « to yourself » : le joueur attaque."""

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        sbires = Worlds.FindCardsOnField(effect, card_type=Minion)
        posees = 0
        if sbires:
            choisi = sbires[0] if len(sbires) == 1 else joueur.AskChooseFace(sbires, effect)
            if choisi is not None:
                posees = Faces.GiveStatus([choisi], "Tough", effect)
        if posees:
            return
        defaussees = [c for c in Worlds.DiscardEncounterCards(3, effect) if Minion.IsType(c)]
        if not defaussees:
            return
        choisi = defaussees[0] if len(defaussees) == 1 else joueur.AskChooseFace(defaussees, effect)
        if choisi is not None:
            joueur.DealEncounterCard(choisi, effect)

    return [AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "This", apres_attaque)]


def CapacitesDaredevil() -> Sequence['Ability']:
    """Forced Response : After you or an ally you control attacks Daredevil, choose: Either discard 1 random card from your hand, or Daredevil attacks you. (Limit once per round per player.)
    Cartes de reference : 24045 Shocker (`AfterUnitBeAttacked(ForcedResponse, "This", ..)` : le joueur par `message.attacker.GetControlBy()`, modele sk228), sm/community_service/27176 (choix
    « Discard 1 random card from your hand » : `DiscardRandomHandCards`), core/ultron/01145 (`DoAttackYou`) ; limite : `LimiteParJoueurEtParRound` (hunting_season).
    ⚠ « you OR AN ALLY you control » : l'identite ou un allie du joueur, jamais le sbire d'un autre ; « once per round PER PLAYER » : une fois par round pour CHAQUE joueur ;
    la branche « discard » n'est offerte que si la main n'est pas vide (un choix sans effet ne se choisit pas)."""

    def attaque_du_joueur(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        joueur = JoueurDe(message.attacker)
        return joueur is not None and LimiteParJoueurEtParRound(effect, joueur, "sl013", consommer=False)

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Villain)
        joueur = JoueurDe(message.attacker)
        if joueur is None:
            return
        LimiteParJoueurEtParRound(effect, joueur, "sl013", consommer=True)
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Discard 1 random card from your hand",
                                            lambda cibles: joueur.DiscardRandomHandCards(1, effect),
                                            condition=bool(joueur.hand_cards.Get())),
            AbilityFactory.ForChoiceAbility("Daredevil attacks you", lambda cibles: this.DoAttackYou(joueur, effect)),
        )

    return [AbilityFactory.AfterUnitBeAttacked(AbilityType.ForcedResponse, "This", apres_attaque, conditions=[attaque_du_joueur])]


def CapacitesElektra() -> Sequence['Ability']:
    """[star] Forced Interrupt : When Elektra attacks you, discard the top card of your deck. If that card's printed cost is an odd number, Elektra gets +1 ATK for this attack; otherwise,
    this attack gains overkill and piercing.
    Cartes de reference : galactic_storm/majestrixs_verdict (`JoueurVise`, `WhenUnitWouldAttack(ForcedInterrupt, "This")`), angela/an013 (`GainOverKill`), jubilee/47027 (`DiscardDeckTopCards`),
    fne/bullseye (`GainRanged`) pour la forme des gains de mots-cles sur l'attaque en cours.
    ⚠ « printed cost » : le cout IMPRIME ; deck vide (aucune carte defaussee) ou carte sans cout imprime : pas impair, donc la branche « otherwise » (overkill + piercing) ;
    « for this attack » : le +1 ATK ne vaut que pour cette attaque (`GainATKForThisAttack`)."""

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = JoueurVise(message)
        if joueur is None:
            return
        defaussees = joueur.DiscardDeckTopCards(1, effect)
        if defaussees and CoutImprimeImpair(defaussees[0]):
            message.GainATKForThisAttack(1, effect)
        else:
            message.GainOverKill(effect)
            message.GainPiercing(effect)

    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", attaque,
                                               conditions=[lambda effect, message: JoueurVise(message) is not None])]


def CapacitesGorgon() -> Sequence['Ability']:
    """[star] Forced Interrupt : When Gorgon attacks you, choose: Spend a [physical] resource. / Stun your identity. / Take 2 indirect damage.
    Cartes de reference : shadowland/shadows_in_the_night/sl004a (choix dont une branche payante : `ForChoiceAbilityWithCost` + `PeutCouvrirLeCout`), fne/bullseye (`WhenUnitWouldAttack`),
    superior_spider_man/superior_spider_man_nemesis/su016 (`TakeIndirectDamage`).
    ⚠ « Spend a [physical] resource » = UNE ressource physique (`Cost("R")`, la carte wild en vaut une) ; la branche payante n'est offerte que si elle est payable (le moteur reduit sinon
    un choix payant au plus gros morceau payable) ; « stun YOUR identity » : l'identite du joueur attaque ; « indirect » : degats sur l'identite, sans defense."""

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Villain)
        joueur = JoueurVise(message)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbilityWithCost(Cost("R"), "Spend a [physical] resource", lambda cibles, res: None,
                                                    conditions=[lambda e, m: PeutCouvrirLeCout(joueur, e, Cost("R"))]),
            AbilityFactory.ForChoiceAbility("Stun your identity", lambda cibles: Faces.GiveStatus([identite], "Stunned", effect)),
            AbilityFactory.ForChoiceAbility("Take 2 indirect damage", lambda cibles: identite.TakeIndirectDamage(this, 2, effect)),
        )

    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", attaque,
                                               conditions=[lambda effect, message: JoueurVise(message) is not None])]


def CapacitesLadyBullseye() -> Sequence['Ability']:
    """[star] Forced Response : After Lady Bullseye attacks you, if that attack was undefended, take 1 indirect damage; otherwise, place 1 threat on the main scheme.
    Cartes de reference : skrull_menace/super_skrull/sk128 (`AfterUnitAttackUnit(.., "You", is_undefended_attack=True)`), su016 (`TakeIndirectDamage`), sl004a (`PlaceThreatOnSchemes("MainScheme")`).
    ⚠ « undefended » : personne n'a defendu (un allie qui defend, meme vaincu, rend l'attaque DEFENDUE) ; « the main scheme » : le complot principal, pas une manigance annexe.
    Deux capacites (undefended / defended) : chacune n'a que sa branche, une seule part par attaque."""

    def non_defendue(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Villain)
        joueur = message.GetToPlayer()
        if joueur is not None:
            joueur.GetIdentity().TakeIndirectDamage(this, 1, effect)

    def defendue(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Unused(message)
        effect.this.CastTo(Villain).PlaceThreatOnSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", "You", non_defendue, is_undefended_attack=True),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", "You", defendue, is_undefended_attack=False),
    ]


def CapacitesWhiteTiger(plus_un_atq: bool) -> Sequence['Ability']:
    """[star] Forced Response : After White Tiger attacks you, she attacks you again [with +1 ATK]. (Limit once per round per player.) Face A : « with +1 ATK » ; face B : sans.
    Cartes de reference : luke_cage/luke_cage_nemesis/62029 (`AfterUnitAttackUnit(ForcedResponse, "This")` puis `DoAttackYou` : attaque supplementaire), hunting_season/trap
    (`LimiteParJoueurEtParRound`, la limite par joueur sur un declencheur sans joueur cible).
    ⚠ « attacks you AGAIN » : une NOUVELLE attaque (avec sa carte de boost) ; la limite est CONSOMMEE AVANT la 2e attaque (sinon elle se redeclenche a l'infini) ; « per player » : le joueur
    attaque ; la limite est partagee entre les deux faces (cle `sl017`) ; « +1 ATK » : pour cette seconde attaque seulement."""

    def joueur_attaque(message: 'Message.AfterUnitAttackEnd') -> 'Player|None':
        return message.GetAgainstPlayer()

    def possible(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> bool:
        joueur = joueur_attaque(message)
        return joueur is not None and LimiteParJoueurEtParRound(effect, joueur, "sl017", consommer=False)

    def encore(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Villain)
        joueur = joueur_attaque(message)
        if joueur is None:
            return
        LimiteParJoueurEtParRound(effect, joueur, "sl017", consommer=True)
        if plus_un_atq:
            this.DoAttackYou(joueur, effect, operation=lambda attaque: attaque.GainATKForThisAttack(1, effect))
        else:
            this.DoAttackYou(joueur, effect)

    return [AbilityFactory.AfterUnitAttackYou(AbilityType.ForcedResponse, "This", encore, conditions=[possible])]


################################################################################
# CARTES LIEES (sl018 a sl027)
################################################################################
def CapacitesArtOfTheKill() -> Sequence['Ability']:
    """Attach to your identity. Forced Interrupt : When an enemy attacks you, it gets +1 ATK for that attack. If that attack defeats a character, place 1 threat on the main scheme.
    Alter-Ego Action : Spend [energy][mental][physical] resources -> discard this card.
    Cartes de reference : skrull_menace/paibok/sk149 Hypnotized (`AttachToFaceWhenPutIntoPlay("YourIdentity")` + `PlayerActionToDiscardThis` + cout), friend.py:277 (`has_defeated_target`),
    `RunAt.AfterEnemyActivationEnd` (apres l'attaque).
    ⚠ « an enemy attacks YOU » : le porteur ; n'importe quel ennemi (vilain ou sbire), seulement quand l'attaque vise l'identite du porteur ; « defeats A character » : n'importe quel personnage
    (le sien ou un allie) ; « [energy][mental][physical] » = Y B R (trois ressources de trois types : `Cost("YBR")`) ; Alter-Ego Action : jouable en forme alter-ego seulement."""

    def porteur(effect: 'Effect') -> 'Player|None':
        cible = effect.this.CastTo(Attachment).bind_face
        return None if cible is None else JoueurDe(cible)

    def vise_le_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        joueur = porteur(effect)
        return joueur is not None and JoueurVise(message) is joueur

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        message.GainATKForThisAttack(1, effect)

        def apres() -> None:
            if message.has_defeated_target:
                this.PlaceThreatOnSchemes("MainScheme", 1, effect)

        RunAt.AfterEventEnd(effect, message, apres)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, Enemy, attaque, conditions=[vise_le_porteur]),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction).SetCost(Cost("YBR")),
    ]


def CapacitesKrahllaksBlessing() -> Sequence['Ability']:
    """Attach to the villain. Forced Interrupt : When attached villain would take any amount of damage from a character, reduce that amount by 3. Attached villain attacks that character.
    Discard this card.
    Cartes de reference : fne/the_getaway/60129a (attachement pose sur le vilain, `AttachToFaceWhenPutIntoPlay(Villain)`), `message.ReduceDamage(n, effect)`
    (`WhenUnitWouldTakeDamage`, sender_damage.py:643), `Enemy.AttackCharacter` (brique commune : un ennemi attaque un allie), `DoAttackYou` (identite).
    ⚠ « from a CHARACTER » : l'attaque ou le pouvoir d'un personnage (identite ou allie), pas un evenement ni une carte d'ameliorations ; « reduce that amount by 3 » : jamais sous 0 ;
    « attacks THAT character » : la source des degats ; si c'est l'identite d'un joueur, l'attaque vise ce joueur (`DoAttackYou`, il peut defendre) ; « discard this card » : toujours, meme si
    les degats retombent a 0 ; l'attaque a lieu APRES la reduction, dans la meme interruption."""

    def degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        vilain = this.bind_face
        source = message.source
        if source is vilain:
            return
        message.ReduceDamage(3, effect)
        Faces.DiscardAll([this], effect)
        if vilain is None or not vilain.IsInPlay() or source is None or not source.IsInPlay():
            return
        vilain = vilain.CastTo(Villain)
        joueur = JoueurDe(source)
        if Identity.IsType(source) and joueur is not None:
            vilain.DoAttackYou(joueur, effect)
        else:
            vilain.AttackCharacter(source, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "AttachedEnemy", degats, who_deal_damage="Character"),
    ]


def CapacitesArchpriestessMinion() -> Sequence['Ability']:
    """Villainous. When Revealed : Each other minion engaged with you attacks you. If no attack was made this way, discard the top 3 cards of the encounter deck.
    Cartes de reference : core/rhino/01106 Stampede (attaque a la revelation : `DoAttackYou`), `DoAttackYou(.., if_no_attack_was_made=fn)` (27029, 22031, dz023) ; Villainous = base
    automatique (`desc.Villainous`, fiche mots-cles/villainous.md).
    ⚠ « each OTHER minion » : pas elle-meme ; « engaged WITH YOU » : les sbires engages avec le joueur qui la revele (le vilain n'est pas un sbire) ; « if NO attack was made » : AUCUN sbire n'a
    attaque (aucun autre sbire, ou tous etourdis), pas « une seule attaque ratee » ; les attaques se resolvent l'une apres l'autre."""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        autres = [m for m in Worlds.FindCardsOnField(effect, card_type=Minion, engaged_with=joueur) if m is not this]
        ratees: List['CardFace'] = []
        for sbire in autres:
            sbire.CastTo(Minion).DoAttackYou(joueur, effect, if_no_attack_was_made=lambda sbire=sbire: ratees.append(sbire))
        if len(ratees) == len(autres):
            Worlds.DiscardEncounterCards(3, effect)

    return [AbilityFactory.WhenThisRevealed(None, revele)]


def CapacitesGorgonMinion() -> Sequence['Ability']:
    """Guard. Villainous. Forced Response : After a character attacks and damages Gorgon, stun that character.
    Cartes de reference : shredder/foot_goon_squad/ts202 (`AfterUnitAttackAndDamageUnit(ForcedResponse, .., target_in_play=True)`), 24045 Shocker (`GiveStatus(.., "Stunned")` sur l'attaquant) ;
    Guard et Villainous = bases automatiques (fiches guard.md, villainous.md).
    ⚠ « attacks AND DAMAGES » : une attaque absorbee (Toughness, 0 degat) ne declenche pas ; « that character » : l'attaquant (identite ou allie), pas le controleur ; Gorgon doit rester en jeu."""

    def etourdir(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        Faces.GiveStatus([message.attacker], "Stunned", effect)

    return [AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, "Character", "This", etourdir, target_in_play=True)]


def CapacitesLadyBullseyeMinion() -> Sequence['Ability']:
    """Villainous. [star] Forced Interrupt : When Lady Bullseye attacks you, this attack gains ranged and she attacks the ally with the highest printed cost you control, if able.
    Cartes de reference : galactic_storm/majestrixs_verdict (`AttaqueDetourneeVersStarjammer` : `message.ReplaceTarget(allie)`, modele officiel 50089b), fne/bullseye (`GainRanged`),
    jubilee/47027 (`Filter.One(allies, effect, highest_cost=True)`).
    ⚠ « the ally with the HIGHEST PRINTED cost » : le cout IMPRIME, ex aequo : le joueur choisit ; « you control » : un allie de CE joueur ; « if able » : sans allie, l'attaque reste sur l'identite
    (mais « gains ranged » joue quand meme) ; « this attack gains ranged » : le ranged vaut pour cette attaque, qu'elle vise l'allie ou l'identite."""

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = JoueurVise(message)
        if joueur is None:
            return
        message.GainRanged(effect)
        allies = [c for c in joueur.GetControlCharacters() if Ally.IsType(c)]
        meilleurs = Filter.All(allies, Ally, highest_cost=True) if allies else []
        if not meilleurs:
            return
        allie = meilleurs[0] if len(meilleurs) == 1 else joueur.AskChooseFace(meilleurs, effect)
        if allie is not None:
            message.ReplaceTarget(allie)

    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", attaque,
                                               conditions=[lambda effect, message: JoueurVise(message) is not None])]


def CapacitesWhiteTigerMinion() -> Sequence['Ability']:
    """Villainous. When Revealed : Take 2 indirect damage.
    Cartes de reference : superior_spider_man/superior_spider_man_nemesis/su016 (`TakeIndirectDamage(this, 2, effect)`), skrull_menace/sk245.
    ⚠ « Take 2 indirect damage » : le joueur a qui la carte est revelee, sur son identite, sans defense possible."""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is not None:
            joueur.GetIdentity().TakeIndirectDamage(effect.this, 2, effect)

    return [AbilityFactory.WhenThisRevealed(None, revele)]


def CapacitesRiteOfOffering() -> Sequence['Ability']:
    """When Defeated : The defeating player removes an ally they control from the game. If no ally was removed this way, that player takes 3 damage.
    Cartes de reference : galactic_storm/hala_ultimatum/gs151 (`WhenSchemeBeDefeated(WhenDefeated, "This", .., has_defeating_player=True)` + `GetDefeatingPlayer`), fne/purple_man/60104
    (`DealDamage([identite], 3)`), cards/pack/__init__ `RemoveThisFromGame` (`Faces.RemoveAllFromGame`).
    ⚠ « the DEFEATING player » : celui qui a vaincu la manigance, pas le premier joueur ; « an ally THEY control » : un allie de CE joueur, a son choix, obligatoire s'il en a ; « removes from the
    game » : retire de la partie (pas defausse) ; « takes 3 damage » : degats directs sur l'identite (pas indirects), seulement si AUCUN allie n'a ete retire."""

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this
        joueur = message.GetDefeatingPlayer() or effect.GetInitiator()
        if joueur is None:
            return
        allies = [c for c in joueur.GetControlCharacters() if Ally.IsType(c)]
        if allies:
            choisi = allies[0] if len(allies) == 1 else joueur.AskChooseFace(allies, effect)
            if choisi is not None:
                Faces.RemoveAllFromGame([choisi], effect)
                return
        this.DealDamage([joueur.GetIdentity()], 3, effect)

    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue, has_defeating_player=True)]


def CapacitesShadowyPlot() -> Sequence['Ability']:
    """When Defeated : The defeating player looks at the top 3 cards of the encounter deck, reveals 1 of them, and discards the rest.
    Cartes de reference : galactic_storm/hala_ultimatum/gs151 (When Defeated d'une manigance, joueur vainqueur), sm/mysterio (`encounter_deck.GetTops(n)`), sl002a (`Reveal(joueur, effect)`).
    ⚠ « looks at the TOP 3 » : les trois du dessus (moins s'il en reste moins) ; « reveals 1 of them » : le joueur CHOISIT laquelle, elle est revelee (ses When Revealed partent) ;
    « discards the rest » : les deux autres vont a la defausse rencontre."""

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        joueur = message.GetDefeatingPlayer() or effect.GetInitiator()
        if joueur is None:
            return
        haut = list(Worlds.GetEncounterDeck(effect).GetTops(3))
        if not haut:
            return
        choisie = haut[0] if len(haut) == 1 else joueur.AskChooseFace(haut, effect, peek=True)
        reste = [c for c in haut if c is not choisie]
        if reste:
            Faces.DiscardAll(reste, effect)
        if choisie is not None:
            choisie.Reveal(joueur, effect)

    return [AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue, has_defeating_player=True)]


def CapacitesDarknessWithin() -> Sequence['Ability']:
    """When Revealed : Change to hero form. The villain attacks you. --- [star] Boost : If this activation is an attack, it gains overkill.
    Cartes de reference : rainy/hulk_rainy/90102b (`identite.ChangeToForm(Hero, effect)`), sl011 (`vilain.DoAttackYou(joueur, effect)`), angela/an013 (boost : `would_atk_message.GainOverKill`).
    ⚠ « Change to hero form » : seulement si le joueur est en alter-ego (deja heros : rien) ; l'attaque a lieu APRES le changement (le joueur est alors un heros) ; Boost : l'activation en
    cours doit etre une ATTAQUE (une manigance du vilain ne gagne rien)."""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        if joueur.IsAlterEgo():
            joueur.GetIdentity().ChangeToForm(Hero, effect)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            vilain.DoAttackYou(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        attaque = getattr(message, "would_atk_message", None)
        if attaque is not None:
            attaque.GainOverKill(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]


def CapacitesEmbracedByDarkness() -> Sequence['Ability']:
    """When Revealed : The villain schemes. If 2 or less threat was placed on the main scheme this way, discard the top 3 cards of the encounter deck. --- [star] Boost : If this activation is
    an attack, place 2 threat on the main scheme.
    Cartes de reference : core/ultron/01145 et gmw/nebula/16102 (`DoSchemes(joueur, effect, ..)` : la menace posee se lit sur `AfterUnitSchemeEnd.placed_threat`), sl010 (boost), sabretooth 32069.
    ⚠ « 2 OR LESS » : 0, 1 ou 2 (donc aussi une manigance etourdie ou sans menace posee) ; « placed THIS WAY » : la menace de CETTE manigance (boost compris), pas la menace deja presente ;
    Boost : seulement si l'activation est une ATTAQUE."""

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindVillain(effect)
        if joueur is None or vilain is None:
            return
        fin = vilain.DoSchemes(joueur, effect)
        posee = fin.placed_threat if fin is not None else 0
        if posee <= 2:
            Worlds.DiscardEncounterCards(3, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if getattr(message, "would_atk_message", None) is not None:
            effect.this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
