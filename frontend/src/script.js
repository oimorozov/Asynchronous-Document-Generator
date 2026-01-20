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
async function pollForFile(filename) {
    const response = await fetch(`http://localhost:8000/status/${filename}`); 
    const data = await response.json();

    if (data.status === 'uploaded') {
        submitBtn.innerText = "Downloaded!";
        const file_url = `http://localhost:8000/download/${data.filename}`
        downloadFile(file_url); 
    } else {
        setTimeout(() => pollForFile(filename), 2000);
    }
}

async function downloadFile(url) {
    const a = document.createElement('a');
    a.href = url;
    a.download = '';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Действие Drag&Drop
dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    console.log('Dropped');
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

    const formData = new FormData(form);

    const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData
    });

    const json_response = await response.json();

    console.log(`status=${json_response.status}`);
    console.log(`filename=${json_response.filename}`);
    if (response.ok) {
        submitBtn.innerText = "Converting...";
        submitBtn.disabled = true;
        pollForFile(json_response.filename)
    } else {
        alert(`Error: ${json_response.message}`);
        submitBtn.innerText = "Конвертировать в PDF";
        submitBtn.disabled = true;
    }
    submitBtn.disabled = false;
});