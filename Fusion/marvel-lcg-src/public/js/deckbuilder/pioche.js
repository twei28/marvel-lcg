// Simulateur de pioche de l'éditeur de deck. Module pur.
// Testé par tools/tests-lanceur/deckbuilder-pioche.test.mjs.
"use strict";

/** Le paquet complet : cartes du héros puis cartes choisies, une entrée par exemplaire. */
export function construirePaquet(kit, choisies) {
    const paquet = [...(kit || [])].map((id) => String(id).split(",")[0]);
    for (const [id, n] of choisies) for (let i = 0; i < n; i++) paquet.push(id);
    return paquet;
}

/** Mélange de Fisher-Yates ; `alea` rend un nombre dans [0, 1). */
export function melanger(liste, alea = Math.random) {
    const copie = [...liste];
    for (let i = copie.length - 1; i > 0; i--) {
        const j = Math.floor(alea() * (i + 1));
        [copie[i], copie[j]] = [copie[j], copie[i]];
    }
    return copie;
}

/** C(n, k) en flottants : suffisant pour des paquets de 50 cartes. */
function combinaisons(n, k) {
    if (k < 0 || k > n) return 0;
    let r = 1;
    for (let i = 1; i <= Math.min(k, n - k); i++) r = (r * (n - k + i)) / i;
    return r;
}

/** Chance d'avoir au moins un des `k` exemplaires parmi `n` cartes tirées d'un paquet de `total`. */
export function probaAuMoinsUne(total, k, n) {
    if (k <= 0 || total <= 0) return 0;
    const tirees = Math.min(n, total);
    if (tirees <= 0) return 0;
    return 1 - combinaisons(total - k, tirees) / combinaisons(total, tirees);
}

/**
 * Chances par tour, en supposant une main entièrement rejouée à chaque tour :
 * au tour T, on a vu `taille * T` cartes. C'est un plafond, la vraie partie
 * en voit un peu moins quand on garde des cartes en main.
 */
export function probasParTour(total, k, taille, tours = [1, 2, 3]) {
    return tours.map((tour) => ({ tour, proba: probaAuMoinsUne(total, k, taille * tour) }));
}
