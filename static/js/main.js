for (let day = 0; day < 7; day++) {
    start_day = getFirstDay
}

function getFirstDay(d) {
    d = new Date(d);
    var day = d.getDay(), diff = d.getDate() - day;
    return new Date(d.setDate(diff));
}

function getLastDay(d) {
    d = new Date(d);
    var day = d.getDay(), diff = d.getDate() + (6 - day);
    return new Date(d.setDate(diff));
}