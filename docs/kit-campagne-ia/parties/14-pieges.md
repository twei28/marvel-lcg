---

## 14. Les pièges déjà payés, classés — **lis-les avant d'écrire**

Chacun de ces pièges a déjà cassé une carte, un scénario ou une campagne du projet, **presque toujours sans
aucune erreur visible**. La source est indiquée entre parenthèses (annexes du zip).

### 14.1 Données (`cards.json`, scénarios, sets)

1. **Toutes les valeurs de `desc` sont des chaînes** (`"HP": "10"`).
2. **Un compteur de `desc.Uses` absent de l'énum `COUNTER` du moteur fait lever une assertion** : la carte ne se
   construit pas. Signale-le dans `BESOINS-MOTEUR.md` *avant* de livrer (`reference/compteurs.json`).
3. **Un mot-clé du texte absent de `desc` (ou l'inverse)** : « Uses (3 tactic counters) » sans `"Uses": "3,tactic"` →
   la carte entre en jeu sans compteur, son action reste **grisée pour toujours**, sans message. Certains attributs
   n'existent que pour certains types (`Uses` : Upgrade/Support/Attachment/Obligation/Environment ; `Villainous` :
   Minion) : le mettre ailleurs **empêche la carte de se générer**.
4. **`Victory: "0"` envoie la carte dans la pile de victoire** : ce n'est pas « neutre ».
5. **Le `*` n'a pas le même sens partout** : `HP`/menaces = « par joueur » ; `ATK`/`THW` d'un **allié** = dégâts
   consécutifs ; `SCH` avec `*` = multiplié par le nombre de joueurs (constat Skrull Menace : un `SCH` plein
   s'écrit `"2"`, jamais `"2*"`).
6. **`type: "SideScheme"` dans le JSON, `EncounterSideScheme` dans les scripts.**
7. **Le dossier d'un script est le `set_name` « nettoyé »** (`CleanName`) ; un dossier de set **sans
   `__init__.py`** rend toutes ses cartes **muettes, sans erreur** ; un script mal rangé aussi.
8. **L'extension de l'image est obligatoire** ; **les complots restent stockés en paysage** (le serveur les pivote).
9. **Un set de rencontre cité dans un scénario mais sans fichier se charge VIDE, sans erreur.**
10. **Les checksums** de `cards.json` et `sets_info.json` : un fichier au checksum faux est rejeté **en silence**.
11. **Un `card_id` est une clé partout** (image, texte français, script, scénario, carnet) : on ne le renomme pas.
12. **Un préfixe fan-made non déclaré, un numéro officiel emprunté, un identifiant en double** : le second écrase
    le premier, sans un mot.
13. **`full_link`** : la carte ne porte **rien d'autre** que `card_id` et `full_link`. **`ability_link`** : mêmes
    capacités, données propres. **Avant d'écrire un script, cherche si la carte existe déjà** (Web of Deceit :
    six `ability_link` à la place de six scripts).
14. **Le nom d'un set de rencontre (`name`) s'affiche tel quel** : casse normale.
15. **`_expert` ne figure jamais dans l'`id` d'un scénario de campagne** : l'écran prend la variante tout seul.
16. **Les stades** : le `villain` standard liste les stades 1-2, l'expert 2-3 ; les complots principaux sont une paire
    a/b **par stade**.

### 14.2 Scripts de cartes

17. **Aucune fonction, aucune chaîne de ciblage inventée** : une chaîne inventée ne lève **rien**, la carte est inerte.
18. **`CardFinder(name="* X")` ne trouve jamais rien** : le nom s'écrit sans l'étoile.
19. **Les mots-clés de `desc` ne se recodent pas** (Toughness, Surge, Guard… appliqués deux fois).
20. **Un filtre va dans `conditions`**, jamais en tête de l'opération : une capacité facultative est **proposée**
    dès que son message part.
21. **Les fabriques qui rendent une LISTE** (`GiveKeywordToAttached`, `GiveKeywordToInPlayWhenApplyThis`) : sans
    `*` pour la déplier, la carte se construit avec une liste dans sa liste et le moteur plante **à la
    génération** — **`test_cards` ne le voit pas**, seule une vraie partie l'attrape (Web of Deceit, deux fois).
22. **Le `Setup` d'une carte à mot-clé `Setup`** se code `AfterGameSetup` ; **`WhenCardSetup("This", …)` est
    réservé à la face 1A du complot principal.**
23. **Les PV sont portés par la CARTE, pas par la face** : une carte retournée à 0 PV arrive sur sa nouvelle face
    **déjà vaincue** et le moteur redéclenche la défaite pendant le retournement (Shocker se retournait sans fin :
    A → B → A…). Rends les PV à la face avant de retourner.
24. **Les capacités d'une carte dans la pile de victoire ne se déclenchent jamais** (hors jeu).
25. **Une obligation révélée reste en jeu** si le script ne la défausse pas : code toutes les branches.
26. **Ne réimplémente jamais le choix de face standard/expert** : la carte le fait (`StandardModeOnly()` /
    `ExpertModeOnly()`).
27. **Une limite imprimée (« once per round ») sur un déclencheur de défaite** : piège moteur connu, signale-le.
28. **`Puzzle.PutIntoPlay` sur une carte d'un paquet de scénario spécial ne l'attache pas** : utilise
    `Puzzle.Reveal` (chemin réel).
