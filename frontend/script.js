const inputData = document.getElementById('inputData');
const startButton = document.getElementById('start_button');
const outputData = document.getElementById('outputData');

let chosenFile = null;

inputData.addEventListener('change', (event) => {
    chosenFile = event.target.files[0]; 
});

startButton.addEventListener('click', () => {
    if (chosenFile) {
        const reader = new FileReader();

        reader.onload = (event) => {
            const fileContent = event.target.result;
            
            outputData.textContent = fileContent;
        };
        
        reader.readAsText(chosenFile);

    } else {
        alert("Пожалуйста, сначала выберите файл!");
    }
});