let num = 0;

document.getElementById('btn').addEventListener('click', function () {
    if (num < 100){
        document.getElementById(num.toString()).classList.remove('invisible');
        num+=1;
    }
})
