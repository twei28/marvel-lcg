#!/usr/bin/env python3
"""Genere GABARITS.md (gabarits PROCESSUS-CARTE.md, carte par carte) du pack hellfire_hunt_cassandra_nova.
Lit /tmp/.../subst.txt (preuve par substitution) et le journal d'autoplay pour les chiffres ; tout le reste est ecrit ici, a la main.
Usage : python3 generer_gabarits.py <fichier_subst> <fichier_autoplay_resume> > GABARITS.md"""
import re
import sys

SUBST = {}
for l in open(sys.argv[1], encoding="utf-8"):
    m = re.match(r"SUBST (\S+) : (.*)", l.strip())
    if m:
        SUBST[m.group(1)] = m.group(2)
AUTOPLAY = open(sys.argv[2], encoding="utf-8").read().strip()

# card_id : (nom, reference, mots-pieges, nombres, cas, limite, plateau)
C = {}
# Ce que la lecture des cas restes VERTS sans module apprend (tous les autres verts sont des temoins d'ABSENCE d'effet ou des valeurs imprimees).
NOTES_SUBST = {
    "hf381": "Les cas verts sans module : temoin non-SENTINEL, temoin sans SENTINEL (+ Victory natif), temoin menace restante, ET « la DERNIERE SENTINEL part -> manigance vaincue » (la manigance etant deja vaincue a 0 menace sans le module, le cas ne distingue pas : seule la moitie « reste en jeu » est PROUVEE par substitution ; l'autre moitie est exercee, pas prouvee).",
    "hf606b": "Le cas « complot COMPLETE -> les joueurs PERDENT » reste vert sans module : la regle du dernier stade est NATIVE (`World.AdvanceMainScheme`, « The Final Stage of the Main Scheme was Completed ») ; la capacite explicite est redondante mais fidele au texte imprime.",
    "hf602": "Le cas VICTOIRE reste vert sans module : « dernier stade du vilain vaincu = victoire » est NATIF ; hf602 est prouve par ses cas When Revealed (compteurs, PV, Steady).",
    "hf603": "Le cas VICTOIRE (expert) reste vert sans module : natif ; hf603 est prouve par ses cas When Revealed (acceleration par joueur, compteurs, Stalwart).",
    "hf607": "Verts sans module : le compteur reste apres changement de forme (propriete du moteur) et le seuil de 2 compteurs (absence d'effet).",
}


def carte(cid, nom, ref, pieges, nombres, cas, limite="NON", plateau="NON (la jauge est couverte)"):
    C[cid] = (nom, ref, pieges, nombres, cas, limite, plateau)


carte("hf601", "Cassandra Nova (I), vilain",
      "Reponse forcee apres activation CONTRE le joueur : `AfterEnemyActivatesAgainstYou`, comparable parce que sk255 reagit a l'activation d'un ennemi (attaque ou complot) ; compteur nomme sur l'identite : hg `PoserInfection` (meme geste `Faces.PlaceCountersOn([identite], ...)`).",
      "`against you` (joueur VISE, pas le joueur courant : cas 2 joueurs) ; `activates` = attaque ET complot (2 cas) ; `This` seulement (temoin sbire) ; `your identity card` = l'identite quelle que soit la forme (cas changement de forme).",
      "PV 15[per_hero] (`15*`), ATK 1, SCH 2, Stage I : cas `hf604a mise en place` (PV 15, ATK 1, MUMMUDRAI, PSIONIC).",
      "`hf601 Reponse forcee` x4 (attaque, complot, temoin sbire, deux joueurs) + `hf607 compteur sur l'identite : il reste quand le joueur change de forme`.")
carte("hf602", "Cassandra Nova (II), vilain",
      "When Revealed sur un vilain : `WhenThisRevealed(None, op)` (01096 Rhino III) ; Steady natif (`desc.Steady`) ; Reponse forcee : hf601.",
      "`each identity` (tous les joueurs, dans l'ordre : cas 2 joueurs = [1, 1]) ; Steady (cle `steady`).",
      "PV 18[per_hero], ATK 2, SCH 3, Steady : cas `hf602 When Revealed` (solo : PV 18, ATK 2 ; 2 joueurs : PV 36, steady).",
      "`hf602 When Revealed` x2 (2 joueurs, solo).")
