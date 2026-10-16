# Baxter Stockman v3 : questions en attente (aucune réponse de l'utilisateur à ce jour)

Format : card_id, scan, texte anglais exact, lectures possibles (la recommandée en premier), ce que le
script fait PROVISOIREMENT (marque `TODO-QUESTION` dans le code). Rien n'a été deviné en silence.

Scans : `.planning/tmnt/pics-baxter/` (copie versionnée, JPEG).

---

## Q1 : tx005 Baxter Blaster, la case « ATK ★ »

- **Scan** : `.planning/tmnt/pics-baxter/tx005.jpg` (case rouge en bas à gauche : « ATK » surmonté d'une ÉTOILE
  blanche, comme la MNG/ATQ ★ des essaims ; aucun chiffre).
- **Texte anglais exact** : « Attach to Baxter Stockman. ★ Forced Response: After Baxter Stockman attacks and damages a
  friendly character, daze them. Hero Action: Exhaust your hero or spend 2 resources of any type → discard this card. ★ Boost:
  Attach Baxter Blaster to Baxter Stockman. » Aucune phrase ne dit ce que vaut l'étoile de la case ATK.
- **Lectures** :
  1. **Aucun bonus d'ATQ** (recommandée) : l'étoile est le simple repère « cette carte a un texte étoilé » (les
     lignes ★ Forced Response / ★ Boost) ; Baxter garde son ATQ imprimée.
  2. +1 ATQ au vilain porteur (comme `ATK+ 1` de The Hypernova `sp015`, qui est imprimé « +1 » : rien de tel ici).
  3. Une valeur dynamique que l'auteur aurait oublié d'écrire (ex. +1 ATQ par carte d'état Dazed en jeu) : non
     défendable sans texte.
- **Provisoire** : lecture 1, AUCUN bonus (`tx005.py`, cas `[baxter] tx005 ATQ « ★ »`).

## Q2 : tx016 Wrapped Up, QUI choisit le personnage hébété

- **Scan** : `tx016.jpg`.
- **Texte anglais exact** : « When Revealed: Daze a friendly character. If you cannot, this card gains surge. »
- **Lectures** :
  1. **Le joueur à qui la carte est révélée choisit** parmi TOUS les personnages amis qui peuvent l'être (identités et
     alliés de tous les joueurs) (recommandée : même lecture que `td005` « Cloak two friendly characters ») ;
  2. seulement parmi SES personnages (« friendly » = « you control ») ;
  3. le premier joueur choisit toujours.
- **Provisoire** : lecture 1 (`tx016.py`, `Worlds.GetOnFieldFriendlyCharacters`, choix du joueur qui révèle).

## Q3 : tx017 Auto Defense Bots, plus aucun compteur shield

- **Scan** : `tx017.jpg`.
- **Texte anglais exact** : « Forced Interrupt: When this minion would be defeated, heal all damage from this minion, and
  remove 1 shield counter from here instead. »
- **Lectures** :
  1. **Sans compteur shield, l'interruption ne s'applique pas** : le sbire est vaincu normalement (recommandée : sans
     cela il serait immortel après son dernier compteur) ;
  2. l'interruption s'applique toujours (il se soigne sans fin, rien à retirer) : sbire invincible, absurde ;
  3. l'interruption s'applique, mais seulement tant qu'un shield existe, ET soigne même si aucun shield n'est retiré.
- **Provisoire** : lecture 1 (`tx017.py`, condition `a_un_bouclier`, TODO-QUESTION Q3).

## Q4 : tx012 / tx013, trait « FLYBORG » (singulier) contre FLYBORGS (pluriel) de td017

- **Scans** : `tx012.jpg`, `tx013.jpg` (« AERIAL. FLYBORG. SWARM. ») ; `.planning/tmnt/pics-donatello/td017.jpg`
  (« AERIAL. FLYBORGS. SWARM. »).
- **Texte anglais exact** : la ligne de traits ; et `td014` Extermination! : « a MOUSER or FLYBORG minion ».
- **Lectures** :
  1. **Deux traits distincts, comme imprimé** (recommandée : fidélité 100 % aux scans) : FLYBORG (tx012, tx013) et FLYBORGS
     (td017) ; Extermination! (td014, qui cherche « MOUSERS or FLYBORGS ») ne trouvera donc PAS les Flyborgs de Baxter ;
  2. normaliser tout en FLYBORGS (ou FLYBORG) : un seul trait, mais ce n'est plus ce que les scans impriment.
- **Provisoire** : lecture 1 (traits `FLYBORG` et `FLY` ajoutés à `card_face.py`). Aucun impact de jeu connu : les deux cartes
  ne se croisent que si le joueur mélange Donatello et ce scénario.

## Q5 : « Content » de 1A, orthographe « Baxter (III) » en expert

- **Scan** : `tx004a.jpg`. Texte : « (Baxter Stockman (II) and Baxter (III) for expert mode.) » : « Baxter (III) » est
  manifestement le stade III de Baxter Stockman (la carte `tx003`, qui s'appelle « Baxter Stockman »).
- **Provisoire** : stades II et III en expert (`data/scenarios/baxter_stockman_expert.json`), pas de question de fond, notée pour
  mémoire.

## Hors question (décidé par les sources)

- « all-purpose counter » (tx004b, tx006) : la FAQ officielle (MC4DB, 29/09/2026, déjà dans `gmw/16034`) dit que la carte qui
  porte le compteur en définit le type : swarm / ooze / cable / shield selon le sbire. Fiche `all-purpose-counter.md`.
- Dazed : toutes les règles viennent de l'encart `Dazed Rules Insert.png` (un seul Dazed, Tough d'abord, Cloaked et Dazed
  simultanés, un seul effet puis la carte part). Fiche `dazed.md`.
