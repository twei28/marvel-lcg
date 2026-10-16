# Questions en attente, scenario Shredder v3 (`ts`) et TMNT Standard-Expert (`te`)

Aucune question n'a pu etre posee a l'utilisateur pendant ce travail : pour chaque lecture AMBIGUE d'un texte
imprime, la lecture la plus fidele est implementee provisoirement, marquee `TODO-QUESTION` dans le script, et
consignee ici. Scans : `.planning/tmnt/pics-shredder/<card_id>.jpg` (copie versionnee), sources dans le zip
`TMNT Enemies -20261014T200338Z-1-001.zip`.

## Q1. ts006 Bladed Armor : « take 1 damage » sans sujet
- Scan : `.planning/tmnt/pics-shredder/ts006.jpg` (zip : `Shredder v3/Shredder Deck/6 Bladed Armor.png`).
- Texte : « **Hero Action**: If there are no cloaked status cards on Shredder, take 1 damage and spend 1 resource of any type → discard this card. »
- Lectures : (1) **recommandee, implementee** : l'IDENTITE du joueur qui paie prend 1 degat (cout, comme « take 1 damage → » de Blade bl009 et She-Hulk 01027) ; (2) Shredder prend 1 degat ; (3) n'importe quel personnage controle par le joueur, au choix.
- Script : `src/cards/pack/shredder/shredder/ts006.py`, `CostFunc.TakeDamage(1, "YourIdentity")`.