carte("hf603", "Cassandra Nova (III), vilain (expert)",
      "hf602 + `MainScheme.PlaceAccelerationToken` (hf104b).",
      "`1[per_hero] acceleration tokens` = UN PAR JOUEUR (cas solo 1, 2 joueurs 2) ; `on the main scheme` (le complot COURANT : hf605b en expert) ; Stalwart natif.",
      "PV 20[per_hero], ATK 3, SCH 3, Stalwart : cas expert 2 joueurs (PV 40, ATK 3, Stalwart, 2 jetons, compteurs [2, 2]).",
      "`hf603 When Revealed (EXPERT)` x2 (2 joueurs, solo ; compteur de depart du stade II = 1, donc 2 apres le stade III).")
carte("hf604a", "Diplomatic Sabotage 1A (Setup + mise en place de CAMPAGNE)",
      "Retrait de sbires homonymes : hf104a ; environnement mis de cote puis en jeu : `world.aside_deck` (campaign.py) ; mise en place de campagne : `CampaignSetup(5)` (cards.pack.hellfire_hunt.campaign, modele skrull_menace).",
      "`minion named Cassandra Nova` : `Minion.IsType` (le vilain porte le meme nom) ; `In expert mode, advance to stage 2A` : porte par hf604b (voir recette) ; campagne : `WhenCampaignSetup` n'est envoye qu'en mode campagne.",
      "Menace de depart (dans hf604b), cases `Contents` / `Setup` : texte seul. Campagne : `tools/epreuves_campagnes.py` bloc hellfire (3 epreuves).",
      "`hf604a mise en place` (standard), `hf604a mise en place EXPERT`, `hf604a Setup : le sbire ... hf351 ... RETIRE` ; 3 epreuves de campagne `hellfire — ...` (victoire, defaite, expert : PV restants + pion Acceleration).")
carte("hf604b", "Diplomatic Sabotage 1B",
      "Reponse forcee de fin de tour d'un complot : sk193b ; Hero Action payee en defaussant le deck de rencontre : gb006b ; `LimitOncePerRoundPerPlayer` : 27065.",
      "`you must choose` (forced=True : pas de choix de passer) ; `take 2 damage` (directs, a l'identite) ; `once per round per player` ; `if there is Cassandra Controls counter on YOUR identity` (le joueur dont le tour finit) ; Hero Action = forme heros seulement.",
      "Cible 7[per_hero], escalade +1[per_hero], depart 1[per_hero], 1 menace, 2 degats, 5 cartes : cas (menace 1 -> 2, degats 2, 5 cartes defaussees).",
      "`hf604b Reponse forcee` x4 (menace, degats, temoin sans compteur, 2 joueurs) + `hf604b Action de heros` x3 (nominal, TEMOIN D'EPUISEMENT, sans compteur).",
      "OUI : `hf604b Action de heros : TEMOIN D'EPUISEMENT` (2 compteurs au depart, 1 seul retire apres DEUX actions du meme round, 5 cartes defaussees et pas 10)")
carte("hf605a", "Silent Takeover 2A", "Recherche du sbire nemesis : hf321 Echoes of Enmity (`Search.EncounterCard(..., is_nemesis=joueur)`).",
      "`each player` (boucle sur tous les joueurs) ; `finds` (deck + defausse + zone de cote) ; `engaged with themself`.",
      "Texte seul (aucun nombre).", "`hf605a When Revealed` x2 (Vulture nemesis de Spider-Man mis en jeu ; sans nemesis rien ne plante).")
carte("hf605b", "Silent Takeover 2B",
      "hf604b (meme squelette) ; `Player.DealEncounterCards`.", "`deal yourself 1 facedown encounter card` (a SOI, face cachee, pas revelee tout de suite : cle `distribuees`).",
      "Cible 11[per_hero], depart 2[per_hero], 2 menaces, 1 carte, 6 cartes : cas (menace 2 -> 4 ; 1 carte distribuee ; 6 cartes defaussees).",
      "`hf605b Reponse forcee` x2 (menace, carte distribuee) + `hf605b Action de heros` (6 cartes + temoin d'epuisement).", "OUI (meme cas : seconde action tolerante refusee)")
