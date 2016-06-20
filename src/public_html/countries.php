<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />
<title>IPhO: List of Countries</title>
</head>
<body>
<? $pagetype_countries = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<h2>List of countries</h2>
	<table>
	<thead>
	<tr>
	<th>Code</th>
	<th>Country</th>
	<th>National PhO site</th>
	<th>IPhO Host</th>
	</tr>
	</thead>
	<tbody>
	<?
	$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
	if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
	$result = $conn->query("SELECT * FROM countries ORDER BY name");
	while($row = $result->fetch_assoc()) {
		echo '<tr>
		<td align="center"><a href="country_info.php?code='.$row['code'].'">'.$row['code'].'</a></td>
		<td><a href="country_info.php?code='.$row['code'].'">'.$row['name'].'</a></td>';
		echo '<td>'.($row['nationalsite']==''?'':'<a href="'.$row['nationalsite'].'" target="_blank">'.(strlen($row['nationalsite'])<50?$row['nationalsite']:substr($row['nationalsite'],0,50)."...").'</a>').'</td>';
		$result2 = $conn->query("SELECT * FROM organizers WHERE country='".$row['code']."' ORDER BY year");
		echo '<td>';
		$flag=False;
		while($row2 = $result2->fetch_assoc()) {
			if($flag) echo ", ";
			echo '<a href="year_info.php?year='.$row2['year'].'">'.$row2['year'].'</a>';
			$flag=True;
		}
		echo '</td></tr>';
	}
	$conn->close();
	?>
	</tbody>
	</table>
	
</div>
<? include 'footer.php'; ?>
</body>
</html>
