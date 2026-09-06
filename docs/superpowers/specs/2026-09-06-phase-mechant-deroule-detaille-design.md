# Le déroulé détaillé de la phase du méchant

Conception validée le 06/09/2026, question par question, avant toute ligne de
code. Ce document fait foi : ce qui n'y est pas n'est pas décidé.

## Le problème

Deux plaintes, dans ces mots-là : **« on ne comprend pas ce qui vient de se
passer »** et **« on ne voit pas assez les cartes »**.

Ni la lenteur ni l'esthétique ne sont en cause. Ce qui manque, c'est de pouvoir
suivre la phase du méchant pendant qu'elle se joue : chaque étape doit être
détaillée, impossible à rater, validée avant la suivante, et très visuelle.

## Ce qui existe déjà, et qu'on ne refait pas

- `RecapPhaseMechant.tsx` (689 lignes) : le bilan groupé de fin de phase, bâti
  sur les entrées du journal. Il découpe la phase selon les quatre points de la
  carte de référence et met les faits en phrases.
- `CouchePasAPas.tsx` + `pas-a-pas.ts` : le halo qui met en lumière l'étape
  courante, posé en impératif sur le DOM pour ne pas re-rendre le plateau.
- `HistoriquePartie.tsx` : une entrée par fait, avec `cibleId`, `type`, `valeur`
  et la phase où elle est née. C'est notre source de vérité.
- Le tempo : `moteur.ts` retient l'accusé de réception (`/client_updated`) le
  temps qu'une étape se lise. Le moteur attend sans limite, aucun monde n'est
  mis en tampon.

## Décisions

### Le mode

Un quatrième mode, nommé **« Détaillé »**, qui **devient le mode par défaut** et
remplace « manuel » à cette place. « Pas à pas » et « Instantané » restent
disponibles pour qui veut accélérer.

Le menu Options présente les **quatre modes avec une phrase d'explication
chacun**, au lieu du bouton qui cycle aujourd'hui. Le choix est **retenu d'une
partie à l'autre**, comme les animations, le son et la langue.

### La forme d'une étape

**Sur le plateau, autour de la carte.** La carte concernée s'agrandit à sa
place, le reste du plateau est **assombri mais reste lisible** — on doit
continuer à voir la manigance monter ou un héros encaisser ailleurs.

Le **cartouche est fixe, en bas au centre**, au-dessus de la main. Il porte le
fil de progression, le texte de l'étape, le rappel de règle et les boutons. Il
ne bouge jamais : l'œil sait où lire et la main où cliquer dès le deuxième tour.

La carte mise en avant s'affiche **à la taille de l'aperçu au survol** (~300 px
de large), déjà validée comme lisible sur ce plateau.

> **Exigence explicite, née d'un défaut constaté en jeu :** toutes les cartes
> mises en avant ont **la même taille**, quel que soit leur rôle (méchant,
> sbire, boost, traîtrise). Les cartes **en paysage** (complots) gardent leur
> format paysage mais **la même taille relative** que les autres. Aujourd'hui ce
> n'est pas toujours le cas.

### Naviguer

- **« Suivant »**, bouton bien visible, toujours au même endroit. Raccourcis :
  **Entrée** et **Espace**.
- **« Précédent »** : on peut revenir relire une étape déjà passée. Purement
  visuel — rien n'est rejoué dans la partie.
- **« Tout dérouler »**, discret, à côté de « Suivant ». Raccourci **Échap**.
  Les étapes restantes **défilent sans attendre** (rien n'est sauté, on peut
  encore apercevoir ce qui se passe), puis le bilan s'affiche.
- Pendant une étape, **le plateau reste consultable** : on survole une carte
  pour l'agrandir, on ouvre le journal, on regarde la défausse. Seules les
  actions de jeu sont bloquées, ce n'est pas notre tour.
- **« Annuler la dernière action » reste actif**, comme aujourd'hui.

### Le fil de progression

Les **quatre temps de la carte de référence** — Menace, Activations,
Distribution, Révélation — affichés **en haut du cartouche**, l'étape courante
mise en avant.

### L'annonce de phase

Un **bandeau rouge qui traverse tout l'écran**, la phrase qui s'affiche, **et un
éclair**. Durée : **2 secondes** aux rounds 1 à 3, puis **1 seconde à partir du
round 4**.

### Les étapes, une par une

**1. Menace sur la manigance principale.** La manigance en grand, **avec le
détail par héros** : « +1 pour Shuri, +1 pour Thor ». **Même présentation en
solo**, où la liste tient sur une ligne : un seul comportement à apprendre.

