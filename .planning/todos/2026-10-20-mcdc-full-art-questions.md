# Full Art Reprints MC/DC 2026 : 10 cartes non branchées, une question chacune (20/10/2026)

Contexte : la galerie https://www.mcdc.fun/2026-card-gallery contient 41 « reprints » en pleine illustration (RP, numéros MC/DC
6138 et 6142 à 6181). 31 sont branchés comme arts alternatifs (code `mcdc26`, voir `docs/packs/mcdc-2026-punisher/GALERIE.md`
et `importer-full-art.py`). Les 10 ci-dessous ne le sont pas, parce que l'image imprime autre chose que la carte du jeu, ou parce
que la carte est introuvable. Les images sont dans `docs/packs/mcdc-2026-punisher/sources/galerie/<section>/` (dossier ignoré par git).

Critère de branchement des 31 autres, pour mémoire : même nom, même coût, mêmes statistiques, mêmes traits, même ressource, même
aspect, et un texte dont l'EFFET est identique. Les reformulations de gabarit ne comptent pas (« Prerequisite (X) » pour « Play only
if your identity has X », « After you play from hand » pour « After you play X from your hand », « Max 1. » pour « Max 1 per
player », « tuck » pour « attach facedown », « Find » pour « Search the encounter deck, discard pile, and set-aside area for »).
Ces reformulations sont listées carte par carte en fin de fichier : si l'une d'elles doit faire écarter une carte, il suffit de
retirer son `card_id` de `CARTES` dans `importer-full-art.py`, de retirer `mcdc26` dans `data/arts_alternatifs.json` et de
relancer `tools/generer_arts_cartes.py`.

Chaque question : options en multichoix, recommandation en premier, ce que chaque option change en jeu. Une même carte du jeu
n'est jamais modifiée par ces choix : seule l'image proposée change (le moteur joue toujours la carte du jeu).

---

## Q1. Heli-Quincarrier (Basic, MC/DC 6142) : `B - heli_quincarrier - RP.jpg`

Image : Support coût 3, Basic, titre « Heli-Quincarrier » (étiquettes de ruban adhésif « HELI » et « JET »), traits barrés
« S.H.I.E.L.D. Avenger. Vehicle. », texte « Do: Whatever the hell a Quincarrier or Helicarrier^ does. » et citation « Champions
players are too lazy to swap cards ». Carte du jeu la plus proche : `08023` Quincarrier (Basic, Support, coût 3, Avenger / Vehicle,
« Play only if your identity has the Avenger trait. Resource: Exhaust → generate a wild resource »), et `01092` Helicarrier (Core, Basic,
Location / S.H.I.E.L.D.). L'image est une carte plaisanterie qui reprend l'effet des deux sans être l'une ni l'autre.
- **A (recommandé) : ne pas brancher.** Le texte imprimé ne décrit pas l'effet réel de 08023 ; un art alternatif qui affiche « Do: whatever the hell… » ment au joueur en partie.
- B : brancher sur `08023` (Quincarrier). En jeu, rien ne change ; le joueur voit un titre et un texte différents de ceux de la carte jouée.
- C : brancher sur `01092` (Helicarrier). Même remarque.
- D : brancher sur les deux cartes. Même remarque, deux fois.

## Q2. Spider-Man, Peter (B.) Parker (Basic, MC/DC 6143) : `B - spider man peter - RP.jpg`

Image : Ally coût 3, THW 2 ATK 2, Web-Warrior, « Requirement (energy, mental, physical) », « Response:
After Spider-Man attacks or thwarts, ready another Web-Warrior character ». Sous-titre imprimé « Peter (B.) Parker » (Spider-Verse).
Carte du jeu : `27049` Spider-Man, sous-titre « Peter Parker » (pack `sm`, Basic, coût 3, HP 3, ATK 2*, THW 2*, mêmes traits, même effet). Seul
le sous-titre diffère (« Peter (B.) Parker » contre « Peter Parker »). La règle du projet (GUIDE §12 bis) range un changement de nom dans les cartes exclusives.
- **A (recommandé) : brancher sur `27049`.** L'effet et les statistiques sont identiques, le « (B.) » ne change rien au jeu (l'unicité se lit sur le nom, et Spider-Man est « Spider-Man » dans les deux cas, sous-titre à part). En jeu, aucune différence.
- B : ne pas brancher, tant que le sous-titre diffère. Le joueur n'a pas cette illustration.
- C : créer une carte distincte « Spider-Man (Peter B. Parker) » au code propre. Effet : une seconde Spider-Man de même effet dans la collection, qui peut se jouer en plus de `27049` si l'unicité ne les relie pas ; à éviter sauf demande.

