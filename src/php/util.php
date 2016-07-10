<!DOCTYPE html>
<html>
<head>
<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />
</head>
<body>
<?
$conn = new mysqli("localhost", "iphouser", "ornitorenk17", "ipho");
if ($conn->connect_error) {
	die("Connection failed: " . $conn->connect_error);
} 
$sql = "SELECT * FROM estudiante ORDER BY rank";
if($result = $conn->query($sql)) {
	while($row = $result->fetch_assoc()) {
		echo $row['name'].",".$row['country'].",".$row['year'].",".$row['rank'].",".$row['medal']."<br>";
	}
}
$conn->close();
?>
</body>
</html>