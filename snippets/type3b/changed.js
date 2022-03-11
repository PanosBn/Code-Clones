const number = parseInt(prompt('Enter a positive integer: '));
if (number < 0){
    number = Math.abs(number)
}
function fibonacci_calculation(number){
    
    let n1 = 0, nextTerm;
    let n2 = n1 + 1; //Added this little change here with n2 taking its value from n1
    console.log('Fibonacci Series:');
    nextTerm = 0 + n2;
    
    while (nextTerm <= number) {

        console.log(nextTerm);

        n1 = n2;
        n2 = nextTerm;
        nextTerm = n1 + n2;
        cubedTerm = 0;
    }
}