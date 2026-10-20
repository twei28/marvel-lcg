# Backlog 9 : coop locale, decks un héros après l'autre : trois questions ouvertes (20/10/2026)

Fiche d'origine : `2026-10-07-choix-des-decks-en-coop-locale-un-heros-apres-l-autre.md`.
Drapeau : `COOP_DECKS_SEQUENTIELS` (`Fusion/marvel-lcg-src/public/js/prepare/app.js`, près de `stepComplete`).

## Ce qui est déjà fait (non contesté)
En coop locale (2 à 4 héros, même poste, hors salon en ligne et hors création d'équipe de campagne) :
aucun deck n'est présélectionné ; l'étape Decks montre un héros à la fois ; le bouton du bas devient
« Valider le deck de <héros> » (grisé tant qu'aucun deck n'est cliqué), puis « Héros suivant » ; « Continuer »
n'apparaît qu'une fois tous les decks validés. Solo et salon inchangés. Les trois points ci-dessous
ont reçu le comportement le plus simple, décrit en « État actuel ».

## Question 1 : retour arrière sur un héros déjà validé

État actuel : on peut cliquer la pastille d'un héros déjà validé (rangée « Ton équipe ») pour rouvrir son
écran de deck ; on ne peut pas sauter vers un héros non encore atteint. Changer le deck d'un héros validé
ne retire pas sa validation (il reste valide avec le nouveau deck, bouton « Héros suivant » pour revenir).

- Option A (actuelle) : retour libre par les pastilles, validation conservée. Écran : rien de plus ; la pastille
  d'un héros validé porte le nom de son deck. Risque : un changement de deck passe sans re-validation.
- Option B : retour libre, mais un changement de deck retire la validation et demande de revalider.
  Écran : le bouton redevient « Valider le deck de X » après un clic sur un autre deck.
- Option C : aucun retour, seul « Retour » (étape Équipe) permet de tout reprendre. Écran : pastilles des héros
  validés non cliquables ; plus strict mais un oubli oblige à tout refaire.

Recommandation : B. Même souplesse qu'aujourd'hui, et la règle « un deck n'est joué que s'il a été validé »
reste vraie jusqu'au bout.

## Question 2 : récapitulatif avant le méchant

État actuel : aucun. Après le dernier « Valider le deck », le bouton « Continuer » mène directement à l'étape Méchant.
Le nom de chaque deck reste lisible sous chaque pastille de la rangée « Ton équipe ».

- Option A (actuelle) : pas de récapitulatif. Écran : inchangé.
- Option B : écran intermédiaire « Héros 1 : deck X, héros 2 : deck Y » avec « Modifier » par ligne et
  « Continuer ». Écran : une page de plus dans l'assistant (ou un panneau dans l'étape Decks).
- Option C : récapitulatif dans le panneau de gauche de l'étape Méchant, en lecture seule (rappel, sans étape de plus).

Recommandation : B sous forme de panneau dans l'étape Decks (après le dernier héros, la liste des decks est
remplacée par le récapitulatif, avec « Modifier » par ligne). Il réutilise le retour arrière de la question 1
et ne rajoute pas d'étape à la barre (Équipe, Decks, Méchant, Final).

## Question 3 : le deck de base, explicite

État actuel : le deck de départ du héros reste dans la liste (étiquette « Deck de départ ») mais n'est plus
présélectionné ; il se choisit en un clic comme n'importe quel autre. La mémoire « dernier deck utilisé pour ce héros »
n'est plus appliquée d'office en coop locale (elle l'est toujours en solo). Pour un héros sans deck de base,
rien ne change : les paquets d'aspect s'ouvrent d'office, sans être choisis.

- Option A (actuelle) : un clic sur le deck de départ, comme pour tout deck. Écran : liste telle quelle.
- Option B : mettre en évidence le dernier deck utilisé (liseré, étiquette « Dernier utilisé »), sans le sélectionner.
  Écran : un repère de plus sur une tuile, le clic reste obligatoire.
- Option C : bouton dédié « Jouer avec le deck de départ » à côté de « Valider ». Écran : un bouton de plus, un clic
  économisé (choix + validation en un geste).

Recommandation : B. On ne perd pas la mémoire des choix, et rien n'est jamais posé sans geste.

## Aussi à signaler
- La question « Arts alternatifs » (modale après chaque choix de deck) se pose pour chaque héros ; elle est
  inchangée et peut s'enchaîner deux fois en coop. À revoir si elle gêne le rythme.
- Le parcours séquentiel s'applique aussi au mode Bataille (2 ou 4 héros sur un poste), faute de raison de
  l'exclure ; à confirmer.
- Version téléphone : le bouton est partagé (`boutonPrincipalNav`) mais n'a pas été vérifié (PC seulement).
