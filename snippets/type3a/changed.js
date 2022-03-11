const number = parseInt(prompt('Enter a positive integer: '));
if (number < 0){
    number = Math.abs(number)
}
// The user provides a number that is the upper limit of the fibonacci sequence
const flag = parseInt(prompt('Enter the flag variable: '));
function fibonacci_calc(number, flag){
    
    let n1 = 0, n2 = 1, nextTerm;
    flag = flag + 1;
    console.log('Fibonacci Series:');
    nextTerm = n1 + n2;

    while (nextTerm <= number) {

        console.log(nextTerm);

        n1 = n2;
        n2 = nextTerm;
        nextTerm = n1 + n2;
    }
}