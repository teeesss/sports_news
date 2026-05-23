<?php
/**
 * Sovereign Sports Intelligence - Sync Bridge
 * Writes a timestamp to database/sync_trigger.txt to notify the local engine.
 */
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');

$trigger_file = 'database/sync_trigger.txt';
$timestamp = time();

if (file_put_contents($trigger_file, (string)$timestamp)) {
    echo json_encode([
        "status" => "triggered",
        "timestamp" => $timestamp,
        "message" => "Sync request received by bridge. Local engine will process shortly."
    ]);
} else {
    http_response_code(500);
    echo json_encode([
        "status" => "error",
        "message" => "Bridge failure: Ensure 'database/' directory is writable."
    ]);
}
?>