## Q2. te201 Intense Combatants : le mot « intensify » n'est defini nulle part
- Scan : `.planning/tmnt/pics-shredder/te201.jpg` (zip : `TMNT Standard-Expert (Status Card Standard-Expert)/Optional Intense Version/X1 Intense Combatants.png`).
- Texte : « Permanent. Setup. **Forced Interrupt**: When a status card would be placed on a character, if that character already has 1 copy of that status card on them, intensify them instead. »
- Aucun scan du zip ne definit « intensify » / « intensified » (encarts Shredder, Baxter et Bebop relus). La carte est CREEE dans `cards.json` (pack `tmnt_standard_expert`, image `te201.jpg`) mais N'EST PAS SCRIPTEE, n'est dans aucun ensemble de rencontre ni scenario : on n'invente pas une regle.
- Lectures : (1) **recommandee** : fournir la definition de « intensify » (carte, encart ou regle) ; (2) « intensify » = poser une SECONDE carte du meme statut (doublon, au-dela du plafond de 1) ; (3) « intensify » = doubler l'effet de la carte d'etat existante (Sonne : pas d'attaque + 1 degat, etc.).
- Dependance : le plafond « une seule carte Cloaked par personnage » (ci-dessous, Q8) rend la lecture (2) pertinente pour Cloaked.

## Q3. Quel ensemble « Standard » pour Shredder ? (TMNT Standard ou habillage du core)
- Scan : `ts004a.jpg`, « Content: Shredder, Shadow of the Foot, and **Standard** sets ».
- Le zip contient DEUX jeux de rencontre standard : « TMNT Standard-Expert (Status Card...) » (cartes propres : No Quarter, Outmatched, Pursued by Shadows, Skulk... avec Cloak et Daze) et « Normal Standard-Expert Reskins » (les 10 cartes du core 01186-01193 avec une illustration TMNT).
- Lectures : (1) **recommandee, implementee** : `tmnt_standard` (+ `tmnt_expert` en expert) = le jeu TMNT propre ; les habillages sont fournis sous `tmnt_standard_reskin` / `tmnt_expert_reskin`, interchangeables ; (2) les habillages par defaut ; (3) au choix du joueur a la mise en place.
- Fichiers : `data/scenarios/shredder.json`, `shredder_expert.json`.

## Q4. ts010 Foot Ninja : « When Foot Ninja is defeated, shuffle them » : remplacement ou apres la defaite ?
- Scan : `ts010.jpg`. Texte : « **Forced Interrupt**: When Foot Ninja is defeated, shuffle them into the encounter deck. »
- Lectures : (1) **recommandee, implementee** : la defaite A LIEU (elle compte pour 1B « After a FOOT CLAN minion is defeated, place 1 threat ») puis le sbire est melange au lieu de la defausse (modele hood 24015 Griffin) ; (2) remplacement « would be defeated... instead » : pas de defaite, pas de menace sur 1B (modele an014 / lj015).
- Cas : « ts010 Forced Interrupt : la defaite COMPTE ».

## Q5. ts103 Kira no Ken : que devient la carte si Karai est introuvable ?
- Scan : `ts103.jpg`. Texte : « Attach to Karai. If Karai is not in play, search the encounter deck and discard pile for Karai and reveal her. Then, attach this card to her. »
- Le texte ne dit pas quoi faire si la recherche echoue. Lectures : (1) **recommandee, implementee** : l'attachement ne peut pas s'attacher, il est defausse ; (2) il reste en jeu non attache ; (3) « surge » (aucun mot-cle imprime).
- Meme point pour ts006 Bladed Armor / ts007 Kuro Kabuto si Shredder est absent (cas impossible en jeu normal).

## Q6. « Karai » : la Karai NEMESIS de Leonardo (tl015) est-elle visee ?
- Scans : `ts102.jpg` (boost : « Search ... for Karai »), `ts103.jpg` (« Attach to Karai »).
- tl015 `* Karai` (set Leonardo Nemesis) est le MEME personnage unique que ts101. Lectures : (1) **recommandee, implementee** : le texte « Karai » designe l'une OU l'autre (`IDS_KARAI = ["ts101", "tl015"]`, par card_id) ; (2) uniquement ts101 (set Chunin).

## Q7. ts007 Kuro Kabuto, boost « Attach Kuro Kabuto to Shredder » : quand ?
- Scan : `ts007.jpg`. Le texte ne dit pas « after this activation » ; comme une carte de boost est defaussee par le moteur APRES sa resolution, un attachement immediat serait ecrase. Lectures : (1) **recommandee, implementee** : apres l'activation (modele Nebula gmw, Luger 04132, Gauntlet) ; (2) immediatement, avec un detournement du rangement de la carte de boost.

## Q8. Plafond d'UNE seule carte Cloaked par personnage (encart du scenario) : change l'etat actuel du moteur
- Encart `Shredder Insert.png` : « Normally characters can only have one Cloaked status card on them at a time, but the Shredder can have more than one, depending on his villain stage » et « Unless otherwise specified, a character can only have one Cloaked status card placed on them. »
- Avant ce travail, `cloaked.md` disait « Cloaked s'empile (aucun plafond) ». **Le moteur applique desormais le plafond de l'encart** (`CanStatus.cloaked_max`, 1 par defaut, Shredder 2/3/4) : une carte qui « Cloak X » alors que X est deja camoufle ne fait rien (c'est ce que ts020 Foot Rikugun appelle « If you cannot »). Les cas de `tools/cas/cloaked.py` ne posent qu'un Cloaked a la fois : verts. A confirmer par l'utilisateur : le plafond vaut-il aussi pour td005 Improvised Tactics, tl015/tl016 ?

## Q9. « daze » : traduction francaise et carte d'etat
- te001, te002, te103 posent la carte d'etat **Dazed** (encart « Dazed Rules Insert » du vilain Baxter Stockman, autre agent). Traduction FR provisoire : « hebetez ». A harmoniser avec le pack Baxter lors de la fusion.

## REPONSES DE L'UTILISATEUR (16/10/2026)

- **Q1** : Bladed Armor, l'IDENTITE du joueur qui paie prend le degat (confirmee).
- **Q2** : l'utilisateur a fourni la carte d'etat **INTENSIFIED** (capture Discord du serveur Bebop & Rocksteady, `.planning/tmnt/intensified-capture.webp`) :
  « The next time this character would discard a status card, discard this status card instead. This card cannot be given to a character that has no status cards. »
  « Intensify X » = poser une carte d'etat Intensified sur X (7e carte d'etat). IMPLEMENTE le 16/10/2026 (moteur + te201, fiche `docs/reference/mots-cles/intensified.md`, cas `tools/cas/intensified.py`).
- **Q3** : jeu standard/expert TMNT PROPRE par defaut (tmnt_standard / tmnt_expert) pour TOUS les scenarios TMNT ; Baxter bascule (8 parties d'essai sans erreur).
- **Q4** : Foot Ninja est VAINCU (la defaite compte) puis melange (confirmee).
- **Q5** : Kira no Ken defaussee si Karai est introuvable (confirmee).
- **Q6** : « Karai » = ts101 OU tl015 (confirmee).
- **Q7** : Kuro Kabuto s'attache APRES l'activation (confirmee).
- **Q8** : tranchee par l'encart lui-meme (« Unless otherwise specified, a character can only have one Cloaked status card ») : plafond d'UN Cloaked pour tous les personnages, Shredder 2/3/4 selon son stade. Les trois regles chiffrees de l'encart (« Shredder Cloaked Rules ») sont desormais couvertes par des cas : +6 sur une activation avec 3 Cloaked (base mesuree 3 -> 9), une attaque de 3 retire 2 Cloaked et laisse le dernier, trois attaques de 1 les retirent tous.
- **Q9** : « Hébété / hébétez » valide par l'utilisateur.

### Q2 suite : lectures d'Intensified tranchees par l'utilisateur (16/10/2026)
1. L'effet de la carte d'etat d'origine a lieu, seule sa defausse est remplacee : confirme.
2. Defausse groupee : chaque Intensified remplace UNE carte : confirme.
3. Perimetre : toute defausse d'un etat precis (consommation, carte de joueur, Percant) ; pas la sortie de jeu, « chaque carte d'etat », ni les plafonds de regle : confirme.
4. te201 « 1 copy » = des la 1re copie, pour tout etat : confirme.
5. Plafond : Intensified suit les regles des cartes d'etat, UNE par personnage, DEUX pour un Solide (Steady). CHANGE (l'agent avait code « aucun plafond »).
6. te201 en jeu : case a cocher a la preparation, decochee par defaut, avec le jeu TMNT Standard / Expert.
