<?php

declare(strict_types=1);

require_once __DIR__ . '/../app/autoload.php';

use Throwable;
use WebInsights\Bootstrap;

function check_item(string $label, bool $ok, string $details = ''): array
{
    return [
        'label' => $label,
        'ok' => $ok,
        'details' => $details,
    ];
}

$checks = [];
$checks[] = check_item('PHP version >= 8.2', version_compare(PHP_VERSION, '8.2.0', '>='), PHP_VERSION);
$checks[] = check_item('PDO extension loaded', extension_loaded('pdo'));
$checks[] = check_item('PDO SQLite extension loaded', extension_loaded('pdo_sqlite'));
$checks[] = check_item('JSON extension loaded', extension_loaded('json'));

try {
    Bootstrap::boot();
    $storagePath = Bootstrap::storagePath();
    $checks[] = check_item('Storage directory exists', is_dir($storagePath), $storagePath);
    $checks[] = check_item('Storage directory writable', is_writable($storagePath), $storagePath);

    $reportsPath = Bootstrap::storagePath('reports');
    $checks[] = check_item('Reports directory exists', is_dir($reportsPath), $reportsPath);
    $checks[] = check_item('Reports directory writable', is_writable($reportsPath), $reportsPath);

    Bootstrap::storage()->latestReports(1);
    $checks[] = check_item('SQLite storage works', true, Bootstrap::storagePath('webinsights.sqlite'));
} catch (Throwable $exception) {
    $checks[] = check_item('Application boot/storage', false, $exception->getMessage());
}

$allOk = array_reduce($checks, static fn (bool $carry, array $check): bool => $carry && $check['ok'], true);
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>WebInsights Assistant · Status</title>
    <link rel="stylesheet" href="assets/app.css">
</head>
<body>
    <main class="page">
        <p><a href="index.php">← Back to dashboard</a></p>
        <section class="hero">
            <p class="eyebrow">Installation status</p>
            <h1><?= $allOk ? 'The app looks ready.' : 'Some checks failed.' ?></h1>
            <p>This page checks the minimum server requirements for the current demo app.</p>
        </section>

        <section class="card">
            <h2>Checks</h2>
            <ul class="data-list">
                <?php foreach ($checks as $check): ?>
                    <li>
                        <span><?= htmlspecialchars($check['label'], ENT_QUOTES, 'UTF-8') ?></span>
                        <strong><?= $check['ok'] ? 'OK' : 'FAIL' ?></strong>
                    </li>
                    <?php if ($check['details'] !== ''): ?>
                        <li><span><?= htmlspecialchars($check['details'], ENT_QUOTES, 'UTF-8') ?></span><strong></strong></li>
                    <?php endif; ?>
                <?php endforeach; ?>
            </ul>
        </section>
    </main>
</body>
</html>
