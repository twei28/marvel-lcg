"use strict";
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let mouseX = 0;
let mouseY = 0;
document.addEventListener('mousemove', (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
    drawLines();
});
function drawLines() {
    const boxes = document.querySelectorAll('.card.highlight-effect');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    boxes.forEach(box => {
        const rect = box.getBoundingClientRect();
        const boxX = rect.left + rect.width / 2;
        const boxY = rect.top + rect.height / 2;
        const transformedBoxX = boxX;
        const transformedBoxY = boxY / Math.cos(20 * Math.PI / 180);
        ctx.beginPath();
        ctx.moveTo(transformedBoxX, transformedBoxY);
        ctx.lineTo(mouseX, mouseY);
        ctx.strokeStyle = 'green';
        ctx.lineWidth = 2;
        ctx.stroke();
    });
}
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    drawLines();
});
//# sourceMappingURL=canvas.js.map