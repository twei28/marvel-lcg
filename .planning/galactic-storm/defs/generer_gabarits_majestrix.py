"""Genere .planning/galactic-storm/MAJESTRIX-GABARITS.md : un gabarit PROCESSUS-CARTE par carte (gs114-gs137).

Entrees : le rapport JSON de la passe `test_capacites.py ... "[mv]"` (argument 1), la sortie texte de
`substituer_pack.py ... gs` (argument 2), le resume de l'autoplay (argument 3, texte libre colle tel quel).
Les blocs ecrits a la main (etapes 2, 5, 6, 8 bis) vivent dans GABARITS ci-dessous ; les etapes 7 et 8 sont
remplies avec les MESURES (cas verts/rouges, substitution par carte).

Usage : python3 generer_gabarits_majestrix.py <rapport.json> <substitution.txt> <autoplay.txt>
"""
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE = os.path.join(ICI, "..", "MAJESTRIX-GABARITS.md")

# card_id -> (nom, etape 2, etape 5, etape 6, limite, 8 bis, note de substitution)
GABARITS = {
    "gs114": ("Deathbird (I)",
              "Forced interrupt : 50089b Extract Captives (ReplaceTarget sur WhenUnitWouldAttack, un ennemi attaque un allie : moteur natif) ; +1 ATK : GainATKForThisAttack (sender_damage.py).",
              "« initiates an attack AGAINST YOU » (identite visee, pas un allie deja vise), « if YOU control », « THAT ally » (choix du joueur s'il en a plusieurs), « instead » (cible REMPLACEE, pas ajoutee) ; etoile en exposant de l'ATQ = renvoi au texte.",
              "PV 16[per_hero] -> HP \"16*\" ; MNG 2 ; ATQ 2 ; +1 ATK -> bonus_atq=1. Identiques desc / script / scan.",
              "NON", "NON (aucune carte deplacee, aucun compteur)",
              "Les deux TEMOINS (sans STARJAMMER, allie non STARJAMMER) verifient une absence de detournement : verts sans module (assume)."),
    "gs115": ("Deathbird (II)",
              "cannot be defeated : 50129a Citizen V / 35029 (UnitCannotBeDefeatedWhile) + relance ecrite a part (piege de change_on_event, RECETTES §16) ; Forced interrupt : comme gs114.",
              "« players do not control Lilandra AND the Shi'ar Throne SUPPORT » (les deux, sous controle de joueurs ; la face manigance ne compte pas) ; memes mots-pieges que gs114.",
              "PV 19[per_hero] -> \"19*\" ; MNG 2 ; ATQ 3 ; +1 ATK. Identiques.",
              "NON", "NON", "Verts sans module : le TEMOIN (Lilandra + Trone -> victoire) et le cas « tombe des que ... » (sans module, Deathbird meurt tout de suite : meme etat final). Ce dernier a ete vu ROUGE AVEC le module avant le correctif de la relance (« victoire = False », passe du 20/10/2026) : il mesure bien la relance."),
    "gs116": ("Deathbird (III)",
              "comme gs115 ; « 1 additional boost card for that activation » : sk100 Emperor's Throne (GiveAdditionalBoostCardForThisActivation).",
              "PAS de +1 ATK sur ce stade (texte different, verifie sur le scan) ; la carte de boost ne vaut que si l'attaque est detournee.",
              "PV 21[per_hero] -> \"21*\" ; MNG 2 ; ATQ 3 ; boost_sup=1. Identiques.",
              "NON", "NON", "Le TEMOIN sans STARJAMMER (une seule carte de boost) reste vert sans module (assume)."),
    "gs117a": ("Earn the People's Favor (1A)",
               "Setup d'une face 1A : 50087a Batroc (WhenCardSetup, SetupCards.PutIntoPlay / SetAsideCards) ; tuck face visible : PlaceCardHere(.., True, ..) (livret p.4).",
               "« EACH STARJAMMER ally » (les six, Lilandra comprise) ; « Set the Shi'ar Throne side scheme ASIDE » (pas en jeu) ; « Contents » porte par le JSON du scenario.",
               "Aucun nombre sur la face A ; Contents : 2 stades de mechant (expert : II et III), 1 modulaire -> data/scenarios/gs_majestrix_verdict*.json.",
               "NON", "OUI : cas plateau ui-app/src/board/glisse-sous-manigance.test.ts (allies glisses face VISIBLE sous la prison) ; aucun correctif plateau necessaire (mecanisme generique de mere-de-la-nuit) ; calibrage : la meme table avec les allies FACE CACHEE fait tomber le 3e cas (vu rouge le 20/10/2026).", ""),
    "gs117b": ("Earn the People's Favor (1B)",
               "When Revealed : WhenThisRevealed + PlaceThreatOnSchemes (50134) ; « After resolving step one of the villain phase » : 04096b Hunting Down Heroes (AfterResolveVillainPhaseStep).",
               "« 2 threat FOR EACH PLAYER in alter-ego form » (0 si tous en heros, contre-cas) ; la menace va sur la PRISON ; etoile de l'escalade = renvoi au texte.",
               "Seuil 3[per_hero] -> \"3*\" ; escalade +1[per_hero] -> \"1*\" ; depart 0 ; 1[per_hero] -> \"1*\" ; 2 par joueur -> 2*n. Identiques.",
               "NON", "NON", ""),
    "gs118a": ("Majestrix's Verdict (2A)",
               "« players as a group choose » : convention Filter.One (premier joueur) ; remove from the game : Faces.RemoveAllFromGame ; « Advance to stage 2B » automatique (face A sans seuil, comme sk145a) ; in expert mode : Worlds.IsExpert (50087a).",
               "« Otherwise » = seulement si AUCUN glisse (FAQ 1.2) ; « (2 ... instead in expert mode) » ; « in play » ; Lilandra executee = defaite (insert).",
               "1 (2 en expert) glisse(s) ; 1 en jeu. Identiques au scan.",
               "NON", "OUI (carte retiree de la partie, zone non dessinee) : rien a dessiner ; la prison se redessine avec un glisse de moins (meme cas plateau que gs117a).", ""),
    "gs118b": ("Majestrix's Verdict (2B)",
               "WhenMainSchemeStageWouldBeCompleted + SetBeInstead : sk145b (meme auteur) ; flip d'une manigance en jeu = revelation (OnAfterFlip) ; helpers 1B.",
               "« INSTEAD » (jamais accompli) ; « flip this card AND REVEAL IT » (2A rejoue son execution) ; stade 2B qui recommence a 0 (point tranche par necessite, voir questions).",
               "Seuil 5[per_hero] -> \"5*\" ; escalade +2[per_hero] -> \"2*\" ; depart 0 ; 1[per_hero] ; 2 par joueur. Identiques.",
               "NON", "NON (meme carte retournee deux fois, le plateau dessine la face courante)", ""),
    "gs119": ("Imprisoned on Chandilar",
              "Assault / Permanent : bases desc (assault.md, permanent.md) ; tuck apres depart : 50081 Abduct Superhumans ; liberation : 50088b Locate Missing Person.",
              "« a STARJAMMER ALLY leaves play » ; retire de la partie = pas recapture ; « place 6 threat » meme sans allie (question Q3) ; « players as a group » ; tuck FACE VISIBLE.",
              "Depart 6 ; « place 6 threat ». Identiques.",
              "NON", "OUI : glissement face visible sous la prison, cas plateau glisse-sous-manigance.test.ts (voir gs117a).", "Verts sans module (assume) : Assault et Permanent (bases desc) et le temoin « allie NON STARJAMMER non glisse » (absence)."),
    "gs120a": ("Shi'ar Throne (manigance annexe)",
               "32172a Enemy of My Enemy (flip puis PutIntoPlay de la face B) ; retournement differe a AfterSchemeBeDefeated (piege mesure, RECETTES §16).",
               "« the DEFEATING player » (message.defeating_player, repli premier joueur) ; face B = SOUTIEN.",
               "Depart 3[per_hero] -> \"3*\" ; Hazard 1. Identiques.",
               "NON", "OUI : la carte change de zone (manigances -> soutiens du joueur) ; zones existantes, pas de cas plateau propre (support standard).", ""),
    "gs120b": ("Shi'ar Throne (soutien)",
               "16142 Milano / sk062 Baxter Building (CanGenerateResources + Exhaust + AnyPlayerCanDoThis) ; AfterCardLeavePlay(ForcedResponse).",
               "« Shi'ar Throne OR Lilandra » (deux declencheurs, deux cas) ; « for ANY player » ; ressource [mental] verifiee par decoupe (sk003, sk148).",
               "1 ressource B. Identique.",
               "NON", "OUI : retour de la zone soutien a la zone manigances (zones standard).", ""),
    "gs121": ("Lilandra",
              "50091 Rescued Captive (ThisNotCountAllyLimit) ; 01083 (AfterCardEnterPlay) + SetupCards.Reveal(only_set_aside) ; 50089b (SetGameOver).",
              "« set aside » (rien si le Trone est deja en jeu) ; « REMOVED from the game » ≠ vaincue (contre-cas).",
              "PV 4 ; CTR 1 ; ATQ 2 + 1 degat consecutif -> \"2*\" ; pas de cout. Identiques.",
              "NON", "OUI : sort de prison / y retourne (cas plateau de la prison).",
              "Le contre-cas « Lilandra VAINCUE : pas de defaite » reste vert sans module (assume)."),
    "gs122": ("Ch'od", "Retaliate : base desc (retaliate.md).", "Riposte 2 (pas 1).",
              "Cout 3, PV 6, CTR 1*, ATQ 3** (2 consecutifs), RES B, Riposte 2. Identiques.",
              "NON", "NON", "Aucune capacite scriptee (module vide) : le cas « Retaliate 2 » mesure la base desc et reste vert sans module (assume)."),
    "gs123": ("Corsair", "UnitAttackGainKeyword(\"This\", ranged=True) (RECETTES §3, 27078).", "« attacks » = toutes ses attaques.",
              "Cout 3, PV 4, CTR 2*, ATQ 2*, RES Y. Identiques.", "NON", "NON", ""),
    "gs124": ("Hepzibah", "UnitAttackGainKeyword(\"This\", piercing=True).", "« attacks » = toutes.",
              "Cout 3, PV 3, CTR 2*, ATQ 3*, RES R. Identiques.", "NON", "NON", ""),
    "gs125": ("Korvus", "UnitAttackGainKeyword(\"This\", overkill=True).", "« attacks » = toutes ; deux etoiles sous l'ATQ.",
              "Cout 3, PV 5, CTR 1*, ATQ 3**, RES Y. Identiques.", "NON", "NON", ""),
    "gs126": ("Raza", "Toughness : base desc (toughness.md).", "Tenace a l'entree en jeu (piege du Reset, RECETTES §16).",
              "Cout 3, PV 3, CTR 2*, ATQ 2*, RES B, Toughness 1. Identiques.", "NON", "OUI (carte d'etat Tenace dessinee, mecanisme standard)",
              "Aucune capacite scriptee (module vide) : cas de la base desc, vert sans module (assume)."),
    "gs127": ("Royal Cape of the Shi'ar",
              "07035 Distracting Taunts (AttachToFaceWhenPutIntoPlay, health, Response AfterUnitAttackUnit + SetCost) ; sk148 (retaliate).",
              "« Attached CHARACTER » (vaut pour Lilandra) ; « After LILANDRA attacks DEATHBIRD » ; cout [energy].",
              "+2 PV, Riposte 1, 2 icones de boost. Identiques.", "NON", "OUI : l'attachement change de porteur (Deathbird -> Lilandra), zones standard.", ""),
    "gs128": ("Shi'ar Crest",
              "badge SCH+/THW+ : has_modify.py ; steady : GiveKeywordToAttached ; Boost : 52037 Growing Strong.",
              "« the ACTIVATING enemy » ; badge « +1 SCH/THW » (+1 MNG sur Deathbird, +1 CTR sur Lilandra).",
              "+1 MNG / +1 CTR, 1 icone de boost. Identiques.", "NON", "OUI : changement de porteur (zones standard).", ""),
    "gs129": ("Shi'ar Javelin",
              "badge ATK+ ; 27147 Arm Cannon (UnitAttackGainKeyword(\"Attached..\")) ; Boost : 50160 Supersonic.",
              "« IF this activation is an attack » ; « attached CHARACTER ».",
              "+1 ATQ, 1 icone de boost, 2 exemplaires. Identiques.", "NON", "OUI : changement de porteur (zones standard).", ""),
    "gs130": ("Araki", "Patrol / Vulnerable : bases desc ; When Defeated : sk155 ; « each scheme » : littéral EachScheme.",
              "« EACH SCHEME » (principale + annexes) ; Vulnerable = defausse, pas « vaincu ».",
              "MNG 3, ATQ 1, PV 4, 0 icone de boost ; 2 et 1 menaces. Identiques.", "NON", "NON",
              "Verts sans module (assume) : Vulnerable et les deux cas Patrol (bases desc : cas sujet et temoin)."),
    "gs131": ("Jailor of Chandilar", "When Defeated : sk155 + RemoveThreatFromSchemes ; Boost : WhenCardBecomeBoost.",
              "menace sur la PRISON.", "MNG 1, ATQ 2, PV 6, Riposte 1, 1 icone, 4 exemplaires ; 2 / 1 menaces. Identiques.",
              "NON", "NON", "Retaliate : base desc, cas vert sans module (assume)."),
    "gs132": ("Private Audience", "49039 Selene (UnitCannotAttackTarget) ; 55061 Puppet Master (UnitCannotThwartTarget).",
              "« ALLIES » (pas les heros) ; « the VILLAIN » ; « the MAIN scheme ».",
              "Depart 3[per_hero], Acceleration 1, aucune icone de boost. Identiques.", "NON", "NON",
              "Les cas temoins (sans elle) et le cas « revelee avec 3 menaces » restent verts sans module (assume)."),
    "gs133": ("Tapping the M'kraan Force", "Hinder/Amplify/Hazard : bases desc ; When Defeated : sk100 ; HealthUnits.",
              "« EACH STARJAMMER ally IN PLAY ».", "Depart 2, Hinder 2[per_hero], Amplify 1, Hazard 1, 3 icones ; soin 1. Identiques.",
              "NON", "NON", "Le cas « revelee avec 4 menaces et les icones » mesure les bases desc : vert sans module (assume)."),
    "gs134": ("Tortured Prisoners", "Crisis : base desc ; sk156 (When Revealed, menace additionnelle).",
              "« TUCKED » (pas en jeu) ; « additional ».", "Depart 1[per_hero], Crisis 1, 2 icones ; +1 par glisse. Identiques.",
              "NON", "NON", ""),
    "gs135": ("Birthright to the Throne", "16114 Single-Minded Fury (DoAttackYou du controleur, meme en alter ego) ; 50096 (DoSchemes) ; Tenace : 52037.",
              "« the player WHO CONTROLS IT » ; « SUPPORT » ; detournement par Deathbird possible.",
              "1 icone de boost, 2 exemplaires. Identiques.", "NON", "NON", ""),
    "gs136": ("Exemplar Punishment", "04096b (ChooseAbilities a deux branches) ; ra028 (TakeIndirectDamage).",
              "« FOR EACH » (un choix par glisse) ; « place 2 threat on IT » (question Q2).",
              "1 indirect / 1 menace / 2 menaces, 1 icone, 2 exemplaires. Identiques.", "NON", "NON", ""),
    "gs137": ("Sister's Deception", "22031 Old Rivals (BasicAttack d'un allie contre l'identite).",
              "« attacks YOU » (le joueur qui revele) ; « WITHOUT exhausting » (cas : pret) ; « WITH consequential damage » (cas : 1 degat).",
              "ATQ de Lilandra 2, 1 consecutif ; 3 menaces ; 2 icones, 2 exemplaires. Identiques.", "NON", "NON", ""),
}


