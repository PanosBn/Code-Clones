const number = parseInt(prompt('Enter a positive integer: '));
if (number < 0){
    number = Math.abs(number)
}
// The user provides a number that is the upper limit of the fibonacci sequence
function fibonacci_calc(number){
    
    let number1 = 0;
    let number2 = 1, nextTerm;

    console.log('Fibonacci Series:');
    nextTerm = number1 + number2;

    while (nextTerm <= number) {

        console.log(nextTerm);

        number1 = number2;
        number2 = nextTerm;
        nextTerm = number1 + number2;
    }
}