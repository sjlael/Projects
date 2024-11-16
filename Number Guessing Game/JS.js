document.querySelectorAll('input[type="radio"]').forEach(function(radio){
    radio.addEventListener('change', function(){
        document.getElementById('startButton').disabled = false;
    });
});

document.getElementById('startButton').addEventListener('click', function(){
    const range = parseInt(document.querySelector('input[name="range"]:checked').value);
    const randomNumber = Math.floor(Math.random() * range) + 1;

    document.querySelectorAll('input[type="radio"]').forEach(function(radio){
        radio.disabled = true;
    });
    this.disabled = true;
    
    const container = document.querySelector('.container');
    container.innerHTML += `
        <p>Guess a number between 1 and ${range}:</p>
        <input type="text" id="userGuess"></input>
        <button id="guessButton">Guess</button>
        <div id="message"></div>
        <div id="guessesLeft">Guesses left: 3</div>
        <div id="guessList"></div>
    `;
    startGame(randomNumber, range);
});

function startGame(randomNumber, range){
    let guessesLeft = 3;
    document.getElementById('guessButton').addEventListener('click',function(){
        const userGuess = parseInt(document.getElementById('userGuess').value);
        const message = document.getElementById('message');
        const guessList = document.getElementById('guessList');

        if (isNaN(userGuess) || userGuess < 1 || userGuess >range){
            message.innerHTML = 'Please enter a valid number within the range.';
            return;
        }

        guessesLeft--;
        document.getElementById('guessesLeft').innerHTML = 'Guesses Left: ${guessesLeft}';

        let hint;
        if (userGuess === randomNumber) {
            hint = 'Correct. Well done!';
            endGame(true);
        } else if (userGuess < randomNumber) {
            hint = 'Too low. Try again!';
        } else {
            hint = 'Too high. Try again!';
        }
        message.innerHTML = hint;
        if (guessesLeft === 0){
            endGame(false);
        }
    });
}

function endGame(isWin){
    const message = isWin ? 'Congratulations!' : 'No more guesses left.';
    setTimeout(function(){
        alert (message);
        location.reload();
    }, 100);
}