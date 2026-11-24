from . import *

# Trapped Survivor: Wolverine — MANIGANCE ANNEXE. Menace de depart 4 (fixe). Hinder 2[per_hero].
#
# Hinder 2.
# Forced Response: After step 1 of the villain phase, place 1 counter and 2[per_hero] threat here. At 3
# counters, remove this card and Wolverine from the game; each player places 1 infection counter.
# When Defeated: Remove this card from the game. The player who defeated it adds Wolverine to their
# hand from the Survivor deck.
#
# ---------------------------------------------------------------------------
# FAMILLE hg051-hg055 (« Trapped Survivor: <allie> »)
#
# Les 5 manigances annexes hg051 (Franklin Richards), hg052 (Chewie), hg053 (Valeria Richards), hg054 (Blade),
# hg055 (Wolverine) partagent EXACTEMENT la meme mecanique, seul le nom de l'allie Survivor change (meme
# `desc` : StartingThreat 4, Hinder 2*). Le raisonnement ci-dessous (mots-cles, cartes de reference,
# texte-contre-code) est donc ECRIT UNE FOIS pour les 5 ; seul le card_id de l'allie lie change d'un fichier a
# l'autre (`commun.CARD_ID_SURVIVOR_ALLY_PAR_HEROS`, deja pose par un autre travail : Franklin Richards ->
# hg072, Chewie -> hg073, Valeria Richards -> hg074, Blade -> hg075, Wolverine -> hg076).
#
# Contexte scenario (CORRIGE le 27/10/2026, lecture du livret p. 6-7) : les 5 manigances sont MELANGEES AU
# DECK DE RENCONTRE (« The Hunger Core set (13 cards, with the remaining Trapped Survivors) », etape 6 de la
# mise en place ; `data/scenarios/the_hunger_core*.json`, champ `encounters`) et entrent en jeu quand on les
# revele, comme toute manigance annexe ; seuls les 5 allies restent mis de cote (« the Survivor deck »). Le
# Trapped Survivor d'un heros joue (Wolverine, Blade) est retire du jeu au Setup
# (`commun.RetirerZombiesEtSurvivorsHomonymes`). Rien ici ne suppose COMMENT la carte entre en jeu : le code
# lit l'etat du jeu au moment du declenchement.
#
# « the Survivor deck » (texte de hg051-055 ET de hg004a) : d'apres `data/scenarios/.../set_aside` et
# `commun.py` (commentaire de `CARD_ID_SURVIVOR_ALLY_PAR_HEROS`), ce n'est PAS un Deck2 construit par le code
# (a la difference du Horde deck, `commun.HordeDeck`) : les 5 allies hg072-hg076 sont de simples cartes
# `set_aside` (zone `Worlds.GetSetAsideAreaCards`), le livret appelant cette zone « the Survivor deck » par
# ambiance plutot que par mecanique. Aucun Deck2 a construire : on cherche l'allie PAR card_id dans la zone de
# mise de cote, exactement comme le fait deja `commun.RetirerZombiesEtSurvivorsHomonymes` pour les memes
# cartes.
#
# ---------------------------------------------------------------------------
# MOTS-CLES (fiches lues avant d'ecrire)
#
# - « Hinder 2. » (texte imprime, `desc.Hinder` = "2*") : mot-cle NATIF, fiche `mots-cles/hinder.md` lue en
#   entier avant d'ecrire ce fichier. Aucun script requis : le moteur pose 2 menace PAR HEROS sur la carte
#   elle-meme a son entree en jeu (`CanHinder.ResolveHinder`, lu dans `desc`). Rien a coder ici pour cette
#   phrase.
# - « Forced Response » / « When Defeated » : types d'habilete de base du moteur (comme Response/Interrupt),
#   pas des mots-cles IMPRIMES listes dans `mots-cles/README.md` (ni Toughness/Restricted/Setup qui y figurent
#   pourtant : ce sont des mecaniques de base, ouvertes a chaque fois sans fiche dediee par des centaines de
#   cartes du depot, par ex. `04122` Hydra Prison, `ap305` The Hunt Begins). Rien a creer.
# - « place 1 counter » : PAS un mot-cle imprime nomme (a la difference de « infection counter » juste apres,
#   et au meme titre que « energy counter » sur `hg032`/`hg011`, deja juge dans ce pack comme « un NOM de
#   compteur, pas un mot-cle a fiche dediee ») : c'est le compteur generique natif `CardFace.COUNTER` valeur
#   `'counter'` (`card_face.py` ligne 310, deja utilise par `pu143` Punisher's Ordnance Cache pour un mecanisme
#   IDENTIQUE — un compteur non-nomme propre a la carte, qui s'accumule round apres round). Aucune fiche a
#   creer : pas un mot-cle imprime, un nom de compteur parmi d'autres deja presents nativement.
# - « 1 infection counter » : le compteur du SCENARIO (« Infection. When an attack from a Zombie or Metazombie
#   enemy deals damage to your hero, place 1 Infection counter », livret p.6), DEJA code et commente par
#   `commun.PoserInfection` (compteur `'infection'`, ajoute a `CardFace.COUNTER` le 27/10/2026 par un autre
#   travail de ce meme lot). Meme lecture que « energy counter » : nom de compteur de scenario, pas un mot-cle
#   imprime a fiche dediee dans `mots-cles/README.md` (cette liste ne recense que des mots-cles OFFICIELS —
#   Hinder, Boost, Teamwork... — jamais les noms de compteurs maison). Reutilise ici via `PoserInfection`, pas
#   reimplemente.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - « Hinder 2. » : lu nativement depuis `desc`, cf. `hinder.md`, carte exemple `16066` Blockade — aucun code.
# - « Forced Response: After step 1 of the villain phase, place 1 counter and X threat here » :
#   `AbilityFactory.AfterResolveVillainPhaseStep(ForcedResponse, 1, op)`, modele EXACT `07001b` Breakout (meme
#   pack que `ap005b`, qui cite aussi ce modele) — step=1, aucune garde supplementaire necessaire (l'habilete
#   n'est liee qu'a la carte EN JEU, comme toute habilete non-Setup du moteur). « place 1 counter » :
#   `Faces.PlaceCountersOn([this], 1, 'counter', effect)`, modele `pu143` (meme compteur generique, meme
#   mecanique de cumul borne par un seuil). « 2[per_hero] threat HERE » : la carte place de la menace SUR
#   ELLE-MEME, methode generique `CardFace.PlaceThreatOnSchemes` (`card_face.py:1010`, final, disponible sur
#   toute `Scheme2` donc sur cette manigance annexe) appelee avec `[this]` comme cible — accepte directement le
#   LITTERAL `"2*"` (`value: int|Literal["1*", "2*", "3*"]`) et le resout via
#   `Worlds.ConvertPerPlayerIconToInt`, EXACTEMENT le mecanisme qui lit `desc.Hinder = "2*"` par ailleurs :
#   pas besoin de multiplier a la main par `commun.NombreDeJoueurs`, le moteur le fait deja pour ce type de
#   valeur.
# - « At 3 counters, remove this card and <allie> from the game » : lecture du seuil par
#   `this.GetCounters('counter')` (modele `hg032`/`hg011`, memes lectures `GetCounters('energy')` sur ce
#   pack), puis `Faces.RemoveAllFromGame([...], effect)`, modele EXACT `commun.RetirerZombiesEtSurvivorsHomonymes`
#   (meme fabrique, memes cartes hg051-055/hg072-076 retirees du jeu de la meme facon). L'allie est retrouve
#   dans la zone de mise de cote PAR card_id, modele EXACT `commun.RetirerZombiesEtSurvivorsHomonymes`
#   (`Worlds.GetSetAsideAreaCards(effect)` + filtre `f.paper.card_id == ...`).
# - « each player places 1 infection counter » : reutilise directement `commun.PoserInfection`, bouclee sur
#   TOUS les joueurs via `Players.ForEachPlayer`, modele `hg032` (« Deal indirect damage... to each player »,
#   meme fabrique `Players.ForEachPlayer` pour une phrase qui vise explicitement « each player » et pas
#   seulement le joueur a qui la carte est revelee).
# - « When Defeated: Remove this card from the game. The player who defeated it adds <allie> to their hand
#   from the Survivor deck. » : declencheur `AbilityFactory.WhenSchemeBeDefeated(WhenDefeated, "This", op)`,
#   modele EXACT `ap305` The Hunt Begins (meme fabrique, meme lecture defensive de
#   `message.defeating_player`) ET `04122` Hydra Prison (meme sequence retrait-de-la-manigance /
#   remise-en-main d'une autre carte). « adds ... to their hand » : `Faces.AddToHand([allie], joueur, effect)`
#   (alias direct de `Faces.ReturnToHand`, meme fabrique que `04122` qui utilise `ReturnToHand(..., "Owner",
#   ...)` pour remettre en main — ici la cible n'a pas de « owner » joueur (carte de mise de cote, jamais
#   possedee), donc `AddToHand` avec le JOUEUR explicite, pas `"Owner"`). Avant l'appel, l'allie est deplace en
#   zone neutre via `Faces.MoveAllToProcessingArea`, meme etape intermediaire que `04122`
#   (`MoveAllToProcessingArea` AVANT `ReturnToHand`/`AddToHand`) pour une carte qui ne sort pas de la main d'un
#   joueur mais d'une zone de mise de cote.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « Hinder 2. » -> non code, lu nativement dans `desc.Hinder` ("2*", menace PAR HEROS a l'entree en jeu).
# « Forced Response » -> `AbilityType.ForcedResponse` (pas Interrupt : se resout APRES l'etape 1 du vilain,
#   deja le sens du message `AfterResolveVillainPhaseStep`, pas `WhenVillainPhaseStepStart`).
# « After step 1 of the villain phase » -> `step=1` passe a la fabrique, pas une autre etape.
# « place 1 counter » -> `Faces.PlaceCountersOn([this], 1, 'counter', effect)`, valeur FIXE (pas de `*`, a la
#   difference de la menace juste apres : relu au mot, aucune multiplication par le nombre de heros ici).
# « and 2[per_hero] threat HERE » -> `this.PlaceThreatOnSchemes([this], "2*", effect)`, cible = CETTE carte
#   (« here »), jamais le complot principal ni une autre manigance annexe.
# « At 3 COUNTERS » -> seuil verifie sur le compteur `'counter'` qu'on vient de poser
#   (`this.GetCounters('counter') >= 3`), jamais sur la menace ni sur un autre compteur (« infection » est un
#   compteur DIFFERENT, pose uniquement en CONSEQUENCE du seuil, pas le compteur qui DECLENCHE le seuil).
# « remove THIS CARD and <allie> from the game » -> DEUX cartes retirees ENSEMBLE dans le meme appel
#   (`Faces.RemoveAllFromGame([this, allie], effect)` quand l'allie est trouve ; `[this]` seul sinon, garde
#   defensive documentee en « A CONFIRMER » plus bas) — PAS seulement cette carte, PAS seulement l'allie.
# « each player places 1 infection counter » -> TOUS les joueurs, un compteur chacun, UNIQUEMENT quand le
#   seuil de 3 est atteint (la phrase est a l'interieur du « At 3 counters, ... » : ni avant, ni a chaque
#   declenchement du Forced Response).
# « When Defeated » -> `AbilityType.WhenDefeated`, `WhenSchemeBeDefeated("This", ...)`, distinct du Forced
#   Response ci-dessus (deux chemins de sortie du jeu differents pour cette carte : vaincue par un joueur VS
#   retiree par le seuil de compteurs — jamais les deux a la fois pour la meme occurrence).
# « Remove THIS CARD from the game » -> seule CETTE carte est retiree ici (a la difference du Forced Response
#   qui retire aussi l'allie) : l'allie, lui, ne quitte pas le jeu, il REJOINT la main d'un joueur juste apres.
# « The player WHO DEFEATED IT » -> `message.defeating_player`, jamais le premier joueur ni le joueur actif
#   par defaut (sauf garde defensive si l'information est absente, cf. « A CONFIRMER »).
# « adds <allie> to THEIR hand » -> la main du joueur qui a vaincu la manigance, jamais celle du proprietaire
#   (l'allie n'a pas de proprietaire : carte de mise de cote neutre) ni celle du premier joueur par defaut.
# « from the Survivor deck » -> l'allie est retrouve DANS LA ZONE DE MISE DE COTE (pas un deck construit, cf.
#   note de contexte ci-dessus) par son card_id exact, jamais par son nom (deux allies pourraient en theorie
#   partager un nom affiche, jamais un card_id).
#
# ---------------------------------------------------------------------------
# BLOC NOMBRES (etape 6)
#
# `desc.StartingThreat` = "4" (texte : menace de depart de la manigance, native, pas de "*" : FIXE, pas par
#   heros) ; `desc.Hinder` = "2*" (texte « Hinder 2 », native, PAR HEROS) ; « place 1 counter » = 1 (fixe,
#   code) ; « 2[per_hero] threat » = "2*" (texte, PAR HEROS, code) ; « At 3 counters » = 3 (texte, code) ;
#   « 1 infection counter » = 1, par joueur (texte, code). Toutes les valeurs numeriques du texte imprime sont
#   reprises a l'identique dans `data/cards_custom.json` (desc) et dans ce script : aucun ecart.
#
# ---------------------------------------------------------------------------
# A CONFIRMER (commun aux 5 cartes hg051-hg055, pose UNE fois dans ce fichier — voir le rapport de fin de
# travail pour ne pas le repeter sur les 4 autres)
#
# - `message.defeating_player` absent (improbable pour une manigance annexe vaincue par un joueur, mais la
#   signature de la fabrique le permet) : garde defensive -> premier joueur, modele EXACT `ap305` (« si not
#   Player.IsType(joueur), joueur = Worlds.GetFirstPlayer(effect) »). Aucune regle imprimee ne couvre ce cas ;
#   jamais rencontre en pratique (une defaite de manigance annexe est toujours causee par un thwart de
#   joueur).
# - Allie introuvable dans la zone de mise de cote au moment du declenchement (deja retire par
#   `commun.RetirerZombiesEtSurvivorsHomonymes` si le heros homonyme est en jeu, deja retire par le Forced
#   Response de CETTE carte si le seuil de 3 a deja ete atteint une fois — ne devrait jamais arriver deux fois
#   pour la meme carte puisqu'elle quitte alors le jeu, ou un bug amont) : garde defensive -> AUCUN effet pour
#   la partie « ajoute l'allie » (la manigance est quand meme retiree du jeu dans le cas Forced Response /
#   When Defeated, seule l'addition en main est sautee), meme lecture « sujet absent -> rien ne se passe pour
#   ce sujet » que `hg023`/`hg032` dans ce meme pack.
# - Qui met hg051-055 EN JEU pendant la partie (aucune carte scriptee a ce jour ne le fait, cf. note de
#   contexte) : hors perimetre de cette carte, qui se contente de reagir UNE FOIS en jeu — a verifier quand la
#   manigance principale 2A/2B (hg005a/hg005b) ou le Coeur stade II/III (hg002/hg003) seront scriptes.


