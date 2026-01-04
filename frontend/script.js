const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('csv-file');
const fileNameDiv = document.getElementById('file-name');
const submitBtn = document.getElementById('convert-btn');
const form = document.getElementById('converter-form');

// Отключаем дефолт 
dropzone.addEventListener('dragover', (event) => {
    event.preventDefault(); 
});

const handleFile = (file) => {
    if (file && file.name.endsWith('.csv')) {
        fileNameDiv.textContent = `Selected: ${file.name}`;
        fileNameDiv.hidden = false;        
        submitBtn.disabled = false;
        } else {
            alert('Please select a valid .csv file');
        }
};

// Действие Drag&Drop
dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    console.log('Dropped!');
    const droppedFiles = event.dataTransfer.files;
        
    if (droppedFiles.length > 0) {
        fileInput.files = droppedFiles;
        handleFile(droppedFiles[0]);
    }
});

// Действие вручную выбрать файл
fileInput.addEventListener('change', (event) => {
    console.log("Changed");

    const selectedFiles = event.target.files;
        
    if (selectedFiles.length > 0) {
        handleFile(selectedFiles[0]);
    }
});

// Действие POST запроса на бэк
form.addEventListener('submit', async (event) => {
    event.preventDefault();
    submitBtn.innerText = "Converting...";
    submitBtn.disabled = true;
    const formData = new FormData(form);
    const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
    });
});