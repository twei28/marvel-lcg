#!/usr/bin/env python3
"""Ajoute (ou remplace) la section « Torn / Negasonic / Immensity » de docs/reference/RECETTES-MOTEUR.md. Idempotent, sous flock /tmp/cards_json.lock,
bloc borne par <!-- DEBUT hellfire_hunt_torn --> ... <!-- FIN hellfire_hunt_torn -->. Usage : python3 recettes.py <racine du depot>"""
import fcntl
import os
import sys

DEBUT, FIN = "<!-- DEBUT hellfire_hunt_torn -->\n", "<!-- FIN hellfire_hunt_torn -->\n"
TEXTE = DEBUT + r'''
## 40. Hellfire Hunt, scénario 4 « Torn » + modules Negasonic Teenage Warhead et Immensity (Dipsome, `hf501`-`hf510`, `hf341`-`hf358`, 01/11/2026) : recettes et pièges payés

Pack `hellfire_hunt_torn` (set 244), cas `tools/cas/hellfire_torn.py` (verificateur `hft_etat`), données `docs/packs/hellfire-hunt-torn/generer_donnees.py`.

| Mécanique imprimée | API / chemin | Modèle | Piège |
|---|---|---|---|
| Vilain à PV INFINIS sur sa face retournée, qui revient avec ses PV imprimés | face `desc.HP = "INF"` ; face active : `WhenUnitWouldBeDefeated(ForcedInterrupt, "This", op)` + `message.SetBeInstead` + `this.card.Flip` ; face infinie : `AfterPhaseEnd(ForcedResponse, "Villain", flip)` | `sl037`, `16080a` Collector, `can_health.py OnFlip` | le moteur REMET LES PV quand on quitte une face infinie (`OnFlip` : `origin_face.is_infinite_health` -> `ResetHealth`) : le « set the hit point dial to her printed hit points » est natif, aucun code. Les dégâts restent quand on ENTRE sur la face infinie. `degats_de` ne sait pas lire une face INF (`max_health` vaut 0) : mesurer `en_jeu` / `absents` |
| « place / remove N threat on each scheme » (principale ET annexes) | `this.PlaceThreatOnSchemes("EachScheme", n, effect)` / `this.RemoveThreatFromSchemes("EachScheme", n, effect)` | `hf501a`, `hf501b` | « each scheme » retire AUSSI de la manigance qui donne un bonus (Psionic Paragon est vaincue à moins de 5 menaces) et fait déclencher « when the last threat is removed » des autres (Puppetry se retourne) |
| Deck de TABLE avec défausse propre (Hellfire deck) | `Deck2(monde.scenario, DeckType.AdditionalDeck/AdditionalDiscardPile, CardFace)` ajouté à `monde.additional_decks` / `additional_discard_piles` ; `card.bind_discard_pile = défausse` sur chaque carte | `hellfire_hunt.RecruitedMutants`, `hellfire_hunt_torn.DeckHellfire` | `bind_discard_pile` est ce qui envoie un sbire vaincu ou défaussé dans LA défausse Hellfire ; `deck.Get(True)[0]` = le dessus ; `face.Reveal(joueur, effect)` marche depuis un deck annexe (`is_deck` -> zone de pioche des rencontres) ; remélange « sans pénalité » = `Faces.MoveAllTo(défausse, deck)` + `deck.Shuffle` à la demande |
| Table : piles Hellfire distinctes | `ui-app/src/board/zones.ts` : `sontDuHellfire` (traits `t_ELITE` ET `t_HELLFIRE`) | `sontDesPieges` | sans cela le deck Hellfire se fondait dans « Cartes cachées » avec le deck Recruited Mutants ; le titre d'une pile n'apparait que sur une pile `regardable` |
| Manigance annexe à deux faces, Permanent, Hinder, dernière menace -> retourner / gagner | `WhenLastThreatRemoveFromThisScheme(ForcedInterrupt, op)` + `this.card.Flip` ; face B : `Worlds.SetGameOver(True, effect)` | `27102a/b` Light at the End | `Hinder` et la menace de départ de la face B sont posés APRÈS le retournement (fiche hinder.md) ; `Puzzle.Flip` d'une face qui garde 13 menaces donne 26 : retirer la menace avec `Puzzle.PlaceThreat(carte, -n)` (vrai chemin) |
| « Threat cannot be removed from other side schemes » / « ... from here except by thwarting » | `ThreatCannotBeRemovedFromWhile(SchemeSide2, conditions=[effect.this != message.trigger])` / `ThreatCannotBeRemovedFromWhile("This", by_thwarting=False)` | `27107` Brute Force Barricade | une contrarie sur la manigance bloquée retire 0 ; l'interruption de défaite d'Emma aussi |
| « At the start of the player phase » | `WhenPlayerPhaseBegin(ForcedInterrupt, op)` | `ls013` | part dès le round 1 ; le harnais ne joue AUCUNE phase : `Puzzle.BeginPlayerPhase()` (AJOUT moteur, additif) |
| « Each X minion gains <trait> / guard and patrol » | `GiveKeywordToInPlayWhenApplyThis(CardFinder2("HELLFIRE", Minion), trait=ILLUSION, change_on_event=OnEvent.CardInPlay(Minion))` ; `...(Minion, guard=1, patrol=1)` | `cw/56097b` | le trait donné se lit tout de suite par `HasTrait` ; un sbire qui entre ensuite l'a aussi |
| « Each ILLUSION card gains incite 1 » (cartes pas encore en jeu) | `GiveKeywordToInPlayWhenApplyThis(CardFinder2("ILLUSION", EncounterCard), incite=1)` | `39035` Dial M for Mojo | marche aussi pour une carte révélée (traîtrise, attachement) ; sans la carte, aucune menace |
| Obligation avec icône Amplify | `desc.Amplify` + **`HasAmplify` ajouté au type `Obligation`** (`card_type/obligation.py`) | `Obligation(...CanCrisis...)` | sans lui : `KeyError: 'Amplify'` à la mise en place d'un scénario qui contient la carte (avalé, partie injouable). L'icône « avion + croix » est Amplify, « carte penchée + croix » est Hazard (`01180`, `16054`) |
| Coût « reveal 1 card from the Hellfire deck » | `CostFunc.Custom(None, fn)` ; `fn(targets, effect)` rend `False` quand le deck ET sa défausse sont vides | `im009` | le coût est payé AVANT l'effet : le sbire est engagé même si la suite échoue |
| « When X attacks you, you must exhaust a support or upgrade » | `WhenUnitAttackYou(ForcedInterrupt, "This", op)` + `message.GetAgainstPlayer()` ; candidats : `joueur.supports.Get()` + `joueur.GetControlUpgrade()` prêts | `40105a` | un sbire NON Villainous n'a PAS de carte de boost : pour mesurer « additional boost card » prendre un sbire Villainous (Black Bishop hf311) |
| « Attach to Cassandra Nova. If she is not in play, find her, reveal her, then attach » | `AttachToFaceWhenPutIntoPlay(finder, if_cannot_operation=fn)` ; `Search`/`face.Reveal` ; `this.AttachTo2` | `02020`, `pt019` | `*UnitCannotTakeDamage(finder)` (liste à déballer) tient tant que la carte est en jeu ; un attachement non attaché est défaussé à l'entrée : un cas « après » doit mesurer un EFFET durable (dégât prévenu puis subi), pas la seule absence |
| Carnet de victoire propre au scénario | `WriteCampaignLogAtGameOver(ReleveTorn, scenario_id=...)` (le relevé commun + les alliés qui ne sont plus dans `world.aside_deck`) | `hellfire_hunt.campaign.Releve` | l'invariant « un allié sorti de la zone mise de côté n'y retourne jamais » couvre deck, défausse, main, deck/défausse Recruited |
| Correctif d'un autre pack | `SbireWQEntreEnJeu` (hf301/hf302) : l'interruption ne vaut que si le VILAIN White Queen est en jeu | `hellfire_hunt_white_queen/__init__.py` | sinon les White Queen du module Perfection ne pouvaient jamais entrer en jeu au scénario 4 |

Pièges du HARNAIS payés par ce pack (à ajouter à §7) :
- `Puzzle.Attack` / `Activate` / `EnemyAttacks` : le héros en forme héros DÉFEND toujours (il s'incline) : pour mesurer un « exhaust your hero » (boost), faire défendre un ALLIÉ (`Puzzle.Attack('villain', '01002')`) ; Mockingbird `01083` étourdit le vilain en entrant : prendre Black Cat `01002`.
- `01105` n'est PAS « Bomb Scare » : c'est « I'm Tough » (« If Rhino already has a tough status card, this card gains surge ») : il gagne surge sans Rhino, et plusieurs `01105` de suite font une chaîne de renforts (`AssertionError is_revealing`). Pour un cas qui révèle des cartes, prendre un filler inerte (`hf307`).
- `01089` Genius génère [mental][mental] d'un seul coup : un cas « une seule ressource ne suffit pas » doit utiliser une ressource d'un AUTRE type (Strength `01090`).
- Le complot 1B fait révéler un sbire du Hellfire deck dès la 1re phase des joueurs : chaque cas commence avec un sbire ELITE HELLFIRE engagé ; `tools/cas/hellfire_torn.py` le retire par `Puzzle.RemoveMinionsInPlay()` (clé `libre=True` pour la mise en place).
- `Puzzle.EmptyEncounterDeck()` / `deck(...)` doivent PRÉCÉDER les commandes qui révèlent des cartes du Hellfire deck (sinon le deck de test est posé après la révélation).
- Surge dans le harnais : l'ancienne règle (la carte suivante est révélée tout de suite), pas la distribution RR 1.8.
- `fnefin_carnet_sortant` lit un fichier unique (`campaign_log_last_file`) : deux cas de carnet ne tournent jamais en parallèle.
- `tools/substituer_pack.py` pose les stubs dans `src/cards/pack/` PARTAGÉ : pour un pack dont d'autres scénarios réutilisent les cartes (Immensity -> Cassandra Nova), utiliser `docs/packs/hellfire-hunt-torn/substituer_prive.py` (copie privée du seul pack).
''' + FIN


def main():
    chemin = os.path.join(sys.argv[1], "docs", "reference", "RECETTES-MOTEUR.md")
    with open("/tmp/cards_json.lock", "w") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX)
        s = open(chemin, encoding="utf-8").read()
        if DEBUT in s:
            i, j = s.index(DEBUT), s.index(FIN) + len(FIN)
            s = s[:i] + s[j:]
        s = s.rstrip("\n") + "\n\n" + TEXTE
        open(chemin, "w", encoding="utf-8").write(s)
    print("RECETTES-MOTEUR.md : section 40 ecrite")


main()
