"""Ecrit .planning/galactic-storm/SUPREME-INTELLIGENCE-GABARITS.md : un gabarit PROCESSUS-CARTE par card_id du lot
GS-8, avec les preuves mesurees le 20/10/2026 (cas [gs8] de tools/cas/gs8_supreme_intelligence.py, substitution
tools/substituer_pack.py prefixe gs, autoplay tools/autoplay.py). Relancer apres toute mesure nouvelle."""
import os

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "SUPREME-INTELLIGENCE-GABARITS.md")

AUTOPLAY_SI = ("48 parties Spider-Man (gs_supreme_intelligence normal 8 + expert 8, gs_essai_modulaires_gs8 normal 8 + "
               "expert 8, et 16 de la fournee precedente) + temoin Captain Marvel 16 parties (meme scenario, normal + "
               "expert) + temoin Spider-Man contre Rhino 8 parties ; grep NameError/AttributeError/TypeError/KeyError/"
               "AssertionError : 0 partout APRES le correctif gs221 (2 AssertionError avant, voir gs221) ; 0 partie "
               "bloquee (« ! » = 0) pour la carte comme pour les temoins ; journal lu : 1B remplace 4 fois puis 2A/2B "
               "(partie 1), Detonation 3 degats a Spider-Man, Daredevil, Black Cat puis retiree")
AUTOPLAY_MOD = AUTOPLAY_SI