carte("hf606a", "Mutant Extermination 3A", "`Player.DealEncounterCards` (hf118).",
      "`each character they control` = identite + allies (cas 1 allie : 2 cartes ; temoin sans allie : 1).", "Texte seul.", "`hf606a When Revealed` x2.")
carte("hf606b", "Mutant Extermination 3B (dernier stade)",
      "hf604b ; gb006b (`IfThisSchemeStageIsCompletedPlayersLoseTheGame`).",
      "`When this scheme is completed` ne correspond pas a la phrase LUE par le moteur (« If this stage/scheme is completed ») : capacite posee a la main (vue rouge sans module) ; `discard 1 card from your hand` : le JOUEUR choisit ; main vide -> option retiree.",
      "Cible 13[per_hero], depart 3[per_hero], 3 menaces, 1 carte, 7 cartes : cas (menace 3 -> 6, defaite a 13, temoin 12).",
      "`hf606b Reponse forcee` x3 (menace, defausse, main vide) + `hf606b Action de heros` + `hf606b : complot COMPLETE -> les joueurs PERDENT` + TEMOIN a 12.")
carte("hf607", "Cassandra Domination (environnement)",
      "Seuil sur compteur d'identite : hg `limite_atteinte` (`AfterCounterPlacedOn(..., at_least=)`) ; choix a options dynamiques : mt011 (`ChooseAbilities` + `ForChoiceAbility(condition=)`) ; degats indirects : `Player.AssignDamage`.",
      "`at least 3` ; `remove 3` ; `each scheme` (principale ET annexes : cas 1 manigance annexe) ; `another friendly character` (jamais soi-meme ; autres identites comprises : cas 2 joueurs) ; FAQ p.22 : options impossibles retirees (5 cas : allie a 2 PV, aucun ami, deja etourdi, deja desoriente, deux exclusions).",
      "Seuil 3, retire 3, 2 menaces, 3 degats : cas (menace 1 -> 3 ; 3 degats = Jessica Jones PV 3 vaincue).",
      "`hf607 Reponse forcee` x3 branches + 5 cas FAQ + 2 joueurs + 2 cas de SEUIL (2 compteurs : rien ; 4 d'un coup : une resolution, il en reste 1) + `hf607 compteur ... forme`.",
      "NON", "OUI (carte `hf607` en jeu, libelle FR du compteur) : `ui-app/src/board/cassandra-nova-plateau.test.ts`, TEMOIN FR vu ROUGE sans l'entree `compteurs-fr.ts`")
carte("hf608", "Exploding Their Head (obligation)",
      "Obligation du joueur qui la revele (`GiveTo` vide) : 32099 ; fin de tour : `AfterPlayerTurnEnd(ForcedResponse, \"AttachedPlayer\")` ; Peril : mot-cle natif (`mots-cles/peril.md`), pose par `WhenPlayerRevealCard`.",
      "`cards you control` (alliés, ameliorations, soutiens) ; `total resource cost is at least 2` (cout imprime) ; `Take 1 damage for each card` ; `Otherwise` (QUESTIONS.md n°1) ; `Then, discard this card` ; `you revealed` (porteur de l'obligation).",
      "Cout 2, 1 degat par carte : cas (Black Cat cout 2 : 1 degat ; deux ameliorations cout 1 : 2 degats ; cout 1 seul : carte rencontre).",
      "`hf608 Obligation revelee` + `deux cartes de cout 1` + `Otherwise` + `Peril` (+ temoin sans obligation).")
carte("hf609", "Exploding Their Head (2e exemplaire)", "= hf608.", "= hf608.", "= hf608.", "`hf609 Exploding Their Head (illustration 2)`.")
carte("hf610", "Psychic Control (obligation, 1/3)",
      "32099 (Forced Response + Alter-Ego Action « Exhaust your identity -> discard this card »), hf120 (`villain.DoSchemes`).",
      "`Cassandra Nova schemes` (contre le porteur, +2 menaces en solo, + son compteur par sa propre Reponse) ; `Confuse your identity, then, discard` (ordre) ; `Alter-Ego Action` : forme alter-ego seulement (temoin heros).",
      "Boost 3 : cas `hf610 Boost 3 imprime` (1 + 3 = 4 degats).",
      "`hf610 Reponse forcee` + `Action d'alter-ego` + TEMOIN forme heros + Boost 3.")
