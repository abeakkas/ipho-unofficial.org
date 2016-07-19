(function () {
    var countries = null;
    var students = null;
    function loadCountries() {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "countries.csv", true);
        xmlhttp.overrideMimeType("text/plain");
        xmlhttp.onreadystatechange = function() {
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                countries = [];
                var tx = xmlhttp.responseText;
                var lines = tx.split("\n");
                for(var i = 0; i < lines.length; i++) {
                    var ps = lines[i].split(",");
                    countries[ps[0]] = ps[1];
                }
            }
        }
        xmlhttp.send();
    }
    function loadStudents() {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "estudiantes.csv", true);
        xmlhttp.overrideMimeType("text/plain");
        xmlhttp.onreadystatechange = function() {
            if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                students = [];
                var tx = xmlhttp.responseText;
                var lines = tx.split("\n");
                for(var i = 0; i < lines.length; i++) {
                    var ps = lines[i].split(",");
                    students.push({year: ps[0], rank: ps[1], name: ps[2], code: ps[3], medal: ps[4].trim()});
                }
            }
        }
        xmlhttp.send();
    }
    window.ipho_search = function() {
        if(countries != null && students != null) {
            var html = "";
            var name = document.getElementById("search_query").value;
            var t_row = document.getElementById("t_row").innerHTML;
            var t_gold = document.getElementById("t_gold").innerHTML;
            var t_silver = document.getElementById("t_silver").innerHTML;
            var t_bronze = document.getElementById("t_bronze").innerHTML;
            var t_honourable = document.getElementById("t_honourable").innerHTML;
            if(name.length > 1) {
                for(var i = 0; i < students.length; i++) {
                    if(students[i].name.toLowerCase().indexOf(name.toLowerCase()) != -1) {
                        var row = t_row.replace(/{{name}}/g, students[i].name);
                        row = row.replace(/{{code}}/g, students[i].code);
                        row = row.replace(/{{country}}/g, countries[students[i].code]);
                        row = row.replace(/{{year}}/g, students[i].year);
                        row = row.replace(/{{code}}/g, students[i].code);
                        switch(students[i].medal) {
                            case "1":
                                row = row.replace(/{{medal}}/g, t_gold);
                                break;
                            case "2":
                                row = row.replace(/{{medal}}/g, t_silver);
                                break;
                            case "3":
                                row = row.replace(/{{medal}}/g, t_bronze);
                                break;
                            case "4":
                                row = row.replace(/{{medal}}/g, t_honourable);
                                break;
                            default:
                                row = row.replace(/{{medal}}/g, "");
                                break;
                        }
                        html += "<tr>" + row + "</tr>";
                    }
                }
                window.low = html;
                document.getElementById("search_results").innerHTML = html;
            }
        }
    }
    loadCountries();
    loadStudents();
})();
