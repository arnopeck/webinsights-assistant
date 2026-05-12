<?php

declare(strict_types=1);

namespace WebInsights\Reports;

use RuntimeException;
use WebInsights\Bootstrap;

final class DemoReportBuilder
{
    public function build(string $startDate, string $endDate): array
    {
        $fixture = $this->loadFixture();
        $metrics = $fixture['metrics'];
        $channels = $fixture['channels'];
        $pages = $fixture['pages'];
        $devices = $fixture['devices'];

        $engagementRate = $metrics['sessions'] > 0
            ? round(($metrics['engagedSessions'] / $metrics['sessions']) * 100, 1)
            : 0.0;

        $insights = [
            [
                'title' => 'Organic search is the main acquisition channel',
                'severity' => 'opportunity',
                'evidence' => 'Organic Search accounts for ' . $channels[0]['sessions'] . ' sessions in the selected period.',
                'confidence' => 0.82,
            ],
            [
                'title' => 'Mobile traffic deserves specific attention',
                'severity' => 'info',
                'evidence' => 'Mobile sessions represent ' . $devices[0]['sessions'] . ' sessions.',
                'confidence' => 0.76,
            ],
        ];

        $recommendations = [
            [
                'action' => 'Review the top landing pages and improve calls to action.',
                'why' => 'The pages with most views are likely to influence a large share of user journeys.',
                'priority' => 'high',
                'effort' => 'medium',
            ],
            [
                'action' => 'Check mobile rendering and performance before changing acquisition strategy.',
                'why' => 'Mobile usage is high enough to affect total engagement.',
                'priority' => 'medium',
                'effort' => 'medium',
            ],
        ];

        return [
            'title' => 'Demo Web Analytics Report',
            'source' => 'demo',
            'period' => [
                'start' => $startDate,
                'end' => $endDate,
            ],
            'generatedAt' => gmdate('c'),
            'warnings' => [
                'This report uses explicit demo data. It is not connected to Google Analytics.',
            ],
            'metrics' => [
                'users' => $metrics['users'],
                'sessions' => $metrics['sessions'],
                'views' => $metrics['views'],
                'engagementRate' => $engagementRate,
            ],
            'channels' => $channels,
            'pages' => $pages,
            'devices' => $devices,
            'insights' => $insights,
            'recommendations' => $recommendations,
        ];
    }

    private function loadFixture(): array
    {
        $path = Bootstrap::fixturePath('ga4-demo.json');
        if (!is_file($path)) {
            throw new RuntimeException('Demo fixture not found.');
        }

        $data = json_decode((string) file_get_contents($path), true);
        if (!is_array($data)) {
            throw new RuntimeException('Demo fixture is not valid JSON.');
        }

        return $data;
    }
}
