# Le plateau en portrait sur téléphone

**Décidé avec l'utilisateur le 11/09/2026**, en relevant point par point ce que
fait `play.marvelsimulator.com` sur un écran de téléphone.

Aujourd'hui, le téléphone reçoit `PlateauPaysage` et le portrait affiche
« Tourne ton téléphone » (spec du 07/09/2026, §3). Mesure du jour, à 844x390 :
les cartes sont trop petites pour être lues, un tiers de l'écran est du noir
perdu, aucun panneau ne dit quoi faire, et « Fin du tour » sort du cadre.

**On inverse.** Le téléphone ne jouera plus qu'en portrait.

## Ce qui a été relevé chez eux, et mesuré

- La page **ne défile pas** : `scrollHeight` = `innerHeight` = 844. Tout tient.
- Deux éléments collés : le bandeau du haut (`.strip`) et la barre du bas
  (`.board__bar`).
- Ce qui rend cela possible : la table n'est **pas** faite de cartes jouables.
  Le vilain, le complot et les alliés sont la **vraie carte en petit**, avec
  leurs chiffres en gros **à côté** — jamais posés dessus. Seule la main est en
  cartes qu'on lit à vue.
- Pendant la phase du méchant, le plateau est **assombri** et un panneau occupe
  le bas : surtitre `VILLAIN PHASE`, titre `THE MINIONS ACTIVATE`, une phrase
  d'explication, un bouton `CONTINUE`, et « See the board » dessous.

## Les décisions

| Sujet | Décision |
|---|---|
| Orientation | Portrait SEUL sur téléphone. Le paysage affiche « remets ton écran droit » : l'exact inverse d'aujourd'hui. |
| `PlateauPaysage` | N'est plus servi. Conservé dans le dépôt, sans être monté, jusqu'à ce qu'on décide de son sort sur pièce. |
| Tablettes | Reçoivent le plateau PC, pas le portrait. Un iPad en paysage a la place d'une vraie table. |
| Cartes | La vraie carte, en petit, avec les chiffres en gros à côté. Pas de médaillon abstrait. |
| Défilement | Aucun. Tout tient sur un écran, comme chez eux. |
| Lire une carte | **Tap = ouvrir, re-tap = fermer, appui long = jouer.** Trois sorties sans rien engager : re-tap, tap sur le voile, Retour d'Android. |
| La main | Rangée qui défile horizontalement, cartes à taille lisible. |
| Phase du méchant | La scène ACTUELLE, avec ses cartes, ancrée sur la moitié basse. Plateau assombri au-dessus. |
| Multijoueur | Un onglet par héros. Tout est visible, mains comprises. |
| Ambiance | Gardée, avec les réglages existants pour l'éteindre. |

## Le point technique à trancher dans le code

`REQUETE_MOBILE` vaut aujourd'hui `(max-width: 900px), (pointer: coarse)`. Cette
règle attrape les tablettes, que l'on veut désormais sur le plateau PC, et elle
ne sait pas distinguer un téléphone couché d'une tablette.

Le discriminant n'est pas la largeur mais le **petit côté** de l'écran :

    (max-width: 600px), (max-height: 500px)

- téléphone portrait (390x844) : largeur 390 → mobile ✅
- téléphone paysage (844x390) : hauteur 390 → mobile ✅, et on lui demande de
  se remettre droit
- tablette portrait (768x1024) : 768 > 600 et 1024 > 500 → plateau PC ✅
- tablette paysage (1024x768) : → plateau PC ✅

`?mobile` continue de forcer le mode depuis un PC, pour éprouver le rendu.

## Découpage

Un `PlateauPortrait.tsx`, choisi par `PlateauMobile` quand l'orientation est
portrait, et construit dans cet ordre :

1. bandeau de statut, et le bloc vilain (vignette + chiffres) ;
2. complot principal avec sa barre segmentée, et les compteurs de rencontre ;
3. ennemis engagés, héros, alliés ;
4. la main qui défile, et la barre du bas ;
5. le panneau d'action (`AssistantAction`, déjà refondu le 11/09) et la scène
   de phase du méchant ancrée en bas ;
6. les onglets du multijoueur.

## Ce qu'on réutilise sans y toucher

`ScanCard`, `AssistantAction`, `libelleQuiAgit` et `libellePhase`
(`etat-partie.ts`), `zones.ts` pour lire la table, `useAppuiLong` pour le
« jouer », `CarteApercu` pour la lecture d'une carte.

## Vérification

Tests unitaires sur la répartition des blocs et sur chaque bloc rendu, puis
captures réelles dans Chrome à 500x844 (le minimum qu'autorise une fenêtre
Chrome). Livraison en une fois, une capture à la fin, rien en ligne sans accord.
