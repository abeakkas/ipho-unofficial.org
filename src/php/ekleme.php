<?
header('Content-Type: text/html; charset=UTF-8');
if(isset($_POST['iphosubmit'])){
	$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
	if ($conn->connect_error) {
		die("Connection failed: " . $conn->connect_error);
	} 
	$sql = "INSERT INTO estudiante (name, country, year, rank, medal)
	VALUES ('".$_POST['iphoname']."','".$_POST['iphocode']."','".$_POST['iphoyear']."',' ".$_POST['iphorank']."',' ".$_POST['iphomedal']."')";
	
	if ($conn->query($sql) === TRUE) {
		echo "New record created successfully";
	} else {
		echo "Error: " . $sql . "<br>" . $conn->error;
	}
	
	$conn->close();
}else if(isset($_POST['json'])){
	$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
	$bebeler=json_decode($_POST['json'],true);
	for($i=0;$i<count($bebeler);$i++){
		$sql = "INSERT INTO estudiante (name, country, year, rank, medal)
		VALUES ('".$bebeler[$i]['name']."','".$bebeler[$i]['code']."','".$bebeler[$i]['year']."','".$bebeler[$i]['rank']."','".$bebeler[$i]['medal']."')";
		$conn->query($sql);
	}
	$conn->close();
	echo "Done!";
}else{
	?>
	<html>
	<body>
	<center>
	<div id="resp"></div><br><br>
	name:<input type="text" id="iphoname"><br>
	country:<input type="text" id="iphocode"><br>
	iphoyear:<input type="text" id="iphoyear"><br>
	iphorank:<input type="text" id="iphorank"><br>
	iphomedal:<input type="text" id="iphomedal"><br>
	id<input type="text" id="iphoid" value="-1"><br>
	<input type="submit" onclick="submitipho()" value="submit"><br><br>
	<input type="submit" onclick="bebeler=JSON.parse(bebetext.value)" value="parse list text"><br>
	<input type="submit" onclick="sendjson()" value="send json"><br>
	<input type="submit" onclick="overlist()" value="go over list"><br>
	<textarea id="bebetext" cols=150 rows=10></textarea><br><br>
	<input type="submit" onclick="texttolist()" value="text to json list"><br>
	<textarea id="bebetexttext" cols=150 rows=10></textarea>
	</center>
	<script>
	submitipho=function(){
		xmlhttp=new XMLHttpRequest();
		resp.innerHTML="";
		xmlhttp.onreadystatechange=function()
		{
			if (xmlhttp.readyState==4 && xmlhttp.status==200)
			{
				resp.innerHTML=xmlhttp.responseText;
				if(isoverlist && bebeix<bebeler.length) overlist();
			}
		}
		xmlhttp.open("POST","ekleme.php",true);
		xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		xmlhttp.send("iphoname="+iphoname.value
			+"&iphocode="+iphocode.value
			+"&iphoyear="+iphoyear.value
			+"&iphorank="+iphorank.value
			+"&iphomedal="+iphomedal.value
			+"&iphosubmit=17");
	}
	bebeix=0;
	isoverlist=false;
	overlist=function(){
		isoverlist=true;
		iphoname.value=bebeler[bebeix].name;
		iphocode.value=bebeler[bebeix].code;
		iphorank.value=bebeler[bebeix].rank;
		iphomedal.value=bebeler[bebeix].medal;
		bebeix++;
		submitipho();
	}
	sendjson=function(){
		resp.innerHTML="Uploading...";
		xmlhttp=new XMLHttpRequest();
		xmlhttp.onreadystatechange=function()
		{
			if (xmlhttp.readyState==4 && xmlhttp.status==200)
			{
				resp.innerHTML=xmlhttp.responseText;
			}
		}
		xmlhttp.open("POST","ekleme.php",true);
		xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
		xmlhttp.send("json="+bebetext.value);
	}
	texttolist=function(){
		var lines = bebetexttext.value.split("\n");
		var year = lines[0];
		var medal = 1;
		var kekolar = [];
		var rank = 1;
		for(var i = 1;i < lines.length; i++) {
			if(lines[i] == "") continue;
			var line = lines[i].split(" ");
			if(line[0] == "Gold") continue;
			if(line[0] == "Silver") { medal++; continue; }
			if(line[0] == "Bronze") { medal++; continue; }
			if(line[0] == "Honourable") { medal++; continue; }
			if(line[0] == "Special") continue;
			if(line[0] == "Absolute") continue;
			var keko = {};
			keko.year = year;
			keko.medal = medal;
			keko.rank = rank++;
			keko.code = "";
			for(var j = 2; j < line.length; j++) keko.code += line[j] + " ";
			keko.code = keko.code.trim();
			keko.name = line[0]+ " "+line[1];
			kekolar.push(keko);
		}
		bebetext.value = JSON.stringify(kekolar);
		bebetext.value=bebetext.value.replace(/\}\,\{/g,"},\n{");
	}
	</script>
	</body>
	</html>
	<? } ?>