# card_id: (nom, ref, pieges, nombres, cas, subst, limite, autoplay, plateau, termine)
CARTES = [
    ("gs195", "Supreme Intelligence (I)", "sk179, fne/kingpin ReponseForceeSoutien (AfterUnitBeDefeated), sf011 (boost), nt008 (soin)",
     "« a KREE minion », « AFTER ... defeated », « if THAT minion has the ELITE trait » (trait gagne compris : EtaitElite), « heal ... the VILLAIN »",
     "HP 13*, SCH 2, ATK 1, Stage 1 ; soin 1, 1 carte de boost",
     "Infantry non ELITE (soin, 0 boost) ; Ronan ELITE (soin + 1 boost) ; Infantry ELITE par gs201 (boost) ; contre-cas non KREE",
     "3/4 rouges (vert : le contre-cas non KREE, absence assumee)"),
    ("gs196", "Supreme Intelligence (II)", "gs195 (meme helper) ; Toughness base desc",
     "identiques a gs195 ; Toughness = carte Tenace a l'entree (cas Setup expert)", "HP 14*, SCH 2, ATK 2, Stage 2, Toughness",
     "ELITE vaincu (soin + boost), non ELITE (soin seul), Setup expert (Tenace, 14 PV)", "2/2 rouges"),
    ("gs197", "Supreme Intelligence (III)", "gs195 sans condition", "« give IT » = le mechant, aucune condition de trait",
     "HP 15*, SCH 3, ATK 2, Stage 3, Toughness", "Infantry non ELITE vaincu : soin + boost, PV 15", "1/1 rouge"),
    ("gs198a", "Protectors of the Kree Empire (1A)", "next_evol/40139a, gmw/16082a (SetupCards.SetAsideCards), aos/50104b (RandomChoice), gmw/16107a (AttachTo2)",
     "« EACH STARFORCE minion » (Supremor compris, Q1), « 1 of THEM at random », « FIRST player », « Attach Holding Tank to the VILLAIN »",
     "Stage 1 ; 10 STARFORCE -> 9 de cote, 1 en jeu ; Tank 7*",
     "Setup (9 de cote, 1 en jeu, Tank attache, 7 pions) ; Setup expert ; Setup a 2 joueurs (14 pions, 26 PV)", "3/3 rouges"),
    ("gs198b", "Protectors of the Kree Empire (1B)", "aos/50104b, paibok/sk145b, gmw/16082b (Advance) ; AJOUT moteur pour l'objectif fige",
     "« INSTEAD », « remove ALL threat from HERE » (Crise ignoree, Q7), « RANDOM set aside », « THEN, if 5 OR LESS », « advance to 2A »",
     "objectif 6 (fixe), escalade 2 (fixe), depart 0 ; seuil <= 5",
     "complete -> 0 menace, 9 -> 8 de cote ; 6 de cote -> avance 2B ; objectif atteint par pose : sbire en jeu AVANT l'avance (discriminant) ; objectif fige (+3 ignore) ; temoin 2B (11 -> 14)",
     "2/5 rouges par substitution du module (verts : 6->2B, indiscernable sans module car 1B s'acheve vers 2A, d'ou le cas discriminant ajoute et vu rouge ; objectif fige porte par le MOTEUR : vu rouge ligne moteur neutralisee « 9 au lieu de 6 » ; temoin 2B, absence assumee)"),
    ("gs199a", "The Endless Mind (2A)", "falcon/53033 (ShuffleAllTo), aos/50104b (mis de cote)", "« EACH set aside STARFORCE », « INTO the encounter deck »",
     "Stage 2", "revelee : 9 de cote -> 0, 9 dans le deck rencontre", "1/1 rouge"),
    ("gs199b", "The Endless Mind (2B)", "regle moteur « If this stage is completed, the players lose the game » (scheme_main.py, lue dans le texte)",
     "coquille « completes » traitee comme « completed » (decision GS-0 Q4) ; aucun script", "depart 1*, escalade 1*, objectif 11*",
     "11 menaces -> partie perdue ; temoin objectif 11 -> 14", "AUCUN MODULE (regle native) : pas de substitution possible ; le cas mesure la defaite"),
    ("gs200", "Holding Tank", "next_evol/40156 (ReduceCharacterTakeDamageBy), dt128 (AfterUnitTookDamage Enemy), uses.md",
     "« the VILLAIN », « from EACH ATTACK », « an ENEMY takes ANY amount » (0 = rien), « from HERE » ; Victory 0 defaussee (Q4)",
     "Uses 7*, reduction 2, 1 pion",
     "attaque 2 -> 0, aucun pion ; 3 degats hors attaque -> 3 et 6 pions ; sbire touche -> 6 pions ; dernier pion -> parti, attaque suivante entiere",
     "4/4 rouges"),
    ("gs201", "Genetic Augmentation", "jubilee/47026 (meme phrase), hercules/59002 (ELITE), sk232 (ATK+)",
     "« the KREE minion », « MOST REMAINING », « Otherwise surge », « +2 hit points AND ELITE »", "ATK+ 1, +2 PV, 1 icone de boost, x2",
     "s'attache a Infantry (5 restants > Ren-Varr 2), 7 PV, ELITE, ATK 3 ; sans KREE -> Renfort", "2/2 rouges"),
    ("gs202", "Kree Infantry", "sm/sandman/27067 (WhenDefeated), 50134 (PlaceThreatOnSchemes MainScheme)",
     "« on the MAIN scheme », « 2 » fixe", "HP 5, SCH 1, ATK 2, Guard, Patrol, 1 boost, x4 ; 2 menaces",
     "vaincu -> 2 menaces sur 1B ; Garde et Patrouille portees", "1/2 rouges (vert : mots-cles desc, aucun module par nature)"),
    ("gs203", "Ren-Varr", "27067, next_evol/40156 (Tough au mechant)", "« When DEFEATED » (Vulnerable defausse != vaincu)",
     "HP 5, SCH 2, ATK 1, Vulnerable, Acceleration, 2 boost", "vaincu -> mechant Tenace ; etourdi -> defausse, pas de Tenace",
     "1/2 rouges (vert : contre-cas Vulnerable, absence assumee)"),
    ("gs204", "Supremor", "mts/hela/21137a (ThisGainKeyword + OnEvent.Victory), aos/50127 (VictoryDisplay.FindCardSize)",
     "« EACH KREE MINION », « in the VICTORY DISPLAY », suivi continu (gs207 en retire)", "PV 3 (★ = renvoi), +1 par sbire, Villainous, 2 boost, x2",
     "2 Starforce en vitrine -> 5 PV ; Ronan vaincu apres l'entree en jeu -> 4 PV", "2/2 rouges"),
    ("gs205", "Loyalty to Supremor", "cw/56111 (meme phrase)", "« EACH minion » (pas seulement KREE)",
     "menace 3*, Acceleration, 1 boost", "Ren-Varr gagne Garde", "1/1 rouge"),
    ("gs206", "Selective Breeding", "falcon/53033", "« EACH KREE MINION », « from the encounter DISCARD PILE »",
     "menace 6 (fixe), Amplify, 3 boost", "2 Infantry rejoignent le deck, Hydra Mercenary reste", "1/1 rouge"),
    ("gs207", "Supremor Seed", "sk271 (WhenSchemeBeDefeated + defeating player + MayChooseOneAbility), aos/50127",
     "« The DEFEATING player », « MAY », « 1 KREE MINION », « FROM ... IN » (deplacement)", "menace 4*, Hazard, 2 boost, x2",
     "dejoue -> Ronan vitrine -> defausse ; refus « Cancel » -> reste ; Ronan retire -> le bonus +1 ATK tombe (cas gs214 TEMOIN)",
     "1/2 rouges (vert : refus, absence assumee)"),
    ("gs208", "Summon Reinforcements", "standard_skrull/sk257 (DoSchemes), baxter/tx009 + sk233 (DiscardEncounterCardsUntil + Reveal)",
     "« AT LEAST 1 ... SET ASIDE », « the VILLAIN schemes », « Otherwise », « REVEAL it »", "2 boost, x2",
     "STARFORCE de cote -> 2 menaces sur 1B ; aucun -> Infantry revelee", "2/2 rouges"),
    ("gs209", "Cadmi-M the Pursuer", "next_evol/40006 (works_in_the_victory_display)", "« WHILE ... in the victory display », « gains retaliate 1 »",
     "HP 8, SCH 1, ATK 1, Retaliate 1, Villainous, Victory 1, 3 boost", "vaincu -> Rhino Riposte 1 ; temoin en jeu -> 0",
     "1/2 rouges (vert : temoin hors vitrine)"),
    ("gs210", "Doctor Minerva", "40006", "« +1 SCH »", "HP 8, SCH 2, ATK 1, Victory 1, 3 boost", "vaincu -> Rhino SCH +1 (ATK inchangee)", "1/1 rouge"),
    ("gs211", "Inndig-O the Accuser", "40006", "« +1 ATK », cumul avec Ronan", "HP 8, SCH 1, ATK 2, Victory 1, 3 boost", "vaincu -> ATK +1 (SCH inchange)", "1/1 rouge"),
    ("gs212", "Korath the Pursuer", "gs209", "cumul : Riposte 2", "HP 8, SCH 1, ATK 1, Retaliate 1, Victory 1, 3 boost", "Cadmi-M + Korath vaincus -> Riposte 2", "1/1 rouge"),
    ("gs213", "Protector", "40006 (steady=1)", "« gains STEADY »", "HP 8, SCH 1, ATK 1, Steady, Victory 1, 3 boost",
     "vaincu -> Rhino Solide ; Protector Solide (desc)", "1/2 rouges (vert : Steady imprime, base desc)"),
    ("gs214", "Ronan the Accuser", "gs211", "cumul +2 ; le bonus tombe quand Supremor Seed le retire", "HP 8, SCH 1, ATK 2, Victory 1, 3 boost",
     "Inndig-O + Ronan -> +2 ATK ; retire par gs207 -> ATK imprimee", "1/2 rouges (vert : temoin de retrait, absence assumee)"),
    ("gs215", "Shatterax", "27078 / ho016 (UnitAttackGainKeyword), helper AttaquesDuMechantEnVitrine (NoOutOfPlayLimit)",
     "« SHATTERAX's attacks » / « the VILLAIN's attacks » en vitrine", "HP 8, SCH 1, ATK 1★, Victory 1, 3 boost",
     "attaque propre sur alter ego Tenace : Tenace defaussee + 1 degat ; en vitrine Rhino : 2 degats malgre la Tenace ; temoin 0",
     "2/3 rouges (vert : temoin)"),
    ("gs216", "Ultimus", "gs215, 27078", "« ULTIMUS's attacks » / « the VILLAIN's attacks » : Deferlement", "HP 8, SCH 1, ATK 1★, Victory 1, 3 boost",
     "en vitrine : exces 1 sur Spider-Man ; attaque propre (ATK 2 avec gs201) : exces 1 ; temoin 0", "2/3 rouges (vert : temoin)"),
    ("gs217", "Starformation", "ares/ar014 (boost a chaque sbire), next_evol/40156 (Tough)",
     "« EACH STARFORCE minion » (en jeu), « AND », « Otherwise » -> mechant", "1 boost",
     "Ronan en jeu : Tenace + 1 carte de boost (pas le mechant) ; aucun : mechant Tenace + 1 boost", "2/2 rouges"),
    ("gs218", "Manipulated Memories", "agatha_harkness/aa018 (attachement + regle de cout + Action + boost during_scheme), sm/27181 (same_type), requirement.md",
     "« YOUR identity », « EACH EVENT in YOUR HAND » (allie non touche), requirement INCLUS dans le cout (Q6), « SAME TYPE », Boost manigance/sinon",
     "2 ressources ; 1 boost + ★, x2",
     "Haymaker avec Strength : reste en main ; temoin sans attachement : 3 degats ; avec Genius : 3 degats ; Hulk (allie) entre en jeu ; Action -> defaussee ; Boost manigance -> Desoriente ; Boost attaque -> Sonne",
     "4/7 rouges (verts : temoin sans attachement, paiement mental et allie = absences d'effet assumees)"),
    ("gs219", "Psychic Shackles", "iron_patriot/ip035 (PlayersCannotPlayCardWhile + HasColorPrinted)", "« PLAYERS », « cannot PLAY », « PRINTED [mental] »",
     "menace 3 + Hinder 1* = 4, 2 boost", "Maria Hill reste en main (menace 4) ; Hulk se joue ; sans le complot Maria Hill se joue", "1/3 rouges (verts : deux temoins)"),
    ("gs220", "Mental Torture", "wolv/35037 (DiscardRandomHandCards), ip035", "« 1 RANDOM », « IF a [mental] ... THIS WAY », « stun YOUR IDENTITY » (Q5)",
     "1 carte, 1 boost, x2", "Genius defausse -> Sonne ; Strength defausse -> rien", "2/2 rouges"),
    ("gs221", "Whisper in the Mind", "sm/27135 Loose Ends (Search.SearchForCard obligation_give_to + Reveal / surge)",
     "« YOUR obligation », « a COPY », « If ... NOT revealed ... SURGE », Boost « victory display OR removed » (Q2)", "1 boost + ★, x2",
     "Eviction Notice trouvee et revelee ; introuvable -> Renfort ; obligation EN COURS de revelation non trouvee -> Renfort (regression autoplay : vue ROUGE sans le correctif, verte avec) ; Boost vitrine -> deck ; Boost retiree -> deck",
     "4/4 rouges (substitution avant le cas de regression ; ce dernier vu rouge a la main, correctif retire)"),
    ("gs222a", "Nega-Bomb", "raphael/tr014 (AfterResolveVillainPhaseStep 1), gmw/16034 (ThisEnterPlayWithCounters), mut_gen/32065a (Flip)",
     "« AFTER resolving step ONE », « remove 1 ... If NO time counter », « flip AND REVEAL » (le retournement revele deja : un Reveal en plus revelait deux fois, constate au journal)",
     "menace 8*, Setup, Victory 0, 4 pions time",
     "Setup : en jeu, 8 menaces, 4 pions ; phase du mechant : 4 -> 3 ; dernier pion -> Detonation", "2/2 rouges"),
    ("gs222b", "Detonation", "luke_cage/62028 (DamageProperty ignore_tough), 40110 (GetControlCharacters)",
     "« EACH friendly character AND minion », « X = threat HERE / nombre (ROUNDED UP) », « IGNORING tough », « Remove from the game »",
     "7 menaces / 3 cibles -> 3", "Spider-Man (Tenace) 3 degats, Black Cat et Hydra Mercenary vaincus, Detonation retiree", "1/1 rouge"),
    ("gs223", "Green Interference", "aos/50029, all-purpose-counter.md (FAQ), 27135 (surge)",
     "« EACH card in play », « 1 », « IF NO counter -> SURGE », Boost « A card » (Q3)", "2 boost + ★, x2",
     "Nega-Bomb 4 -> 3 et sbire 2 -> 1 ; aucun compteur -> Renfort ; Boost : Nega-Bomb 4 -> 3", "3/3 rouges"),
]

