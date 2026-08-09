const draggables = document.querySelectorAll('.draggable');
draggables.forEach(draggable => {
    let offsetX, offsetY;
    draggable.addEventListener('mousedown', (e) => {
        offsetX = e.clientX - draggable.getBoundingClientRect().left;
        offsetY = e.clientY - draggable.getBoundingClientRect().top;
        document.addEventListener('mousemove', mouseMoveHandler);
        document.addEventListener('mouseup', mouseUpHandler);
    });
    const mouseMoveHandler = (e) => {
        draggable.style.left = `${e.clientX - offsetX}px`;
        draggable.style.top = `${e.clientY - offsetY}px`;
    };
    const mouseUpHandler = () => {
        document.removeEventListener('mousemove', mouseMoveHandler);
        document.removeEventListener('mouseup', mouseUpHandler);
    };
});
export function centerDraggableDiv(draggable) {
    const bodyWidth = document.body.clientWidth;
    const divWidth = draggable.clientWidth;
    const centerX = (bodyWidth - divWidth) / 2;
    draggable.style.left = `${centerX}px`;
}
//# sourceMappingURL=draggable.js.map