carte("hf611", "Psychic Control (2/3)", "= hf610.", "= hf610.", "= hf610.", "`hf611 Psychic Control (illustration 2)`.")
carte("hf612", "Psychic Control (3/3)", "= hf610.", "= hf610.", "= hf610.", "`hf612 Psychic Control (illustration 3)`.")
carte("hf613", "Shatter Your Mind (traiterie, 1/3)",
      "`Worlds.DiscardEncounterCards` (WQ `DefausserEtCompterIcones`) ; `set_name` d'une carte : sp006b.",
      "`double the villain's stage number` (1, 2 ou 3) ; `each time ... is discarded` (un compteur par carte, pose un a un) ; `a Cassandra Nova card` (QUESTIONS.md n°4) ; la carte revelee va elle aussi a la defausse (+1 dans les chiffres).",
      "Boost 2 : cas (1 + 2 = 3 degats) ; 2 / 4 cartes selon le stade.", "`hf613 When Revealed` x3 (stade I : 2 cartes Nova, temoin 1 seule ; stade II : 4 cartes + Domination) + Boost 2.")
carte("hf614", "Shatter Your Mind (2/3)", "= hf613.", "= hf613.", "= hf613.", "`hf614 Shatter Your Mind (illustration 2)`.")
carte("hf615", "Shatter Your Mind (3/3)", "= hf613.", "= hf613.", "= hf613.", "`hf615 Shatter Your Mind (illustration 3)`.")
carte("hf616", "Psychic Combo (1/2)",
      "`villain.DoActivate(joueur, effect)` (27082, 27136) ; boost d'attaque : ts201 (`would_atk_message.GainPiercing`) ; `GainOverKill` (sender_damage.py).",
      "`activates against you` PUIS `You are stunned` (ordre) ; `this activation is an attack` (forme heros) / `Otherwise` (complot) ; `equals to the number of counters on YOUR identity` lu AVANT la Reponse du vilain.",
      "Boost 1 (+ etoile) : cas (3 menaces de plus que sans carte = 1 icone + 1 compteur ; overkill : 1 degat d'exces ; piercing : Black Cat Tenace est blessee).",
      "`hf616 When Revealed` x2 (complot, attaque) + Boost attaque (overkill + TEMOIN) + Boost attaque PIERCING (+ TEMOIN) + Boost complot (+ TEMOIN).")
carte("hf617", "Psychic Combo (2/2)", "= hf616.", "= hf616.", "= hf616.", "`hf617 Psychic Combo (illustration 2)`.")
carte("hf618", "Psychic Leech (1/2)",
      "`Player.DiscardAllHands` (rend le nombre), `Player.DrawUp(\"Max\")`, `CanHealth.HealHealth` (hf122).",
      "`if you cannot` JUGE CARTE PAR CARTE (cas mixte : 1 degat, 2 cartes = 1 soin + 1 compteur) ; ordre imprime : defausse, pioche, puis soins ; main vide : rien.",
      "Boost 1 ; 1 degat de soin par carte : cas (5 degats - 2 cartes = 3).", "`hf618 When Revealed` x4 (blessee, sans degat, mixte, main vide).")
carte("hf619", "Psychic Leech (2/2)", "= hf618.", "= hf618.", "= hf618.", "`hf619 Psychic Leech (illustration 2)`.")
carte("hf620", "Global Opinion Controls (manigance annexe)",
      "Texte vide : 39064 / bf023 (`GiveKeywordToInPlayWhenApplyThis(Support, treat_as_blank=True)`) ; menace a la revelation : hf125 ; boost : hf124.",
      "`each support` (de tous les joueurs ; temoin Med Team) ; `in play` (toutes les identites : cas 2 joueurs) ; `your identity card` (joueur vise) ; menace de depart 2 FIXE (pas par joueur).",
      "Menace 2, boost etoile : cas (2 + 2 compteurs = 4 ; 2 + 3 = 5 a deux joueurs ; boost : 2 + 1 = 3 declenche Domination).",
      "`hf620 When Revealed` x3 (2 compteurs, temoin 0, 2 joueurs) + `Texte des soutiens VIDE` (+ temoin) + `Boost` (+ temoin).")
