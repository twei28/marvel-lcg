# Les statistiques sont celles de la TABLE, pas du joueur

Constaté par l'utilisateur le 20/09/2026, pendant une partie à deux.
Diagnostiqué le même soir sur les données de production.

## Ce qui se passe

Un joueur ouvre « Stats » depuis son compte et voit des chiffres qui ne sont
pas les siens.

## Pourquoi

Deux appartenances se superposent, et l'une écrase l'autre.

1. **L'emplacement appartient au compte de l'HÔTE.** C'est écrit noir sur blanc
   dans `site/orchestrateur.py:192` : « CE N'EST PAS UNE TABLE JETABLE.
   L'emplacement appartient au compte, et ses dossiers survivent à l'arrêt du
   moteur. » Mesuré en production : onze emplacements, un compte distinct
   chacun, stable dans le temps.

2. **Le fichier de statistiques appartient à l'EMPLACEMENT.**
   `statistics-serveur-N.json`, désigné par `game_statistics_file` dans la
   configuration de chaque table, servi tel quel par
   `/get_statistics_json` (`engine/device/web/server/server_get.py:278`).

**Conséquence, et c'est exactement ce que l'utilisateur a vu :** l'invité qui
rejoint la table de quelqu'un d'autre lit les statistiques de l'HÔTE. Il n'a
aucun compteur à lui, parce que rien n'attribue quoi que ce soit à un siège.

**Conséquence symétrique, moins visible mais plus gênante à la longue :** les
chiffres de l'hôte sont gonflés par tout ce que ses invités ont fait sur sa
table. Ses dégâts infligés incluent les leurs.

Et ce sont des cumuls sans bornes : `statistics-serveur-1.json` porte
`games_new: 8`, `games_won: 3`, `games_lost: 6` — huit parties commencées,
neuf terminées, tout mélangé depuis l'ouverture du compte.

## Ce que la base du site sait, et ne sait pas

La table `parties` de `narwhal.db` ne porte que
`code, nom, hote, emplacement, ouverte_le, fermee_le`. **Aucun résultat, aucun
score, aucun siège.** Le site ne pourrait pas reconstruire des statistiques par
joueur même s'il le voulait : l'information n'est écrite nulle part.

## Ce qu'il faudrait

Rien de moins qu'une attribution par siège, et c'est un vrai chantier :

1. Le moteur sait qui occupe quel siège (`seat_passwords`, `tient_le_siege`).
   Il faudrait que les compteurs soient tenus **par siège** et non globalement.
2. À la fin d'une partie, verser le résultat de chaque siège vers le compte qui
   le tenait, via le site (qui connaît déjà l'hôte et pourrait connaître les
   invités).
3. Décider ce qu'on fait de l'historique existant. Les cumuls actuels ne sont
   attribuables à personne : les remettre à zéro est sans doute plus honnête
   que de les donner à l'hôte.

⚠ Vérifier si `achievements-serveur-N.json` a le même défaut. Il suit la même
logique de fichier par emplacement, donc probablement oui : un haut fait
débloqué par un invité irait au compte de l'hôte.

## En attendant

Le moins coûteux, et le plus honnête, serait de **dire** sur l'écran que ces
chiffres sont ceux de la table et non du joueur. Une limite dite vaut mieux
qu'une limite muette, et celle-ci fait lire à quelqu'un les chiffres d'un autre
en croyant que ce sont les siens.