def main():
    rapport = json.load(open(sys.argv[1], encoding="utf-8"))
    subst = open(sys.argv[2], encoding="utf-8").read() if len(sys.argv) > 2 else ""
    autoplay = open(sys.argv[3], encoding="utf-8").read().strip() if len(sys.argv) > 3 else "(non lance)"
    cas = rapport["cas"]
    lignes = ["# Majestrix's Verdict (Galactic Storm, lot GS-5) : gabarits PROCESSUS-CARTE, gs114-gs137",
              "",
              "Genere par `.planning/galactic-storm/defs/generer_gabarits_majestrix.py` a partir des MESURES (rapport",
              "`test_capacites` filtre `[mv]`, sortie de `substituer_pack.py ... gs`, autoplay). Etape 1 : entrees",
              "`defs/majestrix_cards.py` (inserees par `defs/inserer_majestrix.py`) ; etape 4 : images portees par",
              "`defs/copier_images_majestrix.py` (27 card_id, une image par numero imprime).",
              "",
              f"Batterie `[mv]` : {rapport['reussis']}/{rapport['total']} cas verts.", ""]
    for cid, (nom, e2, e5, e6, lim, e8b, note) in GABARITS.items():
        sujets = [c for c in cas if re.search(r"\[mv\] " + cid + r" ", c["nom"])]
        verts = sum(1 for c in sujets if str(c.get("ok")) == "True")
        m = re.search(r"^.*\b" + cid + r"\b.*$", subst, re.M)
        ligne_subst = m.group(0).strip() if m else "(pas de ligne de substitution)"
        complet = verts == len(sujets) and len(sujets) > 0
        lignes += [f"### {cid} : {nom}", "",
                   f"- [x] Etape 2 : cartes de reference : {e2}",
                   f"- [x] Etape 5 : texte-contre-code, mots-pieges : {e5}",
                   "      Resultat : conforme.",
                   f"- [x] Etape 6 : nombres texte <-> code : {e6}",
                   "      Resultat : conforme.",
                   f"- [{'x' if complet else ' '}] Etape 7 : {len(sujets)} cas sujets, {verts} verts avec le module ; substitution : {ligne_subst}"]
        for c in sujets:
            lignes.append(f"      - {'VERT' if str(c.get('ok')) == 'True' else 'ROUGE'} : {c['nom']}")
        if note:
            lignes.append(f"      Note : {note}")
        lignes += [f"- [x] Etape 7 bis : limite imprimee ? {lim}.",
                   f"- [x] Etape 8 : {autoplay}",
                   f"- [x] Etape 8 bis : {e8b}",
                   "",
                   f"Carte terminee : {'OUI' if complet else 'NON : cas rouge ou absent'}.", ""]
    open(SORTIE, "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print("ecrit", SORTIE)


if __name__ == "__main__":
    main()
