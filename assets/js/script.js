var d = new Date();

$(document).ready(function() {
    back();
});

$('#goBack').click(function() {
    back();
});

$('#goNext').click(function() {
    next();
});

$('#goLast').click(function() {
    d = new Date();
    back();
});

function back() {
    d.setDate(d.getDate()-1);
    var datum = `${d.getUTCFullYear()}_${pad(d.getUTCMonth()+1)}_${pad(d.getUTCDate())}`;
    $('#datum').text("Date: "+`${pad(d.getUTCDate())}/${pad(d.getUTCMonth()+1)}/${d.getUTCFullYear()}`);
    $('#graphic').attr('src', `images/${datum}.png`);
}

function next(){
    d.setDate(d.getDate()+1);
    var datum = `${d.getUTCFullYear()}_${pad(d.getUTCMonth()+1)}_${pad(d.getUTCDate())}`;
    $('#datum').text("Date: "+`${pad(d.getUTCDate())}/${pad(d.getUTCMonth()+1)}/${d.getUTCFullYear()}`);
    $('#graphic').attr('src', `images/${datum}.png`);
}

function pad(num) {
    num = num.toString();
    while (num.length < 2) num = "0" + num;
    return num;
}

function fallback() {
    $('#graphic').attr('src', 'images/fallback.png');
}