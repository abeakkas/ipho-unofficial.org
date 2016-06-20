<?
header('Content-Type: text/html; charset=UTF-8');
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) die("Connection failed: " . $conn->connect_error);
$sql = "SELECT * FROM organizers WHERE year=".($conn->real_escape_string($_GET['year']));
$result = $conn->query($sql);
if($result && $year_info = $result->fetch_assoc()){
	$nextyear_info = $conn->query("SELECT * FROM organizers WHERE year>'".$year_info['year']."' ORDER BY year LIMIT 1")->fetch_assoc();
	$previousyear_info = $conn->query("SELECT * FROM organizers WHERE year<'".$year_info['year']."' ORDER BY year DESC LIMIT 1")->fetch_assoc();
}else header('Location: organizers.php');
$sql = "SELECT * FROM countries";
$result = $conn->query($sql);
$countries=array();
while($row = $result->fetch_assoc()) {
	$countries[$row['code']]=$row['name'];
}
$conn->close();
function ord_of_num($num){
    switch($num%10) {
        case 1: return "st";
        case 2: return "nd";
        case 3: return "rd";
        default: return "th";
    }
}
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
<link href="App_Themes/fav-logo.ico" rel="shortcut icon" type="image/x-icon" />
<link href="App_Themes/design.css" rel="stylesheet" type="text/css" />
<link href="App_Themes/print.css" rel="stylesheet" type="text/css" media="print" />
<title><? echo $year_info['number'].ord_of_num($year_info['number']); ?> International Physics Olympiad</title>
</head>
<body>
<? $pagetype_timeline = true; ?>
<? include 'header_side.php'; ?>
<div id="main">
	<h2>
	<? if($previousyear_info) echo '<a href="year_info.php?year='.$previousyear_info['year'].'" class="pointer">&#9668;</a>'; ?> 
	<a href="year_info.php?year=<? echo $year_info['year']; ?>" class="highlight"><? echo $year_info['number']; ?><sup><? echo ord_of_num($year_info['number']); ?></sup> IPHO <? echo $year_info['year']; ?></a> 
	<? if($nextyear_info) echo '<a href="year_info.php?year='.$nextyear_info['year'].'" class="pointer">&#9658;</a>'; ?> 
	</h2>
	<h3 class="hideprn">
	<a id="ctl00_CPH_Main_HyperLinkCountry" href="year_country.php?year=<? echo $year_info['year']; ?>">Country results</a> &bull;
	<a id="ctl00_CPH_Main_HyperLinkIndividual" href="year_individual.php?year=<? echo $year_info['year']; ?>">Individual results</a>
	<!-- &bull; <a id="ctl00_CPH_Main_HyperLinkStatistics" href="#">Statistics</a> -->
	</h3>
	<dl class="normal">
	<dt>General information</dt>
	<dd><? echo $year_info['city']?$year_info['city'].", ":""; ?><a href="country_info.php?code=<? echo $year_info['country']; ?>"><? echo $countries[$year_info['country']]; ?></a> 
	<? if($year_info['homepage']!="") echo "(<a href=".$year_info['homepage']." target='_blank'>Home Page IPhO ".$year_info['year']."</a>),"; ?>
	<? echo $year_info['date']; ?> <? echo $year_info['year']; ?></dd>
	<? if($year_info['participatingcountries']) echo "<dd>Number of participating countries: ".$year_info['participatingcountries'].".</dd>"; ?>
	<? if($year_info['contestants']) echo "<dd>Number of contestants: ".$year_info['contestants'].".</dd>"; ?>
	<? if($year_info['gold'] + $year_info['silver'] + $year_info['bronze'] + $year_info['honourable'] > 0) { ?>
		<dt>Awards</dt>
		<dd>Gold medals: <? echo $year_info['gold']; ?>.<br />
		Silver medals: <? echo $year_info['silver']; ?>.<br />
		Bronze medals: <? echo $year_info['bronze']; ?>.<br />
		Honourable mentions: <? echo $year_info['honourable']; ?>.</dd>
		<? } ?>
	</dl>
</div>
<? include 'footer.php'; ?>
</body>
</html>
