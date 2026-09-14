# Défauts signalés en partie le 14/09/2026 — TOUT EST OUVERT, rien n'est déployé

**Fiche d'arrêt.** L'utilisateur a demandé de cesser les corrections et de tout
consigner : « arrête, tu vas arrêter de faire de la merde, tu vas faire un topo
complet de ce que je viens de te dire, la liste complète et détaillée, puis tu
vas mettre tout au backlog ».

Rien de ce qui suit n'est en production. Le dernier déploiement est
`b5c42238` ; tout ce qui a été écrit après est **commité localement ou même pas
commité**, et n'a été vu par personne en partie.

---

## Le reproche de fond, et il est juste

> « On dirait que tu ne vérifies pas et que tu ne vas pas jusqu'au bout des
> choses. Ce n'est pas vérifier de A à Z, ce n'est pas faire un truc, tu
> vérifies chaque truc. »

Constat : j'ai vérifié chaque MORCEAU que j'écrivais, jamais le DÉROULÉ. Le
défaut « ça continue tout seul » a été signalé **trois fois**, corrigé trois
fois sur trois causes différentes, parce qu'à chaque fois je m'arrêtais à la
cause que je venais de trouver au lieu de rejouer la phase entière.

**Ce qui a été fait contre ça** (`ui-check/tests/phase-sur-table.spec.ts`,
`npm run phase-sur-table`) : un test qui parcourt une phase ENTIÈRE, attend cinq
secondes à chaque étape SANS RIEN TOUCHER, et échoue si quoi que ce soit a
bougé ; plus un second qui compte les panneaux au centre. Les deux passent.
**Ce filet n'existait pas, et c'est ce qui manquait.**

---

## 1. « Ça continue tout seul sans que je mette Suivant »

**Signalé TROIS FOIS.** « Je te l'ai dit mille fois [...] ça ne devrait pas
arriver putain. »

Trois causes distinctes, trouvées l'une après l'autre :

| # | Cause | État |
|---|---|---|
| 1 | Le réglage « Avance toute seule » était GRISÉ hors du mode Détaillé, mais sa VALEUR s'appliquait quand même. Griser ne désactive pas. | Corrigé, **déployé** (`b201c6d4`), test `avance-auto-mode.test.ts` |
| 2 | Le mode lui-même, tant qu'il n'existait pas | sans objet |
| 3 | **Le cartouche acquitte le moteur TOUT SEUL sur une étape d'ANNONCE.** C'est la décision 7 de la spec du 07/09/2026 (« pas de clic sur *va attaquer* ») pour le mode Détaillé, et elle contredit exactement la sienne : deux clics par attaque, l'annonce portant le premier « parce que c'est là aussi où on peut choisir de défendre ». | Corrigé, **non commité** |

La règle du rythme est sortie dans `ui-app/src/board/cartouche-a-jour.ts`, avec
une gate de onze cas (`cartouche-a-jour.test.ts`). C'est la seule règle qui
décide du rythme de toute la phase, et une erreur dedans **ne se voit pas** :
rien ne plante, rien ne rougit, la phase défile.

---

## 2. Trois panneaux qui se superposent

> « On est quand même d'accord que là il y a trois trucs qui se superposent,
> c'est n'importe quoi. »

Capture à l'appui : le sélecteur de cibles (« CIBLES HORS TABLE »), le panneau
du moteur (« CHOISIR LA CIBLE ») et le cartouche replié (chronologie + « Le
moteur attend ta réponse ») s'affichaient **tous les trois au centre**.

Cause : depuis que le bouton a été centré (à sa demande), tout ce qui se posait
« au centre » s'y est retrouvé ensemble. Le cartouche n'a rien à ajouter à ce
moment-là : le panneau du moteur dit déjà qu'il attend, et il porte les boutons.

**Corrigé, non commité.** Le cartouche se tait ; le reste du récit (trait,
cartes sorties du paquet, ligne des temps) reste.

---

## 3. Le jeton de menace est un rond, pas un triangle

> « J'ai envie que la menace sur le trafic clandestin se mette quand je fais
> Suivant et qu'il ait déjà la même forme que le triangle là. Pourquoi tu me
> fais un rond ? »

Deux demandes dans la phrase, et **une seule est traitée** :

- **La forme** : j'avais dessiné un disque jaune alors que l'image du vrai
  jeton existait déjà (`components/jetons/menace.png`, le triangle), et servait
  à la scène du mode Détaillé. **Corrigé, non commité, JAMAIS VU À L'ÉCRAN.**
- ⚠ **LE MOMENT : NON TRAITÉ.** « Que la menace se mette quand je fais
  Suivant ». Aujourd'hui le jeton part dès que l'étape s'affiche, avant tout
  clic. Il devrait partir AU CLIC, comme la carte rencontre. À faire.

---

