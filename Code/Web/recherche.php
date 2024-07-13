<?php
if (isset($_GET['hostname'])) {
    $hostname = $_GET['hostname'];
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "agent";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    // Fetch data from all three tables
    $sql = "
        SELECT 
            h.Hostname, h.CPU, h.GPU, h.RAM, h.BaseBoard, h.DiskDrive_Model, h.DiskDrive_Size, h.DiskDrive_State, 
            n.Domain, n.SerialNumber, n.Bios_Releasedate, 
            d.Remaining, d.Total_Size, d.Buzy_Size
        FROM 
            Hardware h
        LEFT JOIN 
            Network n ON h.Hostname = n.Hostname
        LEFT JOIN 
            disk d ON h.Hostname = d.Hostname
        WHERE 
            h.Hostname = ?
    ";

    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $hostname);
    $stmt->execute();
    $result = $stmt->get_result();

    $data = [];
    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $data[] = $row;
        }
    }

    $stmt->close();
    $conn->close();

    header('Content-Type: application/json');
    echo json_encode($data);
} else {
    header('Content-Type: application/json');
    echo json_encode(["error" => "Hostname parameter is missing."]);
}
?>
