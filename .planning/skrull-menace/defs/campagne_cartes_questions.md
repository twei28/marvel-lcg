# Questions ouvertes — bloc CAMPAGNE_CARTES (sk263-sk289b)

Format : card_id, la phrase, les lectures possibles, celle retenue, le chemin de l'image
(`~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/Campaigns/Skrull Menace (Released)/…`).
Aucune de ces lectures ne bloque : chacune est implementee et couverte par un cas (`tools/cas/campagne_cartes.py`).

## Q1 — sk263 Crusader : « INITIATIVE » (ligne de traits)
- Phrase : « INITIATIVE. SKRULL. » (police des traits, en italique gras), aucune regle ecrite sur la carte.
- Lectures : (a) un TRAIT sans effet propre ; (b) un mot-cle maison (comme « Amplify ») dont la definition manque.
- Retenue : (a). Le brief laissait « mot-cle maison ? cherche » : recherche faite dans le moteur (aucune occurrence en dehors
  du set officiel « The Initiative »), dans les cinq transcriptions et dans le livret : rien ne definit un mot-cle
  « Initiative ». Trait declaratif ajoute a l'enum `TRAITS` ; fiche `docs/reference/mots-cles/initiative.md`.
- Image : `campaign allies/crusader.png`.

## Q2 — sk266 Skymax : « Response: When Skymax enters play »
- Lectures : (a) Reponse APRES l'entree en jeu ; (b) Interruption (« When »). Le type imprime est « Response ».
- Retenue : (a) (`AfterCardEnterPlay`). Aucune difference de resultat (le melange ne depend pas de l'ordre).
- Image : `campaign allies/skymax.png`.

## Q3 — sk273 Newbie Training : « defeat a non-ELITE SKRULL minion AND draw 1 card »
- Lectures : (a) un seul bloc facultatif (vaincre puis piocher) ; (b) vaincre facultatif, piocher toujours.
- Retenue : (a). Sans sbire SKRULL non Elite en jeu, la recompense n'est pas offerte (rien n'est pioche).
- Image : `campaign player side schemes/newbie training.png`.

## Q4 — sk271 Cloning Faux Pas : « deal UP TO 3 damage to EACH SKRULL minion engaged with them »
- Lectures : (a) le joueur declare UN montant (0 a 3), applique a chaque sbire ; (b) un montant par sbire.
- Retenue : (a) (`DeclareNumber(0, 3)` une fois). Sbires du vainqueur seulement (« engaged with them »), Elites compris.
- Image : `campaign player side schemes/cloning faux pas.png` (titre « Cloning Program » sous le scotch ; icone Acceleration).

## Q5 — sk272 Fickle Alliance : l'allie issu d'un sbire
- Phrase : « Treat that minion as an ally with a blank text box (except for TRAITS). Its THW is equal to its printed SCH and it
  takes 1 consequential damage after it thwarts or attacks. »
