<?php

declare(strict_types=1);

require_once __DIR__ . '/../app/autoload.php';

use WebInsights\Bootstrap;

$id = (int) ($_GET['id'] ?? 0);
$report = $id > 0 ? Bootstrap::storage()->reportById($id) : null;

if (!$report) {
    http_response_code(404);
    echo 'Report not found.';
    exit;
}

function e(mixed $value): string
{
    return htmlspecialchars((string) $value, ENT_QUOTES, 'UTF-8');
}
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= e($report['title']) ?> · WebInsights Assistant</title>
    <link rel="stylesheet" href="assets/app.css">
</head>
<body>
    <main class="page">
        <p><a href="index.php">← Back to dashboard</a></p>

        <section class="hero">
            <p class="eyebrow"><?= e(strtoupper($report['source'])) ?> report</p>
            <h1><?= e($report['title']) ?></h1>
            <p><?= e($report['period']['start']) ?> → <?= e($report['period']['end']) ?></p>
        </section>

        <?php foreach ($report['warnings'] as $warning): ?>
            <div class="notice"><?= e($warning) ?></div>
        <?php endforeach; ?>

        <section class="metrics-grid">
            <?php foreach ($report['metrics'] as $label => $value): ?>
                <article class="metric-card">
                    <span><?= e($label) ?></span>
                    <strong><?= e($value) ?></strong>
                </article>
            <?php endforeach; ?>
        </section>

        <section class="grid-two">
            <article class="card">
                <h2>Channels</h2>
                <ul class="data-list">
                    <?php foreach ($report['channels'] as $channel): ?>
                        <li><span><?= e($channel['name']) ?></span><strong><?= e($channel['sessions']) ?></strong></li>
                    <?php endforeach; ?>
                </ul>
            </article>

            <article class="card">
                <h2>Devices</h2>
                <ul class="data-list">
                    <?php foreach ($report['devices'] as $device): ?>
                        <li><span><?= e($device['name']) ?></span><strong><?= e($device['sessions']) ?></strong></li>
                    <?php endforeach; ?>
                </ul>
            </article>
        </section>

        <section class="card">
            <h2>Top pages</h2>
            <table>
                <thead>
                    <tr><th>Path</th><th>Views</th><th>Engagement</th></tr>
                </thead>
                <tbody>
                    <?php foreach ($report['pages'] as $page): ?>
                        <tr>
                            <td><?= e($page['path']) ?></td>
                            <td><?= e($page['views']) ?></td>
                            <td><?= e($page['engagementRate']) ?>%</td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </section>

        <section class="grid-two">
            <article class="card">
                <h2>Insights</h2>
                <?php foreach ($report['insights'] as $insight): ?>
                    <div class="stacked-item">
                        <h3><?= e($insight['title']) ?></h3>
                        <p><?= e($insight['evidence']) ?></p>
                        <small>Confidence: <?= e($insight['confidence']) ?></small>
                    </div>
                <?php endforeach; ?>
            </article>

            <article class="card">
                <h2>Recommendations</h2>
                <?php foreach ($report['recommendations'] as $recommendation): ?>
                    <div class="stacked-item">
                        <h3><?= e($recommendation['action']) ?></h3>
                        <p><?= e($recommendation['why']) ?></p>
                        <small>Priority: <?= e($recommendation['priority']) ?> · Effort: <?= e($recommendation['effort']) ?></small>
                    </div>
                <?php endforeach; ?>
            </article>
        </section>
    </main>
</body>
</html>
