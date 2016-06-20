<?
header('Content-Type: text/html; charset=UTF-8');
if(isset($_POST['search_submit'])) {
	$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
	if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
	$result = $conn->query("SELECT * FROM estudiante WHERE name LIKE '".($conn->real_escape_string($_GET['search_name']))."'");
	while($student = $result->fetch_assoc()) {
		
	}
	$conn->close();
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />
<title>IPhO: Search</title>
</head>
<body>
<? $pagetype_search = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<h2>Search</h2>
	<form method="post" action="search.php">
	<p>
	<input type="text" name="search_name" maxlength="30" class="inptText" size="24" id="search_name"/>
	<input type="submit" name="search_submit" value="Search" class="btnSubmit" />
	<span>(Search the IPhO database for a particular contestant)</span>
	</p>
	<table class="plain">
	<tr><th><span>Search period</span></th>
	<td><select name="search_from">
	<?
	for($i = 1967; $i <= 2015; $i++) {
	    echo '<option '.($i == 1967 ? 'selected="selected" ' : '').'value="'.$i.'">'.$i.'</option>';
	}
	?>
	</select>
	&mdash;
	<select name="search_to">
	<?
	for($i = 1967; $i <= 2015; $i++) {
	    echo '<option '.($i == 2015 ? 'selected="selected" ' : '').'value="'.$i.'">'.$i.'</option>';
	}
	?>
	</select></td></tr>
	</table>
	<?
	if(isset($_POST['search_submit'])) {
		$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
		$search_query = trim($conn->real_escape_string($_POST['search_name']));
		$from = trim($conn->real_escape_string($_POST['search_from']));
		$to = trim($conn->real_escape_string($_POST['search_to']));
		if($search_query != "") {
			echo "<script>document.getElementById('search_name').value = '".$search_query."'</script>";
			echo '<h3>Search results for: '.$search_query.'</h3>';
			echo '<table><thead><tr><th>Participant</th><th>Year</th><th>Country</th><th>Award</th></tr></thead><tbody>';
			$result = $conn->query("SELECT * FROM countries");
			$countries = array();
			while($row = $result->fetch_assoc()) {
				$countries[$row['code']] = $row['name'];
			}
			if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
			$result = $conn->query("SELECT * FROM estudiante WHERE name LIKE '%".$search_query."%' AND year >= ".$from." AND year <= ".$to." LIMIT 100");
			while($student = $result->fetch_assoc()) {
				echo '<tr>';
				echo '<td>'.$student['name'].'</td>';
				echo '<td><a href="year_info.php?year='.$student['year'].'">'.$student['year'].'</a></td>';
				echo '<td><a href="country_info.php?code='.$student['country'].'">'.$countries[$student['country']].'</a></td><td>';
				switch($student['medal']) {
					case 1: echo '<img src="m_gold.png" width="9" height="9"> Gold Medal'; break;
					case 2: echo '<img src="m_silver.png" width="9" height="9"> Silver Medal'; break;
					case 3: echo '<img src="m_bronze.png" width="9" height="9"> Bronze Medal'; break;
					case 4: echo '<img src="m_patates.png" width="9" height="9"> Honourable Mention'; break;
				}
				echo '</td></tr>';
			}
			echo '</tbody></table>';
		}
		$conn->close();
	}
	?>
	</form>
</div>
<? include 'footer.php'; ?>
</body>
</html>