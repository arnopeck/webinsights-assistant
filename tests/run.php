<?php

declare(strict_types=1);

if (PHP_SAPI !== 'cli') {
    http_response_code(200);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><html><head><meta charset="utf-8"><title>WebInsights Test</title></head><body>';
    echo '<h1>WebInsights Assistant test runner</h1>';
    echo '<p>This file is a CLI smoke test and should not be opened from the browser.</p>';
    echo '<p>Open <a href="../public/status.php">public/status.php</a> to check the web installation.</p>';
    echo '<p>To run this test from a terminal: <code>php tests/run.php</code></p>';
    echo '</body></html>';
    exit;
}

require_once __DIR__ . '/../app/autoload.php';

use WebInsights\Reports\DemoReportBuilder;

function assert_true(bool $condition, string $message): void
{
    if (!$condition) {
        fwrite(STDERR, "FAIL: {$message}\n");
        exit(1);
    }
}

$builder = new DemoReportBuilder();
$report = $builder->build('2026-04-01', '2026-04-30');

assert_true($report['source'] === 'demo', 'Report source should be demo.');
assert_true(isset($report['metrics']['users']), 'Report should include users metric.');
assert_true(count($report['insights']) > 0, 'Report should include at least one insight.');
assert_true(count($report['recommendations']) > 0, 'Report should include at least one recommendation.');

fwrite(STDOUT, "OK: demo report builder\n");
