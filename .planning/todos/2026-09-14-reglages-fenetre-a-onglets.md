# Les réglages : une fenêtre à onglets, au lieu d'un menu dans un menu

**Constat de l'utilisateur, 14/09/2026** : « je ne trouve pas ça du tout
intuitif, dans le sens où il y a une colonne et puis quand j'ouvre les options,
il y a encore la colonne des options, et puis voilà ainsi de suite ».

Il a raison, et c'est mesurable. Aujourd'hui :

```
barre → [⚙ Réglages] → colonne 1 : Historique, Log, Vue,
                                   [⚙ Options] → colonne 2 : 18 réglages à plat
                                   Journal du héros, Log de la partie,
                                   Musique, Langue, Menu
```

**Deux engrenages, deux colonnes imbriquées**, et dans la seconde une liste de
18 réglages sans aucun regroupement, dont trois font apparaître ou disparaître
des sous-réglages en cours de route.

## Ce qui est décidé

Cinq questions posées une à une, cinq réponses.

| Question | Décision |
|---|---|
| **Forme** | Une **vraie fenêtre à onglets**, au centre de l'écran. Les réglages quittent le menu déroulant. Plus de colonne dans une colonne. |
| **Onglets** | **Quatre** : *Image et son*, *Déroulé de partie*, *Ambiance*, *Avancé*. |
| **Le reste** | Un **bouton « Partie » séparé** dans la barre : historique, log, journal, sauvegardes, quitter. La **Vue reste dans la barre** (elle change à chaque tour en multijoueur). |
| **Sous-réglages** | **Toujours visibles**, en retrait sous leur parent, **grisés et inertes** quand le parent est coupé. |
| **Téléphone** | Les onglets passent **en bandeau horizontal**, en pastilles qui glissent du doigt. |

## Le rangement, réglage par réglage

| Onglet | Réglages |
|---|---|
| **Image et son** | Animations · Sons · Musique · Succès · Scans en français · Textes marvelcdb (réseau) · Langue |
| **Déroulé de partie** | Phase du méchant (Détaillé / Instantané) · ┕ Avance toute seule · ┕ Vitesse du déroulé · Validation courte · Auto-ciblage · Cartes révélées |
| **Ambiance** | Ambiance · ┕ Aperçu d'ambiance · ┕ Demande d'ambiance |
| **Avancé** | Nouveau design · ┕ Actions (Simple / Détaillé) · Curseurs des autres joueurs · Disposition *(téléphone seulement)* · Raccourcis clavier |

## Les deux raisons de fond

⚠ **UN RÉGLAGE N'EST PAS UNE ACTION.** Historique, log, journal et sauvegardes
se consultent **en jouant**, souvent en urgence quand un bug vient de se
produire. Les enfermer dans une fenêtre de réglages obligerait à ouvrir une
modale pour lire un log. D'où le bouton « Partie » à part.

⚠ **UN SOUS-RÉGLAGE QUI APPARAÎT EST UN SOUS-RÉGLAGE QU'ON NE DÉCOUVRE JAMAIS.**
Le comportement actuel fait sauter la liste sous le doigt, et surtout : on ne
peut pas savoir que « Vitesse du déroulé » existe sans d'abord activer « Avance
toute seule ». Grisé et visible, il s'annonce lui-même.

## Ce qu'on ne touche pas

- Aucun réglage n'est supprimé, ajouté ni renommé : c'est un rangement, pas une
  refonte du contenu. Ce qui marche continue de marcher à l'identique.
- La **Vue** reste où elle est, dans la barre.
- Le mode feuille (`enModeFeuille`) ne montrait déjà pas le popover Réglages :
  il garde son comportement.

## Statut

Décisions prises le 14/09/2026, **en cours**.