## Q3. Angela (Aggression, MC/DC 6153) : `A - angela - RP.jpg`

Image : Ally coût 0, THW 0 ATK 2, Asgard / Guardian, « Forced Response: After entering play, search the top 10 cards of the encounter deck
for a minion and put it into play engaged with you. If you cannot, discard Angela. » Carte du jeu : `18011` (pack `gam`), même coût et mêmes
statistiques, texte « … put it into play engaged with you. **Shuffle the encounter deck.** If a minion was not put into play this way, discard Angela. »
Le « Shuffle the encounter deck » n'est pas imprimé sur l'image.
- **A (recommandé) : brancher sur `18011`.** Le moteur joue la carte du jeu, donc le mélange a lieu comme aujourd'hui ; l'image omet seulement la phrase (usage MC/DC : la fouille du dessus du deck est suivie d'un mélange implicite). En jeu : rien ne change.
- B : ne pas brancher. Le joueur n'a pas l'illustration.
- C : brancher et signaler dans la modale que le texte imprimé est abrégé. Demande un libellé de plus dans l'interface.

## Q4. Kaluu (Leadership, MC/DC 6171) : `L - kaluu - RP.jpg`

Image : Ally coût 2, THW 1 ATK 1, Avenger / Mystic, « Response: After entering play, search the top 5 cards of your deck for an event and add
it to your hand. » Carte du jeu : `21014` (pack `mts`), mêmes coût et statistiques, texte « … add that event to your hand. **Shuffle your deck.** »
Même omission du mélange que Angela.
- **A (recommandé) : brancher sur `21014`**, pour les mêmes raisons que Q3 (le moteur mélange, seule la phrase manque sur l'image).
- B : ne pas brancher.
- C : brancher avec un libellé d'avertissement dans la modale.

## Q5. Silk (Protection, MC/DC 6180) : `P - silk - RP.jpg`

Image : Ally coût 2, THW 1 ATK 1, Web-Warrior, « Response: After you play from hand, if you control another Web-Warrior card, search the
encounter deck for a treachery and discard it. » Carte du jeu : `27010` (pack `sm`), mêmes coût et statistiques, texte identique avec en plus « (Shuffle.) ».
Un troisième exemplaire proche existe dans le jeu (`bw002` Silk, héros Brawn, Ally Hero, ressource différente) : il n'est pas concerné.
- **A (recommandé) : brancher sur `27010`**, mêmes raisons que Q3.
- B : ne pas brancher.
- C : brancher avec un libellé d'avertissement dans la modale.

## Q6. White Tiger (Leadership, MC/DC 6169) : `L - white tiger - RP.jpg`

Image : Ally coût 3, THW 2 ATK 2, Avenger, « Response: After you play from hand, draw cards (max 3) equal to the villain's stage number. »
Carte du jeu : `21013` (pack `mts`), mêmes coût, statistiques et ressource, texte « … draw X cards (to a maximum of three), where X is equal to the
villain's stage number. **If the villain has no stage number, draw 1 card.** » La clause finale est absente de l'image : contre un méchant
sans numéro d'étape (scénarios de certaines campagnes), le texte imprimé ne dit rien, le moteur fait piocher 1 carte.
- **A (recommandé) : brancher sur `21013`.** Le moteur joue la carte du jeu (pioche 1 carte sans numéro d'étape). L'image est incomplète sur un cas rare, qui reste correct en jeu.
- B : ne pas brancher.
- C : brancher et changer le moteur pour suivre l'image (aucune pioche sans numéro d'étape). Fidélité 100 % à l'image mais carte différente de l'officielle ; à éviter.

## Q7. Wiccan (Justice, MC/DC 6158) : `J - wiccan - RP.jpg`

Image : Ally coût 2, THW 1 ATK 1, Avenger, « Response: After Wiccan thwarts, discard 1 from the encounter deck. Deal 1 damage to an enemy equal to
the [boost] discarded. » (une seule cible reçoit tous les points). Cartes du jeu : `15011` (pack `scw`) et `aa019` (pack `agatha_harkness`), toutes deux
Ally Justice coût 2, HP 3, mêmes statistiques, texte identique entre elles « … For each boost icon discarded this way, deal 1 damage to an enemy. »
(un point par icône, sur la cible de son choix à chaque fois). Le texte diffère donc sur l'effet : tout sur un ennemi (image) contre un ennemi par icône (jeu). Deux exemplaires dans le jeu.
- **A (recommandé) : ne pas brancher pour l'instant.** Le texte imprimé n'a pas le même effet que la carte jouée, et deux cartes du jeu se disputent l'image.
- B : brancher sur `15011` et `aa019`. En jeu, rien ne change ; l'illustration affiche un texte à effet différent.
- C : brancher sur `15011` seule (l'officielle du pack `scw`). Même remarque ; la copie `aa019` garde son art.
- D : modifier la carte du jeu pour qu'elle suive l'image (« Deal 1 damage to an enemy equal to the number »). Effet : Wiccan inflige toujours tous les points à une seule cible ; cela touche deux packs et leurs deux copies.

## Q8. Overwatch (Justice, MC/DC 6159) : `J - overwatch - RP.jpg`

Image : Upgrade coût 0, « Attach to a scheme. Max 1. » « Hero Interrupt: When attached scheme is thwarted, discard → remove the same amount of threat from
another scheme. » Carte du jeu : `30019` (pack `spiderham`), ressource physique, « Attach to a scheme. **Max 1 per scheme.** » et le même effet (« When any amount of threat is removed
from attached scheme by a thwart… different scheme »). `30019` a déjà un art alternatif `tmnt`. L'image dit « Max 1 » sans préciser : par manigance (comme le jeu) ou par joueur.
- **A (recommandé) : brancher sur `30019`.** « Max 1 » après « Attach to a scheme » se lit « par manigance », comme sur la carte du jeu ; aucun changement en jeu.
- B : ne pas brancher tant que la limite n'est pas confirmée par l'équipe MC/DC.
- C : brancher et fixer la limite à un par joueur, comme le suggère la lecture littérale. Effet : un joueur ne peut plus attacher qu'un seul Overwatch en tout ; carte différente de l'officielle.

## Q9. Clarity of Purpose (Leadership, MC/DC 6168) : `L - clarity of purpose - RP.jpg`

Image : Upgrade coût 1, Condition, « Attach to a friendly character. Max 1. Hero Resource: Exhaust and deal 1 damage to attached character → generate [wild]. »
Carte du jeu : `31029` (pack `spdr`), même coût et ressource, « Max 1 per character. » Même ambiguïté que Q8 (« Max 1 » sans préciser).
- **A (recommandé) : brancher sur `31029`**, mêmes raisons que Q8.
- B : ne pas brancher.
- C : brancher et fixer la limite à un par joueur. Effet : un seul Clarity of Purpose par joueur en tout.

## Q10. Punisher, Frank Castle (Aggression, MC/DC 6138) : `docs/packs/mcdc-2026-punisher/sources/galerie/other/6138 - A - punisher - RP.jpg`

Image : Ally coût 3, THW 1 ATK 2*, Soldier / Vigilante, « ★ Punisher's attacks gain piercing and ranged. Response: After Punisher attacks and defeats a minion, deal 2 damage to an enemy. »
Introuvable dans `cards.json` : les seules cartes « Punisher » sont `dt026` The Punisher (pack `determination`, Ally coût 1, ATK 3**, « Fragile », sans Response) et les cartes de la
future campagne (pas encore créées). C'est une carte nouvelle de la campagne (numéro 6138, juste avant les scénarios de la section « other »), pas un art alternatif d'une carte existante.
- **A (recommandé) : ne pas brancher, la créer avec la campagne Punisher** (carte d'aspect Aggression jouable par tous, à ajouter au pack, `PROCESSUS-CARTE.md`). Elle devient alors carte du jeu, et l'art de la galerie son illustration.
- B : la brancher comme art alternatif de `dt026`. À écarter : coût, statistiques, traits et texte diffèrent (mauvaise carte affichée en partie).
- C : ne rien faire : l'illustration reste dans la galerie téléchargée, sans carte.

---

## Reformulations de gabarit acceptées pour les 31 cartes branchées (à relire en cas de doute)

| Carte du jeu | Nom | Écart entre l'image et le texte du jeu |
|---|---|---|
| 49022 | Face the Past | « Find your nemesis minion » pour « Search the encounter deck, discard pile, and set-aside area for your nemesis minion » |
| 29027 | Ingenuity | « Prerequisite (Genius). Max 1. » pour « Play only if your identity has the Genius trait. Max 1 per player. » ; existe aussi en exclusive TMNT `ub021` (non concernée) |
| 13018 | Ironheart (Riri Williams) | « After you play from hand » pour « After you play Ironheart from your hand » |
| 32019 | Professor X | « At the end of the round, discard. » pour « …if Professor X is still in play, discard him. » |
| 30021 | SP//dr | « …if defeated by excess [consequential damage] » pour « …if she was defeated by taking excess consequential damage » ; « Play only if you control a Web-Warrior » (sans « card ») |
| 31022 | Spider-Man (Otto Octavius) | « After you play from hand, ready an upgrade you control. If it has the Tech trait » pour « After you play Spider-Man from your hand… If that upgrade has the Tech trait » |
| 13016 | Boot Camp | « Max 1. » pour « Max 1 per player. » |
| 17028 | Dive Bomb | « Prerequisite (Aerial). » pour « Play only if your identity has the aerial trait. » |
| 28017 | Honed Technique | formulation condensée (« if you paid with a mental resource, increase its damage by its printed cost ») ; « Max 1. » pour « Max 1 per player. » |
| 10018 | Martial Prowess | « Max 1. » pour « Max 1 per player. » |
| 35014 | Sunfire | « After you play from hand, spend [energy] → discard an attachment with a "Hero Action" or "Hero Response." » (même effet) |
| 25014 | Throg | « After entering play » pour « After Throg enters play » |
| 32041 | Wolverine (Logan) | texte identique, mots de gabarit seulement |
| 41012 | Captain Britain | « takes -1 [consequential damage] after he thwarts a side scheme or attacks a minion » (icône à la place du mot) |
| 04049 | Clear the Area | « If this removes the last threat » pour « …on that scheme » ; a déjà l'art `tmnt` |
| 15012 | Crisis Averted | « If you paid with [mental], ignore [crisis] icon » pour « …using a mental resource, this thwart ignores the crisis icon » |
| 22011 | Eros | « After you play from hand, confuse a minion for each [mental] you paid » pour « …you used to pay for him » |
| 27044 | Field Agent | « When a S.H.I.E.L.D. ally would take [consequential damage] » pour « …any amount of consequential damage » |
| 30013 | Spider-Man (Pavitr Prabhakar) | « …for each Web-Warrior card you control » pour « …(including Spider-Man) » |
| 23012 | Black Panther | « the event tucked here » pour « the event attached to Black Panther » ; « tuck it here » pour « attach it to him facedown » |
| 49015 | Cyclops (Scott Summers) | texte identique, mots de gabarit seulement |
| 08031 | Rapid Response | « put that ally into play » pour « …from your discard pile » (l'allié défait s'y trouve de toute façon) ; « Max 1 per player. » identique |
| 45016 | Side-by-Side | « Ready your sidekick → ready hero, choose: » pour « …ready your hero and choose one: » ; « both » pour « both characters » |
| 03017 | Strength In Numbers | « Exhaust X allies you control → draw X cards. » pour « Exhaust any number of allies → draw 1 card for each exhausted » |
| 38012 | Armor (Hisako Ichiki) | « Prerequisite (X-Men). Toughness. » pour « Play only if your identity has the X-MEN trait. Toughness. » |
| 52017 | Dr. Sinclair | texte identique (la note de SOURCES.md « carte absente du jeu » était fausse : elle existe, `52017`, pack `silk`) |
| 10031 | Electrostatic Armor | « Max 1. » pour « Max 1 per player. » ; existe aussi en exclusive TMNT `up010` (non concernée) |
| 52019 | Ready for a Fight | « They attack you instead. » pour « That enemy attacks you instead. » ; « Max 1. » ; a déjà l'art `tmnt` |
| 48012 | Rogue (Anna Marie) | « Rogue adds their TRAITS and printed THW/ATK to hers » : même effet ; ajoute « (Limit once per round.) » déjà présent dans le jeu |
| 27012 | Spider-UK (Billy Braddock) | « When Spider-UK defends an attack » pour « defends against an attack » |
| 27016 | What Doesn't Kill Me | texte identique ; existe aussi en exclusive TMNT `up042` (non concernée) |