def GetAbilities() -> Sequence['Ability']:

    ALLIE_CARD_ID = "hg076"  # Wolverine (commun.CARD_ID_SURVIVOR_ALLY_PAR_HEROS["Wolverine"])

    def _AllieEnMiseDeCote(effect: 'Effect') -> 'CardFace|None':
        return next(
            (f for f in Worlds.GetSetAsideAreaCards(effect) if f.paper.card_id == ALLIE_CARD_ID),
            None,
        )

    def forced_response(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)

        Faces.PlaceCountersOn([this], 1, 'counter', effect)
        this.PlaceThreatOnSchemes([this], "2*", effect)

        if this.GetCounters('counter') >= 3:
            allie = _AllieEnMiseDeCote(effect)
            a_retirer: List['CardFace'] = [this] if allie is None else [this, allie]
            Faces.RemoveAllFromGame(a_retirer, effect)

            def infection(joueur: 'Player') -> None:
                PoserInfection(effect, joueur)

            Players.ForEachPlayer(effect, infection)

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        joueur = getattr(message, "defeating_player", None)
        if not Player.IsType(joueur):
            # A CONFIRMER (voir bloc en tete de fichier) : aucune regle imprimee ne couvre ce cas, jamais
            # rencontre en pratique pour une manigance annexe vaincue par un thwart.
            joueur = Worlds.GetFirstPlayer(effect)

        Faces.RemoveAllFromGame([this], effect)

        allie = _AllieEnMiseDeCote(effect)
        if allie is not None:
            Faces.MoveAllToProcessingArea([allie], effect)
            Faces.AddToHand([allie], joueur, effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            forced_response,
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            when_defeated,
        ),
    ]
