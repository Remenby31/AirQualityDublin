<?php
$timestamp = $_GET['timestamp'];
$dateString = date('Y-m-d', $timestamp);

$data_type = $_GET['data_type'];

$filePath = __DIR__ . '/DataDublin/' . $data_type . '/' . $dateString . '.csv';

if (file_exists($filePath)) {
    $fileContents = file_get_contents($filePath);
    $fileContents = str_replace("\n", "<br>", $fileContents);
    header('Content-Type: text/html');
    echo $fileContents;
  } else {
    echo "None";
  }
?>
