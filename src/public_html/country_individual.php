<?
header('Content-Type: text/html; charset=UTF-8');
if(!isset($_GET['code'])) header('Location: countries.php');
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$result = $conn->query("SELECT * FROM countries WHERE code='".($conn->real_escape_string($_GET['code']))."'");
if($country = $result->fetch_assoc()) {
	$nextcountry = $conn->query("SELECT * FROM countries WHERE name>'".($conn->real_escape_string($country['name']))."' ORDER BY name LIMIT 1")->fetch_assoc();
	$previouscountry = $conn->query("SELECT * FROM countries WHERE name<'".($conn->real_escape_string($country['name']))."' ORDER BY name DESC LIMIT 1")->fetch_assoc();
} else header('Location: countries.php');
$conn->close();
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head><meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />
<title>IPhO: <? echo $country['name'] ?> - Individual Results</title>
</head>
<body>
<? $pagetype_countries = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<div class="flag hideprn">
		<a href="country_info.php?code=<? echo $country['code']; ?>">
		<img title="<? echo $country['name']; ?>" src="http://imo-official.org/flags/<? echo $country['code']; ?>.gif" alt="<? echo $country['name']; ?>" style="border-width:0px;" /></a>
	</div>
	<h2>
	<? if($previouscountry) echo '<a href="country_individual.php?code='.$previouscountry['code'].'" class="pointer">&#9668;</a> '; ?>
	<a href="country_info.php?code=<? echo $country['code']; ?>"><? echo $country['name']; ?></a>  
	<? if($nextcountry) echo '<a href="country_individual.php?code='.$nextcountry['code'].'" class="pointer">&#9658;</a>'; ?></h2>
	<h3>
	<!-- <a id="ctl00_CPH_Main_HyperLinkTeam" class="hideprn" href="country_team.php?code=<? echo $country['code']; ?>">Team results</a> &bull; -->
	<a id="ctl00_CPH_Main_HyperLinkIndividual" class="highlight" href="country_individual.php?code=<? echo $country['code']; ?>">Individual results</a>
	<!-- &bull; <a id="ctl00_CPH_Main_HyperLinkHall" class="hideprn" href="country_hall.php?code=<? echo $country['code']; ?>">Hall of fame</a> -->
	</h3>
	<table>
	<thead>
	<tr><th rowspan="2" class="highlightDown">Year</th><th rowspan="2">Contestant</th><th colspan="2">Rank</th><th rowspan="2">Award</th></tr>
	<tr><th><span class="hideprnI" title="Absolute ranking">Abs.</span></th><th><span class="hideprnI" title="Relative ranking">Rel.</span></th></tr>
	</thead>
	<tbody>
	<?
	$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
	if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
	$result2 = $conn->query("SELECT * FROM estudiante WHERE country='".$country['code']."' ORDER BY year DESC, rank ASC");
	$lastyear = -1;
	while($row = $result2->fetch_assoc()) {
		$contestants = $conn->query("SELECT * FROM organizers WHERE year='".$row['year']."'")->fetch_assoc()['contestants'];
		echo '<tr'.(($lastyear!=-1 && $lastyear!=$row['year'])?' class=" doubleTopLine"':'').'>
		<td align="center"><a href="year_info.php?year='.$row['year'].'">'.$row['year'].'</a></td>
		<td>'.$row['name'].'</td>
		<td align="right">'.$row['rank'].'</td>
		<td align="right" class="doubleRightLine">'.
		($contestants ? number_format(100 - 100.0 * $row['rank'] / $contestants, 2, '.', '').'%' : '').
		'</td><td>';
		switch($row['medal']) {
			case 1: echo '<img src="m_gold.png" width="9" height="9"> Gold Medal'; break;
			case 2: echo '<img src="m_silver.png" width="9" height="9"> Silver Medal'; break;
			case 3: echo '<img src="m_bronze.png" width="9" height="9"> Bronze Medal'; break;
			case 4: echo '<img src="m_patates.png" width="9" height="9"> Honourable Mention'; break;
		}
		echo '</td></tr>';
		$lastyear = $row['year'];
	}
	$conn->close();
	?>
	</tbody>
	</table>
	<div>
		Results may not be complete and may include mistakes. 
		Please send relevant information to the webmaster: 
		<a href="mailto:webmaster@ipho-official.org">webmaster@ipho-unofficial.org</a>.
	</div>
</div>
<? include 'footer.php'; ?>
</body>
</html>