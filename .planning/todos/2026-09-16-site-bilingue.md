# Le site en deux langues, comme le jeu

**Demande de l'utilisateur, 16/09/2026** : « faire en sorte que tout soit
parfaitement bilingue. Tout, tout, tout. »

## Le constat qui a déclenché ça

Question posée le même jour : « est-ce que tout ce qui existe est en anglais et
en français ? ». Réponse : **non**.

| Partie | État |
|---|---|
| L'assistant de préparation | bilingue (`dico-en.js`) |
| Le plateau | bilingue (`dico-en.ts`) |
| Le deck builder, le salon | bilingues (ils importent le `t()` de l'assistant) |
| **Le site** (`orchestrateur.py`) | **français en dur** |

Ce n'est pas nouveau : le commit `1ca86e05` du 15/09 dit « le SITE n'avait
aucune gate, et 29 clés s'affichaient en français sur un écran anglais ». Le
sujet était connu, jamais traité au fond.

⚠ Et j'y ai ajouté du français en dur le jour même, avec la page
« Mes signalements » et son entrée dans la barre.

## L'ampleur, mesurée

**145 chaînes françaises visibles** dans `site/orchestrateur.py`, réparties
entre onze gabarits HTML (`PAGE`, `PAGE_FORMULAIRE`, `PAGE_ADMIN`,
`PAGE_SUIVI`, `PAGE_HORS_LIGNE`…) et le code lui-même.

## Le point dur : quelle langue parle ce visiteur ?

Le jeu garde son choix dans le `localStorage`, que le serveur ne voit pas. Le
site doit donc s'appuyer sur autre chose :

1. un **cookie** `nc_langue`, posé par le site et — c'est l'astuce — aussi par
   le jeu, sur le domaine parent, pour que le choix fait dans une partie suive
   sur le site ;
2. à défaut, l'en-tête **`Accept-Language`** du navigateur ;
3. à défaut, le français.

## Ce qui est fait (16/09/2026)

- **Le socle** : `site/langue.py`. Dictionnaire dont la clé est la phrase
  française, détection en trois temps, langue portée par le fil de la requête
  (un fil par requête : deux visiteurs peuvent lire deux langues à la seconde).
- **La gate** : `site/test_langue.py` refuse toute phrase passée à `t()` sans
  son anglais, et compte l'avancée.
- **Un bouton FR / EN sur le site**, qui pose le cookie sur le **domaine
  parent** : le choix suit entre le site et les tables `p<N>`. Sans lui, un
  navigateur réglé en anglais n'aurait eu aucun moyen de revenir au français,
  puisque le choix fait dans le jeu vit dans le `localStorage`.
- **53 phrases traduites** : le squelette de toutes les pages, la connexion et
  l'inscription, la barre, « Ta partie t'attend », l'attente du démarrage, la
  page des signalements, et les huit messages qui refusent une connexion.
- **Sept cas** de bout en bout dans `test_parcours.py`, dont la même page rendue
  dans les deux langues, et la vérification qu'il ne reste pas de français
  derrière.

## Ce qui reste

- **Les écrans d'administration** (`PAGE_ADMIN`, `PAGE_SUIVI`) : **hors
  périmètre**, décidé le 16/09/2026. Ce sont les outils de l'utilisateur, qui
  est francophone, et ils représentent près de la moitié du travail pour zéro
  joueur concerné.
- ~~La page hors-ligne, le bouton « Installer l'application »~~ ✅ **faits le
  16/09/2026**, ainsi que l'écran « Mot de passe enregistré ». **60 phrases**
  au total.

  ⚠ Les deux étaient des CONSTANTES, donc figées à la langue du démarrage du
  serveur, quand aucun visiteur n'existe. C'est le même piège que le pied de
  page et les états d'un ticket : ce qui parle au visiteur ne peut pas vivre
  dans une constante de module.

  ⚠ Et la page hors-ligne porte sa feuille de style : `.format` prenait ses
  accolades pour des champs et la route tombait. Ses trois champs sont
  substitués à la main.
- ⚠ **Ce que la gate ne voit pas** : une phrase écrite en dur SANS passer par
  `t()` lui échappe. Elle garantit que ce qui est traduit l'est vraiment, pas
  que tout est traduit.

## Statut

**Fini le 16/09/2026 côté joueurs.** Les écrans qu'un joueur traverse sont
bilingues de bout en bout : connexion, salon, choix de langue, page hors ligne,
bouton « Installer l'application », mot de passe enregistré. **60 phrases,
60/60 à la gate** (`site/test_langue.py`), `test_parcours.py` sans échec.

Restent en français, **sur décision** : `/admin` et `/suivi`, qui ne sont vus
que par l'administrateur.