- Points tranches : PV de l'allie = PV imprimes du sbire (le texte ne dit rien ; sans PV l'allie serait vaincu en entrant) ;
  ATQ de l'allie = ATQ imprime du sbire ; texte blanc = les capacites du sbire disparaissent (traits gardes, mots-cles
  imprimes en `desc` perdus avec le texte) ; l'allie COMPTE contre la limite d'allies (c'est un allie) ; vaincu, la carte
  retourne a sa forme de sbire et va en DEFAUSSE DE RENCONTRE (c'est une carte rencontre : cas `sk272 ... l'allie issu du
  sbire, vaincu`), pas dans la defausse du joueur.
- Image : `campaign player side schemes/fickle alliance.png`.

## Q6 — sk268 « Chilly McHotpants » (War Skrull) : valeurs imprimees et moment de la conversion
- Phrase : « *Treat this ally as a minion engaged with you. » ; badge « SCH 2 » au lieu de THW ; ATQ « 2* » sans pastille.
- Retenue : la conversion a lieu des l'entree en jeu ; le `desc` d'un allie ne porte pas de cle `SCH` : la valeur 2 est ecrite
  `THW` dans le desc (le moteur la reprend comme MNG du sbire) ; l'etoile en exposant de l'ATQ n'a pas de valeur chiffree
  (decision NOTES.md) : ATQ 2, aucune pastille de degats consequents. L'affichage de la carte dit « SCH » (image).
- Quand le sbire est vaincu, la carte retourne dans la defausse de son proprietaire sous sa forme d'allie (`TreatAsMinion`).
- Image : `campaign allies/War Skrull.png`.

## Q7 — sk280 Princess Anelle : « skip the villain phase » et Alliance
- « Skip the villain phase » : la phase ENTIERE est sautee (menace de la manigance principale, activations, cartes rencontre, et
  AUSSI les fenetres de debut/fin de phase du mechant). Ajout minimal au moteur : `World.skip_villain_phases`
  (voir `defs/campagne_cartes_moteur.md`). Alternative rejetee : neutraliser les quatre etapes une a une (`jj/61020`), qui
  laisse partir les Reponses forcees « apres l'etape 2 » des scenarios (Super-Skrull, Paibok).
- Alliance : mot-cle natif reserve aux evenements ; sur un soutien on utilise la marque `cout_en_groupe` (modele sk189a). Sans le
  rappel imprime entre parentheses (la carte n'en imprime pas).
- Cout X : joueurs + ennemis SKRULL en jeu (sbires et mechant), relu a chaque calcul ; `desc.Cost` = 0.
- Image : `campaign supports/princess anelle.png`.

## Q8 — sk270 Buddy Training Program : X
- « X is equal to the villain's stage number » : cout ET plafond de la recompense, relus a chaque usage. Un mechant sans
  numero de stade (aucun dans le coffret) donnerait X = 0 (cout 0, aucune recompense).
- Image : `campaign player side schemes/buddy training program.png`.

## Q9 — sk279 Pool-O-Vision : le compte des icones
- « 1 card for each [Crisis], [Acceleration], [Amplify], and [Hazard] in play » : une carte PAR ICONE (une carte a deux icones
  compte deux fois), cartes de tous les joueurs et du camp rencontre, plafond de 3. Icones lues par `Worlds.GetIconsNum`.
- Icones : ordre Crisis, Acceleration, Amplify, Hazard (decision utilisateur du 15/10/2026).
- Image : `campaign supports/pool-o-vision.png`.

## Q10 — sk288 Sy-Torak Gem : « When your deck empties »
- Le moteur n'a pas de message « quand le deck se vide » (seulement `AfterDeckRunOut`, apres le dernier tirage). La capacite
  « Forced Interrupt » est donc declenchee juste apres que la derniere carte a quitte le deck. Resultat identique pour le joueur.
- « spend [energy] resource » : UNE ressource [energy] ; les ressources wild de la main comptent.

## Q11 — sk269 Xavin : « resolve that event's Hero Action ability »
- Retenue : l'Action de heros est resolue sans payer le cout de l'evenement et QUELLE QUE SOIT la forme du joueur (« resolve »,
  pas « play »). Limite du moteur (`CardFace.ResolveAbility`, comme `dz035`) : la cible est la PREMIERE cible legale, sans
  question au joueur. A confirmer en partie reelle sur un evenement a cible choisie (Haymaker, Uppercut).
- Image : `campaign allies/xavin.png`.

## Q12 — sk265 Paibok (allie) : Ténacité et cout « take 1 damage »
- Regle moteur (RR 1.8 : un cout de degats n'est paye que si TOUS les degats sont subis) : tant que Paibok a sa carte Robuste
  d'entree, sa Reponse ne peut pas etre payee. Cas `sk265 Paibok : tant qu'il est Robuste...` le mesure. Pas un defaut de
  script : c'est la regle ; a signaler a l'auteur (la Reponse n'est utilisable qu'apres avoir perdu le Robuste).

## Q13 — sk289a / sk289b Cooperation Progress Reminder
- Carte sans numero, deux faces : creee comme `Insert` (comme `rule_a` / `rule_b`), card_id `sk289a` (recto) et `sk289b` (verso),
  aucune capacite scriptee. Sa regle (victory display apres defaite d'un sbire ou d'une manigance annexe, en defaussant le dessus
  du deck) est le travail du bloc « campagne / Cooperation Area ». Choix des card_id : 289 est le premier numero libre apres 288.
- Images : `rulebook/cooperation progress reminder.png` et `… back.png`.

## Q14 — Classes de deck
- Toutes les cartes sont `Class` « Campaign;<aspect> » (`Campaign;Basic` pour les cartes grises, `Campaign;'Pool` pour les roses),
  comme `wd123`-`wd127` : elles n'entrent dans un deck que par la Cooperation Area.