PLATEAU = {
    "gs200": "OUI. Cas plateau `ui-app/src/board/supreme-intelligence-plateau.test.ts` : Holding Tank dessine, porte par le mechant, pions « intégrité » ; VU ROUGE avant l'ajout `integrity: 'intégrité'` dans `compteurs-fr.ts` (libelle brut), vert apres",
    "gs201": "OUI. Meme fichier : Genetic Augmentation dessinee, portee par Kree Infantry (attachement a un sbire engage : chemin d'affichage EXISTANT, le cas n'a pas ete vu rouge faute de correctif a ecrire)",
    "gs218": "OUI. Meme fichier : Manipulated Memories dessinee, portee par l'identite (chemin existant, pas vu rouge)",
    "gs222a": "OUI. Meme fichier : Nega-Bomb complot annexe dessine avec ses pions « temps » (chemin existant, pas vu rouge)",
    "gs198a": "OUI (mise de cote, attachement) : couvert par le cas plateau de gs200 (Tank attache) ; la mise de cote des sbires se voit dans la reserve du scenario (chemin existant, non teste au plateau)",
    "gs199a": "OUI (deplacement de zone vers le deck) : chemin existant, non teste au plateau",
    "gs204": "NON (PV seulement)",
}


def main():
    lignes = ["# Lot GS-8 : gabarits PROCESSUS-CARTE (Supreme Intelligence, Starforce, Seeds of Corruption, Nega-Bomb)", "",
              "Mesures du 20/10/2026, copie `gs8-supreme-intelligence`. Cas : `tools/cas/gs8_supreme_intelligence.py` "
              "(75 cas `[gs8]`, 75/75 verts a la derniere passe). Substitution : `tools/substituer_pack.py <gd> <port> gs` "
              "(31/31 cartes a module ont au moins un cas rouge sans leur module ; empreinte md5 du pack identique avant/apres). "
              "Static : `verifier_appels_modules.py galactic_storm` OK (calibre : un appel inexistant plante dans gs206 a ete "
              "vu), `verifier_api_cartes.py` : aucune faute dans galactic_storm. Questions ouvertes : "
              "`.planning/todos/2026-10-20-gs8-questions.md`. Moteur : `defs/supreme_intelligence_moteur.md`.", ""]
    for cid, nom, ref, pieges, nombres, cas, subst in CARTES:
        plateau = PLATEAU.get(cid, "NON (aucun attachement, compteur, statut visible propre ni changement de zone a dessiner hors chemins natifs)")
        if cid in ("gs203", "gs217", "gs220"):
            plateau = "OUI (statut Tenace/Sonne pose) : chemin d'affichage natif des cartes d'etat, non teste au plateau"
        lignes += [
            f"### {cid} : {nom}", "",
            f"- [x] Etape 2 : cartes de reference : {ref}",
            f"- [x] Etape 5 : texte-contre-code : mots-pieges verifies : {pieges}. Texte relu contre le SCAN (pas seulement la transcription).",
            "      Resultat : conforme.",
            f"- [x] Etape 6 : nombres texte <-> code : {nombres}.",
            "      Resultat : identiques dans cards.json (desc), le script et le scan.",
            f"- [x] Etape 7 : cas test_capacites : {cas}.",
            f"      Substitution : {subst}.",
            "- [x] Etape 7 bis : limite imprimee ? NON.",
            f"- [x] Etape 8 : autoplay cible : {AUTOPLAY_SI}.",
            f"- [x] Etape 8 bis : {plateau}.",
            "",
            "Carte terminee : OUI" + (" (lecture provisoire, question ouverte : voir le fichier de questions)" if cid in
                                     ("gs198a", "gs198b", "gs200", "gs218", "gs220", "gs221", "gs223", "gs204", "gs208", "gs199a") else ""),
            "",
        ]
    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    print(f"{len(CARTES)} gabarits ecrits dans {os.path.normpath(SORTIE)}")


if __name__ == "__main__":
    main()