carte("hf621", "The Hate Machine (manigance annexe)",
      "27106 / 27142 (`PlayersCannotAttackWhile`, `PlayersCannotThwartWhile`) ; boost : hf110 (`RevealThisCard`).",
      "`you cannot` = le heros, PAS ses allies (QUESTIONS.md n°7 ; temoin allie) ; `Cassandra Nova` seulement (temoin sbire) ; `at least 1 counter on YOUR identity` (temoin sans compteur).",
      "Menace 2, boost etoile : cas (2 + 1 compteur = 3).",
      "`hf621` x9 (menace, attaque bloquee, 3 temoins attaque, thwart bloque, 2 temoins thwart, boost revele).")
carte("hf371", "Psychic Aegis (Mind Control, attachement)",
      "16149 Power Stone (Setup + `AttachToFaceWhenPutIntoPlay(Villain)`), mt012 (`UnitCannotBeConfused`), sk147 (Cost(\"BB\") + `PlayerActionToDiscardThis`), `PlayersCannotDamageUnit`.",
      "`Setup` natif ; `attached character cannot be confused` ; `damage from a player while that player is confused` (initiateur = joueur) ; `Action` (pas Hero Action : alter-ego possible) ; [mental][mental] = `BB` (verifie sur hf110) ; Boost etoile = reveler.",
      "Setup 1, coût BB : cas (Action payee par 2 Genius).", "`hf371` x7 (mise en place, non-desorientation + temoin, degats bloques + temoin, Action, Boost).")
carte("hf372", "False Reality (Mind Control, attachement)",
      "sk147 (Hero Action BB), sk194 / `WhenSchemeWouldRemoveThreat`, ar007 (`LimitOncePerPhase`).",
      "MOTEUR additif `PreventRemoval` ; `that player` (controleur du personnage qui contre) ; `Then` : desorientation APRES ; `once per phase` (temoin d'epuisement) ; Hero Action.",
      "Prevention 2, coût BB : cas (Jessica Jones THW 2 : 3 reste 3 ; temoin sans carte : 3 -> 1).",
      "`hf372` x4 (nominal, temoin, EPUISEMENT, Action).", "OUI : `hf372 TEMOIN D'EPUISEMENT` (second retrait de la phase non empeche : 3 -> 2)")
carte("hf373", "Mind Maze (Mind Control, attachement)",
      "sk147 (`WhenUnitWouldThwart(ForcedInterrupt, \"AttachedIdentity\")`), `message.SetBeInstead`.",
      "`When YOU thwart` (l'identite, pas un allie : temoin) ; `instead` (le contre n'a pas lieu) ; `Then, you are confused` ; Action BB.",
      "Coût BB : cas.", "`hf373` x4 (remplacement, attache, temoin allie, Action).")
carte("hf374", "Illusory Attacks (Mind Control, traiterie 1/2)",
      "mt011 (`IsConfused` sur personnages amis ET ennemis).", "`each confused character in play` (amis de tous les joueurs ET ennemis) ; `You are confused` AVANT les degats.",
      "Boost 1 + etoile ; 1 degat : cas (identite 1, Black Cat 1, Hydra Bomber 1, Jessica 0).", "`hf374 Illusory Attacks` + Boost.")
carte("hf375", "Illusory Attacks (2/2)", "= hf374.", "= hf374.", "= hf374.", "`hf375 Illusory Attacks (illustration 2)`.")
carte("hf376", "Mind Shatter (Mind Control, traiterie)",
      "`Player.DiscardHandCards((0, \"All\"))`, Peril natif.", "QUESTIONS.md n°2 (main apres defausse, moitie arrondie au superieur) ; `each identity in play` (2 joueurs : [1, 1]) ; main vide : 0.",
      "Peril 1, boost 1 : cas (main de 4 -> 2 degats ; 3 -> 2 ; 0 -> 0 ; 2 joueurs -> 1 chacun).", "`hf376 Mind Shatter` x4.")
