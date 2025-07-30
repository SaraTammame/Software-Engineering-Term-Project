const myTextarea = document.getElementById('log');
const wordCountDisplay = document.getElementById('wordCount');
const maxWords = 250;

myTextarea.addEventListener('input', function() {
    const text = myTextarea.value.trim();
    const words = text.split(/\s+/).filter(word => word.length > 0); // Handle multiple spaces
    const currentWordCount = words.length;

    if (currentWordCount > maxWords) {
        // Trim the text to the allowed word limit
        myTextarea.value = words.slice(0, maxWords).join(' ');
        wordCountDisplay.style.color = 'red'; // Indicate limit exceeded
    } else {
        wordCountDisplay.style.color = '#333'; // Default color
    }

    wordCountDisplay.textContent = `Words: ${currentWordCount} / ${maxWords}`;
});
