// Requries asciify.js

(function () {
    if (typeof(asciify) != "function") {
        console.error("asciify is not imported!");
        return;
    }
    var countries = null;
    var students = null;
    function loadCountries() {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "countries.csv", true);
        xmlhttp.overrideMimeType("text/plain");
        xmlhttp.onreadystatechange = function() {
            // Let's ignore xmlhttp.status as it doesn't work local
            if (xmlhttp.readyState == 4 && xmlhttp.responseText != null) {
                countries = [];
                countries[""] = "";
                var tx = xmlhttp.responseText;
                var lines = tx.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    var ps = lines[i].split(",");
                    if (ps.length > 2) {
                        countries[ps[0]] = ps[1];
                    }
                }
            }
        }
        xmlhttp.send();
    }
    function loadStudents() {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "estudiantes.csv", true);
        xmlhttp.overrideMimeType("text/plain");
        xmlhttp.onreadystatechange = function () {
            // Let's ignore xmlhttp.status as it doesn't work local
            if (xmlhttp.readyState == 4 && xmlhttp.responseText != null) {
                students = [];
                var tx = xmlhttp.responseText;
                var lines = tx.split("\n");
                for (var i = 0; i < lines.length; i++) {
                    var ps = lines[i].trim().split(",");
                    if (ps.length > 4) {
                        students.push({
                            year: ps[0],
                            rank: ps[1],
                            name: ps[2],
                            code: ps[3],
                            medal: ps[4],
                            website: ps[8],
                            name_ascii_lower: asciify(ps[2]).toLowerCase(),
                        });
                    }
                }
            }
        }
        xmlhttp.send();
    }
    window.ipho_search = function () {
        if (countries == null || students == null) {
          return;
        }
        var html = "";
        var t_row = document.getElementById("t_row").innerHTML;
        var t_website = document.getElementById("t_website").innerHTML;
        var t_gold = document.getElementById("t_gold").innerHTML;
        var t_silver = document.getElementById("t_silver").innerHTML;
        var t_bronze = document.getElementById("t_bronze").innerHTML;
        var t_honourable = document.getElementById("t_honourable").innerHTML;
        var query = document.getElementById("search_query").value;
        query = asciify(query).toLowerCase().trim();
        if (query.length <= 1) {
            return;
        }
        // Traverse in reverse order so that recent results show up higher.
        for (var i = students.length - 1; i >= 0; i--) {
            var student = students[i];
            if (student.name_ascii_lower.indexOf(query) != -1) {
                var row = t_row.replace(/{{code}}/g, student.code)
                    .replace(/{{country}}/g, countries[student.code])
                    .replace(/{{year}}/g, student.year);
                if (student.website) {
                    var link = t_website.replace(/{{name}}/, student.name)
                                        .replace(/{{link}}/, student.website);
                    row = row.replace(/{{name}}/, link)
                } else {
                    row = row.replace(/{{name}}/, student.name)
                }
                switch (student.medal) {
                    case "G":
                        row = row.replace(/{{medal}}/g, t_gold);
                        break;
                    case "S":
                        row = row.replace(/{{medal}}/g, t_silver);
                        break;
                    case "B":
                        row = row.replace(/{{medal}}/g, t_bronze);
                        break;
                    case "H":
                        row = row.replace(/{{medal}}/g, t_honourable);
                        break;
                    default:
                        row = row.replace(/{{medal}}/g, "");
                        break;
                }
                html += "<tr>" + row + "</tr>";
            }
        }
        document.getElementById("search_results").innerHTML = html;
    }
    loadCountries();
    loadStudents();
})();
