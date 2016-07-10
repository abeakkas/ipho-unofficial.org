<?
header('Content-Type: text/html; charset=UTF-8');
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$sql = "SELECT * FROM organizers ORDER BY year DESC";
$result = $conn->query($sql);
$years=array();
while($row = $result->fetch_assoc()){
	$years[]=$row;
}
$sql = "SELECT * FROM countries";
$result = $conn->query($sql);
$countries=array();
while($row = $result->fetch_assoc()) {
	$countries[$row['code']]=$row['name'];
}
$conn->close();
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<!--<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />-->
<title>IPhO: Timeline</title>
</head>
<body>
<? $pagetype_timeline = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<h2>Timeline</h2>
	<table>
	<thead>
	<tr>
	<th>#</th>
	<th class="highlightDown">Year</th>
	<th>Country</th>
	<th>City</th>
	<th>Date</th>
	<th>Countries</th>
	<th>Contestants</tr>
	</thead>
	<tbody>
	<?
	for($i=0;$i<count($years);$i++){
		echo '<tr>
		<td align="right"><a href="year_info.php?year='.$years[$i]['year'].'">'.$years[$i]['number'].'</a></td>
		<td align="center"><a href="year_info.php?year='.$years[$i]['year'].'">'.$years[$i]['year'].'</a></td>
		<td><a href="country_info.php?code='.$years[$i]['country'].'">'.$countries[$years[$i]['country']].'</a></td>
		<td>'.($years[$i]['city'] ? $years[$i]['city'] : "").'</td>
		<td align="center">'.($years[$i]['date'] ? $years[$i]['date'] : "").'</td>
		<td align="center">'.($years[$i]['participatingcountries'] ? $years[$i]['participatingcountries'] : "").'</td>
		<td align="right">'.($years[$i]['contestants'] ? $years[$i]['contestants'] : "").'</td>
		</tr>';
	}
	?>
	</tbody>
	</table>
</div>
<? include 'footer.php'; ?>
</body>
</html>
