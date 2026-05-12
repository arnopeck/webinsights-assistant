<?php

declare(strict_types=1);

require_once __DIR__ . '/../../app/autoload.php';

use WebInsights\Bootstrap;
use WebInsights\Reports\DemoReportBuilder;

Bootstrap::boot();

$startDate = (string) ($_POST['start_date'] ?? '');
$endDate = (string) ($_POST['end_date'] ?? '');

if (!$startDate || !$endDate || $startDate > $endDate) {
    http_response_code(422);
    echo 'Invalid date range.';
    exit;
}

$builder = new DemoReportBuilder();
$report = $builder->build($startDate, $endDate);
$id = Bootstrap::storage()->saveReport($report);

header('Location: ../report.php?id=' . $id, true, 303);