29. **L'unicité d'une FAMILLE de cartes** (WEB-WARRIOR ou « Spider » dans le titre) : `UniqueRuleNotApplyTo` ne sait
    viser qu'une carte : une capacité écrite à la main (écart assumé, écrit).
30. **Le résultat de fin de partie se lit dans le message** (`message.players_won`), jamais dans le monde.

### 14.3 Logique de campagne

31. **Une clé de carnet mal orthographiée ne lève rien** : la récompense disparaît en silence.
32. **Une face 1A qui n'appelle pas `*CampaignSetup(n)`** : le carnet est ignoré en silence ; **un `n` faux** applique les
    récompenses d'un autre scénario.
33. **Un collecteur qui plante n'écrit RIEN** et ne le dit qu'au journal du moteur (`s.GetThreatInternal()` n'existe
    pas : c'est la propriété `.threat`).
34. **L'estampille du carnet sortant doit égaler l'`id` du scénario** : sinon le panneau ignore **tout** le relevé du
    moteur (les unités de gmw n'arrivaient jamais au Marché).
35. **`player.GetHero()` lève une assertion en forme Alter Ego** ; utilise `identity.GetHeroFace()`.
36. **`Faces.ShuffleAllTo` ne mélange que s'il a déplacé quelque chose** : une carte générée directement dans le deck
    reste sur le dessus (les captifs de Mutant Genesis arrivaient dans la main de départ).
37. **La mise en place de campagne précède la pioche** (étape 13 puis 14) : une carte mélangée au deck par une
    récompense peut arriver en main ; « cherchez une carte et mettez-la en main » n'AJOUTE rien à la main.
38. **« may » / « any player's deck »** : le joueur choisit ; ne jamais mélanger d'office dans le deck du joueur 1.
39. **Une carte que le livret fait CHERCHER dans le deck** : déclare `deck: "requis"` ; sinon, si le joueur l'a retirée,
    la récompense disparaît.
40. **Le livret imprimé et le carnet imprimé font foi, pas le code** (Mutant Genesis : deux lignes d'alliés au carnet
    officiel, une seule collectée).
41. **Un champ `int` sans `detection` est un drapeau** : `"0"` est retiré avant l'enregistrement. Un champ `int` avec
    `detection` garde son `"0"` (vraie mesure).
42. **Une condition de champ inconnue MASQUE le champ** ; **une `detection` inconnue le laisse vide** : tous deux en
    silence.
43. **Ne garde que des clés déclarées** : le panneau ne reporte que celles de la description.

### 14.4 Textes, images, interface

44. **Un pack sans texte français est muet en français sans que rien ne le signale.**
45. **Vocabulaire officiel** ; jamais « étourdi », « Inébranlable », « Robustesse », « carte de statut Robuste » : une gate
    échoue.
46. **Noms propres et traits restent en anglais** dans le texte français.
47. **Les biographies de vilain s'indexent par le `card_id` de la première face**, jamais par le nom.
48. **Une planche posée en tête de la colonne de récit** de l'écran de campagne en ordre libre **pousse le carnet hors
    de l'écran** : un test d'écran vérifie la présence, pas la place ; regarde une capture.
49. **Les pages du livret sont carrées, 975 × 975** ; les pages françaises vont dans `fr/` ; `livret_fr: true` sinon
    l'écran ne les cherche pas.
50. **Une chaîne d'interface nouvelle sans entrée dans `dico-en`** reste en français dans l'interface anglaise.

### 14.5 Méthode et fidélité

51. **Transcris une planche de 4 cartes par lecture** : au-delà, le texte d'encart n'est plus sûr.
52. **Les fichiers de l'auteur font foi, pas les captures de son livret** (la page 15 du livret de Web of Deceit
    montre un Shocker que la carte du dossier ne porte plus).
53. **Les icônes de complot n'ont pas la même forme chez tous les auteurs.** Conventions **validées par l'utilisateur**,
    **propres à leur pack** : *Skrull Menace* (Kajislav) — Crise = « ! » dans une explosion ; Accélération = croix +
    pointe + barre ; Aléas (Hazard) = croix sur carte penchée ; Amplify = croix + avion ; « Y » rouge = icône de
    boost ordinaire ; ★ = renvoi au texte. *MC/DC Punisher 2026* — « !! » = Crise ; croix à trois pointes + = Amplify ;
    triangle « toit de maison » + = Accélération ; carré « carte + » = Aléas. **Compare toujours à une carte du
    MÊME pack dont l'icône est connue ; une icône inconnue → `QUESTIONS.md`.**
54. **Une carte « impr. Interrupt » dont le texte dit « After »** : question à l'utilisateur, **pas de correction
    silencieuse** (Swarmed by Rats, Hunting Season).
55. **« Je n'ai pas lancé » ≠ « c'est vert »** : écris-le. Une livraison antérieure ne devait pas être déclarée
    jouable avec des points ouverts.
56. **Une gate qui répond OK n'est pas une preuve tant qu'on ne l'a pas vue échouer** ; ne retire jamais une assertion
    parce qu'elle échoue (le défaut revient en jeu).
57. **Un cas de test peut être vert en n'exerçant rien** (une carte du deck paie à elle seule le coût ; le pilote décline
    les choix facultatifs) : fixe la main (`main_exclusive`), mesure un **chiffre**.
