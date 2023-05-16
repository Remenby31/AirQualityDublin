var xhttp = new XMLHttpRequest();

function sendPhpRequest(timestamp, data_type_pm) {
    // split data_type by -
    var data_type = data_type_pm.split("-")[0];
    var pm = data_type_pm.split("-")[1];
    // Diviser le timestamp par 1000 pour le convertir en secondes
    timestamp = timestamp / 1000;
    url = "http://localhost/mapHTML_dtd/getDayData.php?timestamp=" + timestamp + "&data_type=" + data_type;
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            // No data
            if (xhttp.responseText == "none") {
                console.log("No data");
                clearHeatmap();
                printNoData();
                return;
            }

            // Data
            outputdata = preparedData(xhttp.responseText, pm);
            clearHeatmap();
            addHeatmap(outputdata);
        }
      }
    xhttp.open("GET", url, true);
    xhttp.send();
}

function preparedData(data, pm) {
    var outputdata = [];
    data = data.split("<br>");
    // Remove the last element of the array (empty)
    data.pop();
    for (var i = 0; i < data.length; i++) {
        line = data[i].split(";");
        if (pm == "pm25") {
            outputdata.push([parseFloat(line[4]), parseFloat(line[5]), parseFloat(line[2])]);
        }
        else if (pm == "pm10") {
            outputdata.push([parseFloat(line[4]), parseFloat(line[5]), parseFloat(line[3])]);
        }
    }
    return outputdata;
}

function getMidnightTimestamp(timestamp) {
    // Convert the timestamp to a date
    var date = new Date(timestamp);
    
    // Reset the hours, minutes, seconds, and milliseconds to zero
    date.setHours(0);
    date.setMinutes(0);
    date.setSeconds(0);
    date.setMilliseconds(0);
    
    // Convert the date back to a timestamp and return it
    return date.getTime();
}
  

function setDayData(timestamp, data_type_pm) {
    sendPhpRequest(timestamp, data_type_pm);
}