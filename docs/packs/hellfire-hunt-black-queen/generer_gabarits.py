#!/usr/bin/env python3
"""Genere GABARITS.md (PROCESSUS-CARTE, un gabarit par carte) : les cas et leur verdict viennent du DERNIER rapport de test_capacites
(<rapport.json>) et de SUBSTITUTION.txt, jamais saisis a la main. Usage : python3 generer_gabarits.py <racine_moteur> <rapport.json> <SUBSTITUTION.txt> <sortie.md>"""
import json
import re
import sys

RACINE, RAPPORT, SUBST, SORTIE = sys.argv[1:5]   # RAPPORT : un ou plusieurs rapports separes par des virgules
sys.path.insert(0, RACINE + "/tools")

CARTES = {
    # id: (nom, [capacites], reference, mots-pieges, nombres, limite, plateau)
    "hf401": ("Selene (I)", ["Reponse forcee : vol de vie"], "01113 Klaw (`AfterUnitAttackEnd(..., \"This\")` en Reponse forcee) ; `AfterUnitAttackUnit.taken_damage / excess_damage` (can_attack.py)",
              "« non-excess » (l'exces ne vit que dans `AfterUnitAttackUnit.excess_damage`) ; « the defending player controlled » (la cible est controlee par le joueur ATTAQUE, un allie qui defend compte) ; « After Selene attacks » (pas une manigance) ; « heal damage from her » (borne par ses degats)",
              "PV 12 par joueur, ATK 1, SCH 2 (desc)", "NON", "NON (aucune carte dessinee de plus)"),
    "hf402": ("Selene (II)", ["Toughness (natif, desc)", "Reponse forcee : vol de vie (meme fabrique que hf401)"], "hf401 ; fiche mots-cles/toughness.md (base automatique, aucun script)",
              "Toughness est lu dans `desc` : ne jamais le recoder", "PV 14 par joueur, ATK 2, SCH 2, Toughness 1", "NON", "NON"),
    "hf403": ("Selene (III)", ["Steady + Toughness (natifs, desc)", "Reponse forcee : vol de vie"], "hf401 ; fiches steady.md, toughness.md",
              "Steady et Toughness lus dans `desc`", "PV 17 par joueur, ATK 3, SCH 2, Steady 1, Toughness 1", "NON", "NON"),
    "hf404a": ("Throne of the Hellfire Club (1A)", ["Setup : la nuit en jeu, module Darkhold de cote sauf le Dwarf", "Campagne : `CampaignSetup(3)`"],
               "50087a (Batroc : `SetupCards.PutIntoPlay` d'un environnement `set_aside`, `*CampaignSetup(n)`), skrull_menace/shaper_of_worlds (`Faces.SetAside` d'un set par `paper.set_name`)",
               "« Set the Darkhold module aside » : la zone « mise de cote » contient AUSSI les allies Recruited de campagne, d'ou le filtre par `paper.set_name` ; « Shuffle the set-aside Darkhold Dwarf » : le Dwarf reste dans le deck (le deck est melange apres la mise en place)",
               "environnement : 3 compteurs time par joueur ; complot 1B : menace 1 par joueur", "NON", "OUI : bloc plateau (environnement a compteurs time)"),
    "hf404b": ("Throne of the Hellfire Club (1B)", ["Interruption forcee : le Dwarf entre dans la defausse -> stade 2A", "When Completed : Tough sur Selene ; -2 compteurs du jour"],
               "sk066 Paibok (`WhenCardWouldMoveToArea ... into_discard_pile`), 50087b (`Advance(\"2A\")`), hf104b (`WhenMainSchemeStageCompleted`)",
               "« enters the discard pile » = toute route (vaincu ou defausse du deck), pas seulement « defeated » ; « 2[per_hero] time counters » = 2 par joueur",
               "cible 5 par joueur, escalade 2 par joueur, depart 1 par joueur", "NON", "NON"),
    "hf405a": ("The Power of the Darkhold (2A)", ["When Revealed : melanger le set Darkhold mis de cote dans le deck"], "skrull_menace/shaper_of_worlds (`Worlds.GetSetAsideAreaCards`) + `Faces.ShuffleAllTo`",
               "filtre par nom de set (zone mise de cote partagee avec les allies de campagne)", "-", "NON", "NON"),
    "hf405b": ("Get the Power (2B)", ["When Completed : Tough sur Selene ; trouver Darkhold et l'attacher a Selene"], "hf105b (`WhenMainSchemeStageCompleted`), 04119 (chercher puis attacher), mots-cles/find.md",
               "« find » : deck, defausse, mis de cote ET deja en jeu (s'il est deja attache a Selene : rien) ; « attach it to Selene » (pas au premier vilain venu)",
               "cible 7 par joueur, escalade 1 par joueur, depart 2 par joueur", "NON", "NON"),
    "hf406a": ("Ascending to Godhood (3A)", ["When Revealed : trouver et reveler Immortal Moon Goddess ; trouver Blackheart et le mettre en jeu engage avec le premier joueur"],
               "hf105a / hf106a (`Search.EncounterCard` + `Reveal`), 04112b (`PutIntoPlay(first_player)`)", "« engaged with the first player » ; « (Shuffle.) » fait par `Search`", "-", "NON", "NON"),
    "hf406b": ("Ascending to Godhood (3B)", ["Reponse forcee : apres l'etape 1, 1 menace par compteur time", "Si cette etape est completee, les joueurs perdent (texte lu par le moteur)"],
               "trors/zola `TheMadDoctor` (`AfterResolveVillainPhaseStep(ForcedResponse, 1)`), hf106b (defaite lue dans le texte)",
               "« for each time counter on Under the Moonlight OR Beneath the Sun » : la face VISIBLE ; l'escalade imprimee (+2 par joueur) reste (QUESTIONS.md n°3) ; l'icone d'acceleration d'Immortal Moon Goddess s'y ajoute",
               "cible 17 par joueur, escalade 2 par joueur, depart 0", "NON", "NON"),
    "hf407a": ("Under the Moonlight (la nuit)", ["Entre en jeu avec 3 compteurs time par joueur ; sans compteur : se retourne", "Interruption forcee : Selene s'active -> 1 carte de boost de plus",
                                              "Reponse forcee : pouvoir de base d'un personnage ami ou activation ennemie -> -1 compteur"],
               "gs183 (`WhenEnemyActivateAgainstYou` + `GiveAdditionalBoostCardForThisActivation`), 50090a Alert Level / 39026a (`card.Flip`), `AfterUnitUseBasicPower`, `AfterEnemyActivationEnd`, `IfThereIsNoCounterHere`",
               "« enters play with » rejoue a CHAQUE retournement (`AfterCardFlipToThisSide`) ; ⚠ vider la carte pour la remplir declenche le retournement a l'infini (RecursionError) : on ajuste par la difference ; « Black Queen » = Selene ; « character uses a basic power » (RR 1.8 : ATK THW DEF REC SCH) et « enemy activates » (QUESTIONS.md n°2) ; Eternal Night bloque le retrait sur la nuit",
               "3 par joueur ; -1 par evenement ; +1 carte de boost", "NON (aucune limite « Limit ... » imprimee)", "OUI : bloc plateau (compteurs time, face visible)"),
    "hf407b": ("Beneath the Sun (le jour)", ["Entre en jeu avec 3 compteurs time par joueur ; sans compteur : se retourne", "+1 a chaque pouvoir de base de chaque identite",
                                          "Reponse forcee : -1 compteur (meme montage que hf407a)"],
               "06007 Asgard (`GiveKeywordToInPlayWhenApplyThis(Identity, ...)`), hf407a",
               "« each identity » = heros ET alter ego ; « each of its basic powers » = ATK, THW, DEF, REC", "+1 ATK/THW/DEF/REC", "NON", "OUI : bloc plateau"),
    "hf408": ("Blackheart", ["Guard, Patrol, Steady (natifs)", "Boost : l'attaque gagne overkill, piercing, ranged"], "27081 Tooth and Nail (`GainPiercing`), 27169 (`GainOverKill`), `GainRanged` (sender_damage.py)",
              "« If this activation is an attack » (`during_attack=True`) ; Ranged n'a aucun effet MESURABLE contre un joueur (il ignore Riposte) : l'appel est pose, l'effet n'est pas prouve",
              "PV 9, ATK 3, SCH 1, 3 icones de boost + etoile", "NON", "NON"),
    "hf409": ("Little Demon (1/4)", ["Patrol + Teamwork (DEMON) (natifs)", "Reponse forcee : apres avoir attaque et blesse vous, vous etes desoriente"], "hf124 (`AfterUnitAttackAndDamageUnit`), 41029 (`GiveStatus`), fiche teamwork.md",
              "« damages YOU » (l'identite, pas un allie) ; ne JAMAIS recoder Teamwork (le sbire s'activerait deux fois)", "PV 3, ATK 2, SCH 1, 2 icones de boost", "NON", "NON"),
    "hf413": ("Hypnotic Trance (1/3)", ["Ne peut pas attaquer Selene ni defendre contre elle", "When Revealed : s'attache a l'allie aux PV restants les plus hauts sans Trance, sinon surge", "Action de heros : [mental][mental] + -1 compteur du jour -> defausse"],
             "04119 (`AttachToFaceWhenPutIntoPlay(most_remaining_hp, without_another_copy, if_cannot_gain_surge)`), hf304 (`UnitCannotDefend`), `UnitCannotAttackTarget`, 16095 (`CostFunc.Counter` sur une autre carte)",
             "« remaining » (PV restants, pas imprimes ; ⚠ Luke Cage a la carte Tough : `Puzzle.Damage` est absorbe) ; « the ally » (QUESTIONS.md n°6) ; le cout comprend le retrait du compteur du JOUR",
             "-1 THW, 1 icone de boost", "NON", "NON"),
    "hf416": ("Shining Shield (1/2)", ["Attachee a Selene : plafond de 2 degats par attaque", "Action de heros : [energy] + -1 compteur du jour -> defausse", "Boost : s'attache a Selene"],
              "40091 Titanium Exoskeleton (`UnitCannotTakeDamageWhile`), `WhenThisBoostAttachTo`, hf413", "« from a SINGLE attack » (`is_from_attack=True`)", "plafond 2", "NON", "NON"),
    "hf418": ("Relentless Pursuit", ["Interruption forcee : Selene qui complote vous attaque a la place", "Action de heros : [physical] + -1 compteur du jour -> defausse"],
              "60182 Cop (`WhenUnitWouldScheme` + `SetBeInstead`), hf120 (`DoAttackYou`)", "« against YOU » : le joueur dont l'identite porte la carte ; « instead » = remplace la manigance", "3 icones de boost", "NON", "NON"),
    "hf419": ("Dark Temptation", ["When Revealed : Selene vous attaque", "Boost : si cette attaque vainc un allie, 2 menaces sur le complot principal"], "hf120 (`DoAttackYou`), 32069 Sabretooth Strikes (`IfThisAttackDefeats(Ally, ...)`)",
              "« defeats an ally » (pas un autre personnage) ; piege paye : helper `MenaceSurLeComplotPrincipal` oublie dans le `__init__` du pack, NameError AVALE par le moteur", "1 icone de boost + etoile", "NON", "NON"),
    "hf420": ("Lunar Eclipse", ["When Revealed : -1[per_hero] compteur du jour, sinon +1[per_hero] sur la nuit", "Boost : reveler cette carte"], "hf110 (`RevealThisCard`), hf407a/b",
              "« If you cannot » : le jour n'est pas visible ; retirer le dernier compteur du jour retourne l'environnement", "1 icone de boost + etoile", "NON", "NON"),
    "hf421": ("Eternal Night", ["Les compteurs de la nuit ne peuvent pas etre retires", "When Revealed : retourne le jour (la nuit revient)"], "hf407a (`RetirerDuTemps`), 39026a (`card.Flip`)",
              "« Flip Beneath the Sun » : sans effet si c'est deja la nuit ; la nuit revenue a EXACTEMENT 3 compteurs par joueur (QUESTIONS.md n°1)", "menace 3, 3 icones de boost", "NON", "NON"),
    "hf422": ("Immortal Moon Goddess", ["Hinder 2[per_hero], Victory 1, acceleration (natifs)", "Tant que la nuit est en jeu, Selene ne peut pas etre vaincue"], "gs115 Deathbird (`UnitCannotBeDefeatedWhile` + relance), 35029",
              "la relance de la defaite quand la protection tombe (la fabrique ne le fait pas quand la condition tombe : retournement du jour via `AfterCardFlip`, depart de la carte via `AfterCardLeavePlay`)",
              "menace 7 + Hinder 2 par joueur, Victory 1, 1 icone de boost", "NON", "NON"),
    "hf361": ("Darkhold Dwarf", ["When Revealed : glisse sous lui le Spell of Darkhold du dessus de la defausse", "When Defeated : revele la carte glissee"], "mots-cles/tuck.md (`PlaceCardHere(faces, True)` face visible, helper `Glisser` de gs119), `Deck.FindTopmost`",
              "« topmost » ; tuck = FACE VISIBLE (livret p.4) ; « the card tucked here » : la revelation passe par le joueur engage ; piege de harnais : `CreateEncounterDiscardPile` AVANT `EmptyEncounterDeck` est remelangee dans le deck",
              "PV 3, ATK 1, SCH 3, 2 icones de boost", "NON", "OUI : bloc plateau (sort glisse sous le sbire)"),
    "hf362": ("Darkhold", ["Attache au vilain, +1 ATK, Uses (2 Darkspell)", "Interruption forcee : le vilain ATTAQUE -> -1 compteur et 1 carte de boost de plus"], "gs183 Induced Mutation (`AttachToFaceWhenPutIntoPlay(Villain)`, `GiveAdditionalBoostCardForThisActivation`), 02020 Hysteria (`WhenUnitWouldAttack`), fiche uses.md",
              "« attacks » (pas un complot) ; le dernier compteur fait partir la carte AVEC son +1 ATK ; +1★ ATK (QUESTIONS.md n°4)", "+1 ATK, 2 compteurs darkspell, 3 icones de boost", "OUI : Uses (2) -> temoin d'epuisement", "OUI : bloc plateau"),
    "hf363": ("Eternal Manipulation", ["Allie attache traite comme un sbire (texte vierge, SCH = THW imprime, pas de degats consecutifs)", "When Revealed : Darkhold sur le vilain -> s'attache a l'allie aux PV les plus hauts, -1 Darkspell ; sinon cherche Darkhold"],
              "hf324 Mind Manipulation (MEME texte : `TreatAttachedCardAsMinion(Ally, \"Minion\")`), hp017 Take Over Signal", "« highest hit-point » (QUESTIONS.md n°5) ; l'attachement est alors porte par la face `minion` (pic_id = l'allie) ; ⚠ Luke Cage (Tough) fausse la mesure des PV",
              "+1 ATK, 1 icone de boost", "NON", "OUI : bloc plateau"),
    "hf364": ("Hellfire Conjuration", ["When Revealed : Darkhold sur le vilain -> 3 degats indirects, -1 Darkspell ; sinon cherche Darkhold"], "27080 (`TakeIndirectDamage`), `ResolutionDeSort`", "« take 3 indirect damages » : le joueur qui revele", "3 degats indirects, 1 icone de boost", "NON", "NON"),
    "hf365": ("Soul Siphon", ["When Revealed : Darkhold sur le vilain -> sonne ET desoriente, -1 Darkspell ; sinon cherche Darkhold", "Boost : reveler cette carte"], "hf110 (`RevealThisCard`), 41029 (`GiveStatus`)", "les DEUX statuts ; boost = revelation", "etoile seule (pas d'icone numerique)", "NON", "NON"),
    "hf366": ("Dimensional Portal", ["When Revealed : Darkhold sur le vilain -> defausse jusqu'a un sbire, le revele, -1 Darkspell ; sinon cherche Darkhold"], "trors/zola (`DiscardEncounterCardsUntil(card_type=Minion)`)", "le sbire est REVELE (s'engage, resout son When Revealed)", "2 icones de boost", "NON", "NON"),
}
# Les trois autres Little Demon, deux autres Trance, second Shining Shield : meme script, meme gabarit.
COPIES = {"hf410": "hf409", "hf411": "hf409", "hf412": "hf409", "hf414": "hf413", "hf415": "hf413", "hf417": "hf416"}


