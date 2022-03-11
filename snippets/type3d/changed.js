const number = parseInt(prompt('Enter a positive integer: '));
if (number < 0){
    number = Math.abs(number)
}
// The user provides a number that is the upper limit of the fibonacci sequence
function fibonacci_calc(n){
    
    if (n >=1000){
        prompt("You entered a very large number");
    }
    
    console.log('Fibonacci Series:');
    upcomingterm = n1 + n2;

    while (upcomingterm <= number) {

        console.log(upcomingterm);
        upcomingterm = nextTerm

        n1 = n2;
        n2 = nextTerm;
        nextTerm = n1 + n2;
    }
}