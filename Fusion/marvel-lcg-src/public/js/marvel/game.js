import { ClassName } from './class_name.js';
import { Message } from './message.js';
import { Cards } from './cards.js';
import { HoverCard } from './hover.js';
class GameStatistics {
    static async fetchStatistics() {
        try {
            const response = await fetch('/get_session_statistics');
            if (!response.ok) {
                throw new Error('Failed to fetch statistics');
            }
            const rawData = await response.json();
            GameStatistics.currentStats = Object.entries(rawData).map(([id, stats]) => ({
                id: parseInt(id),
                ...stats
            }));
            GameStatistics.renderTable();
        }
        catch (error) {
            console.error("Error fetching session statistics:", error);
            const table = document.getElementById('session-statistics');
            if (table) {
                table.innerHTML = '<tr><td colspan="4">Error loading statistics.</td></tr>';
            }
        }
    }
    static renderTable() {
        if (!GameStatistics.tableElement || GameStatistics.currentStats.length === 0) {
            if (GameStatistics.tableElement)
                GameStatistics.tableElement.innerHTML = '<tr><td>No statistics available.</td></tr>';
            return;
        }
        const headers = Object.keys(GameStatistics.currentStats[0]);
        GameStatistics.tableElement.innerHTML = '';
        const thead = GameStatistics.tableElement.createTHead();
        const headerRow = thead.insertRow();
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = GameStatistics.formatHeader(headerText);
            th.dataset.key = headerText;
            th.addEventListener('click', () => GameStatistics.handleSort(headerText));
            if (GameStatistics.sortKey === headerText) {
                th.textContent += GameStatistics.sortDirection === 'asc' ? ' ▲' : ' ▼';
            }
            headerRow.appendChild(th);
        });
        const tbody = GameStatistics.tableElement.createTBody();
        GameStatistics.currentStats.forEach(stats => {
            const row = tbody.insertRow();
            headers.forEach(key => {
                const cell = row.insertCell();
                if (key === 'id') {
                    const card = Cards.getCard(stats.id);
                    if (card && card.pic_id !== undefined) {
                        const img = document.createElement('img');
                        img.src = card.pic_id;
                        img.alt = `${card.pic_id}`;
                        img.style.width = '50px';
                        img.style.height = 'auto';
                        cell.appendChild(img);
                        cell.onmouseenter = () => {
                            HoverCard.showLogImage(stats.id, card.pic_id);
                        };
                    }
                    else {
                        cell.textContent = 'No Image';
                    }
                }
                else {
                    cell.textContent = stats[key].toString();
                }
            });
        });
    }
    static formatHeader(text) {
        return text.replace(/_/g, ' ')
            .replace(/\b\w/g, char => char.toUpperCase());
    }
    static handleSort(key) {
        if (GameStatistics.sortKey === key) {
            GameStatistics.sortDirection = GameStatistics.sortDirection === 'asc' ? 'desc' : 'asc';
        }
        else {
            GameStatistics.sortKey = key;
            GameStatistics.sortDirection = 'desc';
        }
        GameStatistics.currentStats.sort((a, b) => {
            const valueA = a[key];
            const valueB = b[key];
            if (valueA < valueB) {
                return GameStatistics.sortDirection === 'asc' ? -1 : 1;
            }
            if (valueA > valueB) {
                return GameStatistics.sortDirection === 'asc' ? 1 : -1;
            }
            return 0;
        });
        GameStatistics.renderTable();
    }
}
GameStatistics.currentStats = [];
GameStatistics.sortKey = null;
GameStatistics.sortDirection = 'asc';
GameStatistics.tableElement = document.getElementById('session-statistics');
export class Game {
    static setGameOver(game_over) {
        if (Game.game_over != game_over) {
            Game.game_over = game_over;
            if (Game.game_over) {
                document.body.classList.add(ClassName.game_over);
                console.log('Game over');
            }
            else {
                document.body.classList.remove(ClassName.game_over);
                GameStatistics.tableElement.innerHTML = '';
                document.getElementById('game-over-box-container').classList.remove('minimize');
                Message.cleanGameOverMessage();
            }
            if (Game.game_over) {
                setTimeout(async () => {
                    await GameStatistics.fetchStatistics();
                    GameStatistics.renderTable();
                }, 1000);
            }
        }
    }
}
Game.game_over = false;
Game.players_won = false;
Game.is_pause = false;
Game.is_lost_connect = true;
Game.forced_on_player = -1;
Game.total_players = 1;
Game.asking_players = [];
Game.current_step_id = -1;
window.Game = Game;
//# sourceMappingURL=game.js.map