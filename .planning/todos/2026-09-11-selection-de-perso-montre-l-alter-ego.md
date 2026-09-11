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
