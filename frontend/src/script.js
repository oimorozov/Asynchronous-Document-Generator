const API_BASE = "http://localhost:8000/api/v1";

const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('csv-file');
const fileNameDiv = document.getElementById('file-name');
const submitBtn = document.getElementById('convert-btn');
const form = document.getElementById('converter-form');
const statusBlock = document.getElementById('status-block');
const statusText = document.getElementById('status-text');
const downloadLink = document.getElementById('download-link');

dropzone.addEventListener('dragover', (event) => {
    event.preventDefault();
});

const handleFile = (file) => {
    if (file) {
        fileNameDiv.textContent = `Выбран файл: ${file.name}`;
        fileNameDiv.hidden = false;
        submitBtn.disabled = false;
        return;
    }
    alert('Пожалуйста, выберите файл');
};

const updateStatus = (text) => {
    statusBlock.hidden = false;
    statusText.textContent = text;
};

const resetDownload = () => {
    downloadLink.hidden = true;
    downloadLink.href = "#";
};

const pollStatus = async (id) => {
    const response = await fetch(`${API_BASE}/status/${id}`);
    if (!response.ok) {
        throw new Error("status request failed");
    }
    return await response.json();
};

dropzone.addEventListener('drop', (event) => {
    event.preventDefault();
    const droppedFiles = event.dataTransfer.files;
    if (droppedFiles.length > 0) {
        fileInput.files = droppedFiles;
        handleFile(droppedFiles[0]);
    }
});

fileInput.addEventListener('change', (event) => {
    const selectedFiles = event.target.files;
    if (selectedFiles.length > 0) {
        handleFile(selectedFiles[0]);
    }
});

form.addEventListener('submit', async (event) => {
    event.preventDefault();
    resetDownload();
    updateStatus("Загрузка файла...");

    const formData = new FormData(form);
    const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        updateStatus("Ошибка загрузки");
        return;
    }

    const jsonResponse = await response.json();
    const taskId = jsonResponse.id;

    submitBtn.innerText = "Обработка...";
    submitBtn.disabled = true;
    updateStatus(`В очереди. Задача #${taskId}`);

    const pollInterval = setInterval(async () => {
        try {
            const data = await pollStatus(taskId);
            updateStatus(`Статус: ${data.status}`);

            if (data.status === "COMPLETED") {
                clearInterval(pollInterval);
                downloadLink.href = data.download_url;
                downloadLink.textContent = `Скачать результат (${data.filename})`;
                downloadLink.hidden = false;
                submitBtn.innerText = "Готово";
            } else if (data.status === "FAILED") {
                clearInterval(pollInterval);
                updateStatus("Ошибка обработки");
                submitBtn.innerText = "Конвертировать в PDF";
                submitBtn.disabled = false;
            }
        } catch (e) {
            clearInterval(pollInterval);
            updateStatus("Ошибка статуса");
            submitBtn.innerText = "Конвертировать в PDF";
            submitBtn.disabled = false;
        }
    }, 2000);
});