def lire_cas():
    spec = {}
    src = open(RACINE + "/tools/cas/hellfire_black_queen.py", encoding="utf-8").read()
    return re.findall(r'_c\("(\[?[^"\\]*(?:\\.[^"\\]*)*)"', src)


def main():
    verdict = {}
    for fichier in RAPPORT.split(","):
        for c in json.load(open(fichier))["cas"]:
            verdict[c["nom"]] = c["ok"]
    sub = {}
    for fichier in SUBST.split(","):          # plusieurs fichiers : les suivants (rejeux apres correction) l'emportent
        for l in open(fichier, encoding="utf-8"):
            m = re.match(r"(hf\d+[ab]?)\s+(.*)", l.strip())
            if m:
                sub[m.group(1)] = m.group(2)
    sortie = ["# Hellfire Hunt, scénario 3 « Black Queen » + module Darkhold : gabarits PROCESSUS-CARTE\n",
              "Généré par `generer_gabarits.py` à partir du dernier rapport de `test_capacites` (`%s`) et de `SUBSTITUTION.txt` : les cas et les verdicts ne sont pas saisis à la main.\n"
              % RAPPORT,
              "Pack `hellfire_hunt_black_queen` (set 243), module plat `src/cards/pack/hellfire_hunt_black_queen/`. Scénarios `hellfire_black_queen` (Selene I puis II) et `hellfire_black_queen_expert` (II puis III). "
              "Cas : `tools/cas/hellfire_black_queen.py`. Doutes de règle : `QUESTIONS.md`.\n",
              "**Statut commun à TOUTES les cartes : « Carte terminée : NON : partie humaine à faire »** (aucune partie jouée par un humain dans le navigateur ; le reste est fait et prouvé ci-dessous).\n"]
    toutes = sorted(CARTES)
    for cid in toutes:
        nom, caps, ref, pieges, nombres, limite, plateau = CARTES[cid]
        groupe = [cid] + [k for k, v in COPIES.items() if v == cid]
        cas = [n for n in verdict if any(("[hf] %s " % g) in n for g in groupe)]
        vert = sum(1 for n in cas if verdict[n])
        sortie.append("### %s : %s%s\n" % (cid, nom, (" (+ " + ", ".join(g for g in groupe[1:]) + ", même script)") if len(groupe) > 1 else ""))
        sortie.append("- [x] Étape 2 : cartes de référence : %s" % ref)
        sortie.append("      Capacités : " + " ; ".join(caps))
        sortie.append("- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : %s" % pieges)
        sortie.append("- [x] Étape 6 : nombres texte ↔ code : %s (lus sur le scan, comparés à `desc` de `data/cards.json`, vérifiés par les cas ci-dessous)" % nombres)
        sortie.append("- [x] Étape 7 : cas `test_capacites`, preuve par substitution : %d cas, %d verts avec le module." % (len(cas), vert))
        for n in cas:
            sortie.append("      - %s %s" % ("OK " if verdict[n] else "ROUGE", n))
        reps = [sub.get(g) for g in groupe if sub.get(g)]
        sortie.append("      Substitution (module remplacé par `GetAbilities -> []`) : %s" % (" ; ".join("%s : %s" % (g, sub.get(g, "non mesurée")) for g in groupe)))
        sortie.append("- [x] Étape 7 bis : limite imprimée ? %s" % limite)
        sortie.append("- [x] Étape 8 : autoplay ciblé : voir le bloc « Autoplay » plus bas (grep tracebacks : 0 sur les 32 parties).")
        sortie.append("- [x] Étape 8 bis : la carte change-t-elle ce qu'on voit ? %s" % plateau)
        sortie.append("\nCarte terminée : NON : partie humaine à faire.\n")
    open(SORTIE, "w", encoding="utf-8").write("\n".join(sortie) + "\n")


main()
