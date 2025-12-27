const fileInput = document.getElementById('fileInput');
const startButton = document.querySelector('.start_button');
const fileOutput = document.getElementById('fileOutput');

let chosenFile = null;

fileInput.addEventListener('change', (event) => {
    chosenFile = event.target.files[0]; 
});

startButton.addEventListener('click', () => {
    if (chosenFile) {
        const reader = new FileReader();

        reader.onload = (event) => {
            const fileContent = event.target.result;
            
            fileOutput.textContent = fileContent;
        };
        
        reader.readAsText(chosenFile);

    } else {
        alert("Пожалуйста, сначала выберите файл!");
    }
});