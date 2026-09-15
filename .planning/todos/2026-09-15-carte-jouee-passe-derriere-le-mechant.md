# Une carte jouée se pose derrière le méchant avant d'aller à la défausse

**Constat de l'utilisateur, 15/09/2026**, signalé en passant, à traiter plus
tard : « pourquoi les cartes que je joue, on dirait qu'elles se placent derrière
le méchant quand je les joue, avant d'aller à la défausse ».

## La cause, trouvée le 15/09/2026, aux DEUX bouts de la chaîne

Elle n'était pas dans l'animation, contrairement à ce que cette fiche
soupçonnait : c'était un PLACEMENT.

1. **Le moteur savait, et jetait l'information.**
   `Faces.MoveAllToProcessingArea` (`src/game/operate/faces.py:123`) range la
   carte en cours de résolution dans `player.area_processing` quand elle
   appartient à un joueur, et dans `world.area_processing` sinon. Mais
   `to_descriptor.py:82` **fusionnait les deux** en une seule liste au moment de
   publier la trame.
2. **Le plateau dessinait cette liste chez le méchant.**
   `zones.ts`, emplacement « Méchant » : `posees(world.area_processing, rendu)`,
   juste après les vilains. Toute carte en résolution atterrissait donc là,
   qu'elle soit jouée par toi ou révélée par le scénario.

D'où le trajet observé : la carte quitte ta main, vole vers la zone du méchant
(son vrai point d'arrivée dessiné), y reste le temps de sa résolution, puis
part à la défausse.

## Le correctif

- **Moteur** : `PlayerDescriptor.area_processing` publie la zone de résolution
  de chaque joueur à côté de ses autres zones. La liste fusionnée du monde
  **reste publiée telle quelle** : l'ancien client la lit, on ne la lui retire
  pas.
- **Plateau** : la résolution d'un joueur se dessine dans `terrain-soutien`,
  auprès de son héros. Ce que le scénario résout reste chez le méchant, et la
  liste du monde est filtrée de ce qui appartient déjà à un joueur, sinon la
  même carte serait dessinée deux fois.
- Un moteur antérieur ne publie pas le champ : l'ensemble est vide, rien n'est
  retiré, le plateau se comporte exactement comme avant.

### Ce qui le prouve

Trois cas dans `ui-app/src/board/carte-en-resolution.test.ts`, vus ROUGES
d'abord (« expected undefined to be defined », « expected 'rencontre' to be
'terrain-soutien' ») :

- l'événement joué se dessine dans `terrain-soutien` ;
- la traîtrise que le scénario résout reste dans `rencontre` (ce cas était vert
  dès le départ : c'est le témoin qui prouve qu'on n'a pas tout déplacé) ;
- publiée par les deux canaux, la carte n'est dessinée qu'UNE fois.

Batterie complète : 1570 cas verts, 138 fichiers, typage propre. Et le moteur
tourne toujours (`tools/test_manigance_face_a.py`, deux cas verts, qui montent
une vraie partie et rendent de vraies trames).

### ⚠ Ce qui n'est PAS prouvé

Personne n'a encore VU la carte se poser près du héros dans une vraie partie.
Les cas dessinent un monde construit à la main ; le champ moteur est vérifié
présent et rempli, pas observé de bout en bout. À confirmer à l'écran après le
prochain déploiement.

## Statut

Cause trouvée et **correctif écrit le 15/09/2026**, moteur et plateau. Non
déployé, et pas encore vu en jeu.

⚠ **Déployé le 15/09/2026 à 13h02, MOITIÉ SEULEMENT.** Le plateau est à jour
(bundle `board-DJhLSY-t.js, redeploye a 14h07 apres les correctifs de la relecture d'ensemble`). La moitié MOTEUR, elle, ne prendra effet qu'au
prochain démarrage du serveur : `launcher_fast.py` compile `src/` vers `.game`
AU LANCEMENT, un serveur déjà en marche garde son code en mémoire. Tant qu'il
n'a pas redémarré, il publie encore la liste fusionnée sans
`PlayerDescriptor.area_processing`, et le plateau se comporte comme avant, ce
qui est exactement le repli prévu.
