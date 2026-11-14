// Le rendu de l'onglet « Decks des joueurs » (site/static/admin-decks-joueurs.js).
//   node --test site/test-admin-decks-joueurs.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const { rendre } = createRequire(import.meta.url)('./static/admin-decks-joueurs.js');
const T = { aucun: 'Aucun', cartes: 'cartes', importer: 'Importer dans mon compte' };

test('liste vide : un message, aucun bouton', () => {
  const h = rendre({ comptes: [] }, T);
  assert.match(h, /Aucun/);
  assert.doesNotMatch(h, /<button/);
});

test('un bouton par deck, avec le compte et le deck en attributs', () => {
  const h = rendre({ comptes: [
    { compte: 'alice', decks: [{ id: 'a', nom: 'A', heros: 'Spider-Man', cartes: 40, date: '2026-10-19 10:00' },
                               { id: 'b', nom: 'B', heros: 'Hulk', cartes: 41, date: '2026-10-18 09:00' }] },
    { compte: 'bob', decks: [{ id: 'c', nom: 'C', heros: 'Thor', cartes: 38, date: '2026-10-17 08:00' }] },
  ] }, T);
  assert.equal((h.match(/<button/g) || []).length, 3);
  assert.match(h, /data-compte="alice" data-deck="b"/);
  assert.match(h, /Spider-Man · 40 cartes · 2026-10-19 10:00/);
  assert.match(h, /Importer dans mon compte/);
});

test('un nom de deck ecrit par un joueur ne casse pas la page', () => {
  const h = rendre({ comptes: [{ compte: 'x"><img src=x onerror=alert(1)>', decks: [
    { id: 'i', nom: '<script>alert(1)</script>', heros: '"&', cartes: 1, date: 'd' }] }] }, T);
  assert.doesNotMatch(h, /<script|<img/);
  assert.match(h, /&lt;script&gt;/);
});
