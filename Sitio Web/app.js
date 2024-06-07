// app.js

// Example coordinates and statuses from Python program
const boxes = [
    { id: 'box1', x: 473, y: 296, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
    { id: 'box2', x: 389, y: 296, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
    { id: 'box3', x: 473, y: 235, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
    { id: 'box4', x: 389, y: 235, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
    { id: 'box5', x: 473, y: 177, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
    { id: 'box6', x: 389, y: 177, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
    { id: 'box7', x: 473, y: 117, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
    { id: 'box8', x: 389, y: 117, width: 80, height: 55, status: 'green', info: 'Unoccupied' },
];

// Function to create bounding boxes
function createBoundingBoxes() {
    const container = document.querySelector('.container');
    boxes.forEach(box => {
        const div = document.createElement('div');
        div.id = box.id;
        div.className = 'bounding-box';
        div.style.left = `${box.x}px`;
        div.style.top = `${box.y}px`;
        div.style.width = `${box.width}px`;
        div.style.height = `${box.height}px`;
        div.style.borderColor = box.status;
        div.dataset.info = box.info;
        div.addEventListener('mouseover', () => showPopup(box));
        div.addEventListener('mouseout', hidePopup);
        container.appendChild(div);
    });
}

// Function to update bounding boxes' status
function updateBoundingBoxes(data) {
    data.forEach(box => {
        const div = document.getElementById(box.id);
        if (div) {
            div.style.borderColor = box.status;
        }
    });
}

function showPopup(box) {
    const popup = document.getElementById('popup');
    popup.textContent = box.info;
    popup.style.left = `${box.x + box.width*8}px`;
    popup.style.top = `${box.y + box.height*4.25}px`;
    popup.style.display = 'block';
}

function hidePopup(){
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
}

// Initial creation of bounding boxes
createBoundingBoxes();
