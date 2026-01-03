const fileInput = document.getElementById('upload-file');
const btn = document.getElementById('file-upload-btn');

btn.addEventListener('click', async function() {
    const formData = new FormData();
    formData.append('file', fileInput.files[0]); 
        const response = await fetch('http://localhost:8000/', {
            method: 'POST',
            body: formData 
        })
    }
);