carte("hf381", "Mutant Extinction Agenda (manigance annexe)",
      "27142 (boost `PutThisIntoPlay`), `GiveKeywordToInPlayWhenApplyThis(<finder>, attack=1, scheme=1)`, `SchemeCannotLeavlPlayWhile` (defeated.py).",
      "`each SENTINEL minion` (temoin Hydra Bomber) ; `cannot be defeated while` + etat coince (QUESTIONS.md n°5) ; `Victory 1` natif (pile de victoire : cas) ; `in player order` ; boost = mettre en jeu SANS When Revealed.",
      "Menace 2[per_hero], Victory 1, boost 1 : cas (menace 2 ; Wild Sentinel ATK 3, SCH 2).",
      "`hf381` x7 (When Revealed + bonus, temoin non-SENTINEL, defaite remplacee, temoin sans SENTINEL + Victory, Boost, derniere SENTINEL partie, temoin menace restante).")
carte("hf382", "Wild Sentinel (sbire, 1/4)",
      "sl033-sl034 (`WhenUnitBeDefeated(WhenDefeated, \"This\")`), 39015b (`WhenCardWouldDiscard` + `SetBeInstead` + `MoveToBottom`).",
      "`The defeating player` (pas de joueur vainqueur = pas de choix : temoin) ; `instead of the discard pile` (jamais dans la defausse : cas negatif) ; `take 2 damage` (a l'identite du vainqueur).",
      "PV 4, ATK 2, SCH 1, boost 3 : cas `hf382 Wild Sentinel : valeurs imprimees`.", "`hf382` x4 (valeurs, 2 degats, dessous du deck, vaincue sans joueur).")
carte("hf383", "Wild Sentinel (2/4)", "= hf382.", "= hf382.", "= hf382.", "`hf383 Wild Sentinel (illustration 2)`.")
carte("hf384", "Wild Sentinel (3/4)", "= hf382.", "= hf382.", "= hf382.", "`hf384 Wild Sentinel (illustration 3)`.")
carte("hf385", "Wild Sentinel (4/4)", "= hf382.", "= hf382.", "= hf382.", "`hf385 Wild Sentinel (illustration 4)`.")
carte("hf386", "E for Extinction (traiterie ATTACK, 1/2)",
      "hf111 (`TakeIndirectDamage`), hf381 (`MettreUneSentinelle`).", "`for each SENTINEL minion in play, deal 1 indirect damage to each player` (N degats par joueur, repartis par lui) ; sans SENTINEL : cherche et met en jeu engagee.",
      "Boost 1 : cas (2 SENTINEL = 2 degats ; 0 SENTINEL = recherche).", "`hf386` x2.")
carte("hf387", "E for Extinction (2/2)", "= hf386.", "= hf386.", "= hf386.", "`hf387 E for Extinction (illustration 2)`.")
carte("hf388", "Worldwide Sentinel Deployment (manigance annexe)",
      "hf381 (`UneSentinelleParJoueur`) ; mots-cles/hazard.md (icone lue sur le scan).", "`Each player ... in player order` (2 joueurs : 2 SENTINEL) ; Hazard 1 (icone au centre, une carte penchee a croix) ; Victory 1.",
      "Menace 3[per_hero] (6 a deux joueurs), Hazard 1, Victory 1, boost 2 : cas.", "`hf388` x1 (2 joueurs).")

PLATEAU = {
    "hf371": "OUI : attachement posé sur le VILAIN : `ui-app/src/board/cassandra-nova-plateau.test.ts` (dessinée, `portePar` = Nova) + table vue dans Chromium (`captures/cassandra-nova-voiles/voile-psychic-aegis.png`). Aucun correctif nécessaire : le plateau la dessinait déjà (cas écrit après coup, pas de ROUGE à montrer).",
    "hf372": "OUI : attachement posé sur le COMPLOT PRINCIPAL : même test (`portePar` = complot) ; aucun correctif nécessaire.",
    "hf373": "OUI : attachement posé sur l'IDENTITÉ : même test (`portePar` = identité) ; aucun correctif nécessaire.",
    "hf601": "OUI : compteurs « Cassandra Controls » sur l'IDENTITÉ : même test (`compteurs.cassandra_controls`) et libellé français `compteurs-fr.ts` (« contrôle de Cassandra »), TÉMOIN vu ROUGE sans l'entrée du libellé ; badge « 2 » vu sur Peter Parker dans Chromium.",
    "hf602": "OUI : voir hf601 (compteurs posés sur chaque identité au dévoilement).",
    "hf603": "OUI : voir hf601 (compteurs + jetons d'accélération sur le complot).",
    "hf607": "OUI : environnement en jeu dès la mise en place (même test + capture Chromium `voile-cassandra-domination.png`) ; libellés des trois branches en français (`vocabulaire-moteur.test.ts`).",
    "hf608": "OUI : obligation posée dans la zone du joueur (même test, hf610 ; capture `voile-exploding.png`).",
    "hf610": "OUI : obligation posée dans la zone du joueur (même test ; capture `voile-psychic-control.png`).",
}
for _k, _v in PLATEAU.items():
    _t = list(C[_k]); _t[6] = _v; C[_k] = tuple(_t)