**2. Activation du méchant.** Un **trait fin terminé par une pointe de flèche**,
tracé de l'attaquant vers sa cible, qui reste affiché pendant l'étape.

Quand le héros peut défendre avec un allié, **trois temps** : l'attaque
s'annonce, on choisit, puis l'impact tombe. On décide en voyant la menace
arriver.

**3. Activation des sbires.** **Un sbire = une étape à valider.** Trois sbires
font trois étapes.

**4. Cartes rencontre.** **Distribution puis révélation, en deux temps** : on
voit d'abord la carte face cachée arriver devant chaque héros, puis chaque carte
se retourne à son tour.

Une carte qui pose une question au joueur **reste à l'écran pendant le choix**,
les options affichées dessous.

**5. Passage du premier joueur.** Une étape brève, **à plusieurs seulement** :
en solo le jeton ne bouge pas réellement.

### Les boosts

**Retournés un par un, en grand.** Ils **s'enchaînent seuls**, **1,5 seconde
chacun** — de quoi lire un boost à capacité — et c'est l'étape d'attaque qui
attend la validation. Un seul clic pour toute l'attaque.

### Les impacts

**Chiffre qui jaillit, jauge qui bouge, et secousse de la carte.** La secousse
est **brève et franche** : deux ou trois oscillations sur ~200 ms, quelques
pixels d'amplitude.

### Les cas particuliers

- **Ennemi étourdi** : étape complète. Le jeton se consume, l'attaque est
  annulée. C'est le résultat d'un choix du joueur, il se voit.
- **Étape sans contenu** (aucun sbire, rien à révéler) : **affichée quand même**,
  pour marquer le passage. **Cartouche seul, au même endroit**, sans rien mettre
  en avant sur le plateau.
- **Cascade d'une carte rencontre** : la carte, puis **chaque conséquence l'une
  après l'autre** — les dégâts, la menace, la pioche.
- **Héros vaincu** : une étape à lui seul. **Un allié qui tombe, non** : c'est
  son rôle, il reste une conséquence dans la cascade.
- **Statut gagné par un ennemi** : pas d'étape, c'est une conséquence de la
  carte qui l'a posé, avec le halo de statut qui existe déjà.
- **Sbire qui entre en jeu en pleine phase** : sa mise en jeu, puis son attaque,
  **séparément**.
- **Défaite en pleine phase** : le coup fatal s'affiche normalement et c'est
  **après validation** que vient l'écran de fin. On comprend ce qui nous a tués.
- **Fait que le journal ne sait pas mettre en phrase** : on montre **la carte,
  avec le texte brut du moteur dessous**. Mieux vaut un texte technique qu'un
  silence.

### Les décisions du joueur

Les moments où le joueur décide vraiment (défendre ou non, jouer une réponse,
choisir une cible) sont **très différents à l'œil** : couleur, cadre et libellé
distincts. Le risque à écarter est de cliquer « Suivant » sans voir qu'on
renonçait à défendre.

### Le texte

**Des phrases écrites par nous** — « Ultron frappe Shuri de 4 dégâts » — et non
la narration brute du moteur. Le récap sait déjà les fabriquer : on réutilise
cette mécanique.

**Une ligne discrète rappelle la règle** en cours d'application : « Point 1 de
la phase du méchant : chaque joueur ajoute 1 menace à la manigance
principale. » On apprend en jouant, et on vérifie que le moteur fait juste.

**Français et anglais dès le départ**, par le dictionnaire, comme le reste du
plateau.

### Les couleurs

Le rouge du camp adverse, **`#F0131E`**, pour le bandeau et le cartouche. Le
trait est **fin (2-3 px), dans ce rouge, avec une légère lueur**.

### Le son

Sur les **moments forts seulement** : l'annonce de phase, l'impact d'une
attaque, un héros vaincu. Pas sur chaque étape, sinon c'est du bruit.
Débrayable comme le reste.

### Sans animations

Le réglage « animations coupées » et la préférence système enlèvent le bandeau,
l'éclair, la secousse et le défilement des jauges. **Les étapes, les cartes, les
textes et les validations restent identiques** : couper les animations ne veut
pas dire vouloir moins de détail.

### Sur mobile

**Version simplifiée** : les étapes principales, sans les cascades détaillées,
faute de place.

### Au-delà de la phase du méchant

Le même cartouche sert aux **effets subis pendant notre tour** (obligation,
réponse forcée), **sans le bandeau ni le fil**, qui n'ont pas de sens hors de la
phase.

