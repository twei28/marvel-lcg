# Phase du méchant « Sur la table » — LA REFONTE, après la première partie jouée

**Fiche de travail, 14/09/2026.** La première version est décrite dans
`2026-09-14-phase-du-mechant-sur-la-table.md` ; elle a été jouée une fois, en
production, et l'utilisateur a listé ce qui n'allait pas. Cette fiche-ci porte
ce qu'il faut construire.

⚠ **LE MODE EST RETIRÉ DU SITE** le temps du chantier (sa décision). Il ne
s'affiche plus dans les Réglages, et un joueur qui l'avait choisi retombe sur
« Détaillé ».

⚠ **Vingt-sept décisions, prises en sept blocs de questions à sa demande
expresse** : « pose-moi encore au moins quarante questions parce que sinon on
va repartir dans vingt-mille sens [...] parce que tu vas de nouveau faire
n'importe quoi ». Rien de ce qui suit n'est une interprétation de ma part.

---

## Ce qu'il a constaté en jouant

> « Tout avance tout seul sans attendre le suivant. »

✅ **CORRIGÉ, et c'était le plus grave.** Le réglage « Avance toute seule » est
grisé hors du mode Détaillé (`FenetreReglages`, `disponible`) mais sa VALEUR
continuait d'être transmise au cartouche. Un joueur qui l'avait allumée en
Détaillé la gardait active ici, où le mode est défini par l'inverse.
**Griser n'est pas désactiver** : c'est à la source que ça se décide
(`avanceAutoActive`, board.tsx), et un test le verrouille
(`avance-auto-mode.test.ts`).

Les deux autres défauts vus sur sa capture, sans décision à prendre :
- l'encadré doré de la carte rencontre est **beaucoup plus grand que la carte
  qu'il contient** : `--card-w` l'emporte sur le `width:100%` de l'enveloppe ;
- la phrase dit « **L'Homme-Radioactif révèle L'Homme-Radioactif** » : sur une
  étape de révélation, `auteurNom` doit porter le HÉROS qui révèle, pas la
  carte révélée.

---

## 1. Le rythme et les arrêts

| # | Question | Décision |
|---|---|---|
| 1 | Étape où il ne se passe rien | **On la saute, mais on le dit** : la ligne des temps la barre d'un trait. |
| 2 | Fin de phase | **Un bilan**, comme aujourd'hui. C'est le seul panneau qui reste. |
| 3 | Revenir en arrière | **Oui, une petite flèche** à côté du bouton. |
| 4 | Tout passer | **Échap fait défiler**, comme dans le mode Détaillé. |

## 2. L'ouverture de la phase

| # | Question | Décision |
|---|---|---|
| 5 | Le bandeau | **Il joue SEUL**, et la première étape n'arrive qu'une fois qu'il est parti. C'est sa phrase : « d'abord le bandeau, puis après on montre la manigance. On attend que le bandeau soit parti. » |
| 6 | Sa durée | **~1,5 s**, puis il s'efface seul. Aucun clic. |
| 7 | Son texte | **« Phase du méchant · round 3 »**. |
| 8 | La ligne des temps | **Gardée, dans la barre du haut**, temps courant en surbrillance, passés cochés. |

## 3. La menace (point 1)

| # | Question | Décision |
|---|---|---|
| 9 | Le départ | **Un jeton part du MILIEU DE L'ÉCRAN** et vole jusqu'à la manigance visée. |
| 10 | Son allure | **Le jeton du jeu, avec son nombre dessus** (« +1 ») pendant le vol. |

## 4. L'attaque et la manigance du méchant (point 2)

| # | Question | Décision |
|---|---|---|
| 11 | Le découpage | **DEUX CLICS.** Clic 1 : l'annonce (« Klaw va attaquer Jessica Jones »), les boosts sortent FACE CACHÉE. Clic 2 : elles se retournent, le total paraît, le coup porte. |
| 12 | Pourquoi deux | Sa raison : « c'est là aussi où on peut choisir de défendre ». La fenêtre d'interruption est à l'annonce, et le moteur l'ouvre déjà là. |
| 13 | Les sbires | **Deux temps SEULEMENT si le joueur peut réagir.** Sinon le coup part en un clic. Le nombre de clics suit ce qu'on peut faire. |
| 14 | Où se posent les boosts | **Contre la carte du MÉCHANT qui frappe** (ou du sbire), plus près du deck rencontre. Le trajet depuis le paquet reste visible. |
| 15 | Leur dos | **Un vrai dos de carte rencontre.** |
| 16 | Le trait | **Dès l'annonce, AVEC le montant prévu** (l'attaque imprimée), qui devient le vrai chiffre après les boosts et la défense. |

## 5. Les nombres

| # | Question | Décision |
|---|---|---|
| 17 | Le total des boosts | **Le calcul entier** : « 3 imprimé + 1 boost = 4 ». |
| 18 | Quand on défend | **Le calcul complet dans la phrase** : « 4 dégâts, 3 bloqués, 1 encaissé », et le trait porte 1. |
| 19 | Les compteurs | **Au moment du coup, animés, ET le nombre perdu s'envole** (« -3 » rouge qui monte au-dessus de la carte). |
| 20 | Un boost à capacité | **Signalé, et son texte s'ajoute à la phrase.** |
| 21 | Le style de la phrase | **Texte normal, NOMS EN GRAS, nombre en couleur.** Pas de gros titre. |

## 6. Les trajets

| # | Question | Décision |
|---|---|---|
| 22 | Quand la carte rencontre part | **Au clic** : on lit, puis elle vole. |
| 23 | Sa vitesse | **2 secondes.** Un vrai trajet, pas un saut. |
| 24 | Vers la défausse | **Oui, on la voit y aller**, comme les autres. |
| 25 | Un sbire qui s'engage | **Le vol, PLUS un trait vers le héros, PLUS un tressaillement du héros à l'arrivée** (il a répondu « 2 et 3 »). |
| 26 | Sans destination | **Elle va à la défausse** : c'est sa place, il y a toujours une destination. |

## 7. Multijoueur et cas limites

| # | Question | Décision |
|---|---|---|
| 27 | Ce qu'on voit des autres | **Tout se joue sous tes yeux, mais tu ne cliques que pour tes étapes.** Les autres avancent quand leur joueur clique. |
| 28 | Rythmes différents à la table | **Chacun son rythme**, comme aujourd'hui entre Détaillé et Instantané. Le moteur attend déjà que tous aient accusé réception. |
| 29 | Une carte morte pendant la phase | **Pas de trait, la phrase suffit.** Le nom reste (le fait le porte en clair) ; on n'invente aucune position. |
| 30 | Le coup fatal | **Le panneau, mais APRÈS avoir vu le coup** sur la table : trait, dégâts, PV à zéro, puis le panneau. |
| 31 | La question du moteur | **Le panneau reste, mais AU CENTRE**, là où sont déjà l'œil et la souris. |
| 32 | Les sons | **Pas maintenant** : le chantier son est séparé et viendra après. |

## Ordre de construction

**Tout d'un coup**, sa décision : il ne rejoue qu'à la fin. Pas de livraison
intermédiaire à tester.

## Statut

Décisions prises le 14/09/2026, **non commencé**. Le mode est retiré du site
en attendant.