## 4. ⚠ RÉGRESSION en mode Détaillé : on ne sait plus quand on peut défendre

> « Et en mode détaillé il n'indique même plus quand on peut défendre etc, il
> fait cliquer sur la carte sans rien indiquer. C'est une putain de
> régression. »

**LE PLUS GRAVE DE LA LISTE** : ce mode est celui de tout le monde, il marchait,
et quelque chose de la journée l'a cassé.

**Cause NON TROUVÉE.** L'examen a commencé et n'est pas allé au bout. Ce qui a
été écarté par lecture, sans preuve en partie :

- `unCartouche` remplaçant `modePhase === 'detaille'` en huit endroits : les
  deux valent la même chose QUAND le mode est « detaille », donc pas de
  changement pour lui ;
- l'extraction de `cartoucheEstAJour` : la formule est équivalente à l'ancienne
  tant que `surTable` est faux ;
- le silence du cartouche devant la question : gardé par `surTable`.

**Pistes à ouvrir** : `questionEnScene` et `afficherDemandeCentrale`
(board.tsx), la prop `question` passée à `DeroulePhase`, et
`texteFenetreReponse()` dans la branche repliée. Le commit le plus suspect est
celui qui a introduit `sceneCentrale`/`unCartouche` (`56b6e6e8`), parce qu'il
touche huit conditions d'un coup.

⚠ **À vérifier EN PARTIE, pas par lecture.** C'est exactement l'erreur qu'il
reproche.

---

## 5. « Maîtres du Chaos révèle Maîtres du Chaos »

**Signalé DEUX FOIS** (d'abord « L'Homme-Radioactif révèle L'Homme-Radioactif »).
La première fois je l'avais classé « non reproduit », à tort : une capture
d'autoplay montrait `joueur_nom = 'Jessica Jones'`, donc la donnée était bonne
et j'en avais conclu qu'il n'y avait rien. **Le défaut n'était pas dans la
donnée, il était dans l'affichage.**

**CAUSE TROUVÉE, CORRECTION NON ÉCRITE.** Dans `DeroulePhase`, la traduction des
noms fait :

```ts
auteurNom: enFrancais(etape.carteId, etape.auteurNom)
```

`enFrancais(id, nom)` rend `nomFr(id) ?? nom`. Or sur une révélation, `carteId`
désigne **la carte révélée**, pas le héros qui la révèle. Le nom du héros est
donc remplacé par celui de la carte, des deux côtés de la phrase.

La ligne voisine (`cibleNom`) porte DÉJÀ ce cas particulier, écrit le
09/09/2026 pour une raison jumelle (« prendre carteId ici écrivait *Klaw attaque
Klaw* »). Le même piège, à une ligne d'écart, non vu.

**Correctif** : ne pas traduire l'auteur par `carteId` sur une révélation.
Il faudra un cas de test, ce fichier n'en a aucun sur ce point.

---

## 6. Le texte marvelcdb sous la carte agrandie est en ANGLAIS

> « Je suis en FR et le texte dans le tooltip sous la carte est en
> anglais............... »

Capture à l'appui : la carte Hulk agrandie, le bloc « MARVELCDB » en dessous,
en anglais, en pleine partie française.

**NON EXAMINÉ.** À chercher du côté du réglage « Textes marvelcdb » et de la
source qu'il interroge (le proxy réseau, coupé par défaut, contre le
dictionnaire local `noms-fr.ts` / `textes-fr-complets`).

⚠ **Troisième défaut de langue de la journée**, après les 61 clés sans
traduction anglaise et les noms anglais du bilan. Les deux premiers sont
corrigés et déployés. Celui-ci s'ajoute à la liste et suggère qu'il faudrait
une passe de langue à part entière, pas des correctifs au coup par coup.

---

## État exact du dépôt à l'arrêt

**Déployé** : jusqu'à `b5c42238` inclus.

**Commité mais PAS déployé** : rien.

**Écrit mais PAS commité** (donc perdu si on nettoie sans y penser) :
- `ui-app/src/board/cartouche-a-jour.ts` + son test (défaut 1, cause 3)
- la correction de la superposition, dans `DeroulePhase.tsx` (défaut 2)
- le jeton en triangle, dans `JetonMenaceVolant.tsx` et `board.css` (défaut 3,
  la forme seulement)
- `ui-check/tests/phase-sur-table.spec.ts` + son entrée dans `package.json` :
  le test de bout en bout

**Non écrit** : le moment du jeton (défaut 3), la régression du mode Détaillé
(défaut 4), « X révèle X » (défaut 5), le texte marvelcdb (défaut 6).

## Statut

Arrêté le 14/09/2026 à sa demande. **Six défauts, dont une régression sur le
mode que tout le monde utilise.** Rien ne doit être déployé avant que le
défaut 4 soit compris.