### Reprise

Après un rechargement ou une reconnexion en pleine phase, **on reprend à l'étape
en cours** : le moteur attend toujours au même endroit. Ce qui est passé reste
dans le journal.

### À plusieurs

**Celui qui tient l'écran valide pour tous**, y compris les attaques subies par
les autres héros. C'est déjà le fonctionnement du hot-seat.

## Architecture

**Fondation : ce que le plateau reçoit déjà**, et rien de neuf côté moteur.

Deux sources, et le récap les combine déjà — précision apportée à la relecture
du code, la formulation « le journal seul » était incomplète :

1. **Les faits structurés du moteur** (`World.faits_mechant`, type `FaitMechant`
   dans `world.ts`). Pour chaque activation résolue : `auteur`, `cible`, `base`,
   `boost`, `defense`, `inflige`, `subi`, `restant`, la `phase` où elle a eu
   lieu, la `cause` éventuelle, et le détail des boosts avec leur apport. Une
   déduction ne saurait pas dire « 5 dégâts = 3 de base + 2 de boost », et
   compterait plusieurs fois ce que le moteur rend plusieurs fois autour d'une
   seule résolution.
2. **Les entrées du journal** pour tout ce que les faits ne couvrent pas : les
   cartes révélées, la menace posée, les statuts.

On ne relit pas le monde pour déduire, et **on n'ajoute aucun flux d'événements
au moteur Python** : ces deux sources existent et sont déjà consommées.

> ⚠ **DÉPASSÉ le 06/09/2026 (tâche A2 de l'audit de la phase du méchant).** Les
> deux sources n'avaient pas la même durée de vie : les faits voyagent avec le
> monde, le journal est reconstruit dans le navigateur et un F5 en pleine phase
> le perdait pour de bon (constat F4). Et le temps DISTRIBUTION n'avait aucune
> source du tout (constat M3). Le moteur enregistre donc DÉSORMAIS aussi la
> menace du point 1, la distribution du point 3 et les révélations du point 4,
> aux trois endroits où il les produit (`MainScheme.Phase`,
> `PlayerAction.DealEncounterCard`, `PlayerAction.RevealEncounterCards`).
> `etapesDeroule` lit tout depuis `faits_mechant` ; le journal ne lui sert plus
> que d'un repli de compatibilité, temporaire, pour un moteur pas encore mis à
> jour. « Aucun flux ajouté au moteur » ne vaut plus.

**Un composant nouveau, séparé** du récap. Le récap garde son rôle — le bilan de
fin, **conservé mais raccourci** — et les deux partagent la lecture des faits,
extraite dans un module commun.

Découpage visé :

- `deroule-phase.ts` — pur, testable sans navigateur : des entrées d'historique
  vers une liste d'étapes (titre, règle, cartes à mettre en avant, cible,
  boosts, conséquences).
- `DeroulePhase.tsx` — le cartouche, le fil, la mise en avant, les boutons.
- La mise en scène (bandeau, éclair, trait, secousse) en couches à part, sur le
  modèle de `halo-statut.ts` : classes CSS posées en impératif, jamais un
  re-rendu du plateau pour une décoration.

**Le tempo ne change pas** : le moteur attend notre validation, comme le
pas-à-pas d'aujourd'hui. Rien n'est mis en file d'attente ; on n'affiche jamais
un passé pendant que le plateau réel serait en avance.

## Vérification

**Tests durs sur la lecture des faits** : quelles étapes naissent de quelles
entrées, dans quel ordre, avec quel texte, dans les deux langues. C'est ce qui
se raisonne, donc ce qui se teste.

**Contrôle visuel** pour l'animation et la mise en page, sur de vraies parties.

## Livraison

**Le squelette d'abord, la mise en scène ensuite.**

1. **Les quatre temps complets, sans effets** : toutes les étapes, leurs textes
   en français et en anglais, la carte mise en avant, « Suivant », « Précédent »
   et le fil. **Jouable de bout en bout dès cette première livraison.**
2. La mise en scène : bandeau, éclair, trait fléché, secousses, sons.
3. Les cas particuliers et le mobile.

## Points laissés ouverts

- La forme exacte de l'éclair reste à dessiner.
- Le comportement quand une étape dure très longtemps parce que le joueur s'est
  absenté : rien de prévu, le moteur attend sans limite.
- La version mobile simplifiée n'est pas détaillée : elle sera cadrée au moment
  de la livraison 3.
