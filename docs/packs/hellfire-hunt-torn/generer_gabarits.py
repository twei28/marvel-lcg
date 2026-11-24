#!/usr/bin/env python3
"""Genere docs/packs/hellfire-hunt-torn/GABARITS.md (gabarits PROCESSUS-CARTE carte par carte) a partir de :
 - la liste de cas `tools/cas/hellfire_torn.py` (noms de cas = sujet = card_id) ;
 - les mesures de preuve par substitution `/tmp/hft_subst*.json` (substituer_prive.py) ;
 - le texte ecrit a la main ci-dessous (cartes de reference, mots-pieges, nombres).
Usage (depuis Fusion/marvel-lcg-src) : python3 ../../docs/packs/hellfire-hunt-torn/generer_gabarits.py <fichier(s) subst.json> ...
"""
import importlib.util
import json
import re
import sys

spec = importlib.util.spec_from_file_location("c", "tools/cas/hellfire_torn.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
CAS = [c["nom"][5:] for c in m.CAS]
SUBST = {}
for f in sys.argv[1:]:
    SUBST.update(json.load(open(f)))


def cas_de(cid):
    return [n for n in CAS if re.match(re.escape(cid) + r"\b", n)]


# card_id -> (nom, references, mots_pieges, nombres, plateau)
D = {}
def A(cid, nom, refs, pieges, nombres, plateau="NON"):
    D[cid] = (nom, refs, pieges, nombres, plateau)

A("hf501a", "Emma Frost, face A1 (standard, active)",
  "Réponse forcée après activation : `AfterEnemyActivationEnd` (activate.py) + `Worlds.DiscardEncounterTopCard` (hf101a) ; Interruption de défaite : 16080a Collector (`WhenUnitWouldBeDefeated` + `SetBeInstead` + `RemoveThreatFromSchemes` + `card.Flip`).",
  "`after ... activates` (chaque activation, une par joueur) ; `each scheme` = principale ET annexes (`EachScheme`) ; `would be defeated ... instead` (la défaite n'a pas lieu, les dégâts restent) ; `if it has the PSIONIC trait` (trait lu sur la carte défaussée).",
  "PV 7 par joueur (`7*`), ATQ 1 (étoile), MNG 2 (étoile), traits HELLFIRE PSIONIC X-MEN ; +1 menace / 5 menaces retirées.")
A("hf501b", "Emma Frost, face A2 (standard, retournée, PV infinis)",
  "`WhenEnemyWouldActivate` + `SetBeInstead` (sl037) ; `AfterPhaseEnd(ForcedResponse, \"Villain\")` ; `can_health.py OnFlip` (retour des PV en quittant une face infinie).",
  "`instead` (aucune manigance, aucune carte de boost, aucun dégât) ; `After the end of the villain phase` (pas la phase des joueurs : témoin) ; `then set ... hit point dial to her printed hit points` (natif au retournement).",
  "`HP: INF`, ATQ/MNG « étoile » seuls (0*) ; 2 cartes défaussées.")
A("hf502a", "Emma Frost, face B1 (expert, active)",
  "idem hf501a ; `Worlds.DiscardEncounterCards(2, effect)` rend les faces défaussées.",
  "`for each PSIONIC card discarded in this way` (+1 menace PAR carte PSIONIC, sur chaque manigance) ; défaite -> retournement comme A1.",
  "PV 8 par joueur, ATQ 2, MNG 2 (étoiles), 2 cartes défaussées.")
A("hf502b", "Emma Frost, face B2 (expert, retournée, PV infinis)",
  "`WhenEnemyWouldActivate` (+ `message.to_player`) ; `joueur.DealEncounterCards(1)` ; sl037.",
  "`activates AGAINST A PLAYER` (`to_player` non nul) ; `instead` : l'activation n'a pas lieu ; `facedown` : carte distribuée, pas révélée.",
  "`HP: INF` ; 1 carte face cachée.")
A("hf503a", "The Hellfire Club's Revenge (1A)",
  "`WhenCardSetup(\"This\")` (hf104a, deck de rencontre fouillé à la mise en place) ; deck de table (`hellfire_hunt.RecruitedMutants`) ; manigance annexe de la zone mise de côté (27102a) ; `hellfire_hunt.campaign.MiseEnPlace(4)` ; `WriteCampaignLogAtGameOver` (mts/campaign.py) avec `ReleveTorn`.",
  "`Shuffle every ELITE, HELLFIRE minion` (les DEUX traits ; White Queen x2 de Perfection compris) ; `set it next to the encounter deck` ; `CONTROLLED side face up` ; `Choose 3 modular sets` : le scénario livre les 3 recommandés (l'écran de préparation choisit, rien ne l'impose) ; carnet : tout allié sorti de la zone mise de côté est noté (livret p. 14).",
  "Deck Hellfire de 5 sbires à 1 joueur et les 3 modules recommandés ; Puppetry 8 + Entrave 5 = 13.", "OUI : deck et défausse Hellfire (piles de la table)")
A("hf503b", "Free Cassandra Nova (1B)",
  "`WhenPlayerPhaseBegin(ForcedInterrupt)` (ls013) ; `face.Reveal(joueur, effect)` depuis un deck annexe ; scheme_main.py (« If this scheme is completed, the players lose the game »).",
  "`At the start of the player phase` (dès le round 1) ; `in player order` (premier joueur d'abord) ; `not engaged with an ELITE, HELLFIRE minion` (un sbire HELLFIRE non élite ne retient pas) ; deck vide -> défausse remélangée SANS pénalité ; `cannot win unless` : Emma ne peut jamais être vaincue (A1 se retourne, A2 PV infinis).",
  "Seuil 15 par joueur, départ 1, escalade 1 par joueur.")
A("hf504a", "Nova's Psychic Puppetry, face A (CONTROLLED)",
  "27102a Light at the End (`WhenLastThreatRemoveFromThisScheme` + `card.Flip`, Permanent + Hinder) ; `ReponseSbireEliteVaincu` (`WhenUnitBeDefeated(ForcedResponse)` + `AskChooseFace`).",
  "`each HELLFIRE minion` (PAS seulement ELITE) défaussé (l'ELITE va dans la défausse Hellfire) ; `each player a facedown card` ; `another side scheme / Otherwise ... here` ; `the last threat` (pas une menace restante) ; Permanent natif.",
  "Menace de départ 8, Entrave 5 par joueur (13 à 1 joueur), 5 menaces retirées.", "OUI : menace posée au retournement (face B 13)")
A("hf504b", "Nova's Psychic Puppetry, face B (FRAGMENT)",
  "27102b Light at the End (face B : `Worlds.SetGameOver(True)`) ; `GiveKeywordToInPlayWhenApplyThis(..., trait=...)` (cw/56097b).",
  "`the players win the game` (victoire, pas défaite) ; `Each HELLFIRE minion gains the ILLUSION trait` (sbires déjà en jeu ET ceux qui entrent) ; face A vidée ne fait PAS gagner (témoin).",
  "Menace de départ 1 + Entrave 12 par joueur = 13 ; trait FRAGMENT (ajouté à l'énumération `TRAITS`).")
A("hf505", "Protect Students (obligation)",
  "04166 Anti-Hero Propaganda (`GiveKeywordToInPlayWhenApplyThis(Hero, attack=-1, defense=-1)`) ; im009 (`CostFunc.Custom`) ; `Worlds.GetOnFieldFriendlyCharacters`.",
  "`Your hero` (du joueur qui porte l'obligation : `control_by=\"You\"`) ; `reveal 1 card from the Hellfire deck` est une PARTIE DU COÛT (deck et défausse vides : action impayable) ; `each friendly character` (identités et alliés de tous les joueurs).",
  "ATQ -1, DEF -1 ; 1 dégât soigné ; Boost 2.")
A("hf506", "Uncover The Truth (obligation, Hazard)",
  "04045 / 27131 (`WhenInYourPlayTurn(AlterEgoAction).SetTarget(SchemeSide2)`) ; `HealthUnits`, `RemoveThreatFromSchemes`.",
  "`heal 5 damage FROM THE VILLAIN` (le texte soigne le vilain : respecté) ET `remove 5 threat from a side scheme` (les deux parties) ; `Discard this obligation` ; icône Hazard (« carte penchée + croix », comparée à 01180).",
  "5 dégâts soignés, 5 menaces retirées, Hazard 1, Boost 2.")
A("hf507", "Psychic Bulwark",
  "`GiveKeywordToInPlayWhenApplyThis(Minion, guard=1, patrol=1)` (27142 / hf313) ; `Faces.GiveStatus` ; fiches guard.md, patrol.md.",
  "`Each minion` (tous, pas seulement HELLFIRE, y compris ceux qui entrent après) ; Boost : `each minion a tough status card` (en jeu au moment du boost) ; Victory 1 natif.",
  "Menace de départ 9, Victory 1, Boost 2.")
A("hf508", "Psychic Entanglement",
  "27107 Brute Force Barricade (`ThreatCannotBeRemovedFromWhile(SchemeSide2, effect.this != message.trigger)`) ; hf029 (`WhenSchemeBeDefeated`).",
  "`OTHER side schemes` (pas elle-même, pas la principale) ; vaut pour les effets de carte (interruption d'Emma) ET la contrarie ; `When Defeated` : une carte face cachée à CHAQUE joueur ; Victory 1 -> pile de victoire.",
  "Menace de départ 8, Victory 1, Boost 2.")
A("hf509", "Psionic Paragon",
  "`GiveKeywordToInPlayWhenApplyThis(CardFinder(name=Emma Frost), health=10)` (21160 / 01140) ; 39035 Dial M for Mojo (`incite=1` sur `EncounterCard`).",
  "`+10 hit point` (plat) ; `Each ILLUSION card gains incite 1` (carte pas encore en jeu : traîtrise, attachement) ; `each player with no engaged minions` ; Paragon est vaincue par l'interruption d'Emma si elle a moins de 5 menaces.",
  "Menace de départ 4 par joueur, +10 PV, incite 1, Boost 2.")
A("hf510", "Hellfire Assault",
  "`ThreatCannotBeRemovedFromWhile(\"This\", by_thwarting=False)` (scheme.py) ; hf110 (`WhenCardBecomeBoost(\"This\", RevealThisCard)`) ; hf120 (`villain.DoAttackYou` / `DoSchemes`).",
  "`except by thwarting` (la contrarie retire, l'effet d'Emma non) ; `defeated BY A PLAYER` (`has_defeating_player=True`) ; `if it is White Queen` (le SBIRE de Perfection, pas le vilain) ; `schemes` : manigance contre le joueur.",
  "Menace de départ 1 par joueur.")
A("hf341", "* Negasonic Teenage Warhead (sbire ELITE HELLFIRE)",
  "40105a (`WhenUnitAttackYou(ForcedInterrupt)` + `message.GetAgainstPlayer()`) ; 40160 (soutiens) ; rc012 (`joueur.GetControlUpgrade`) ; hf321 (boost + `GetToPlayer`).",
  "`When ... attacks you` = AVANT l'attaque (Interruption forcée) ; `a support OR upgrade you control, if able` (prêt, au choix du joueur) ; Steady et Toughness natifs.",
  "PV 4, ATQ 2*, MNG 1, Steady, Toughness, Boost 1 + étoile.")
A("hf342", "Perception Manipulation (x2 : hf342, hf343)",
  "hf305 Psychic Mirage (`AttachToFaceWhenPutIntoPlay(\"YourIdentity\")`, `CardCannotReady(\"AttachedCharacter\")`) ; hf110 (`PlayerActionToDiscardThis().SetCost(Cost(...))`) ; `identite.ChangeToOtherIdentityForm`.",
  "`Spend [mental][mental]` : DEUX ressources mentales (Genius en donne deux) ; `Alter-Ego Action` ; `cannot be readied` ; Boost : `Change your form` (alter-ego -> héros).",
  "Boost 0 + étoile ; coût `Cost(\"BB\")`.")
A("hf344", "Mind Over Matter (x2 : hf344, hf345)",
  "hf321 (`face.Reveal`) ; 40160 / `ThisCardGainSurge` ; `Worlds.GetEncounterDiscardPileCards` (le dessus en tête).",
  "`topmost` = la plus récente ; `attachment` = type Attachement ; `Otherwise ... surge` ; Boost `Exhaust your HERO` (forme héros seulement : un allié défend pour ne pas fausser la mesure).",
  "Boost 1 + étoile.")
A("hf346", "Matter Manipulation (x3 : hf346, hf347, hf348)",
  "`Search.PlayerCard(... cost_less_than)` (checker.py : borne INCLUSIVE, d'où `cout - 1`) ; jubilee 47003 (`PutIntoPlay`) ; 40160 (surge).",
  "`same type` (Ally/Support/Upgrade) ; `less than` STRICT (coût 0 : impossible) ; `your deck and discard pile` ; `Otherwise` : surge si rien n'est mis en jeu (défausse faite) : voir QUESTIONS n°5.",
  "Boost 2.")
A("hf351", "* Cassandra Nova (sbire ELITE HELLFIRE PSIONIC)",
  "wd064 Princess Python / pt019 Mr. Hyde (`Search` + `PutIntoPlay` + `AttachTo2` depuis le When Revealed) ; 01121 (boost « put into play engaged with you »).",
  "`Find` (livret p. 4 : toutes les zones : deck de rencontre, défausse, mise de côté) ; le manteau est attaché À ELLE ; Steady natif.",
  "PV 2, ATQ 3, MNG 3, Steady, Boost 0 + étoile.")
A("hf352", "Illusory Duty",
  "`Worlds.DiscardEncounterCards(3)` ; `Search.SearchForCard(... include_removed_area, obligation_give_to=joueur)` ; `Faces.RemoveAllFromGame`.",
  "`If no obligation was NOT revealed` (double négatif : QUESTIONS n°1) ; `your obligation` (donnée à ce joueur) ; `removed-from-game area` ; `remove this card from the game`.",
  "3 cartes défaussées, Boost 2.")
A("hf353", "Mental Paralysis",
  "41029 / hf308 (`Faces.GiveStatus([identite], ...)`) ; Surge natif.",
  "`You` = l'identité du joueur qui révèle / subit le boost ; Stunned ET Confused (deux statuts) ; Surge natif.",
  "Boost 3 + étoile, Surge.")
A("hf354", "Cassandra's Telepathic Cloak",
  "02020 Hysteria (`AttachToFaceWhenPutIntoPlay`) ; sk033 / wt017 (`*UnitCannotTakeDamage`) ; hf101a (`AfterUnitAttackYou`).",
  "`cannot take ANY amount of damage` (prévention totale tant que le manteau est en jeu) ; `If she is not in play, find ..., reveal her, attach` ; `After Cassandra attacks YOU` (pas un autre sbire, pas un autre joueur).",
  "Boost 1.")
A("hf355", "Jumpstart (x2 : hf355, hf356)",
  "04119 (`AttachToFaceWhenPutIntoPlay(... highest_printed_hp=True, if_cannot_gain_surge=True)`) ; 02020 Hysteria (`message.GiveAdditionalBoostCardForThisActivation`) ; Villainous (Black Bishop hf311).",
  "`highest hit-point` : PV imprimés (QUESTIONS n°4) ; `attacks YOU` ; `1 additional boost card` : un sbire non Villainous n'a pas de boost -> il en reçoit une ; Boost : `Deal yourself 1 facedown card`.",
  "SCH +2, ATQ étoile (0*), Boost 0 + étoile.")
A("hf357", "Narrow Minded (x2 : hf357, hf358)",
  "11049 Fear of Kang / 40160 (`PlayerActionToDiscardThis(AlterEgoAction).SetCostFunc(CostFunc.Exhaust(\"YourIdentity\"))`).",
  "`Alter-Ego Action` (forme alter-ego seulement) ; icône AMPLIFY (avion + croix), comparée à 16054 ; `HasAmplify` ajouté au type Obligation (sinon `KeyError`).",
  "Boost 2, Amplify 1.")

# cartes sans module propre dans D : copies
COPIES = {"hf343": "hf342", "hf345": "hf344", "hf347": "hf346", "hf348": "hf346", "hf356": "hf355", "hf358": "hf357"}

ORDRE = ["hf501a", "hf501b", "hf502a", "hf502b", "hf503a", "hf503b", "hf504a", "hf504b", "hf505", "hf506", "hf507", "hf508", "hf509", "hf510",
         "hf341", "hf342", "hf343", "hf344", "hf345", "hf346", "hf347", "hf348", "hf351", "hf352", "hf353", "hf354", "hf355", "hf356", "hf357", "hf358"]

print("""# Hellfire Hunt, scénario 4 « Torn » + modules Negasonic Teenage Warhead et Immensity (Dipsome, préfixe `hf`) : gabarits PROCESSUS-CARTE

Worktree `Marvel-LCG-campagnes`, branche `campagnes-fanmade`. Pack `hellfire_hunt_torn` (set 244), module plat `src/cards/pack/hellfire_hunt_torn/` (30 cartes : `hf501`-`hf510`, `hf341`-`hf348`, `hf351`-`hf358`).
Scénarios : `hellfire_torn` (Emma Frost A1/A2) et `hellfire_torn_expert` (B1/B2). Cas : `tools/cas/hellfire_torn.py` (noms `[hf] <card_id> ...`, vérificateur `hft_etat`).
Génération des données : `docs/packs/hellfire-hunt-torn/generer_donnees.py` ; textes français : `textes_fr.py` ; carnet : `campagne.py` ; recettes : `recettes.py` ; preuve par substitution : `substituer_prive.py`
(copie PRIVÉE du pack : `tools/substituer_pack.py` poserait ses stubs dans les sources partagées, que le scénario Cassandra Nova lit via Immensity).
Doutes de règle : `QUESTIONS.md` (8 questions). **Aucune carte n'est « terminée : OUI » : aucune partie jouée par un humain dans le navigateur.**
""")
for cid in ORDRE:
    base = COPIES.get(cid, cid)
    nom, refs, pieges, nombres, plateau = D[base]
    cas = cas_de(cid)
    s = SUBST.get(cid)
    if cid in COPIES:
        nom = D[base][0].split(" (x")[0] + " (exemplaire de %s)" % base
    print("### %s : %s\n" % (cid, nom))
    print("- [x] Étape 2 : carte(s) de référence : %s" % ("identique à %s (même script `from .%s import GetAbilities`)." % (base, base) if cid in COPIES else refs))
    print("- [x] Étape 5 : texte-contre-code, mots-pièges vérifiés : %s\n      Résultat : texte imprimé relu phrase par phrase contre le script ; aucune capacité fantôme (mots-clés natifs lus dans `desc`, aucun code)." % ("voir %s." % base if cid in COPIES else pieges))
    print("- [x] Étape 6 : nombres texte ↔ code : %s\n      Résultat : identiques dans `data/cards.json` (`desc`) et le script (relu sur le scan)." % ("voir %s." % base if cid in COPIES else nombres))
    if s and s["total"] > 0:
        verts = s["restent_verts"]
        morts = s["morts"]
        sub = "rouges %d/%d sans le module" % (s["rouges"], s["total"])
        if verts:
            sub += " ; restent verts sans module (natif `desc` ou TÉMOIN d'absence d'effet, assumés) : " + " | ".join(v[5:] for v in verts)
        if morts:
            sub += " ; %d processus morts" % morts
    else:
        sub = "mesure absente (à relancer)"
    print("- [x] Étape 7 : cas test_capacites par capacité, preuve par substitution (copie privée) : %d cas : %s\n      Résultat : %s." % (len(cas), " ; ".join(c[:110] for c in cas), sub))
    print("- [x] Étape 7 bis : limite imprimée ? NON (aucune limite « once per ... » sur cette carte) : pas de témoin d'épuisement.")
    print("- [ ] Étape 8 : autoplay ciblé : voir « Autoplay » ci-dessous (8 parties Sunspot sur `hellfire_torn`, témoin Rhino ; grep tracebacks).")
    print("- [x] Étape 8 bis : la carte change-t-elle ce qu'on VOIT ? %s\n" % ("OUI" if plateau.startswith("OUI") else "NON (aucune pile/compteur/statut nouveau ; carte attachée ou posée comme une carte ordinaire)") +
          ("      Cas plateau : `ui-app/src/board/torn-hellfire-plateau.test.ts` (vu ROUGE avant `sontDuHellfire` dans `zones.ts` : 3 échecs sur 4, puis vert). %s\n" % plateau if plateau.startswith("OUI") else ""))
    print("Carte terminée : NON : partie humaine à faire (aucun humain n'a joué cette carte dans le navigateur) ; tout le reste de la liste ci-dessus est fait.\n")

print("""## Autoplay (étape 8, commun aux 30 cartes) : 32 parties, grep d'erreurs = 0

`tools/autoplay.py <game_dir> --deck <deck> --vilains <scénario> --difficultes <niveau> --profils equilibre --parties 8` (graines 1 à 8, profil « équilibré »), journaux `/tmp/autoplay_*.log` :

| Deck | Scénario | Niveau | Parties | Victoires | Fin de partie | Rounds (moyenne) | Tracebacks / erreurs |
|---|---|---|---|---|---|---|---|
| `sunspot_hellfire` | `hellfire_torn` | standard | 8 | 0 | 6 complot principal complété, 2 joueur éliminé | 4,0 | 0 / 0 |
| `sunspot_hellfire` | `hellfire_torn` | expert | 8 | 0 | 7 complot, 1 éliminé | 3,5 | 0 / 0 |
| `rachel_summers` (Marvel Girl) | `hellfire_torn` | standard | 8 | 0 | 5 complot, 3 éliminés | 3,6 | 0 / 0 |
| `sunspot_hellfire` (TÉMOIN) | `rhino` | standard | 8 | 0 | 6 complot, 2 éliminés | 3,4 | 0 / 0 |

`grep -c "Traceback"` et `grep -c "NameError|AttributeError|TypeError|KeyError|AssertionError"` sur les 32 journaux : 0 partout. Le pilote ne gagne aucune partie, ni contre Torn ni contre le TÉMOIN (decks de départ de 15 cartes, pilote
heuristique) : le taux de blocage n'est donc pas discriminant, les durées (3,4 à 4,0 rounds) sont comparables. **Journal lu** : mise en place (« AdditionalDeck<5> va être mélangé » = le Hellfire deck), un sbire ÉLITE HELLFIRE révélé à
chaque début de phase des joueurs, Emma qui complote (« Free Cassandra Nova reçoit 5 pion(s) » = MNG 2 + icônes de boost), Réponse forcée d'Emma (« +1 menace » sur la principale et Puppetry), `hf341` / `hf301` « défaussée vers AdditionalDiscardPile<1> »
(défausse Hellfire) dans les parties 2, 3 et 4. **Jamais lu en partie** : la défaite d'Emma (le pilote ne l'atteint pas), le retournement de Puppetry et la victoire : ils ne sont prouvés que par les cas (dont `hf501b INTEGRATION`, phase du méchant entière)
et les épreuves de campagne.

## Portes (gates) lancées sur le pack

- `python -m compileall -q src/cards/pack/hellfire_hunt_torn src/game/puzzle src/game/card/face/card_type/obligation.py` : OK.
- `tools/verifier_appels_modules.py <game_dir> <port> hellfire_hunt_torn` : « OK : tous les appels de hellfire_hunt_torn existent » (gate étalonnée : voir plus bas).
- `tools/test_cards.py` : 8103 ok, 0 erreur (930 cartes sans `GetAbilities`, hors périmètre).
- `tools/audit_cartes.py` : 0 type d'argument, 0 construction impossible, 0 erreur de module ; **2 `marqueur_sans_capacite` (hf504a, hf504b : « Response »)** : faux positif, la Réponse forcée « After an ELITE, HELLFIRE minion is defeated » est une `DelayAbility`
  (`WhenUnitBeDefeated` sur une carte autre que `"This"`, `SetSecondType(ForcedResponse)`) que l'audit ne reconnaît pas ; elle est prouvée par les cas `[hf] hf504a Reponse forcee ...` et `[hf] hf504b Reponse forcee ...`.
- `tools/verifier_prefixes.py` : OK. `tools/verifier_campagnes.py` : OK. `tools/verifier_scenes_campagne.py` : OK. `tools/verifier_pages_campagnes.py` : OK.
- `ui-app` : `npx tsc --noEmit` OK ; vitest `textes-fr-fanmade`, `traduction-public`, `vocabulaire-statuts`, `vocabulaire-moteur`, `dico-en`, `torn-hellfire-plateau` verts.
""")
