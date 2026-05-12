<?php

declare(strict_types=1);

require_once __DIR__ . '/../app/autoload.php';

use WebInsights\Bootstrap;

Bootstrap::boot();
$reports = Bootstrap::storage()->latestReports(8);
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>WebInsights Assistant</title>
    <link rel="stylesheet" href="assets/app.css">
</head>
<body>
    <main class="page">
        <section class="hero">
            <p class="eyebrow">Self-hosted analytics assistant</p>
            <h1>Turn web analytics into readable reports.</h1>
            <p>Generate a first demo report now. GA4 connection will use the same internal report pipeline when implemented.</p>
        </section>

        <section class="card">
            <h2>Generate demo report</h2>
            <form method="post" action="api/generate-demo-report.php" class="form-grid">
                <label>
                    Start date
                    <input type="date" name="start_date" value="<?= htmlspecialchars(date('Y-m-d', strtotime('-30 days')), ENT_QUOTES) ?>" required>
                </label>
                <label>
                    End date
                    <input type="date" name="end_date" value="<?= htmlspecialchars(date('Y-m-d'), ENT_QUOTES) ?>" required>
                </label>
                <button type="submit">Generate report</button>
            </form>
        </section>

        <section class="card">
            <h2>Report history</h2>
            <?php if (!$reports): ?>
                <p>No reports generated yet.</p>
            <?php else: ?>
                <ul class="report-list">
                    <?php foreach ($reports as $report): ?>
                        <li>
                            <a href="report.php?id=<?= (int) $report['id'] ?>">
                                <?= htmlspecialchars($report['title'], ENT_QUOTES) ?>
                            </a>
                            <span><?= htmlspecialchars($report['period_start'], ENT_QUOTES) ?> → <?= htmlspecialchars($report['period_end'], ENT_QUOTES) ?></span>
                        </li>
                    <?php endforeach; ?>
                </ul>
            <?php endif; ?>
        </section>
    </main>
</body>
</html>
