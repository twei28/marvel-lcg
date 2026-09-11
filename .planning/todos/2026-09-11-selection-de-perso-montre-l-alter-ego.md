# La sélection de perso montre parfois l'alter ego en grand

**Signalé par l'utilisateur le 11/09/2026**, pendant le chantier Zeus, sans
capture : « à la sélection de perso, il montre des fois l'alter ego en grand
à la place de la carte héros, par exemple avec Wolverine et Storm ».

## Ce qu'on sait

- Deux héros nommés : **Wolverine** et **Storm**. Les autres montrent le
  héros, donc ce n'est pas le choix de face par défaut, c'est un cas
  particulier de ces packs.
- Piste à vérifier en premier : pour ces deux-là, l'identité a-t-elle sa face
  héros en `a` et l'alter ego en `b`, ou l'inverse ? Ou bien le `pic_id`
  de la face héros pointe-t-il sur le scan de l'alter ego ? Comparer avec un
  héros qui s'affiche bien.
- Écran concerné : l'écran de préparation (`public/prepare.html`,
  `public/js/prepare/`), pas le plateau.

## Ce qu'il ne faut pas faire

Ne pas corriger « au jugé » en inversant les faces : voir d'abord à quoi
ressemble le défaut sur les deux héros nommés, puis sur un troisième qui
marche (mémoire « demander à quoi ressemble le défaut »).

## ✅ RÉSOLU LE 11/09/2026 : les faces croisées des scans HD

Le défaut avait été trouvé et corrigé le jour même, dans le chantier des
scans HD (commit `2aade3bf`, « les faces d'identité croisées sont détectées
et redressées »). La scène de la sélection affiche le scan HD
(`/hd/<face>`), téléchargé chez les serveurs d'images officiels ; or ceux-ci
suivent la lettre IMPRIMÉE au coin de la carte, et FFG imprime l'alter ego en
« 1A » sur dix identités (Groot, Rocket, et toute la vague X-Men : Wolverine,
Storm...). Le fichier `35001a.jpg` téléchargé était donc Logan.

`tools/telecharger_scans_hd.py` compare désormais chaque paire a/b au scan
habituel de `assets/pics/` et échange les fichiers croisés (logique dans
`src/engine/lib/faces_hd.py`, partagée avec le moteur).

**Vérifié le 11/09/2026 au soir sur le serveur** : `assets/pics-hd/35001a.jpg`
et `36001a.jpg` y ont le même md5 qu'en local (`c62f318f…`, `771fce12…`), et
ces deux fichiers, ouverts, montrent bien Wolverine et Storm en héros.
