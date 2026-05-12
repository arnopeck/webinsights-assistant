<?php

declare(strict_types=1);

namespace WebInsights\Storage;

use PDO;

final class Storage
{
    private PDO $pdo;

    public function __construct(string $databasePath)
    {
        $this->pdo = new PDO('sqlite:' . $databasePath);
        $this->pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $this->migrate();
    }

    private function migrate(): void
    {
        $this->pdo->exec(
            'CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                period_start TEXT NOT NULL,
                period_end TEXT NOT NULL,
                payload TEXT NOT NULL,
                created_at TEXT NOT NULL
            )'
        );
    }

    public function saveReport(array $report): int
    {
        $statement = $this->pdo->prepare(
            'INSERT INTO reports (title, source, period_start, period_end, payload, created_at)
             VALUES (:title, :source, :period_start, :period_end, :payload, :created_at)'
        );

        $statement->execute([
            ':title' => (string) $report['title'],
            ':source' => (string) $report['source'],
            ':period_start' => (string) $report['period']['start'],
            ':period_end' => (string) $report['period']['end'],
            ':payload' => json_encode($report, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES),
            ':created_at' => gmdate('c'),
        ]);

        return (int) $this->pdo->lastInsertId();
    }

    public function latestReports(int $limit = 10): array
    {
        $statement = $this->pdo->prepare(
            'SELECT id, title, source, period_start, period_end, created_at
             FROM reports
             ORDER BY id DESC
             LIMIT :limit'
        );
        $statement->bindValue(':limit', $limit, PDO::PARAM_INT);
        $statement->execute();

        return $statement->fetchAll(PDO::FETCH_ASSOC) ?: [];
    }

    public function reportById(int $id): ?array
    {
        $statement = $this->pdo->prepare('SELECT payload FROM reports WHERE id = :id');
        $statement->execute([':id' => $id]);
        $row = $statement->fetch(PDO::FETCH_ASSOC);

        if (!$row) {
            return null;
        }

        $report = json_decode((string) $row['payload'], true);
        return is_array($report) ? $report : null;
    }
}