print("# Hellfire Hunt, scénario 5 « Cassandra Nova » (Dipsome), préfixe `hf` : gabarits PROCESSUS-CARTE\n")
print("Worktree `Marvel-LCG-campagnes`, branche `campagnes-fanmade`. Pack `hellfire_hunt_cassandra_nova` (set 245) : scénario hf601-hf621, modules Mind Control hf371-hf376 et Mutant Extinction Agenda hf381-hf388 (38 cartes).")
print("Scénarios : `hellfire_cassandra_nova` (standard : Nova I puis II) et `hellfire_cassandra_nova_expert` (Nova II puis III). Cas : `tools/cas/hellfire_cassandra_nova.py` (noms `[hf] hf6.. / hf37.. / hf38..`, vérificateur `hfn_etat`).")
print("Génération : `docs/packs/hellfire-hunt-cassandra-nova/generer_donnees.py` (données + images), `textes_fr.py` (textes français), `campagne.py` (fichier de campagne), `substitution.py` (preuve par substitution), ce fichier par `generer_gabarits.py`.")
print("Le module **Immensity** (hf351-hf358) est porté par l'agent de Torn : le scénario le référence par `hf_immensity`.\n")
print("## Ce qui est fait et ce qui reste (honnête)\n")
print("- Chaque carte : entrée `cards.json`, script, image (`assets/pics/<id>.jpg`, petit côté 615 px, q88), au moins un cas SUJET vert, preuve par substitution lue ci-dessous, texte français (`textes-fr-fanmade.ts`).")
print("- **Aucune carte n'est « terminée : OUI »** : une vraie partie jouée par un humain dans le navigateur n'a pas été faite (aucun outil ne remplace ce juge). Voir « Autoplay » pour ce que le pilote a joué.")
print("- Doutes de règle : `QUESTIONS.md` (7 entrées, choix provisoires codés).\n")
print("## Autoplay (étape 8)\n")
print(AUTOPLAY + "\n")
print("## Cartes\n")
for cid in sorted(C):
    nom, ref, pieges, nombres, cas, limite, plateau = C[cid]
    sub = SUBST.get(cid, "NON LANCEE")
    print("### %s : %s\n" % (cid, nom))
    print("- [x] Étape 2 : carte(s) de référence : %s" % ref)
    print("- [x] Étape 5 : texte-contre-code : mots-pièges vérifiés : %s\n      Résultat : conforme au scan (relu à l'écran, `assets/pics/%s.jpg`)." % (pieges, cid))
    print("- [x] Étape 6 : nombres texte ↔ code : %s\n      Résultat : conforme." % nombres)
    print("- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution : %s\n      Substitution (`docs/packs/hellfire-hunt-cassandra-nova/substitution.py`) : **%s**" % (cas, sub))
    if cid in NOTES_SUBST:
        print("      Lecture des verts : " + NOTES_SUBST[cid])
    print("- [x] Étape 7 bis : limite imprimée ? %s" % limite)
    print("- [x] Étape 8 : autoplay ciblé : voir la section « Autoplay » (parties jouées contre le scénario ; la carte n'est pas visée une par une).")
    print("- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? %s\n" % plateau)
    print("Carte terminée : NON : partie humaine à faire (test dans le navigateur) ; tout le reste est fait.\n")
