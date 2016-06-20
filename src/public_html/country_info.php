<?
header('Content-Type: text/html; charset=UTF-8');
if(!isset($_GET['code'])) header('Location: countries.php');
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$result = $conn->query("SELECT * FROM countries WHERE code='".($conn->real_escape_string($_GET['code']))."'");
if($country = $result->fetch_assoc()) {
	$result2 = $conn->query("SELECT * FROM estudiante WHERE country='".$country['code']."' ORDER BY year DESC");
	$gold = 0;
	$silver = 0;
	$bronze = 0;
	$honourable = 0;
	$participation = 0;
	$firstparticipation = 0;
	while($row = $result2->fetch_assoc()) {
		switch($row['medal']) {
			case 1: $gold++; break;
			case 2: $silver++; break;
			case 3: $bronze++; break;
			case 4: $honourable++; break;
		}
		if($firstparticipation != $row['year']) {
			$participation++;
			$firstparticipation = $row['year'];
		}
	}
	$nextcountry = $conn->query("SELECT * FROM countries WHERE name>'".$country['name']."' ORDER BY name LIMIT 1")->fetch_assoc();
	$previouscountry = $conn->query("SELECT * FROM countries WHERE name<'".$country['name']."' ORDER BY name DESC LIMIT 1")->fetch_assoc();
} else header('Location: countries.php');
$conn->close();
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />
<title>IPhO: <? echo $country['name']; ?></title>
</head>
<body>
<? $pagetype_countries = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<div class="flag">
		<a id="ctl00_CPH_Main_HyperLinkFlag" href="country_info.php?code=<? echo $country['code']; ?>">
		<img id="ctl00_CPH_Main_ImageFlag" title="<? echo $country['name']; ?>" src="http://imo-official.org/flags/<? echo $country['code']; ?>.gif" alt="<? echo $country['name']; ?>" style="border-width:0px;" />
		</a>
	</div>
	<h2>
	<? if($previouscountry) echo '<a href="country_info.php?code='.$previouscountry['code'].'" class="pointer">&#9668;</a> '; ?>
	<a href="country_info.php?code=<? echo $country['code']; ?>" class="highlight"><? echo $country['name']; ?></a>  
	<? if($nextcountry) echo '<a href="country_info.php?code='.$nextcountry['code'].'" class="pointer">&#9658;</a>'; ?></h2>
	<h3 class="hideprn">
	<!-- a id="ctl00_CPH_Main_HyperLinkTeam" href="#">Team results</a> &bull; -->
	<a id="ctl00_CPH_Main_HyperLinkIndividual" href="country_individual.php?code=<? echo $country['code']; ?>">Individual results</a>
	<!-- &bull; <a id="ctl00_CPH_Main_HyperLinkHall" href="#">Hall of fame</a> -->
	</h3>
	<dl class="normal">
	<?
	if($country['nationalsite']!="") echo '<dt>Contact</dt><dd>National PhO site: <a href="'.$country['nationalsite'].'">'.$country['nationalsite'].'</a></dd>';
	$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
	$result = $conn->query("SELECT * FROM organizers WHERE country='".$country['code']."' ORDER BY year");
	$flag = True;
	while($result && $row = $result->fetch_assoc()) {
		if($flag) echo "<dt>IPhO Host</dt>";
		echo '<dd><a href="year_info.php?year='.$row['year'].'">'.$row['year'].'</a>';
		if($row['city']) echo ' - '.$row['city'];
		if($row['homepage']) echo ' (<a href='.$row['homepage'].' target="_blank">Home Page IPhO '.$row['year'].'</a>)';
		echo '</dd>';
		$flag = False;
	}
	$conn->close();
	if($firstparticipation!=0) echo '<dt>Performance at the IPhO</dt>
	<dd>First participation: <a href="year_info.php?year='.$firstparticipation.'">'.$firstparticipation.'</a>.</dd>
	<dd>Number of participations: '.$participation.'.</dd>
	<dd>Gold medals: '.$gold.'. Silver medals: '.$silver.'. Bronze medals: '.$bronze.'. Honourable mentions: '.$honourable.'.</dd>';
	?>
	</dl>
</div>
<? include 'footer.php'; ?>
</body>
</html>
