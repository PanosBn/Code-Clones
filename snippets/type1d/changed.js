const number = parseInt(prompt('Enter a positive integer: '));
if (number < 0){
    number = Math.abs(number)
} 
// The user provides a number that is the upper limit of the fibonacci sequence
function fibonacci_calc(number){
    
    let n1 = 0, n2 = 1, nextTerm;

            console.log('Fibonacci Series:');
            nextTerm = n1 + n2;

    while (nextTerm <= number) {

        console.log(nextTerm);
            n1 = n2;
            n2 = nextTerm;
        nextTerm = n1 + n2;
    }
}