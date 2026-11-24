# Backlog 9 : coop locale, decks un héros après l'autre (20/10/2026)

Fiche d'origine : `2026-10-07-choix-des-decks-en-coop-locale-un-heros-apres-l-autre.md`.
Drapeau : `COOP_DECKS_SEQUENTIELS` (`Fusion/marvel-lcg-src/public/js/prepare/app.js`, près de `stepComplete`).

## Fait
En coop locale (2 à 4 héros, même poste, hors salon en ligne et hors création d'équipe de campagne) :
aucun deck n'est présélectionné ; l'étape Decks montre un héros à la fois ; le bouton du bas devient
« Valider le deck de <héros> » (grisé tant qu'aucun deck n'est cliqué), puis « Héros suivant » ; « Continuer »
n'apparaît qu'une fois tous les decks validés. Solo et salon inchangés.

## Questions tranchées par l'utilisateur (20/10/2026), implémentées
1. Retour arrière : FERMÉE. Changer le deck d'un héros déjà validé retire sa validation ; le bouton redevient
   « Valider le deck de <héros> » et « Continuer » disparaît jusqu'à la nouvelle validation.
2. Récapitulatif : FERMÉE. Un panneau « Récapitulatif des decks » remplace la liste, dans l'étape Decks, une fois
   tous les decks validés : une ligne par héros (portrait, deck), un bouton « Modifier » par ligne qui ramène à
   l'écran de deck de CE héros. Pendant une modification, le bouton du bas devient « Retour au récapitulatif »
   (si le deck a changé, il faut d'abord valider ; la validation ramène au récapitulatif).
3. Deck de base : FERMÉE. Le dernier deck joué avec ce héros porte une petite étiquette « Dernier utilisé »,
   sans être sélectionné (un clic reste obligatoire). Étiquette posée en coop locale seulement.
   Limite connue : elle n'est pas posée sur la version téléphone (PC seulement) ; si le dernier deck est dans
   « Paquets d'aspect » replié, l'étiquette n'est visible qu'une fois la section dépliée.

## Questions encore ouvertes
A. Modale « Arts alternatifs » : elle s'ouvre après chaque choix de deck et s'enchaîne donc pour chaque héros en
   coop. Options : la garder telle quelle ; ne la poser qu'une fois (après la dernière validation) ; la regrouper
   dans le récapitulatif. Recommandation : la garder telle quelle tant que personne ne s'en plaint, sinon la
   déplacer dans le récapitulatif.
B. Mode Bataille (2 ou 4 héros sur un poste) : il est soumis au même parcours séquentiel, faute de raison de
   l'exclure. À confirmer ou à exclure (une ligne dans `decksSequentiels()`).
