<?php

declare(strict_types=1);

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
